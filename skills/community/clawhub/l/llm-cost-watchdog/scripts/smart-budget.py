#!/usr/bin/env python3
"""
Smart Budgeting for Cost Watchdog
Auto-adjusts budgets based on task priority, learns from spending patterns,
and suggests cheaper alternatives.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass, asdict

# Ensure sibling `_pricing` is importable regardless of CWD.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _pricing
from io_utils import write_json_atomic, read_json

DATA_DIR = Path.home() / ".cost-watchdog"
DATA_DIR.mkdir(exist_ok=True)


def _model_prices(model: str) -> tuple:
    """Return (input_per_1M, output_per_1M). Default Sonnet-tier if unknown."""
    price = _pricing.get_price(model)
    if price is None:
        return (3.0, 15.0)
    return (price.input_per_1m, price.output_per_1m)


@dataclass
class BudgetConfig:
    """Budget configuration with smart features."""
    amount: float
    priority: str  # "low", "medium", "high", "critical"
    auto_adjust: bool = True
    learning_enabled: bool = True
    alerts_at: List[float] = None  # Percentages to alert at
    fallback_model: Optional[str] = None
    
    def __post_init__(self):
        if self.alerts_at is None:
            self.alerts_at = [50, 80, 95]


@dataclass
class SpendingPattern:
    """Learned spending pattern."""
    task_type: str
    avg_cost: float
    avg_tokens: int
    typical_duration_minutes: float
    confidence: float  # 0.0 to 1.0
    last_updated: str
    samples: int = 0


class SmartBudgetManager:
    """Manages smart budgeting with learning and auto-adjustment."""
    
    def __init__(self):
        self.config_file = DATA_DIR / "budget-config.json"
        self.patterns_file = DATA_DIR / "spending-patterns.json"
        self.config = self._load_config()
        self.patterns = self._load_patterns()
    
    def _load_config(self) -> Dict:
        return read_json(self.config_file, default={"budgets": [], "settings": {}})

    def _load_patterns(self) -> Dict:
        return read_json(self.patterns_file, default={"patterns": []})

    def _save_config(self):
        write_json_atomic(self.config_file, self.config)

    def _save_patterns(self):
        write_json_atomic(self.patterns_file, self.patterns)
    
    def set_budget(self, amount: float, priority: str = "medium", 
                   auto_adjust: bool = True) -> BudgetConfig:
        """Set a new budget with priority level."""
        budget = BudgetConfig(
            amount=amount,
            priority=priority,
            auto_adjust=auto_adjust
        )
        
        # Adjust budget based on priority if auto-adjust is enabled
        if auto_adjust:
            budget.amount = self._adjust_budget_for_priority(amount, priority)
        
        self.config["budgets"].append(asdict(budget))
        self._save_config()
        
        return budget
    
    def _adjust_budget_for_priority(self, base_amount: float, priority: str) -> float:
        """Adjust budget amount based on task priority."""
        multipliers = {
            "low": 0.5,      # 50% of base for low priority
            "medium": 1.0,   # 100% of base
            "high": 1.5,     # 150% of base
            "critical": 2.0  # 200% of base
        }
        return base_amount * multipliers.get(priority, 1.0)
    
    def get_recommended_budget(self, task_type: str, 
                                historical_data: List[Dict]) -> float:
        """Get recommended budget based on task type and history."""
        if not historical_data:
            return 5.00  # Default budget
        
        # Calculate average cost for this task type
        task_costs = [t["cost"] for t in historical_data 
                      if t.get("task_type") == task_type]
        
        if not task_costs:
            return 5.00
        
        avg_cost = sum(task_costs) / len(task_costs)
        std_dev = self._calculate_std_dev(task_costs)
        
        # Recommend budget at mean + 1 std dev (covers ~84% of cases)
        recommended = avg_cost + std_dev
        
        # Add buffer for unexpected complexity
        return recommended * 1.2
    
    def _calculate_std_dev(self, values: List[float]) -> float:
        """Calculate standard deviation."""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5
    
    def learn_from_task(self, task_type: str, cost: float, tokens: int,
                        duration_minutes: float):
        """
        Update (or create) a spending pattern for `task_type`.

        Confidence is derived from the relative standard error of the
        running cost mean (SEM / |mean|). With few samples it stays low
        (the old `+= 0.05` ramp is gone); with many consistent samples
        it approaches 0.95.
        """
        # Find or create pattern for this task type.
        pattern = None
        for p in self.patterns["patterns"]:
            if p["task_type"] == task_type:
                pattern = p
                break

        if pattern is None:
            new_pattern = SpendingPattern(
                task_type=task_type,
                avg_cost=cost,
                avg_tokens=tokens,
                typical_duration_minutes=duration_minutes,
                confidence=0.25,
                samples=1,
                last_updated=datetime.now().isoformat(),
            )
            # Persist per-sample cost history so we can compute variance.
            record = asdict(new_pattern)
            record["cost_samples"] = [cost]
            self.patterns["patterns"].append(record)
            self._save_patterns()
            return

        # Append the new observation.
        pattern.setdefault("cost_samples", [])
        pattern["cost_samples"].append(cost)
        # Cap history so the file doesn't grow unbounded.
        if len(pattern["cost_samples"]) > 500:
            pattern["cost_samples"] = pattern["cost_samples"][-500:]

        # Running means; EMA still used for tokens/duration because those
        # drift with the workload and confidence there is less load-bearing.
        n = len(pattern["cost_samples"])
        alpha = 0.2
        pattern["avg_cost"] = sum(pattern["cost_samples"]) / n
        pattern["avg_tokens"] = int(
            (alpha * tokens) + ((1 - alpha) * pattern["avg_tokens"])
        )
        pattern["typical_duration_minutes"] = (
            (alpha * duration_minutes)
            + ((1 - alpha) * pattern["typical_duration_minutes"])
        )
        pattern["samples"] = n
        pattern["confidence"] = self._confidence_from_samples(pattern["cost_samples"])
        pattern["last_updated"] = datetime.now().isoformat()
        self._save_patterns()

    @staticmethod
    def _confidence_from_samples(samples: List[float]) -> float:
        """
        Confidence ∈ [0.1, 0.95] derived from the relative standard error
        of the mean. Low samples or high variance → low confidence.
        """
        n = len(samples)
        if n < 2:
            return 0.25 if n == 1 else 0.1
        mean = sum(samples) / n
        if mean == 0:
            # All zeros — mean is exact by construction.
            return 0.9
        variance = sum((x - mean) ** 2 for x in samples) / (n - 1)
        std_dev = variance ** 0.5
        sem = std_dev / (n ** 0.5)
        rel_err = abs(sem / mean)
        conf = 1.0 - min(rel_err, 1.0)
        return max(0.1, min(0.95, conf))
    
    def estimate_task_cost(self, task_type: str, tokens_estimate: int,
                           model: str = "claude-sonnet-4-6") -> Dict:
        """Estimate cost for a task based on learned patterns."""
        pattern = next(
            (p for p in self.patterns["patterns"] if p["task_type"] == task_type),
            None,
        )

        input_price, output_price = _model_prices(model)

        # Assume 20% output tokens.
        estimated_output = int(tokens_estimate * 0.2)
        estimated_input = tokens_estimate - estimated_output
        estimated_cost = (
            (estimated_input / 1_000_000) * input_price
            + (estimated_output / 1_000_000) * output_price
        )

        if pattern and pattern["samples"] >= 3:
            confidence = pattern["confidence"]
            source = "learned pattern"
        else:
            confidence = 0.5
            source = "simple estimation"

        return {
            "task_type": task_type,
            "estimated_cost": round(estimated_cost, 4),
            "estimated_tokens": tokens_estimate,
            "model": model,
            "confidence": confidence,
            "source": source,
            "pricing_used": (input_price, output_price),
        }
    
    def suggest_cheaper_alternatives(self, current_model: str,
                                     task_type: str,
                                     max_savings_percent: float = 50) -> List[Dict]:
        """
        Suggest cheaper model alternatives. Only considers models with the
        same billing unit (tokens, images, seconds, ...) — a chat model and
        an image-generation model aren't comparable.
        """
        current = _pricing.get_price(current_model)
        if current is None:
            return []

        current_cost_per_1M = current.input_per_1m + current.output_per_1m
        if current_cost_per_1M <= 0:
            return []

        alternatives = []
        current_slug = _pricing.canonical_slug(current_model)
        for slug, info in _pricing.load_pricing().items():
            if slug == current_slug:
                continue
            if info.unit != current.unit:
                continue
            new_cost_per_1M = info.input_per_1m + info.output_per_1m
            savings_percent = (
                (current_cost_per_1M - new_cost_per_1M) / current_cost_per_1M * 100
            )
            if savings_percent >= max_savings_percent:
                alternatives.append({
                    "model": slug,
                    "savings_percent": round(savings_percent, 1),
                    "new_cost_per_1M": round(new_cost_per_1M, 4),
                    "current_cost_per_1M": round(current_cost_per_1M, 4),
                    "unit": info.unit,
                    "trade_offs": self._get_trade_offs(current_model, slug),
                })

        alternatives.sort(key=lambda x: x["savings_percent"], reverse=True)
        return alternatives[:5]
    
    def _get_trade_offs(self, current_model: str, alternative_model: str) -> str:
        """Get trade-offs when switching models."""
        trade_offs = {
            "claude-opus-4-7": "Top-tier reasoning, highest cost",
            "claude-opus-4-6": "Strong reasoning, same price tier as 4-7",
            "claude-sonnet-4-6": "Slightly lower quality, much faster",
            "claude-haiku-4-5": "Much faster, lower quality for complex tasks",
            "gpt-4o": "Different strengths, may need prompt adjustment",
            "gpt-4o-mini": "Good for simple tasks, less capable on complex reasoning",
            "gpt-4.1-nano": "Best for classification, extraction, simple tasks",
            "gemini-2.0-flash": "Good value, different knowledge cutoff",
            "groq-llama-3.2-8b": "Very fast, good for simple tasks",
            "deepseek-v3": "Strong on code, different style",
            "perplexity-sonar-small": "Includes web search, good for research"
        }
        
        return trade_offs.get(alternative_model, "May require prompt adjustment")
    
    def get_budget_status(self, current_spend: float) -> Dict:
        """Get current budget status and recommendations."""
        if not self.config["budgets"]:
            return {"status": "no_budget", "message": "No budget set"}
        
        # Get most recent budget
        budget = self.config["budgets"][-1]
        amount = budget["amount"]
        
        percent_used = (current_spend / amount) * 100 if amount > 0 else 0
        
        status = "ok"
        recommendations = []
        
        if percent_used >= 100:
            status = "over_budget"
            recommendations.append("⚠️ Budget exceeded! Consider stopping or increasing budget.")
        elif percent_used >= 95:
            status = "critical"
            recommendations.append("🚨 95% of budget used! Finish current task only.")
        elif percent_used >= 80:
            status = "warning"
            recommendations.append("⚠️ 80% of budget used. Consider wrapping up.")
        elif percent_used >= 50:
            status = "caution"
            recommendations.append("💡 50% of budget used. Monitor spending.")
        
        return {
            "status": status,
            "budget": amount,
            "spent": current_spend,
            "remaining": amount - current_spend,
            "percent_used": round(percent_used, 1),
            "recommendations": recommendations
        }
    
    def auto_adjust_budget(self, task_priority: str, 
                           current_spend: float) -> Optional[float]:
        """Auto-adjust budget based on task priority and spending patterns."""
        if not self.config["budgets"]:
            return None
        
        budget = self.config["budgets"][-1]
        if not budget.get("auto_adjust", True):
            return None
        
        # Adjust based on priority
        multipliers = {
            "low": 0.5,
            "medium": 1.0,
            "high": 1.5,
            "critical": 2.0
        }
        
        new_budget = budget["amount"] * multipliers.get(task_priority, 1.0)
        
        # Don't reduce budget if already spent > 50%
        if current_spend > (budget["amount"] * 0.5) and new_budget < budget["amount"]:
            return budget["amount"]
        
        return new_budget


def main():
    """CLI interface for smart budgeting."""
    manager = SmartBudgetManager()
    
    import sys
    if len(sys.argv) < 2:
        print("Usage: smart-budget.py [command] [args]")
        print("Commands:")
        print("  set <amount> [--priority=low|medium|high|critical]")
        print("  status")
        print("  estimate <task_type> <tokens> [model]")
        print("  alternatives <model> [--savings=50]")
        print("  learn <task_type> <cost> <tokens> <duration_minutes>")
        print("  recommend <task_type>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "set":
        amount = float(sys.argv[2])
        priority = "medium"
        for arg in sys.argv[3:]:
            if arg.startswith("--priority="):
                priority = arg.split("=")[1]
        
        budget = manager.set_budget(amount, priority)
        print(f"✅ Budget set: ${budget.amount:.2f}")
        print(f"   Priority: {budget.priority}")
        print(f"   Auto-adjust: {budget.auto_adjust}")
    
    elif command == "status":
        # For demo, assume $0 spend
        status = manager.get_budget_status(0)
        print(json.dumps(status, indent=2))
    
    elif command == "estimate":
        task_type = sys.argv[2]
        tokens = int(sys.argv[3])
        model = sys.argv[4] if len(sys.argv) > 4 else "claude-sonnet-4-6"
        
        estimate = manager.estimate_task_cost(task_type, tokens, model)
        print(f"💰 Estimate for {task_type}:")
        print(f"   Cost: ${estimate['estimated_cost']:.4f}")
        print(f"   Tokens: {estimate['estimated_tokens']:,}")
        print(f"   Confidence: {estimate['confidence']:.0%}")
        print(f"   Source: {estimate['source']}")
    
    elif command == "alternatives":
        model = sys.argv[2]
        savings = 50
        for arg in sys.argv[3:]:
            if arg.startswith("--savings="):
                savings = int(arg.split("=")[1])
        
        alternatives = manager.suggest_cheaper_alternatives(model, "general", savings)
        if alternatives:
            print(f"💡 Cheaper alternatives to {model} (>{savings}% savings):")
            for alt in alternatives:
                print(f"   • {alt['model']}: Save {alt['savings_percent']}%")
                print(f"     Trade-off: {alt['trade_offs']}")
        else:
            print(f"No alternatives with >{savings}% savings found.")
    
    elif command == "learn":
        task_type = sys.argv[2]
        cost = float(sys.argv[3])
        tokens = int(sys.argv[4])
        duration = float(sys.argv[5])
        
        manager.learn_from_task(task_type, cost, tokens, duration)
        print(f"✅ Learned from {task_type} task")
        print(f"   Cost: ${cost:.4f}, Tokens: {tokens:,}, Duration: {duration}min")
    
    elif command == "recommend":
        task_type = sys.argv[2]
        # For demo, suggest based on common patterns
        print(f"💡 Recommendations for {task_type}:")
        print("   Use Claude Haiku for simple tasks")
        print("   Use Claude Sonnet for complex reasoning")
        print("   Use GPT-4o-mini for code generation")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
