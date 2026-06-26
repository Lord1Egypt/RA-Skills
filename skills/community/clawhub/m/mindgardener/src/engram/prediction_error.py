"""
Prediction Error Engine — The novel core of Hippocampus.

Neuroscience background:
The hippocampus consolidates memories during sleep by replaying experiences.
BUT it doesn't replay everything — it preferentially consolidates *surprising*
experiences (high prediction error). This is how humans learn efficiently:
expected events are boring, unexpected events reshape the world model.

Our implementation:
1. PREDICT: Given the agent's world model (MEMORY.md), predict what likely
   happened today. This creates an "expected events" baseline.
2. OBSERVE: Read the actual daily log.
3. COMPARE: Compute prediction error = |actual - predicted| for each event.
4. CONSOLIDATE: Only high-error events get promoted to long-term memory.

This is different from naive "rate importance 1-10" because:
- It's RELATIVE to what the agent already knows
- It captures genuine learning opportunities
- It naturally decays (once something is in MEMORY.md, it's no longer surprising)

Reference: Complementary Learning Systems theory (McClelland et al., 1995)
           SOAR's impasse-driven learning (Laird, 2012)
           Generative Agents reflection (Park et al., 2023)
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from pathlib import Path
from typing import Optional

from .providers import LLMProvider


@dataclass
class PredictionErrorEvent:
    """A single event with its prediction error score."""
    event: str
    prediction_error: float  # 0.0 = totally expected, 1.0 = completely novel
    predicted: Optional[str] = None  # What was predicted instead
    reason: str = ""  # Why this was surprising
    category: str = "unknown"  # entity_change | new_relationship | status_shift | external_event
    entities: list[str] = field(default_factory=list)
    date: str = ""
    timestamp: str = ""

    def should_consolidate(self, threshold: float = 0.5) -> bool:
        """Events above threshold should be promoted to long-term memory."""
        return self.prediction_error >= threshold

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "PredictionErrorEvent":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class PredictionResult:
    """Full result of a prediction error cycle."""
    date: str
    predictions: list[str]  # What was expected
    actual_events: list[str]  # What actually happened
    errors: list[PredictionErrorEvent]  # Events with their PE scores
    model_updates: list[str] = field(default_factory=list)  # Suggested MEMORY.md updates

    @property
    def high_surprise(self) -> list[PredictionErrorEvent]:
        """Events with PE > 0.7 — genuinely novel."""
        return [e for e in self.errors if e.prediction_error > 0.7]

    @property
    def medium_surprise(self) -> list[PredictionErrorEvent]:
        """Events with PE 0.4-0.7 — noteworthy."""
        return [e for e in self.errors if 0.4 <= e.prediction_error <= 0.7]

    @property
    def mean_surprise(self) -> float:
        """Average prediction error across all events."""
        if not self.errors:
            return 0.0
        return sum(e.prediction_error for e in self.errors) / len(self.errors)


# The two-stage prompt architecture is key.
# Stage 1 runs BEFORE seeing the log — forcing genuine prediction.
# Stage 2 compares — computing actual prediction error.

PREDICT_PROMPT = """You are a prediction engine for an AI agent's daily activities.

Based on the agent's long-term memory (world model) below, predict what likely 
happened on {date}. Consider:
- Active projects and their likely next steps
- Pending tasks or follow-ups
- Regular patterns (daily routines, recurring checks)
- Relationships and expected interactions

Output ONLY valid JSON:
{{
  "predictions": [
    {{"event": "description of predicted event", "confidence": 0.0-1.0, "reasoning": "why you expect this"}}
  ]
}}

Make 5-15 predictions. Be specific, not vague.

AGENT'S WORLD MODEL (MEMORY.md):
{memory}

RECENT ENTITY CONTEXT:
{entities}
"""

COMPARE_PROMPT = """You are computing prediction errors for a memory consolidation system.

You were given predictions about what would happen on {date}.
Now compare against what ACTUALLY happened.

For each ACTUAL event, score it:
- prediction_error: 0.0 = exactly as predicted, 1.0 = completely unexpected
- predicted: what was expected instead (if anything)
- reason: why this deviates from the world model
- category: one of [entity_change, new_relationship, status_shift, external_event, routine, skill_gain]
- entities: list of entity names involved

Also identify what the world model should UPDATE to reduce future prediction errors.

Output ONLY valid JSON:
{{
  "errors": [
    {{
      "event": "what actually happened",
      "prediction_error": 0.0-1.0,
      "predicted": "what was expected instead (or null if unpredicted)",
      "reason": "why this was/wasn't surprising",
      "category": "category",
      "entities": ["Entity1", "Entity2"]
    }}
  ],
  "model_updates": [
    "Suggested update to MEMORY.md to reduce future prediction errors"
  ]
}}

Skip trivial routine events (heartbeats, status checks) — only score meaningful events.

PREDICTIONS MADE:
{predictions}

WHAT ACTUALLY HAPPENED ({date}):
{actual}
"""


class PredictionErrorEngine:
    """Two-stage prediction error computation for memory consolidation."""

    def __init__(self, llm: LLMProvider, memory_dir: Path, memory_file: Path):
        self.llm = llm
        self.memory_dir = memory_dir
        self.memory_file = memory_file
        self.entities_dir = memory_dir / "entities"
        self.scores_file = memory_dir / "prediction-errors.jsonl"

    def _read_memory(self, max_chars: int = 4000) -> str:
        """Read the agent's world model."""
        if self.memory_file.exists():
            return self.memory_file.read_text()[:max_chars]
        return "(empty world model)"

    def _read_entities(self, max_chars: int = 2000) -> str:
        """Read recent entity context."""
        if not self.entities_dir.exists():
            return "(no entities)"
        
        entity_text = ""
        for f in sorted(self.entities_dir.glob("*.md")):
            content = f.read_text()
            if len(entity_text) + len(content) > max_chars:
                break
            entity_text += f"### {f.stem}\n{content[:500]}\n\n"
        return entity_text or "(no entities)"

    def _read_daily_log(self, date_str: str, max_chars: int = 6000) -> str:
        """Read the daily log for a given date, with pre-filtering for large files."""
        path = self.memory_dir / f"{date_str}.md"
        if not path.exists():
            return ""
        
        content = path.read_text()
        
        # For large files, pre-filter to remove noise
        if len(content) > max_chars:
            try:
                from .chunker import pre_filter
                content = pre_filter(content)
            except ImportError:
                pass
        
        # Still too long? Truncate with note
        if len(content) > max_chars:
            content = content[:max_chars] + "\n\n[... truncated, full log was {len(content)} chars]"
        
        return content

    async def compute(self, date_str: str | None = None) -> PredictionResult:
        """
        Run the full two-stage prediction error cycle.
        
        Stage 1: Generate predictions from world model (BEFORE seeing log)
        Stage 2: Compare predictions against actual log
        
        For large daily logs, pre-filters noise before sending to LLM.
        """
        if date_str is None:
            date_str = date.today().isoformat()

        daily_log = self._read_daily_log(date_str)
        if not daily_log:
            return PredictionResult(date=date_str, predictions=[], actual_events=[], errors=[])

        memory = self._read_memory()
        entities = self._read_entities()

        # === STAGE 1: PREDICT (without seeing the log) ===
        predict_prompt = PREDICT_PROMPT.format(
            date=date_str,
            memory=memory,
            entities=entities
        )
        predictions_raw = await self.llm.generate_json(predict_prompt)
        predictions = predictions_raw.get("predictions", [])
        prediction_texts = [p.get("event", "") for p in predictions]

        # === STAGE 2: COMPARE (now we look at reality) ===
        compare_prompt = COMPARE_PROMPT.format(
            date=date_str,
            predictions=json.dumps(predictions, indent=2),
            actual=daily_log
        )
        comparison = await self.llm.generate_json(compare_prompt)

        # Build result
        errors = []
        for e in comparison.get("errors", []):
            pe = PredictionErrorEvent(
                event=e.get("event", ""),
                prediction_error=e.get("prediction_error", 0.5),
                predicted=e.get("predicted"),
                reason=e.get("reason", ""),
                category=e.get("category", "unknown"),
                entities=e.get("entities", []),
                date=date_str,
                timestamp=datetime.now().isoformat()
            )
            errors.append(pe)

        result = PredictionResult(
            date=date_str,
            predictions=prediction_texts,
            actual_events=[e.event for e in errors],
            errors=errors,
            model_updates=comparison.get("model_updates", [])
        )

        # Persist scores
        self._save_scores(errors)

        return result

    def compute_sync(self, date_str: str | None = None) -> PredictionResult:
        """Synchronous wrapper for compute()."""
        import asyncio
        return asyncio.run(self.compute(date_str))

    def _save_scores(self, errors: list[PredictionErrorEvent]):
        """Append prediction error scores to JSONL file."""
        with open(self.scores_file, "a") as f:
            for e in errors:
                f.write(json.dumps(e.to_dict()) + "\n")

    def load_history(self, days: int = 30) -> list[PredictionErrorEvent]:
        """Load historical prediction error scores."""
        if not self.scores_file.exists():
            return []
        
        events = []
        for line in self.scores_file.read_text().strip().split('\n'):
            if line:
                try:
                    events.append(PredictionErrorEvent.from_dict(json.loads(line)))
                except:
                    pass
        return events

    def learning_rate(self, days: int = 7) -> float:
        """
        Compute the agent's "learning rate" — average prediction error over time.
        
        A declining learning rate means the world model is getting better.
        A rising learning rate means the environment is changing faster than
        the agent can adapt.
        """
        history = self.load_history(days)
        if not history:
            return 0.0
        return sum(e.prediction_error for e in history) / len(history)
