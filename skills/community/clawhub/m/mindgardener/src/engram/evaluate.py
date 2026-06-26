"""
Context Evaluator — Closes the memory loop.

After an agent produces output, the evaluator:
1. Fact-checks claims against source entities
2. Detects new entities/facts worth extracting
3. Scores confidence of the agent's output
4. Writes verified new information back to entities

This implements the Context Evaluator from Xu et al. (2025)
"Everything is Context" — the missing third stage of the
context engineering pipeline (Constructor → Updater → Evaluator).

Without this, memory is write-once. With it, every agent response
becomes a potential source of new knowledge.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from .config import EngramConfig
from .filelock import safe_write, safe_append, file_lock
from .recall import fuzzy_score


@dataclass
class FactCheck:
    """A single fact-check result."""
    claim: str
    verdict: str  # "confirmed", "contradicted", "unverified", "new"
    confidence: float  # 0.0–1.0
    source: str = ""  # entity or source that confirms/contradicts
    evidence: str = ""  # the specific text that supports the verdict
    
    @property
    def is_reliable(self) -> bool:
        return self.verdict == "confirmed" and self.confidence >= 0.7


@dataclass
class NewFact:
    """A new fact discovered in agent output, worth writing back."""
    entity_name: str
    fact: str
    confidence: float
    source_context: str = ""  # where in the output this came from


@dataclass
class EvaluationResult:
    """Full evaluation of an agent's output."""
    fact_checks: list[FactCheck] = field(default_factory=list)
    new_facts: list[NewFact] = field(default_factory=list)
    new_entities: list[dict] = field(default_factory=list)
    overall_confidence: float = 0.0
    output_text: str = ""
    evaluated_at: str = ""
    
    @property
    def confirmed(self) -> list[FactCheck]:
        return [f for f in self.fact_checks if f.verdict == "confirmed"]
    
    @property
    def contradicted(self) -> list[FactCheck]:
        return [f for f in self.fact_checks if f.verdict == "contradicted"]
    
    @property
    def new(self) -> list[FactCheck]:
        return [f for f in self.fact_checks if f.verdict == "new"]
    
    def summary(self) -> str:
        lines = [
            f"## Evaluation Summary",
            f"Overall confidence: {self.overall_confidence:.2f}",
            f"Evaluated: {self.evaluated_at}",
            f"",
        ]
        
        if self.confirmed:
            lines.append(f"### ✅ Confirmed ({len(self.confirmed)})")
            for fc in self.confirmed:
                lines.append(f"- [{fc.confidence:.2f}] {fc.claim}")
                if fc.source:
                    lines.append(f"  Source: {fc.source}")
        
        if self.contradicted:
            lines.append(f"")
            lines.append(f"### ❌ Contradicted ({len(self.contradicted)})")
            for fc in self.contradicted:
                lines.append(f"- [{fc.confidence:.2f}] {fc.claim}")
                lines.append(f"  Evidence: {fc.evidence}")
        
        if self.new_facts:
            lines.append(f"")
            lines.append(f"### 🆕 New facts to write back ({len(self.new_facts)})")
            for nf in self.new_facts:
                lines.append(f"- {nf.entity_name}: {nf.fact} (conf: {nf.confidence:.2f})")
        
        if self.new_entities:
            lines.append(f"")
            lines.append(f"### 🌱 New entities detected ({len(self.new_entities)})")
            for ne in self.new_entities:
                lines.append(f"- {ne.get('name', '?')} ({ne.get('type', '?')})")
        
        return "\n".join(lines)
    
    def to_json(self) -> dict:
        return {
            "overall_confidence": self.overall_confidence,
            "evaluated_at": self.evaluated_at,
            "fact_checks": [
                {"claim": f.claim, "verdict": f.verdict, "confidence": f.confidence,
                 "source": f.source, "evidence": f.evidence}
                for f in self.fact_checks
            ],
            "new_facts": [
                {"entity": f.entity_name, "fact": f.fact, "confidence": f.confidence}
                for f in self.new_facts
            ],
            "new_entities": self.new_entities,
        }


def _extract_claims(text: str) -> list[str]:
    """Extract factual claims from agent output text.
    
    Looks for statements that assert facts about entities.
    Simple heuristic: sentences containing proper nouns or entity-like patterns.
    """
    claims = []
    # Split into sentences
    sentences = re.split(r'[.!?\n]', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 10:
            continue
        # Skip questions, commands, meta-commentary
        if sentence.startswith(("?", "!", "Let me", "I'll", "I will", "Sure", 
                                "Okay", "Here", "Note:", "---")):
            continue
        # Must contain something that looks like a factual claim
        # (has a proper noun, number, or entity-like pattern)
        if (re.search(r'[A-Z][a-z]+', sentence) or 
            re.search(r'\d+', sentence) or
            '[[' in sentence):
            claims.append(sentence.strip())
    
    return claims[:20]  # Cap at 20 claims


def _match_entity(claim: str, entities_dir: Path) -> Optional[tuple[str, str]]:
    """Find the best matching entity for a claim.
    
    Returns (entity_name, entity_content) or None.
    """
    best_score = 0.0
    best_match = None
    
    for entity_file in entities_dir.glob("*.md"):
        name = entity_file.stem.replace("-", " ")
        # Check if entity name appears in claim
        if name.lower() in claim.lower():
            content = entity_file.read_text()
            return (name, content)
        
        score = fuzzy_score(claim, name)
        if score > best_score and score > 0.3:
            best_score = score
            best_match = (name, entity_file.read_text())
    
    return best_match


def evaluate_output(
    output_text: str,
    config: EngramConfig,
    source_context: str = "",
) -> EvaluationResult:
    """Evaluate an agent's output against the knowledge graph.
    
    No LLM calls — pure file-based fact checking.
    
    Strategy:
    1. Extract factual claims from output
    2. For each claim, find matching entities
    3. Check if claim is confirmed, contradicted, or new
    4. Identify new facts worth writing back
    5. Detect mentions of unknown entities
    
    Args:
        output_text: The agent's response to evaluate
        config: Engram configuration
        source_context: Optional context that was fed to the agent
    
    Returns:
        EvaluationResult with fact checks and write-back candidates
    """
    result = EvaluationResult(
        output_text=output_text,
        evaluated_at=datetime.now().isoformat(),
    )
    
    claims = _extract_claims(output_text)
    if not claims:
        result.overall_confidence = 0.5  # No checkable claims
        return result
    
    # Load all entity names for new-entity detection
    known_entities = set()
    entity_contents: dict[str, str] = {}
    for entity_file in config.entities_dir.glob("*.md"):
        name = entity_file.stem.replace("-", " ")
        known_entities.add(name.lower())
        entity_contents[name.lower()] = entity_file.read_text()
    
    # Check each claim
    for claim in claims:
        match = _match_entity(claim, config.entities_dir)
        
        if match:
            entity_name, entity_content = match
            fc = _check_claim_against_entity(claim, entity_name, entity_content)
            result.fact_checks.append(fc)
            
            # If claim contains new info about existing entity, mark for write-back
            if fc.verdict == "new" and fc.confidence >= 0.5:
                result.new_facts.append(NewFact(
                    entity_name=entity_name,
                    fact=claim,
                    confidence=fc.confidence,
                    source_context=source_context[:200] if source_context else "",
                ))
        else:
            # Check for proper nouns that might be new entities
            proper_nouns = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', claim)
            for noun in proper_nouns:
                if (noun.lower() not in known_entities and 
                    len(noun) > 2 and
                    noun.lower() not in {"the", "this", "that", "these", "when", 
                                          "where", "what", "which", "here", "there",
                                          "monday", "tuesday", "wednesday", "thursday",
                                          "friday", "saturday", "sunday",
                                          "january", "february", "march", "april",
                                          "may", "june", "july", "august", "september",
                                          "october", "november", "december"}):
                    # Possible new entity
                    if not any(ne.get("name") == noun for ne in result.new_entities):
                        result.new_entities.append({
                            "name": noun,
                            "type": "unknown",
                            "source_claim": claim,
                        })
    
    # Calculate overall confidence
    if result.fact_checks:
        confirmed_count = len(result.confirmed)
        contradicted_count = len(result.contradicted)
        total = len(result.fact_checks)
        
        # Weighted: contradictions hurt more than confirmations help
        result.overall_confidence = max(0.0, min(1.0,
            (confirmed_count * 1.0 - contradicted_count * 2.0 + 
             (total - confirmed_count - contradicted_count) * 0.5) / total
        ))
    else:
        result.overall_confidence = 0.5
    
    return result


def _check_claim_against_entity(claim: str, entity_name: str, 
                                 entity_content: str) -> FactCheck:
    """Check a single claim against an entity's content.
    
    Uses text matching — no LLM needed.
    """
    claim_lower = claim.lower()
    content_lower = entity_content.lower()
    
    # Extract facts from entity
    facts_section = re.search(r'## Facts\n(.*?)(?=\n## |\Z)', entity_content, re.DOTALL)
    facts = []
    if facts_section:
        facts = [line.strip().lstrip("- ") for line in facts_section.group(1).split("\n") 
                 if line.strip().startswith("- ")]
    
    # Extract type
    type_match = re.search(r'\*\*Type:\*\*\s*(\w+)', entity_content)
    entity_type = type_match.group(1) if type_match else ""
    
    # Check for direct confirmation (claim text found in entity)
    claim_words = {w for w in claim_lower.split() if len(w) >= 4}
    
    # Strong confirmation: multiple claim words found in facts
    fact_matches = 0
    best_fact = ""
    for fact in facts:
        fact_lower = fact.lower()
        matching_words = sum(1 for w in claim_words if w in fact_lower)
        if matching_words > fact_matches:
            fact_matches = matching_words
            best_fact = fact
    
    if fact_matches >= 3:
        return FactCheck(
            claim=claim,
            verdict="confirmed",
            confidence=min(1.0, 0.5 + fact_matches * 0.1),
            source=entity_name,
            evidence=best_fact,
        )
    
    # Check timeline for event confirmation
    timeline_matches = 0
    for line in entity_content.split("\n"):
        if line.strip().startswith("- "):
            line_lower = line.lower()
            matching = sum(1 for w in claim_words if w in line_lower)
            if matching >= 2:
                timeline_matches += 1
                best_fact = line.strip().lstrip("- ")
    
    if timeline_matches > 0:
        return FactCheck(
            claim=claim,
            verdict="confirmed",
            confidence=0.6,
            source=entity_name,
            evidence=best_fact,
        )
    
    # Check for contradiction (claim says X, entity says not-X)
    # Simple pattern: "is not" vs "is", type mismatches
    if entity_type:
        type_claim = re.search(r'is (?:a |an )?(\w+)', claim_lower)
        if type_claim and type_claim.group(1) != entity_type.lower():
            # Possible type contradiction — but only flag if explicit
            if type_claim.group(1) in {"person", "company", "project", "tool", "concept"}:
                return FactCheck(
                    claim=claim,
                    verdict="contradicted",
                    confidence=0.7,
                    source=entity_name,
                    evidence=f"Entity type is {entity_type}, claim says {type_claim.group(1)}",
                )
    
    # No match found — claim mentions entity but contains new info
    if entity_name.lower() in claim_lower:
        return FactCheck(
            claim=claim,
            verdict="new",
            confidence=0.5,
            source=entity_name,
        )
    
    # Weak match
    return FactCheck(
        claim=claim,
        verdict="unverified",
        confidence=0.3,
    )


def write_back(
    result: EvaluationResult,
    config: EngramConfig,
    min_confidence: float = 0.6,
    dry_run: bool = False,
) -> list[str]:
    """Write verified new facts back to entity files.
    
    Only writes facts above the confidence threshold.
    Returns list of actions taken.
    """
    actions = []
    
    for nf in result.new_facts:
        if nf.confidence < min_confidence:
            continue
        
        from .core import sanitize_filename
        filepath = config.entities_dir / f"{sanitize_filename(nf.entity_name)}.md"
        
        if not filepath.exists():
            actions.append(f"SKIP: {nf.entity_name} — entity file not found")
            continue
        
        content = filepath.read_text()
        
        # Don't duplicate
        if nf.fact.lower() in content.lower():
            actions.append(f"SKIP: {nf.entity_name} — fact already exists")
            continue
        
        if dry_run:
            actions.append(f"WOULD ADD to {nf.entity_name}: {nf.fact}")
            continue
        
        # Add to facts section
        if "## Facts" in content:
            content = content.replace(
                "## Facts\n",
                f"## Facts\n- {nf.fact} (auto-evaluated, conf: {nf.confidence:.2f})\n",
                1
            )
        else:
            if "## Timeline" in content:
                content = content.replace(
                    "## Timeline",
                    f"## Facts\n- {nf.fact} (auto-evaluated, conf: {nf.confidence:.2f})\n\n## Timeline"
                )
        
        safe_write(filepath, content)
        actions.append(f"ADDED to {nf.entity_name}: {nf.fact}")
    
    # Log evaluation
    log_file = config.memory_dir / "evaluations.jsonl"
    log_entry = json.dumps({
        "evaluated_at": result.evaluated_at,
        "overall_confidence": result.overall_confidence,
        "confirmed": len(result.confirmed),
        "contradicted": len(result.contradicted),
        "new_facts_written": len([a for a in actions if a.startswith("ADDED")]),
    })
    safe_append(log_file, log_entry + "\n")
    
    return actions
