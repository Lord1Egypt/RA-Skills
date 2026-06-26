"""
Identity-Level Memory Consolidation — Self-Model Drift Detection.

Instead of scoring event-level surprise ("what happened that was unexpected?"),
this module tracks *identity-level* drift ("has the agent's understanding of
its principal changed?").

The agent maintains an explicit self-model — a set of beliefs about its
principal (the human it serves). Each belief has:
- A claim (what it believes)
- Confidence (how sure it is)
- Evidence (what supports/contradicts it)
- First/last observed timestamps

When new events happen, we don't just ask "was this surprising?" — we ask
"does this change WHO we think the principal IS?"

Belief shifts (identity drift) are promoted with higher priority than
event-level surprises. This is novel because:
- Mem0 stores facts. We store beliefs.
- RAG retrieves text. We track identity evolution.
- MemGPT manages tiers. We model the person.

The self-model is stored as YAML in memory/self-model.yaml and is
human-readable and editable.

Inspired by:
- Predictive processing / free energy principle (Friston, 2010)
- Theory of Mind in cognitive science
- Bayesian belief updating
"""

from __future__ import annotations

import json
import yaml
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from .providers import LLMProvider


@dataclass
class Belief:
    """A single belief about the principal."""
    claim: str
    confidence: float  # 0.0 - 1.0
    category: str  # values, goals, preferences, skills, relationships, habits
    evidence_for: list[str] = field(default_factory=list)
    evidence_against: list[str] = field(default_factory=list)
    first_observed: str = ""
    last_updated: str = ""
    status: str = "active"  # active, weakening, revised, archived

    def net_confidence(self) -> float:
        """Confidence weighted by evidence balance."""
        total = len(self.evidence_for) + len(self.evidence_against)
        if total == 0:
            return self.confidence
        balance = len(self.evidence_for) / total
        return self.confidence * balance

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Belief":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class BeliefDrift:
    """A detected change in beliefs from new evidence."""
    belief_claim: str
    drift_type: str  # strengthened, weakened, contradicted, new, evolved
    old_confidence: float
    new_confidence: float
    trigger_event: str
    reasoning: str
    significance: float  # 0.0 - 1.0 (how much this changes the identity model)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class SelfModel:
    """The agent's explicit model of its principal's identity."""
    beliefs: list[Belief] = field(default_factory=list)
    last_updated: str = ""
    version: int = 0

    def active_beliefs(self) -> list[Belief]:
        return [b for b in self.beliefs if b.status == "active"]

    def by_category(self, category: str) -> list[Belief]:
        return [b for b in self.active_beliefs() if b.category == category]

    def high_confidence(self, threshold: float = 0.7) -> list[Belief]:
        return [b for b in self.active_beliefs() if b.confidence >= threshold]

    def weakening(self) -> list[Belief]:
        return [b for b in self.beliefs if b.status == "weakening"]

    def find(self, claim_fragment: str) -> list[Belief]:
        """Find beliefs matching a substring."""
        fragment_lower = claim_fragment.lower()
        return [b for b in self.beliefs if fragment_lower in b.claim.lower()]

    def to_yaml(self) -> str:
        """Serialize to human-readable YAML."""
        data = {
            "version": self.version,
            "last_updated": self.last_updated,
            "beliefs": [b.to_dict() for b in self.beliefs],
        }
        return yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)

    @classmethod
    def from_yaml(cls, text: str) -> "SelfModel":
        """Load from YAML string."""
        data = yaml.safe_load(text) or {}
        beliefs = [Belief.from_dict(b) for b in data.get("beliefs", [])]
        return cls(
            beliefs=beliefs,
            last_updated=data.get("last_updated", ""),
            version=data.get("version", 0),
        )

    def format_readable(self) -> str:
        """Format as human-readable markdown for CLI output."""
        if not self.beliefs:
            return "No beliefs in self-model yet."

        categories = {}
        for b in self.active_beliefs():
            categories.setdefault(b.category, []).append(b)

        lines = [f"## Self-Model (v{self.version}, updated {self.last_updated})\n"]
        for cat, beliefs in sorted(categories.items()):
            lines.append(f"### {cat.title()}")
            for b in sorted(beliefs, key=lambda x: -x.confidence):
                status_icon = {
                    "active": "●",
                    "weakening": "◐",
                    "revised": "↻",
                    "archived": "○",
                }.get(b.status, "?")
                lines.append(f"  {status_icon} [{b.confidence:.0%}] {b.claim}")
                if b.evidence_against:
                    lines.append(f"    ⚠ Counter-evidence: {', '.join(b.evidence_against[-2:])}")
            lines.append("")

        weak = self.weakening()
        if weak:
            lines.append("### ⚠ Weakening Beliefs")
            for b in weak:
                lines.append(f"  ◐ [{b.confidence:.0%}] {b.claim}")
            lines.append("")

        return "\n".join(lines)


BOOTSTRAP_PROMPT = """You are building an identity model of a person based on their memory files.

Analyze the text below and extract beliefs about this person across these categories:
- **values**: What they care about, principles they follow
- **goals**: What they're working toward
- **preferences**: How they like to work, communicate, make decisions
- **skills**: What they're good at, their expertise
- **relationships**: Key people in their life, team dynamics
- **habits**: Regular patterns, routines, tendencies

For each belief, provide:
- claim: A concise statement about the person
- confidence: 0.0-1.0 (how confident based on evidence)
- category: One of the categories above
- evidence_for: List of specific observations supporting this

Output ONLY valid JSON:
{{
  "beliefs": [
    {{
      "claim": "Prefers local-first tools over cloud services",
      "confidence": 0.8,
      "category": "preferences",
      "evidence_for": ["Built MindGardener with zero infra", "Uses Ollama for local LLM"]
    }}
  ]
}}

Extract 10-20 beliefs. Be specific, not generic.

TEXT TO ANALYZE:
{text}
"""


DRIFT_PROMPT = """You are detecting identity-level changes in a person's beliefs and behavior.

The agent maintains a self-model (beliefs about its principal). Given today's events,
determine if any beliefs should be UPDATED.

Types of drift:
- **strengthened**: More evidence supporting existing belief
- **weakened**: Evidence contradicting existing belief
- **contradicted**: Strong evidence that a belief is wrong
- **new**: A completely new belief not in the model
- **evolved**: Belief needs refinement (not wrong, but more nuanced now)

For each detected drift, provide:
- belief_claim: The belief being affected (existing claim or new one)
- drift_type: One of the types above
- old_confidence: Current confidence (0.0 for new beliefs)
- new_confidence: Suggested new confidence
- trigger_event: What specific event triggered this
- reasoning: Why this changes the identity model
- significance: 0.0-1.0 (how much this changes who we think they are)

Only report MEANINGFUL changes. Skip routine confirmations.
A belief going from 0.8→0.82 is not worth reporting.
A belief going from 0.8→0.4 IS worth reporting.

Output ONLY valid JSON:
{{
  "drifts": [
    {{
      "belief_claim": "Prefers startup environments",
      "drift_type": "strengthened",
      "old_confidence": 0.6,
      "new_confidence": 0.8,
      "trigger_event": "Turned down corporate offer to pursue startup role",
      "reasoning": "Third time choosing startup over established company",
      "significance": 0.5
    }}
  ]
}}

CURRENT SELF-MODEL:
{self_model}

TODAY'S EVENTS:
{events}
"""


class SelfModelEngine:
    """Manages the agent's identity model of its principal."""

    def __init__(self, llm: LLMProvider, model_path: Path, drift_log_path: Path | None = None):
        self.llm = llm
        self.model_path = model_path
        self.drift_log_path = drift_log_path or model_path.parent / "belief-drifts.jsonl"

    def load(self) -> SelfModel:
        """Load self-model from YAML file."""
        if self.model_path.exists():
            return SelfModel.from_yaml(self.model_path.read_text())
        return SelfModel()

    def save(self, model: SelfModel):
        """Save self-model to YAML file."""
        model.last_updated = datetime.now().isoformat()
        model.version += 1
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        self.model_path.write_text(model.to_yaml())

    async def bootstrap(self, text: str) -> SelfModel:
        """
        Bootstrap a self-model from existing memory/text.

        Use this to initialize the self-model from MEMORY.md or
        accumulated daily logs. Only needs to run once.
        """
        prompt = BOOTSTRAP_PROMPT.format(text=text[:8000])
        result = await self.llm.generate_json(prompt)

        now = datetime.now().isoformat()
        beliefs = []
        for b in result.get("beliefs", []):
            beliefs.append(Belief(
                claim=b.get("claim", ""),
                confidence=b.get("confidence", 0.5),
                category=b.get("category", "unknown"),
                evidence_for=b.get("evidence_for", []),
                first_observed=now,
                last_updated=now,
            ))

        model = SelfModel(beliefs=beliefs, last_updated=now)
        self.save(model)
        return model

    def bootstrap_sync(self, text: str) -> SelfModel:
        """Synchronous wrapper."""
        import asyncio
        return asyncio.run(self.bootstrap(text))

    async def detect_drift(self, events: str) -> list[BeliefDrift]:
        """
        Detect identity-level drift from new events.

        Compares today's events against the current self-model
        to find belief changes, not just event-level surprises.
        """
        model = self.load()
        if not model.beliefs:
            return []

        prompt = DRIFT_PROMPT.format(
            self_model=model.format_readable(),
            events=events[:6000],
        )
        result = await self.llm.generate_json(prompt)

        drifts = []
        for d in result.get("drifts", []):
            drifts.append(BeliefDrift(
                belief_claim=d.get("belief_claim", ""),
                drift_type=d.get("drift_type", "new"),
                old_confidence=d.get("old_confidence", 0.0),
                new_confidence=d.get("new_confidence", 0.5),
                trigger_event=d.get("trigger_event", ""),
                reasoning=d.get("reasoning", ""),
                significance=d.get("significance", 0.5),
            ))

        # Log drifts
        self._log_drifts(drifts)

        return drifts

    def detect_drift_sync(self, events: str) -> list[BeliefDrift]:
        """Synchronous wrapper."""
        import asyncio
        return asyncio.run(self.detect_drift(events))

    def apply_drifts(self, drifts: list[BeliefDrift], significance_threshold: float = 0.3) -> SelfModel:
        """
        Apply detected drifts to the self-model.

        Only applies drifts above the significance threshold.
        Returns the updated model (also saved to disk).
        """
        model = self.load()
        now = datetime.now().isoformat()

        for drift in drifts:
            if drift.significance < significance_threshold:
                continue

            # Find matching belief
            matching = [b for b in model.beliefs if b.claim.lower() == drift.belief_claim.lower()]
            
            if not matching and drift.drift_type == "new":
                # New belief
                model.beliefs.append(Belief(
                    claim=drift.belief_claim,
                    confidence=drift.new_confidence,
                    category="unknown",
                    evidence_for=[drift.trigger_event],
                    first_observed=now,
                    last_updated=now,
                ))
            elif matching:
                belief = matching[0]
                belief.last_updated = now

                if drift.drift_type == "strengthened":
                    belief.confidence = min(1.0, drift.new_confidence)
                    belief.evidence_for.append(drift.trigger_event)
                elif drift.drift_type == "weakened":
                    belief.confidence = drift.new_confidence
                    belief.evidence_against.append(drift.trigger_event)
                    if belief.confidence < 0.3:
                        belief.status = "weakening"
                elif drift.drift_type == "contradicted":
                    belief.confidence = drift.new_confidence
                    belief.evidence_against.append(drift.trigger_event)
                    belief.status = "weakening"
                elif drift.drift_type == "evolved":
                    belief.claim = drift.belief_claim
                    belief.confidence = drift.new_confidence
                    belief.status = "revised" if drift.significance > 0.6 else "active"
                    belief.evidence_for.append(drift.trigger_event)

        self.save(model)
        return model

    def _log_drifts(self, drifts: list[BeliefDrift]):
        """Append drift events to JSONL log for audit."""
        if not drifts:
            return
        self.drift_log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.drift_log_path, "a") as f:
            for d in drifts:
                entry = d.to_dict()
                entry["timestamp"] = datetime.now().isoformat()
                f.write(json.dumps(entry) + "\n")

    def format_drifts(self, drifts: list[BeliefDrift]) -> str:
        """Format drifts for CLI output."""
        if not drifts:
            return "No identity-level changes detected."

        lines = ["## Belief Drift Report\n"]
        for d in sorted(drifts, key=lambda x: -x.significance):
            icon = {
                "strengthened": "📈",
                "weakened": "📉",
                "contradicted": "⚡",
                "new": "🆕",
                "evolved": "🔄",
            }.get(d.drift_type, "❓")

            conf_change = f"{d.old_confidence:.0%} → {d.new_confidence:.0%}"
            lines.append(f"{icon} **{d.drift_type.upper()}** [{conf_change}] significance={d.significance:.0%}")
            lines.append(f"   {d.belief_claim}")
            lines.append(f"   Trigger: {d.trigger_event}")
            lines.append(f"   Reason: {d.reasoning}")
            lines.append("")

        return "\n".join(lines)
