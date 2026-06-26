#!/usr/bin/env python3
# Nex SkillMon - Cost Tracker Module
# MIT-0 License - Copyright 2026 Nex AI

import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional
from collections import defaultdict

from .config import COST_PER_TOKEN, CURRENCY, CURRENCY_SYMBOL
from .storage import get_storage

logger = logging.getLogger(__name__)


class CostTracker:
    """Track and analyze API costs."""

    def estimate_cost(self, tokens: int, model: str) -> Decimal:
        """Estimate cost for tokens and model."""
        cost_per_token = COST_PER_TOKEN.get(model, Decimal("0"))
        return Decimal(tokens) * cost_per_token

    def aggregate_costs(
        self,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        skill_id: Optional[int] = None,
    ) -> Dict[str, any]:
        """Aggregate costs by skill and model."""
        storage = get_storage()
        skills = storage.list_skills()

        result = {
            "period": {
                "start": (since.isoformat() if since else None),
                "end": (until.isoformat() if until else None),
            },
            "by_skill": {},
            "by_model": defaultdict(lambda: {"count": 0, "tokens": 0, "cost": 0}),
            "total": {"triggers": 0, "tokens": 0, "cost": 0},
        }

        for skill in skills:
            if skill_id and skill["id"] != skill_id:
                continue

            usage_logs = storage.get_skill_usage(skill["id"], since=since)
            if not until:
                usage_logs = [
                    log for log in usage_logs
                    if not until or datetime.fromisoformat(log["triggered_at"]) <= until
                ]

            skill_stats = {
                "name": skill["name"],
                "triggers": len(usage_logs),
                "tokens": sum(log.get("tokens_used", 0) for log in usage_logs),
                "cost": sum(log.get("estimated_cost", 0) for log in usage_logs),
            }

            result["by_skill"][skill["name"]] = skill_stats
            result["total"]["triggers"] += skill_stats["triggers"]
            result["total"]["tokens"] += skill_stats["tokens"]
            result["total"]["cost"] += skill_stats["cost"]

            for log in usage_logs:
                model = log.get("model_used", "unknown")
                result["by_model"][model]["count"] += 1
                result["by_model"][model]["tokens"] += log.get("tokens_used", 0)
                result["by_model"][model]["cost"] += log.get("estimated_cost", 0)

        return result

    def generate_cost_report(self, period: str = "monthly") -> str:
        """Generate formatted cost report."""
        storage = get_storage()

        if period == "monthly":
            since = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif period == "weekly":
            today = datetime.now()
            since = today - timedelta(days=today.weekday())
        elif period == "daily":
            since = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            since = None

        aggregated = self.aggregate_costs(since=since)

        symbol = CURRENCY_SYMBOL.get(CURRENCY, CURRENCY)
        report = f"\nCost Report - {period.capitalize()}\n"
        report += "=" * 60 + "\n\n"

        # Top skills by cost
        skills_by_cost = sorted(
            aggregated["by_skill"].items(),
            key=lambda x: x[1]["cost"],
            reverse=True,
        )

        report += "TOP SKILLS BY COST\n"
        report += "-" * 60 + "\n"
        for name, stats in skills_by_cost[:10]:
            cost_str = f"{symbol}{stats['cost']:.2f}"
            report += f"{name:30} | {stats['triggers']:6} triggers | {stats['tokens']:10} tokens | {cost_str:>10}\n"

        # Top models
        report += "\n\nTOP MODELS\n"
        report += "-" * 60 + "\n"
        models_by_cost = sorted(
            aggregated["by_model"].items(),
            key=lambda x: x[1]["cost"],
            reverse=True,
        )
        for model, stats in models_by_cost[:10]:
            cost_str = f"{symbol}{stats['cost']:.2f}"
            report += f"{model:30} | {stats['count']:6} calls | {stats['tokens']:10} tokens | {cost_str:>10}\n"

        # Summary
        report += "\n\nSUMMARY\n"
        report += "-" * 60 + "\n"
        total_cost = aggregated["total"]["cost"]
        total_tokens = aggregated["total"]["tokens"]
        total_triggers = aggregated["total"]["triggers"]
        report += f"Total Cost:      {symbol}{total_cost:.2f}\n"
        report += f"Total Triggers:  {total_triggers}\n"
        report += f"Total Tokens:    {total_tokens:,}\n"
        if total_triggers > 0:
            avg_cost_per_trigger = total_cost / total_triggers
            report += f"Avg Cost/Trigger: {symbol}{avg_cost_per_trigger:.4f}\n"

        return report

    def get_budget_alert(self, monthly_budget: Decimal) -> Optional[Dict[str, any]]:
        """Check if current month's spending exceeds budget."""
        now = datetime.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        aggregated = self.aggregate_costs(since=month_start)
        current_cost = Decimal(str(aggregated["total"]["cost"]))

        if current_cost > monthly_budget:
            days_in_month = (
                now.replace(day=28) + timedelta(days=4)
            ).replace(day=1) - timedelta(days=1)
            days_in_month = days_in_month.day
            days_elapsed = now.day
            projected_cost = current_cost * Decimal(days_in_month) / Decimal(days_elapsed)

            return {
                "exceeded": True,
                "current_cost": float(current_cost),
                "budget": float(monthly_budget),
                "overage": float(current_cost - monthly_budget),
                "percent_of_budget": float(current_cost / monthly_budget * 100),
                "projected_monthly": float(projected_cost),
                "days_elapsed": days_elapsed,
                "days_in_month": days_in_month,
            }

        return {
            "exceeded": False,
            "current_cost": float(aggregated["total"]["cost"]),
            "budget": float(monthly_budget),
            "remaining": float(monthly_budget - current_cost),
            "percent_of_budget": float(current_cost / monthly_budget * 100),
        }

    def get_cost_trend(
        self, skill_id: Optional[int] = None, periods: int = 6
    ) -> List[Dict[str, any]]:
        """Get cost trend over time."""
        storage = get_storage()
        trend = []

        for i in range(periods):
            period_end = datetime.now() - timedelta(days=i * 7)
            period_start = period_end - timedelta(days=7)

            aggregated = self.aggregate_costs(since=period_start, until=period_end, skill_id=skill_id)

            trend.append({
                "week_of": period_start.isoformat(),
                "cost": aggregated["total"]["cost"],
                "tokens": aggregated["total"]["tokens"],
                "triggers": aggregated["total"]["triggers"],
            })

        return list(reversed(trend))
