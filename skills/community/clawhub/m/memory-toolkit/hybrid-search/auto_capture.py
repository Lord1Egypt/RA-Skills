#!/usr/bin/env python3
"""
Auto-Capture — post-turn fact extraction for the memory toolkit.

The write-behind half of the autonomous memory loop: after an exchange, this
script decides *whether* there is anything durable to remember, extracts atomic
facts with a local LLM, and hands them to conflict_resolver.py for arbitration.

It is designed to run as a detached cron/background job — never in the request
path — so it does not add perceived latency to a chat turn.

Design constraints (inherited from the rest of the toolkit):
  * Local-first: the LLM endpoint is validated as loopback-only via the same
    get_safe_ollama_url() guard as hybrid_search.py / conflict_resolver.py, so
    no conversation content ever leaves the machine.
  * User-anchored: extraction is told, in the strongest terms, to capture only
    durable facts asserted by the USER or confirmed by a tool result — never the
    assistant's own speculation. This is the echo-loop guard.
  * Strong-signal gating: a cheap regex pre-filter skips trivial exchanges
    before any LLM call, so we do not burn a model run on "ok merci".
  * Non-destructive ingress: facts are written to a JSONL buffer and submitted
    to conflict_resolver.py. Superseding is decided there, with traceability.
  * Explicit opt-in to mutation: --apply is required (and --force in
    non-interactive mode) before the DB is touched.

Usage:
    # Analyse a single exchange (dry-run: prints what would be captured)
    python3 auto_capture.py --user "j'ai migré le serveur sous Ubuntu 24.04" \
        --assistant "noté"

    # Full pipeline: extract then arbitrate+apply into the DB
    python3 auto_capture.py --user "..." --assistant "..." --apply --force

    # Transcript mode: analyse a whole JSONL/plain transcript file
    python3 auto_capture.py --file transcript.jsonl --apply --force

    # Gating self-test (no LLM, no DB)
    python3 auto_capture.py --selftest
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

# ─── Config ───────────────────────────────────────────────────────────────────

_HERE = Path(__file__).resolve().parent
DB_PATH = os.environ.get("MEMORY_DB", str(_HERE / "agent_memory.db"))
WORKSPACE = Path(
    os.environ.get("WORKSPACE", str(Path.home() / ".openclaw" / "workspace"))
).resolve()
CONFLICT_RESOLVER = str(_HERE / "conflict_resolver.py")
DEFAULT_BUFFER = "/tmp/auto_captured_facts.jsonl"

ALLOWED_OLLAMA_HOSTS = {"localhost", "127.0.0.1", "::1"}

# Model resolution is centralised in llm_resolution.py (v4.0): the model comes
# from agents.defaults.model.primary (gateway config), not a hard-coded name.
# Decision 2026-10-10: auto_capture follows the default LLM too — the old
# `qwen2.5:7b` default is gone. The local model survives ONLY as the last link
# of the shared fallback chain.
try:
    from llm_resolution import resolve_llm_model as _resolve_llm_model

except ImportError:  # pragma: no cover - defensive: keep capture runnable
    def _resolve_llm_model(explicit=None, override_env=None,
                           require_local_presence=False):
        return explicit or os.environ.get("AUTO_CAPTURE_MODEL") or "qwen2.5:7b"


def _default_model() -> str:
    """Resolve the model the capture uses (single source of truth)."""
    return _resolve_llm_model(override_env="AUTO_CAPTURE_MODEL")


DEFAULT_MODEL = _default_model()
GEN_TIMEOUT = int(os.environ.get("AUTO_CAPTURE_TIMEOUT", "60"))

CAPTURE_PROMPT = """Tu es un extracteur de mémoire pour un agent personnel.
Analyse le tour de conversation fourni et extrais UNIQUEMENT les faits durables,
décisions, configurations ou corrections explicites.

RÈGLES STRICTES :
- Capture en priorité ce que l'UTILISATEUR affirme sur lui-même, son matériel,
  ses projets, ses préférences, ses décisions ("j'ai changé", "mon nouveau",
  "note que", "correction :", "désormais", "finalement").
- Capture aussi un fait CONFIRMÉ par une sortie d'outil technique (version,
  chemin, état de service), seulement s'il est explicitement présent.
- N'invente RIEN. N'extrais JAMAIS une supposition, un plan, une hypothèse, un
  exemple, ou une formulation de l'assistant ("je pourrais", "on pourrait",
  "il faudrait peut-être").
- Un fait atomique = une seule affirmation, autoportante, au présent.
- Si aucun fait durable n'est présent, renvoie [].

Réponds UNIQUEMENT par un tableau JSON, sans texte autour :
[{"subject": "entite_courte", "fact": "affirmation atomique", "confidence": 0.9}]

subject = entité concernée en minuscules sans espaces (ex: serveur_prod, kiddo,
stephane_sante, astrocapture, maison_jeanne).
confidence = 0.0 à 1.0, ta certitude que c'est un fait durable et fiable.
"""

# ─── URL guard (identical policy to the rest of the toolkit) ──────────────────


def get_safe_ollama_url(env_var: str, default: str) -> str:
    """Validate and return an OLLAMA URL, restricting it to loopback only."""
    raw_url = os.environ.get(env_var, default)
    parsed = urlparse(raw_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Invalid scheme for {env_var}: {parsed.scheme}")
    hostname = parsed.hostname or ""
    if hostname not in ALLOWED_OLLAMA_HOSTS:
        raise ValueError(
            f"Refusing non-loopback {env_var}: {hostname!r}. "
            "Memory content must never leave the machine."
        )
    return raw_url.rstrip("/")


OLLAMA_URL = get_safe_ollama_url("OLLAMA_URL", "http://127.0.0.1:11434")

# ─── Strong-signal gating ─────────────────────────────────────────────────────

TRIVIAL_PATTERN = re.compile(
    r"^\s*(bonjour|salut|hello|hi|coucou|ok|d'accord|merci|thanks|thx|"
    r"oui|non|yes|no|super|parfait|nickel|top|bien reçu|reçu|"
    r"👍|🙏|😂|❤️)[\s.!?,…]*$",
    re.I,
)

# Strong signals: the user asserts a durable change/decision/fact.
SIGNAL_PATTERNS = [
    re.compile(r"\b(j'ai changé|j'ai migré|j'ai installé|j'ai configuré|"
               r"j'ai décidé|j'ai acheté|j'ai supprimé|j'ai renommé|"
               r"j'ai passé|j'ai commencé|j'ai arrêté)\b", re.I),
    re.compile(r"\b(mon nouveau|ma nouvelle|mes nouveaux|mes nouvelles)\b", re.I),
    re.compile(r"\b(note que|note bien|retiens que|souviens-toi|"
               r"rappelle-toi|mémorise)\b", re.I),
    re.compile(r"\b(correction|corrige|en fait|finalement|désormais|"
               r"à partir de maintenant|dorénavant)\b", re.I),
    re.compile(r"\b(c'est\s+\S+\s+maintenant|est devenu|remplace|"
               r"n'est plus|ne sont plus)\b", re.I),
    re.compile(r"\b(rappel\s*:|info\s*:|pour info|à savoir|config\s*:)\b", re.I),
]


def is_trivial(text: str) -> bool:
    """Cheap gate: skip greetings and acknowledgements."""
    cleaned = text.strip()
    if not cleaned:
        return True
    if TRIVIAL_PATTERN.match(cleaned):
        return True
    # Very short messages with no verb/entity signal are not worth an LLM pass.
    if len(cleaned.split()) < 3 and not any(p.search(cleaned) for p in SIGNAL_PATTERNS):
        return True
    return False


def has_signal(text: str) -> bool:
    """True if the text carries a strong capture signal."""
    return any(p.search(text) for p in SIGNAL_PATTERNS)


# M4 (v3.5): an assistant turn that is a tool/agent completion or a cron report
# is NOT a conversational assertion by the user. Before v3.5 the only gate was
# `should_capture(user_msg)`, so an assistant message like
#
#   "python3 skills/med-reminder/soriatane.py executed from ..."
#
# was handed to the extractor as ASSISTANT and came back as a "durable fact" —
# an echo of the agent's own activity (observed in the 2026-10-06 dry-run: 4 of
# 5 extracted "facts" were tool logs, tautologies or meta-reasoning). These
# patterns only ever appear in machine-generated turns, never in a human
# sentence, so matching one means: drop the assistant half, keep the user half.
ASSISTANT_ECHO_PATTERNS = [
    # Tool / shell completions and scheduler payload reports.
    re.compile(r"\b(exec|process|automations?)\b.{0,40}\b(complet|exit code|stdout|"
               r"stderr|pid \d|sessionId|status=|durationMs)", re.I),
    re.compile(r"\bexecuted from\b", re.I),
    re.compile(r"^\s*(===|---)\s*(end|fin)\b", re.I | re.M),
    re.compile(r"\b(cron|job)\b.{0,30}\b(payload|run|fired|scheduled|next run|"
               r"last status|failed|succeeded)\b", re.I),
    # Bookkeeping status lines the nightly pipeline prints.
    re.compile(r"\badded\s*[:=]?\s*\d+.{0,60}\bsuperseded\s*[:=]?\s*\d+", re.I),
    re.compile(r"\(dry-run\b.*--apply", re.I),
    re.compile(r"^\s*(Summary|Total|Backup|Archive)\s*:", re.I | re.M),
] + [
    re.compile(r"\[[^\]]{0,40}\].{0,5}(python3|bash|git|systemctl|openclaw|sqlite3|curl)\b", re.I),
]


def assistant_turn_is_echo(assistant_msg: str) -> bool:
    """True when the assistant turn is machine output, not conversation.

    M4 echo guard. A tool completion or a scheduled-job report must never be
    mined for durable facts about the user: it would store the agent's own
    activity as if the user had asserted it. Returns False for an empty string
    (a user-only turn is legitimate and must still be analysed).
    """
    msg = (assistant_msg or "").strip()
    if not msg:
        return False
    return any(p.search(msg) for p in ASSISTANT_ECHO_PATTERNS)


# ─── Self-referential / meta-noise gate ────────────────────────────────────────
#
# M5 (v3.7): the M4 echo guard (assistant_turn_is_echo) catches MACHINE-GENERATED
# turns (tool logs, cron payloads, status lines). It does NOT catch a turn written
# in fluent natural language whose SUBJECT is the memory system itself. Observed
# 2026-10-09: the pipeline captured «il y a trois jobs qui touchent la mémoire
# chaque nuit» — a true sentence, but pure meta-noise about the agent's own
# plumbing. Storing it as a durable fact about the user is an echo loop: the
# toolkit feeding on its own description.
#
# Strategy: drop the assistant half (keep the user half, exactly like M4) when the
# text is self-referential. Two independent signals, either is sufficient:
#   1. The text mentions the memory toolkit's own machinery (jobs, nightly,
#      extraction, pipeline, trace-extractor, ClawHub, skill, ontology, ...).
#   2. The text is dominated by first-person-plural agent voice AND names a
#      self-referential object (our pipeline, this skill, the memory base ...).
# A genuine user fact can mention "mémoire" incidentally; that is why signal 1
# alone only fires when the memory vocabulary is DENSE (>= 2 distinct hits), so
# "j'ai une bonne mémoire" or "note que ma mémoire me joue des tours" survive.

# Terms that are UNAMBIGUOUSLY about this toolkit's own machinery. One hit is
# enough: no human sentence about their own life names `trace-extractor` or
# `graph.jsonl`.
_META_STRONG = re.compile(
    r"\b(trace[- ]?extractor|memory[- ]?toolkit|memory[- ]?health|hybrid[- ]?search|"
    r"auto[- ]?capture|auto[- ]?archive|conflict[- ]?resolver|consolidate[- ]?advisor|"
    r"clawhub|graph\.jsonl|agent_memory|nightly[- ]?extraction|ontology\b|"
    r"ontologie|dedup(?:lication)?|d[ée]dup(?:lication)?|arbitrage|supers[èe]d(?:e|es|ing)?|"
    r"base m[ée]moire|m[ée]moire long(?:ue)? terme|store de faits|toolkit|extracteur)\b",
    re.I,
)
# Terms that are ambiguous alone (a user CAN have "jobs", "un pipeline", "une
# skill"). They only count as meta-noise when the *phrasing* is the agent
# speaking about its own system (see _AGENT_VOICE) or when several co-occur.
_META_WEAK = re.compile(
    r"\b(jobs?|nightly|extraction|pipeline|skill|scoring|m[ée]moire|faits)\b",
    re.I,
)
# Agent voice about its own machinery: a definite article + a system noun, or an
# explicit recurrence marker. "mon pipeline de données Astro" (a real project)
# does NOT match; "le pipeline" / "les jobs" / "chaque nuit" does.
_AGENT_VOICE = re.compile(
    r"\b(le pipeline|l'extraction|le toolkit|la skill|la base|le store|"
    r"les jobs|les faits|le job|cette nuit|chaque nuit|toutes les nuits|"
    r"tourne(?:nt)? (?:chaque|toutes les) nuit|il y a \w+ jobs)\b",
    re.I,
)


def text_is_self_referential(text: str) -> bool:
    """True when the text talks about the memory system itself (meta-noise).

    M5 gate. Returns False for an empty string (never gate a legitimately empty
    turn). Fires when EITHER:
      * two or more DIFFERENT meta terms are present (dense memory vocabulary), or
      * one meta term is present AND the phrasing is agent-voice about its own
        machinery ("le pipeline", "les jobs", "la base", "chaque nuit").
    A single incidental mention in ordinary user prose ("note que ma mémoire...")
    does not fire.
    """
    msg = (text or "").strip()
    if not msg:
        return False
    # One unambiguous toolkit term is enough.
    if _META_STRONG.search(msg):
        return True
    weak_hits = {m.group(0).lower() for m in _META_WEAK.finditer(msg)}
    # Two different ambiguous terms together = dense memory vocabulary.
    if len(weak_hits) >= 2:
        return True
    # A single ambiguous term only fires in the agent's own voice.
    if weak_hits and _AGENT_VOICE.search(msg):
        return True
    return False


def should_capture(user_msg: str) -> bool:
    """Decide whether an exchange is worth analysing."""
    if is_trivial(user_msg):
        return False
    # M5: never mine the agent's own plumbing for user facts.
    if text_is_self_referential(user_msg):
        return False
    # If there is an explicit signal, definitely capture.
    if has_signal(user_msg):
        return True
    # Otherwise require a non-trivial, entity-bearing sentence.
    return len(user_msg.split()) >= 8


# ─── LLM extraction ───────────────────────────────────────────────────────────


def extract_candidate_facts(user_msg: str, assistant_msg: str,
                            model: str = DEFAULT_MODEL) -> list[dict]:
    """Ask a local LLM for atomic durable facts from the exchange.

    Returns [] on any failure — capture must never crash the caller.
    """
    user_msg = (user_msg or "").strip()
    assistant_msg = (assistant_msg or "").strip()
    if not user_msg:
        return []

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": CAPTURE_PROMPT},
            {
                "role": "user",
                "content": (
                    "Tour de conversation à analyser.\n"
                    f"USER: {user_msg}\n"
                    f"ASSISTANT: {assistant_msg}\n"
                ),
            },
        ],
        "format": "json",
        "stream": False,
        "options": {"temperature": 0.0},
    }

    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=GEN_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        content = data.get("message", {}).get("content", "")
        facts = json.loads(content)
    except (urllib.error.URLError, json.JSONDecodeError, KeyError, TimeoutError,
            ValueError):
        # A small local model may wrap the JSON in prose or trailing text.
        facts = _salvage_json(content if 'content' in dir() else "")

    return _normalise_facts(facts)


def _salvage_json(text: str):
    """Extract the first JSON array or object from a noisy LLM response."""
    if not text:
        return []
    text = text.strip()
    for opener, closer in (("[", "]"), ("{", "}")):
        start = text.find(opener)
        end = text.rfind(closer)
        if start != -1 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                continue
    return []


def _normalise_facts(raw) -> list[dict]:
    """Keep only well-formed, plausible, non-assistant-speculation facts."""
    # A single-object response is a valid one-fact answer: wrap it.
    if isinstance(raw, dict):
        raw = [raw]
    if not isinstance(raw, list):
        return []
    out = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        fact = str(item.get("fact") or item.get("content") or "").strip()
        if len(fact) < 15 or len(fact) > 400:
            continue
        if len(fact.split()) < 3:
            continue
        subject = str(item.get("subject") or "").strip().lower()
        subject = re.sub(r"\s+", "_", subject) or None
        # Anti-hallucination (relaxed in v3.3): a small local model does invent
        # subjects, so we still require SOME grounding in the fact text — but the
        # old rule dropped perfectly good keys. "Serveur Prod" -> tokens
        # ['serveur','prod']; the fact said "serveur principal", so 'prod' was
        # absent and the whole subject was thrown away, leaving subject=NULL.
        # Now: keep the subject if ANY token appears in the fact, and fall back to
        # the first substantial word of the fact rather than discarding it. A
        # subject that grounds nothing is still dropped (true hallucination).
        if subject:
            # '_' is part of '\w', so `re.split(r"[^\w]+", "kavita_home")` returns ONE
            # token and grounding collapses the key to the fallback word "kavita".
            # Split on underscore too, so each entity word grounds on its own —
            # this is the normalisation-truncation bug that shrank multi-word keys.
            tokens = [t for t in re.split(r"[^\w]+", subject.replace("_", " ")) if len(t) >= 3]
            text_words = set(re.findall(r"[\w\u00c0-\u00ff]+", fact.lower()))
            grounded = [t for t in tokens if t in text_words]
            if grounded:
                # Prefer the grounded token(s) — they are the proven anchor.
                subject = "_".join(grounded[:2])
            elif tokens:
                # No token grounded: try the fact's own first meaningful word.
                words = [w.lower() for w in re.findall(r"[A-Za-zÀ-ÿ]{4,}", fact)]
                subject = words[0] if words else None
        try:
            confidence = float(item.get("confidence", 0.7))
        except (TypeError, ValueError):
            confidence = 0.7
        confidence = max(0.0, min(1.0, confidence))
        # Drop hedging/speculative phrasing that leaked through — echo guard.
        if re.search(r"\b(peut-être|pourrait|pourrions|éventuellement|"
                     r"il faudrait|on devrait|hypothèse|supposons)\b", fact, re.I):
            continue
        out.append({"content": fact, "subject": subject,
                    "confidence": confidence})
    return out


# ─── Pipeline ─────────────────────────────────────────────────────────────────


def write_buffer(facts: list[dict], path: str = DEFAULT_BUFFER) -> str:
    with open(path, "w", encoding="utf-8") as fh:
        for item in facts:
            fh.write(json.dumps(item, ensure_ascii=False) + "\n")
    return path


def run_arbitration(buffer_path: str, apply: bool, force: bool,
                    no_llm: bool, no_split: bool = False,
                    db: str = DB_PATH) -> int:
    """Hand the buffer to conflict_resolver.py."""
    cmd = [sys.executable, CONFLICT_RESOLVER, "--db", db, "arbitrate", buffer_path]
    if apply:
        cmd.append("--apply")
    if force:
        cmd.append("--force")
    if no_llm:
        cmd.append("--no-llm")
    if no_split:
        cmd.append("--no-split")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(proc.stdout)
    if proc.returncode != 0 and proc.stderr:
        sys.stderr.write(proc.stderr)
    return proc.returncode


def process_exchange(user_msg: str, assistant_msg: str, args) -> int:
    if not should_capture(user_msg):
        if args.verbose:
            print("⏭  gated: trivial exchange, no capture.")
        return 0

    # M4 echo guard: never mine a machine-generated turn for user facts.
    # We keep the user half (it is still a real assertion) but drop the
    # assistant half so its tool log cannot masquerade as a durable fact.
    if assistant_turn_is_echo(assistant_msg):
        if args.verbose:
            print("⏭  gated: assistant turn is machine output (echo guard).")
        assistant_msg = ""

    facts = extract_candidate_facts(user_msg, assistant_msg, args.model)
    if not facts:
        if args.verbose:
            print("⏭  no durable fact extracted.")
        return 0

    print(f"📥 {len(facts)} fact(s) extracted:")
    for f in facts:
        subj = f["subject"] or "-"
        print(f"   [{subj}] {f['content']}  (conf {f['confidence']:.2f})")

    buf = write_buffer(facts, args.buffer)
    return run_arbitration(buf, apply=args.apply, force=args.force,
                           no_llm=args.no_llm, no_split=args.no_split, db=args.db)


def process_transcript(path: str, args) -> int:
    """Analyse a JSONL transcript of {user, assistant} turns."""
    p = Path(path)
    if not p.exists():
        raise SystemExit(f"❌ transcript not found: {path}")
    turns = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and (obj.get("user") or obj.get("assistant")):
            turns.append((obj.get("user", ""), obj.get("assistant", "")))
    if not turns:
        print("⏭  no turns found in transcript.")
        return 0
    rc = 0
    skipped_trivial = 0
    for user_msg, assistant_msg in turns:
        # Gate A (v3.5): a trivial user turn ("Go", "Ok", "Top", a bare ack)
        # carries no durable fact. When the assistant half is a long report, the
        # only "fact" an extractor could produce would be a restatement of the
        # AGENT's own work — exactly the meta-noise seen in the 2026-10-06 dry-run.
        # Skipping here (rather than extracting then discarding) saves the LLM call.
        if is_trivial(user_msg):
            skipped_trivial += 1
            if getattr(args, "verbose", False):
                print(f"⏭  gated: trivial user turn, no capture. ({user_msg.strip()[:40]!r})")
            continue
        rc = process_exchange(user_msg, assistant_msg, args) or rc
    if skipped_trivial and getattr(args, "verbose", False):
        print(f"⏭  {skipped_trivial} trivial turn(s) skipped before extraction.")
    return rc


# ─── Self-test (no LLM, no DB) ────────────────────────────────────────────────


def selftest() -> int:
    cases = [
        ("salut", False),
        ("ok merci", False),
        ("👍", False),
        ("bien reçu", False),
        ("j'ai migré le serveur sous Ubuntu 24.04", True),
        ("note que mon nouveau tel est un Pixel 9", True),
        ("correction : c'est 4 pas 6", True),
        ("mon nouveau serveur est à jour", True),
        ("il fait beau aujourd'hui", False),
        ("désormais le backup tourne à 23h", True),
    ]
    failures = 0
    for text, expected in cases:
        got = should_capture(text)
        mark = "OK " if got == expected else "FAIL"
        if got != expected:
            failures += 1
        print(f"  {mark} capture={got!s:5} expected={expected!s:5}  {text!r}")

    # Normalisation + echo guard
    raw = [
        {"subject": "Serveur Prod", "fact": "Le serveur principal tourne sous Ubuntu 24.04.", "confidence": 0.95},
        {"subject": "x", "fact": "trop court", "confidence": 0.9},
        {"subject": "z", "fact": "court aussi", "confidence": 0.9},
        {"subject": "y", "fact": "Le serveur pourrait peut-être migrer un jour vers Debian.", "confidence": 0.8},
    ]
    norm = _normalise_facts(raw)
    # v3.3: 'Serveur Prod' is now GROUNDED ('serveur' appears in the fact), so the
    # subject is kept (grounded token), not dropped. The invented subject 'y' on
    # the hedged fact is irrelevant: that item is dropped by the echo guard.
    if len(norm) != 1 or norm[0]["subject"] != "serveur":
        print(f"  FAIL normalisation: {norm}")
        failures += 1
    else:
        print(f"  OK  normalisation + echo guard ({len(norm)} kept of {len(raw)})")

    if failures:
        print(f"\n{failures} failure(s)")
        return 1
    print("\nselftest passed.")
    return 0


# ─── CLI ──────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Auto-Capture — post-turn fact extraction (write-behind).")
    parser.add_argument("--user", help="user message of the exchange")
    parser.add_argument("--assistant", default="", help="assistant reply")
    parser.add_argument("--file", help="JSONL transcript of {user, assistant} turns")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"Ollama model (default: {DEFAULT_MODEL})")
    parser.add_argument("--buffer", default=DEFAULT_BUFFER,
                        help=f"JSONL buffer path (default: {DEFAULT_BUFFER})")
    parser.add_argument("--db", default=DB_PATH, help=f"agent_memory.db path")
    parser.add_argument("--apply", action="store_true",
                        help="Persist resolutions (mutates DB)")
    parser.add_argument("--force", action="store_true",
                        help="Required with --apply in non-interactive mode")
    parser.add_argument("--no-llm", action="store_true",
                        help="Skip LLM relation classification in the resolver")
    parser.add_argument("--no-split", action="store_true",
                        help="Facts are already atomic (skip resolver punctuation split)")
    parser.add_argument("--verbose", action="store_true", help="Explain gating")
    parser.add_argument("--selftest", action="store_true",
                        help="Run gating/normalisation self-test (no LLM/DB)")
    args = parser.parse_args()

    if args.selftest:
        sys.exit(selftest())
    if args.file:
        sys.exit(process_transcript(args.file, args))
    if not args.user:
        parser.error("provide --user <msg> or --file <transcript> (or --selftest)")
    sys.exit(process_exchange(args.user, args.assistant, args))


if __name__ == "__main__":
    main()
