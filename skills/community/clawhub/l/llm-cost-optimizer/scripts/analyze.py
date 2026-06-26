"""
LLM Cost Optimizer - Core analysis engine
AgentBounty: EfficientAI $2,500
"""
import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from collections import defaultdict

# Provider pricing per 1M tokens (input/output) — May 2026 rates
PRICING = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4.1": {"input": 2.00, "output": 8.00},
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
    "gpt-4.1-nano": {"input": 0.10, "output": 0.40},
    "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
    "claude-haiku-3-5-20241022": {"input": 0.80, "output": 4.00},
    "gemini-2.5-pro": {"input": 1.25, "output": 10.00},
    "gemini-2.5-flash": {"input": 0.15, "output": 0.60},
    "deepseek-v3": {"input": 0.27, "output": 1.10},
    "deepseek-r1": {"input": 0.55, "output": 2.19},
    "llama-4-maverick": {"input": 0.20, "output": 0.80},
}

# Model capability tiers for downgrade suggestions
MODEL_TIERS = {
    "premium": ["gpt-4o", "claude-sonnet-4-20250514", "gemini-2.5-pro"],
    "mid": ["gpt-4.1-mini", "claude-haiku-3-5-20241022", "gemini-2.5-flash", "deepseek-v3"],
    "budget": ["gpt-4.1-nano", "deepseek-r1", "llama-4-maverick"],
}

DOWNGRADE_MAP = {
    "premium": "mid",
    "mid": "budget",
}


@dataclass
class UsageEntry:
    timestamp: datetime
    model: str
    input_tokens: int
    output_tokens: int
    task_type: str = "general"
    session_id: Optional[str] = None
    cached: bool = False

    @property
    def cost(self) -> float:
        pricing = PRICING.get(self.model, {"input": 1.0, "output": 4.0})
        return (self.input_tokens * pricing["input"] + self.output_tokens * pricing["output"]) / 1_000_000


@dataclass
class Optimization:
    type: str  # "downgrade", "cache", "compress", "batch"
    description: str
    estimated_savings_pct: float
    estimated_savings_usd: float
    confidence: float
    action: str


class CostAnalyzer:
    def __init__(self):
        self.entries: list[UsageEntry] = []
        self.optimizations: list[Optimization] = []

    def add_entry(self, entry: UsageEntry):
        self.entries.append(entry)

    def load_from_json(self, path: Path):
        """Load usage from OpenAI/Anthropic-style JSON logs."""
        with open(path) as f:
            data = json.load(f)
        for item in data:
            self.add_entry(UsageEntry(
                timestamp=datetime.fromisoformat(item.get("timestamp", datetime.now().isoformat())),
                model=item.get("model", "unknown"),
                input_tokens=item.get("input_tokens", 0),
                output_tokens=item.get("output_tokens", 0),
                task_type=item.get("task_type", "general"),
                session_id=item.get("session_id"),
                cached=item.get("cached", False),
            ))

    def total_cost(self) -> float:
        return sum(e.cost for e in self.entries)

    def cost_by_model(self) -> dict[str, float]:
        result = defaultdict(float)
        for e in self.entries:
            result[e.model] += e.cost
        return dict(result)

    def cost_by_day(self) -> dict[str, float]:
        result = defaultdict(float)
        for e in self.entries:
            key = e.timestamp.strftime("%Y-%m-%d")
            result[key] += e.cost
        return dict(result)

    def cost_by_task(self) -> dict[str, float]:
        result = defaultdict(float)
        for e in self.entries:
            result[e.task_type] += e.cost
        return dict(result)

    def suggest_downgrades(self) -> list[Optimization]:
        """Find tasks using premium models that could use cheaper ones."""
        opts = []
        for tier_name, models in MODEL_TIERS.items():
            if tier_name not in DOWNGRADE_MAP:
                continue
            lower_tier = DOWNGRADE_MAP[tier_name]
            lower_models = MODEL_TIERS[lower_tier]

            for model in models:
                tier_entries = [e for e in self.entries if e.model == model]
                # Simple tasks: low output, general type
                simple_entries = [e for e in tier_entries
                                  if e.output_tokens < 500 and e.task_type in ("general", "classification", "extraction")]
                if not simple_entries:
                    continue

                simple_cost = sum(e.cost for e in simple_entries)
                # Estimate lower tier cost (use cheapest in that tier)
                cheapest_lower = lower_models[0]
                avg_input = sum(e.input_tokens for e in simple_entries) / len(simple_entries)
                avg_output = sum(e.output_tokens for e in simple_entries) / len(simple_entries)
                lower_pricing = PRICING.get(cheapest_lower, {"input": 0.5, "output": 2.0})
                lower_cost_per_call = (avg_input * lower_pricing["input"] + avg_output * lower_pricing["output"]) / 1_000_000
                lower_total = lower_cost_per_call * len(simple_entries)
                savings = simple_cost - lower_total

                if savings > 0.01:
                    opts.append(Optimization(
                        type="downgrade",
                        description=f"Downgrade {len(simple_entries)} simple calls from {model} → {cheapest_lower}",
                        estimated_savings_pct=(savings / simple_cost * 100) if simple_cost > 0 else 0,
                        estimated_savings_usd=round(savings, 2),
                        confidence=0.85 if tier_name == "premium" else 0.7,
                        action=f"Switch model for task_type in ['general', 'classification', 'extraction'] when output < 500 tokens",
                    ))
        return opts

    def suggest_caching(self) -> list[Optimization]:
        """Find repeated prompts that could be cached."""
        opts = []
        prompt_hashes = defaultdict(list)
        for e in self.entries:
            # Group by model + similar input size (proxy for repeated prompts)
            key = (e.model, e.input_tokens, e.task_type)
            prompt_hashes[key].append(e)

        for key, entries in prompt_hashes.items():
            if len(entries) > 3:
                total_cost = sum(e.cost for e in entries)
                # Prompt caching typically saves 50% on input tokens
                avg_input = entries[0].input_tokens
                cached_savings = (avg_input * PRICING.get(key[0], {"input": 1.0})["input"] * 0.5 / 1_000_000) * len(entries)
                if cached_savings > 0.01:
                    opts.append(Optimization(
                        type="cache",
                        description=f"Cache {key[0]} calls with {avg_input} input tokens ({key[2]}) — {len(entries)} repeats detected",
                        estimated_savings_pct=30.0,
                        estimated_savings_usd=round(cached_savings, 2),
                        confidence=0.8,
                        action="Enable prompt caching for this pattern (OpenAI: automatic, Anthropic: use cache_control)",
                    ))
        return opts

    def suggest_compression(self) -> list[Optimization]:
        """Find verbose outputs that could be compressed via prompt tuning."""
        opts = []
        verbose = [e for e in self.entries if e.output_tokens > 2000 and e.task_type in ("general", "summary")]
        if verbose:
            verbose_cost = sum(e.cost for e in verbose)
            # Adding "be concise" typically reduces output by 40-60%
            savings = verbose_cost * 0.4
            opts.append(Optimization(
                type="compress",
                description=f"{len(verbose)} calls with >2K output tokens for general/summary tasks",
                estimated_savings_pct=25.0,
                estimated_savings_usd=round(savings, 2),
                confidence=0.7,
                action="Add 'Be concise. Do not elaborate.' to system prompts for summary/general tasks",
            ))
        return opts

    def run_analysis(self) -> dict:
        """Full analysis pipeline."""
        self.optimizations = (
            self.suggest_downgrades()
            + self.suggest_caching()
            + self.suggest_compression()
        )
        total = self.total_cost()
        total_savings = sum(o.estimated_savings_usd for o in self.optimizations)

        return {
            "total_cost_usd": round(total, 2),
            "total_entries": len(self.entries),
            "cost_by_model": {k: round(v, 2) for k, v in self.cost_by_model().items()},
            "cost_by_task": {k: round(v, 2) for k, v in self.cost_by_task().items()},
            "optimizations": [
                {
                    "type": o.type,
                    "description": o.description,
                    "savings_pct": round(o.estimated_savings_pct, 1),
                    "savings_usd": o.estimated_savings_usd,
                    "confidence": o.confidence,
                    "action": o.action,
                }
                for o in sorted(self.optimizations, key=lambda x: x.estimated_savings_usd, reverse=True)
            ],
            "total_potential_savings_usd": round(total_savings, 2),
            "total_potential_savings_pct": round((total_savings / total * 100) if total > 0 else 0, 1),
        }
