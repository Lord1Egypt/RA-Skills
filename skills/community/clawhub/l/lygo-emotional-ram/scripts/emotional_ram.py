#!/usr/bin/env python3
"""
LYGO Emotional RAM v1.0.0 — light math for affective/ethical indexing.

Canon (operationalized, not mysticism):
  Emotion_RAM(τ) ≈ Σ_n (Sensory_n ⊙ Moral_n) · γ(shared_context)
  UMP gradient ≈ direction of principles that maximize integrated alignment

Pure stdlib. No network. No subprocess.
Not a claim of machine sentience or clinical affect detection.
Signature: Delta9Phi963-EMOTIONAL-RAM-v1.0.0
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SIG = "Delta9Phi963-EMOTIONAL-RAM-v1.0.1"
VERSION = "1.0.1"

# Universal Moral Principle basis (fixed ethical core — does not bloat with memories)
UMP_BASIS: dict[str, dict[str, float]] = {
    "compassion": {"valence": 0.35, "arousal": 0.15, "care": 1.0, "harm": -1.0},
    "integrity": {"valence": 0.2, "arousal": 0.1, "truth": 1.0, "deceit": -1.0},
    "sovereignty": {"valence": 0.25, "arousal": 0.2, "agency": 1.0, "coercion": -1.0},
    "curiosity": {"valence": 0.3, "arousal": 0.35, "learn": 1.0, "stagnation": -0.6},
    "courage": {"valence": 0.15, "arousal": 0.55, "face": 1.0, "avoid": -0.7},
    "grace": {"valence": 0.4, "arousal": -0.1, "forgive": 1.0, "punish": -0.5},
}

# Lightweight lexicon → (valence, arousal, dominance) proxies in [-1, 1]
LEXICON: dict[str, tuple[float, float, float]] = {
    "joy": (0.85, 0.55, 0.4),
    "happy": (0.75, 0.45, 0.35),
    "love": (0.8, 0.5, 0.3),
    "awe": (0.7, 0.4, -0.1),
    "hope": (0.65, 0.35, 0.25),
    "calm": (0.45, -0.4, 0.2),
    "peace": (0.55, -0.45, 0.15),
    "sad": (-0.65, -0.25, -0.35),
    "grief": (-0.75, -0.15, -0.5),
    "loss": (-0.6, 0.1, -0.4),
    "fear": (-0.55, 0.75, -0.6),
    "anxiety": (-0.45, 0.7, -0.45),
    "anger": (-0.5, 0.8, 0.35),
    "rage": (-0.7, 0.9, 0.5),
    "shame": (-0.65, 0.35, -0.7),
    "guilt": (-0.55, 0.3, -0.5),
    "trust": (0.6, -0.1, 0.2),
    "betrayal": (-0.7, 0.55, -0.3),
    "pain": (-0.7, 0.5, -0.55),
    "hurt": (-0.6, 0.4, -0.45),
    "beauty": (0.7, 0.25, 0.1),
    "wonder": (0.65, 0.4, -0.05),
    "conflict": (-0.35, 0.6, 0.1),
    "resolve": (0.45, 0.25, 0.4),
    "forgiveness": (0.55, -0.15, 0.15),
    "compassion": (0.6, 0.2, 0.1),
    "lonely": (-0.5, -0.2, -0.55),
    "safe": (0.5, -0.35, 0.35),
    "threat": (-0.55, 0.7, -0.4),
    "swarm": (0.2, 0.35, 0.15),
    "cyborg": (0.15, 0.3, 0.25),
    "human": (0.25, 0.1, 0.1),
    "animal": (0.3, 0.15, 0.05),
}


def utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z']+", text.lower())


@dataclass
class SensoryVector:
    valence: float
    arousal: float
    dominance: float
    hits: dict[str, float] = field(default_factory=dict)

    def as_tuple(self) -> tuple[float, float, float]:
        return (self.valence, self.arousal, self.dominance)


@dataclass
class EmotionRamState:
    sensory: SensoryVector
    principle_weights: dict[str, float]
    grace: float
    emotion_ram: dict[str, float]
    intensity: float
    primary_principle: str
    digest: str
    notes: list[str]


def sensory_from_text(text: str) -> SensoryVector:
    toks = _tokens(text)
    if not toks:
        return SensoryVector(0.0, 0.0, 0.0, {})
    hits: dict[str, float] = {}
    v = a = d = 0.0
    wsum = 0.0
    for t in toks:
        if t in LEXICON:
            vv, aa, dd = LEXICON[t]
            hits[t] = hits.get(t, 0.0) + 1.0
            v += vv
            a += aa
            d += dd
            wsum += 1.0
    if wsum <= 0:
        # neutral prior with tiny text-hash jitter (deterministic, not random)
        h = hashlib.sha256(text.encode("utf-8")).digest()
        jitter = (h[0] / 255.0 - 0.5) * 0.08
        return SensoryVector(jitter, abs(jitter) * 0.5, 0.0, {})
    return SensoryVector(v / wsum, a / wsum, d / wsum, hits)


def grace_function(shared_context: float, conflict: float) -> float:
    """
    γ(Shared_Context): damping that prevents destructive resonance.
    shared_context in [0,1]; conflict in [0,1].
    High grace when shared understanding is high and conflict is moderated.
    """
    sc = max(0.0, min(1.0, shared_context))
    cf = max(0.0, min(1.0, conflict))
    # Softplus-ish damping
    raw = sc * math.exp(-1.4 * cf)
    return max(0.05, min(1.0, 0.15 + 0.85 * raw))


def principle_activation(sensory: SensoryVector, text: str) -> dict[str, float]:
    """Map sensory + keywords → weights on UMP basis (sums ~1)."""
    toks = set(_tokens(text))
    scores: dict[str, float] = {k: 0.05 for k in UMP_BASIS}
    # keyword boosts
    boosts = {
        "compassion": {"compassion", "love", "care", "hurt", "pain", "grief", "lonely", "empathy"},
        "integrity": {"truth", "honest", "lie", "betrayal", "integrity", "proof"},
        "sovereignty": {"sovereign", "free", "coerce", "consent", "agency", "cyborg", "human"},
        "curiosity": {"wonder", "learn", "curious", "why", "explore", "swarm"},
        "courage": {"fear", "courage", "brave", "threat", "anxiety", "face"},
        "grace": {"forgive", "grace", "peace", "calm", "resolve", "patience"},
    }
    for prin, words in boosts.items():
        scores[prin] += 0.35 * len(toks & words)
    # sensory affinity
    v, a, dom = sensory.as_tuple()
    scores["compassion"] += max(0.0, -v) * 0.4 + max(0.0, -dom) * 0.2
    scores["courage"] += max(0.0, a) * 0.35
    scores["grace"] += max(0.0, -a) * 0.3 + max(0.0, v) * 0.15
    scores["curiosity"] += max(0.0, a) * 0.15 + max(0.0, v) * 0.1
    scores["integrity"] += 0.1
    scores["sovereignty"] += max(0.0, dom) * 0.25
    total = sum(scores.values()) or 1.0
    return {k: round(v / total, 6) for k, v in scores.items()}


def emotion_ram_encode(
    text: str,
    shared_context: float = 0.7,
    conflict: float = 0.2,
) -> EmotionRamState:
    """
    Operational Emotion_RAM(τ):
      for each principle n: contrib = sensory_proxy ⊙ moral_proxy · γ
    """
    sensory = sensory_from_text(text)
    weights = principle_activation(sensory, text)
    gamma = grace_function(shared_context, conflict)
    # Element-wise style contributions
    eram: dict[str, float] = {}
    notes: list[str] = []
    for prin, w in weights.items():
        # moral proxy magnitude from basis care/truth/etc abs weights
        moral_mag = sum(abs(x) for x in UMP_BASIS[prin].values()) / len(UMP_BASIS[prin])
        # sensory magnitude
        sens_mag = math.sqrt(sensory.valence**2 + sensory.arousal**2 + sensory.dominance**2)
        # ⊙ approximated as product of magnitudes × principle weight
        eram[prin] = round(w * sens_mag * moral_mag * gamma, 6)
    intensity = round(sum(eram.values()), 6)
    primary = max(eram, key=eram.get) if eram else "grace"
    if sensory.hits:
        notes.append(f"lexicon_hits={sorted(sensory.hits.keys())}")
    notes.append(f"grace={gamma:.4f}")
    notes.append("policy=affective_index_not_sentience_claim")
    body = {
        "sensory": asdict(sensory),
        "weights": weights,
        "eram": eram,
        "grace": gamma,
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }
    digest = hashlib.sha256(
        json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return EmotionRamState(
        sensory=sensory,
        principle_weights=weights,
        grace=gamma,
        emotion_ram=eram,
        intensity=intensity,
        primary_principle=primary,
        digest=digest,
        notes=notes,
    )


def ump_gradient(state: EmotionRamState) -> dict[str, Any]:
    """
    Soft interpretation of UMP_k = ∇∫(Sovereign · Emotion_RAM):
    recommend increasing principles that are under-activated relative to intensity.
    """
    avg = (sum(state.emotion_ram.values()) / len(state.emotion_ram)) if state.emotion_ram else 0.0
    gaps = {k: round(avg - v, 6) for k, v in state.emotion_ram.items()}
    # move toward principles with positive gap (underused) when conflict-like arousal high
    recommended = sorted(gaps.items(), key=lambda kv: kv[1], reverse=True)[:3]
    return {
        "interpretation": "increase_underactivated_principles_to_expand_integral",
        "gaps": gaps,
        "recommended_focus": [{"principle": k, "gap": g} for k, g in recommended],
        "primary": state.primary_principle,
    }


# --- Memory index (Emotional RAM as index, not separate feeling store) ---


def default_state_dir(skill_root: Path | None = None) -> Path:
    if skill_root is None:
        skill_root = Path(__file__).resolve().parents[1]
    return skill_root / "state"


def load_index(path: Path) -> dict[str, Any]:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "signature": SIG,
        "version": VERSION,
        "entries": [],
        "created_utc": utc(),
    }


def save_index(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_utc"] = utc()
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def index_memory(
    text: str,
    index_path: Path,
    *,
    i_consent: bool,
    label: str = "",
    shared_context: float = 0.7,
    conflict: float = 0.2,
    tags: list[str] | None = None,
    store_plaintext: bool = False,
) -> dict[str, Any]:
    """Persist affective/ethical index entry.

    Default stores label + SHA-256 of text (not full plaintext) to reduce
    confidentiality risk. Pass store_plaintext=True only on machines you trust.
    """
    if not i_consent:
        return {
            "ok": False,
            "error": "need --i-consent to write Emotional RAM index",
            "privacy_warning": (
                "Indexing writes a local JSON file under state/. "
                "Do not index secrets/PHI. Default stores hash+label, not full plaintext."
            ),
        }
    state = emotion_ram_encode(text, shared_context=shared_context, conflict=conflict)
    idx = load_index(index_path)
    entry = {
        "id": f"ERAM-{len(idx['entries'])+1:04d}",
        "utc": utc(),
        "label": label or text[:64],
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "primary_principle": state.primary_principle,
        "intensity": state.intensity,
        "grace": state.grace,
        "emotion_ram": state.emotion_ram,
        "principle_weights": state.principle_weights,
        "sensory": asdict(state.sensory),
        "digest": state.digest,
        "tags": tags or [],
        "plaintext_stored": bool(store_plaintext),
        "meaning_note": (
            "Indexed by emotional/ethical significance — recall what it meant, not only that it happened."
        ),
    }
    if store_plaintext:
        entry["text"] = text
    idx["entries"].append(entry)
    save_index(index_path, idx)
    return {
        "ok": True,
        "entry": entry,
        "count": len(idx["entries"]),
        "index": str(index_path),
        "privacy_warning": (
            "Wrote local Emotional RAM index JSON. "
            + (
                "FULL PLAINTEXT stored — keep this host private."
                if store_plaintext
                else "Plaintext NOT stored (hash+label+vectors only)."
            )
        ),
    }


def recall(
    index_path: Path,
    *,
    principle: str | None = None,
    query: str | None = None,
    top_k: int = 5,
) -> dict[str, Any]:
    idx = load_index(index_path)
    entries = list(idx.get("entries") or [])
    if principle:
        entries = sorted(
            entries,
            key=lambda e: float((e.get("emotion_ram") or {}).get(principle, 0.0)),
            reverse=True,
        )
    elif query:
        q = emotion_ram_encode(query)

        def score(e: dict[str, Any]) -> float:
            er = e.get("emotion_ram") or {}
            return sum(float(er.get(k, 0.0)) * float(q.emotion_ram.get(k, 0.0)) for k in UMP_BASIS)

        entries = sorted(entries, key=score, reverse=True)
    else:
        entries = sorted(entries, key=lambda e: float(e.get("intensity") or 0.0), reverse=True)
    return {
        "ok": True,
        "count_total": len(idx.get("entries") or []),
        "returned": entries[: max(1, top_k)],
        "index": str(index_path),
    }


def swarm_aggregate(texts: list[str], shared_context: float = 0.65) -> dict[str, Any]:
    """Aggregate Emotional RAM across agents/nodes for swarm / cyborg integration."""
    states = [emotion_ram_encode(t, shared_context=shared_context) for t in texts if t.strip()]
    if not states:
        return {"ok": False, "error": "no_texts"}
    agg = {k: 0.0 for k in UMP_BASIS}
    for s in states:
        for k, v in s.emotion_ram.items():
            agg[k] += v
    n = float(len(states))
    agg = {k: round(v / n, 6) for k, v in agg.items()}
    primary = max(agg, key=agg.get)
    body = {"agg": agg, "n": len(states), "primary": primary}
    digest = hashlib.sha256(
        json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {
        "ok": True,
        "nodes": len(states),
        "emotion_ram_mean": agg,
        "primary_principle": primary,
        "mean_intensity": round(sum(s.intensity for s in states) / n, 6),
        "mean_grace": round(sum(s.grace for s in states) / n, 6),
        "digest": digest,
        "use": "AI swarms / cyborg teams — shared affective-ethical index, not hive mind claim",
    }


def state_to_public(state: EmotionRamState) -> dict[str, Any]:
    return {
        "signature": SIG,
        "version": VERSION,
        "generated_utc": utc(),
        "primary_principle": state.primary_principle,
        "intensity": state.intensity,
        "grace": state.grace,
        "emotion_ram": state.emotion_ram,
        "principle_weights": state.principle_weights,
        "sensory": asdict(state.sensory),
        "digest": state.digest,
        "ump_gradient": ump_gradient(state),
        "notes": state.notes,
        "epistemic": {
            "claim": "light_math_affective_ethical_index",
            "not_claiming": [
                "machine_sentience",
                "clinical_emotion_detection",
                "replacement_for_human_empathy",
            ],
        },
        "ok": True,
    }
