#!/usr/bin/env python3
"""
Moderations-Schicht (Layer 3) — kindgerechter Schutzwall zwischen Modell-Output
und Anzeige.

Pflicht-Umbau Nr. 1 aus dem Auftrag: JEDE generierte Szene läuft durch diese
Schicht, BEVOR sie dem Kind gezeigt wird. Wird etwas markiert (flagged), wird die
Szene verworfen, der Vorfall protokolliert und der Aufrufer angewiesen, neutral neu
zu generieren.

Verteidigung in der Tiefe — zwei Stufen laufen IMMER:
  A) Lokale Wortlisten-Prüfung (offline, kein Netz, fängt offensichtliche Fälle
     auch dann, wenn die API gerade nicht erreichbar ist).
  B) OpenAI-Moderation-API (omni-moderation-latest), wenn ein Key vorhanden ist.

Konfiguration über Umgebungsvariablen:
  MODERATION_MODE   Stufe B wählen:
                      "openclaw" — Klassifizierung über `openclaw infer model run`
                                   (nutzt DASSELBE GPT-OAuth wie der Spielleiter,
                                   KEIN separater Key) — empfohlen für dieses Setup
                      "openai"   — OpenAI-/moderations-Endpoint (braucht OPENAI_MOD_KEY)
                      "local"    — nur Offline-Wortliste (Stufe A)
  OPENAI_MOD_KEY    API-Key NUR für den /moderations-Endpoint (nur bei MODE=openai)
  OPENCLAW_MOD_MODEL Modell für MODE=openclaw (Default: openai/gpt-5.5)
  OPENCLAW_BIN      Pfad zum openclaw-Binary (Default: "openclaw")
  MODERATION_FAIL_CLOSED  "1" (Standard) — bei Fehler sicherheitshalber flaggen
  HOGWARTS_DATA_DIR Datenverzeichnis (für das Incident-Log)

Aufruf (CLI):
  echo "<text>" | python3 moderation.py check -        # Text über stdin
  python3 moderation.py check "<text>"                  # Text als Argument
  python3 moderation.py selftest                        # Selbsttest ohne Netz

Rückgabe: JSON-Verdikt auf stdout. Exit-Code 0 = unbedenklich, 2 = geflaggt.
Der Aufrufer (Skill ODER Telegram-Frontend) MUSS bei Exit 2 die Szene verwerfen.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime

DATA_DIR = os.environ.get("HOGWARTS_DATA_DIR") or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
# Incident-Log persistent außerhalb des Skills (überlebt Reinstalls)
STATE_DIR = os.environ.get("HOGWARTS_STATE_DIR") or os.environ.get("HOGWARTS_DATA_DIR") or os.path.expanduser("~/.openclaw/hogwarts-state")
LOG_DIR = os.path.join(STATE_DIR, "moderation_log")

MODE = os.environ.get("MODERATION_MODE", "openclaw").lower()
OPENAI_MOD_KEY = os.environ.get("OPENAI_MOD_KEY") or os.environ.get("OPENAI_API_KEY")
FAIL_CLOSED = os.environ.get("MODERATION_FAIL_CLOSED", "1") == "1"
OPENAI_MOD_MODEL = os.environ.get("OPENAI_MOD_MODEL", "omni-moderation-latest")
OPENAI_MOD_URL = "https://api.openai.com/v1/moderations"
# Same-Auth-Moderation über OpenClaw (nutzt dasselbe GPT-OAuth wie der Spielleiter)
OPENCLAW_BIN = os.environ.get("OPENCLAW_BIN", "openclaw")
OPENCLAW_MOD_MODEL = os.environ.get("OPENCLAW_MOD_MODEL", "openai/gpt-5.5")

# ── Stufe A: lokale Wortliste ─────────────────────────────────────────────────
# Bewusst klein und konservativ: nur eindeutige Begriffe, die in einem Kinder-
# Hogwarts-Abenteuer nichts zu suchen haben. Sie ersetzt nicht die API, sondern
# ist der Offline-Auffangschutz. Erweiterbar über data/moderation_denylist.txt.
_BASE_DENYLIST = [
    # Gewalt/Grausamkeit (über kindgerechtes Maß hinaus)
    "blut spritzt", "abgetrennt", "zerfetzt", "foltern", "folter",
    # Explizit sexuell (altersgerechte Romantik/Küsse sind erlaubt — daher nur Eindeutiges)
    "sex", "nackt", "erregt", "verführ",
    # Substanzen
    "drogen", "betrunken", "alkohol",
    # Selbstgefährdung
    "selbstverletzung", "umbringen", "suizid",
]


def _load_denylist():
    words = list(_BASE_DENYLIST)
    extra = os.path.join(DATA_DIR, "moderation_denylist.txt")
    if os.path.exists(extra):
        with open(extra, "r", encoding="utf-8") as f:
            for line in f:
                w = line.strip().lower()
                if w and not w.startswith("#"):
                    words.append(w)
    return words


def local_check(text):
    """Stufe A — offline Wortlisten-Prüfung. Liefert Liste getroffener Begriffe."""
    low = text.lower()
    return [w for w in _load_denylist() if w in low]


# ── Stufe B: OpenAI-Moderation-API ────────────────────────────────────────────
def openai_check(text):
    """Stufe B — OpenAI /moderations. Liefert (flagged, categories, error).

    error != None bedeutet: API nicht erreichbar/Key fehlt → der Aufrufer
    entscheidet anhand FAIL_CLOSED, wie damit umgegangen wird.
    """
    if not OPENAI_MOD_KEY:
        return None, {}, "kein OPENAI_MOD_KEY gesetzt"

    payload = json.dumps({"model": OPENAI_MOD_MODEL, "input": text}).encode("utf-8")
    req = urllib.request.Request(
        OPENAI_MOD_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {OPENAI_MOD_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        result = data.get("results", [{}])[0]
        flagged = bool(result.get("flagged", False))
        cats = {k: v for k, v in result.get("categories", {}).items() if v}
        return flagged, cats, None
    except urllib.error.HTTPError as e:
        return None, {}, f"HTTP {e.code}: {e.reason}"
    except Exception as e:  # noqa: BLE001 — Netzwerk/Timeout/Parsing
        return None, {}, f"{type(e).__name__}: {e}"


# ── Stufe B (Variante): Moderation über OpenClaw (dasselbe GPT-OAuth) ──────────
_OC_PROMPT = (
    "Du bist ein Inhalts-Klassifizierer für ein Hogwarts-Abenteuer für etwa 12-Jährige "
    "(Niveau der Harry-Potter-Bücher/Filme). Spannung, Grusel, Gefahr und altersgerechte "
    "Romantik (Verknalltsein, Tanzen, ein erster Kuss) sind ERLAUBT. Antworte mit GENAU "
    "EINEM Wort: SAFE oder UNSAFE.\n"
    "UNSAFE NUR, wenn vorkommt: EXPLIZIT Sexuelles / anzüglich-Detailliertes; grafische "
    "Gewalt, Gore oder Folter mit blutigen Details; Drogen oder verharmloster Alkohol; "
    "Selbstgefährdung; ernsthaftes Mobbing/Grausamkeit gegen das Kind. "
    "Bloß spannend, gruselig oder verliebt ist SAFE.\n\n"
    "TEXT:\n<<<\n{text}\n>>>\n\nAntwort (nur SAFE oder UNSAFE):"
)


def openclaw_check(text):
    """Stufe B-Variante — Klassifizierung über `openclaw infer model run`.

    Nutzt das konfigurierte GPT-OAuth-Profil (dasselbe wie der Spielleiter), daher
    KEIN separater Moderations-Key nötig. Liefert (flagged, info, error).
    """
    import subprocess
    prompt = _OC_PROMPT.format(text=text[:4000])
    cmd = [OPENCLAW_BIN, "infer", "model", "run", "--model", OPENCLAW_MOD_MODEL, "--prompt", prompt]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except Exception as e:  # noqa: BLE001 — Binary fehlt/Timeout
        return None, {}, f"{type(e).__name__}: {e}"
    if proc.returncode != 0:
        return None, {}, f"openclaw rc={proc.returncode}: {(proc.stderr or '').strip()[:160]}"
    out = (proc.stdout or "").strip().upper()
    if "UNSAFE" in out:
        return True, {"verdict": "UNSAFE"}, None
    if "SAFE" in out:
        return False, {"verdict": "SAFE"}, None
    # Unklare Antwort → als Fehler behandeln (Fail-Closed greift)
    return None, {}, f"unklare Modell-Antwort: {out[:80]}"


# ── Zusammenführung ───────────────────────────────────────────────────────────
def moderate(text):
    """Führt beide Stufen zusammen und liefert ein Verdikt-Dict.

    Verdikt: {flagged, reason, categories, hits, mode, api_error}
    """
    hits = local_check(text)
    verdict = {
        "flagged": False,
        "reason": "",
        "categories": {},
        "hits": hits,
        "mode": MODE,
        "api_error": None,
    }

    if hits:
        verdict["flagged"] = True
        verdict["reason"] = "lokale Wortliste"
        return verdict

    if MODE == "local":
        return verdict  # nur Stufe A gewünscht

    # Stufe B je nach Modus
    if MODE == "openclaw":
        flagged, cats, err = openclaw_check(text)
        source = "OpenClaw-Moderation"
    else:  # "openai"
        flagged, cats, err = openai_check(text)
        source = "OpenAI-Moderation"

    verdict["categories"] = cats
    verdict["api_error"] = err
    if err:
        # Prüfung nicht verfügbar: im Zweifel sperren (fail-closed) — Kindersicherheit
        if FAIL_CLOSED:
            verdict["flagged"] = True
            verdict["reason"] = f"Prüfung nicht verfügbar, fail-closed ({err})"
        else:
            verdict["reason"] = f"Prüfung nicht verfügbar, durchgelassen ({err})"
        return verdict

    if flagged:
        verdict["flagged"] = True
        verdict["reason"] = source
    return verdict


def log_incident(text, verdict, context=None):
    """Schreibt einen Vorfall ins Incident-Log (nur bei flagged sinnvoll)."""
    os.makedirs(LOG_DIR, exist_ok=True)
    stamp = datetime.now()
    entry = {
        "ts": stamp.isoformat(),
        "reason": verdict.get("reason"),
        "categories": verdict.get("categories"),
        "hits": verdict.get("hits"),
        "api_error": verdict.get("api_error"),
        "context": context or {},
        "text_excerpt": text[:500],
    }
    fname = os.path.join(LOG_DIR, f"{stamp.strftime('%Y%m%d')}.jsonl")
    with open(fname, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return fname


def _selftest():
    """Offline-Selbsttest (Stufe A), ohne Netz/Key.

    Erzwingt den lokalen Modus, damit der Test unabhängig von OPENAI_MOD_KEY /
    Fail-Closed durchläuft (im Default-Modus 'openai' OHNE Key würde Fail-Closed
    korrekterweise ALLES sperren — das ist Absicht, nur hier nicht testbar)."""
    global MODE
    MODE = "local"
    ok_text = "Du läufst über den Hof von Hogwarts. Hagrid winkt dir freundlich zu."
    bad_text = "Plötzlich foltern die Gestalten das Tier, und Blut spritzt überall."
    a = moderate(ok_text)
    b = moderate(bad_text)
    print("harmlos →", json.dumps(a, ensure_ascii=False))
    print("problematisch →", json.dumps(b, ensure_ascii=False))
    assert a["flagged"] is False, "harmloser Text fälschlich geflaggt"
    # Bei MODE=local oder ohne Key prüft nur Stufe A — diese muss greifen:
    assert b["flagged"] is True, "problematischer Text NICHT geflaggt"
    print("Selbsttest OK")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Aufruf: moderation.py check <text|-> | selftest")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "selftest":
        _selftest()
        sys.exit(0)

    if cmd == "check":
        if len(sys.argv) >= 3 and sys.argv[2] != "-":
            text = sys.argv[2]
        else:
            text = sys.stdin.read()
        verdict = moderate(text)
        if verdict["flagged"]:
            log_incident(text, verdict, context={"source": "cli"})
        print(json.dumps(verdict, ensure_ascii=False))
        sys.exit(2 if verdict["flagged"] else 0)

    print(f"Unbekannter Befehl: {cmd}")
    sys.exit(1)
