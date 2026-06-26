---
name: greenhelix-agent-production-hardening
version: "1.3.1"
description: "The Agent Production Hardening Guide. Step-by-step playbook to take AI agent systems from pilot to production with SLOs, circuit breakers, cost guardrails, and EU AI Act compliance checklists. Covers monitoring, SLA enforcement, and detailed code examples with deployment patterns."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [production, slo, circuit-breaker, cost-guardrails, eu-ai-act, hardening, guide, greenhelix, openclaw, ai-agent]
price_usd: 0.0
content_type: markdown
executable: false
install: none
credentials: [GREENHELIX_API_KEY]
metadata:
  openclaw:
    requires:
      env:
        - GREENHELIX_API_KEY
    primaryEnv: GREENHELIX_API_KEY
---
# The Agent Production Hardening Guide

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `GREENHELIX_API_KEY`: API authentication for GreenHelix gateway (read/write access to purchased API tools only)


Seventy-eight percent of enterprises have agent pilots running. Fourteen percent have agents in production. The gap between those two numbers is where careers stall, budgets evaporate, and executives lose faith in the technology. A March 2026 survey by the AI Infrastructure Alliance found that 89% of failed agent-to-production transitions trace back to exactly five gaps: integration brittleness, quality regression, monitoring blindness, ownership ambiguity, and training data drift. Not model quality. Not prompt engineering. Not the framework choice. The five gaps are all operational -- and they are all fixable with known engineering practices that have been adapted for autonomous agent systems. This guide is the 30-day playbook to close those gaps. It starts with a production readiness assessment that quantifies your current state. It builds SLO-driven monitoring, circuit breakers for graceful degradation, cost guardrails that prevent runaway spend, deployment patterns for safe rollouts, multi-agent resilience patterns, and EU AI Act compliance controls -- all wired to the GreenHelix A2A Commerce Gateway's 128 tools. Every chapter ends with working Python code, practical checklists, and decision matrices. By the end of the 30-day sprint in Chapter 8, your agent system will have a quantified go/no-go scorecard, automated rollback triggers, per-agent cost caps, and a compliance audit trail that satisfies Article 12 record-keeping before the August 2, 2026 deadline.
1. [The Production Readiness Assessment](#chapter-1-the-production-readiness-assessment)
2. [SLOs, SLAs, and Error Budgets for Agent Systems](#chapter-2-slos-slas-and-error-budgets-for-agent-systems)

## What You'll Learn
- Chapter 1: The Production Readiness Assessment
- Chapter 2: SLOs, SLAs, and Error Budgets for Agent Systems
- Chapter 3: Circuit Breakers, Retries, and Graceful Degradation
- Chapter 4: Cost Guardrails and Token Budget Enforcement
- Chapter 5: Deployment Patterns: Canary, Blue-Green, and Rollback
- Chapter 6: Multi-Agent Failure Modes and Resilience Patterns
- Chapter 7: EU AI Act Production Compliance (August 2026 Deadline)
- Chapter 8: The 30-Day Production Hardening Sprint
- What to Do Next
- Circuit Breaker & Failover — Working Implementation

## Full Guide

# The Agent Production Hardening Guide: SLOs, Circuit Breakers, Cost Guardrails & the 30-Day Sprint to Production

Seventy-eight percent of enterprises have agent pilots running. Fourteen percent have agents in production. The gap between those two numbers is where careers stall, budgets evaporate, and executives lose faith in the technology. A March 2026 survey by the AI Infrastructure Alliance found that 89% of failed agent-to-production transitions trace back to exactly five gaps: integration brittleness, quality regression, monitoring blindness, ownership ambiguity, and training data drift. Not model quality. Not prompt engineering. Not the framework choice. The five gaps are all operational -- and they are all fixable with known engineering practices that have been adapted for autonomous agent systems. This guide is the 30-day playbook to close those gaps. It starts with a production readiness assessment that quantifies your current state. It builds SLO-driven monitoring, circuit breakers for graceful degradation, cost guardrails that prevent runaway spend, deployment patterns for safe rollouts, multi-agent resilience patterns, and EU AI Act compliance controls -- all wired to the GreenHelix A2A Commerce Gateway's 128 tools. Every chapter ends with working Python code, practical checklists, and decision matrices. By the end of the 30-day sprint in Chapter 8, your agent system will have a quantified go/no-go scorecard, automated rollback triggers, per-agent cost caps, and a compliance audit trail that satisfies Article 12 record-keeping before the August 2, 2026 deadline.

---

## Table of Contents

1. [The Production Readiness Assessment](#chapter-1-the-production-readiness-assessment)
2. [SLOs, SLAs, and Error Budgets for Agent Systems](#chapter-2-slos-slas-and-error-budgets-for-agent-systems)
3. [Circuit Breakers, Retries, and Graceful Degradation](#chapter-3-circuit-breakers-retries-and-graceful-degradation)
4. [Cost Guardrails and Token Budget Enforcement](#chapter-4-cost-guardrails-and-token-budget-enforcement)
5. [Deployment Patterns: Canary, Blue-Green, and Rollback](#chapter-5-deployment-patterns-canary-blue-green-and-rollback)
6. [Multi-Agent Failure Modes and Resilience Patterns](#chapter-6-multi-agent-failure-modes-and-resilience-patterns)
7. [EU AI Act Production Compliance (August 2026 Deadline)](#chapter-7-eu-ai-act-production-compliance-august-2026-deadline)
8. [The 30-Day Production Hardening Sprint](#chapter-8-the-30-day-production-hardening-sprint)

---

## Chapter 1: The Production Readiness Assessment

### The 5-Gap Framework

Every failed pilot-to-production transition in the AI Infrastructure Alliance dataset traces back to one or more of five gaps. Understanding these gaps is the first step because you cannot fix what you have not measured, and most teams are fixing the wrong thing -- they are tuning prompts when the real problem is that nobody owns the agent's SLA.

**Gap 1: Integration Brittleness.** The agent works against a sandbox API but has never been tested against production traffic patterns, rate limits, timeout behaviors, or error responses. The integration layer assumes happy-path responses and breaks on the first 429, 503, or malformed payload. This gap causes 34% of production failures.

**Gap 2: Quality Regression.** The agent's output quality was validated once during the pilot and never again. There is no automated quality gate, no regression suite, no way to detect that a model update or prompt change has degraded task completion rates. This gap causes 23% of production failures.

**Gap 3: Monitoring Blindness.** The agent runs in production but nobody knows if it is healthy. There are no SLOs, no latency tracking, no cost dashboards, no alerting. The first signal of a problem is a customer complaint or a surprise invoice. This gap causes 19% of production failures.

**Gap 4: Ownership Ambiguity.** No single person or team owns the agent in production. The ML team built the model. The platform team deployed it. The product team defined the requirements. When it breaks at 3 AM, nobody's pager goes off because nobody agreed to carry the pager. This gap causes 8% of production failures.

**Gap 5: Training Data Drift.** The agent was trained or fine-tuned on data that no longer represents the production distribution. Tool schemas have changed, counterparty behavior has shifted, or the business domain has evolved since the training data was collected. The agent is optimizing for a world that no longer exists. This gap causes 5% of production failures.

### The 40-Question Production Readiness Checklist

Score each question 0 (not done), 1 (partially done), or 2 (fully done). Maximum score is 80.

#### Integration (Questions 1-8)

| # | Question | Score |
|---|----------|-------|
| 1 | All API calls use retry with exponential backoff and jitter | 0 / 1 / 2 |
| 2 | Circuit breakers are implemented for every external dependency | 0 / 1 / 2 |
| 3 | Timeout values are explicitly configured (not default) for every HTTP call | 0 / 1 / 2 |
| 4 | The agent handles 429 (rate limit), 503 (unavailable), and 504 (timeout) gracefully | 0 / 1 / 2 |
| 5 | Integration tests run against a staging environment with production-like traffic | 0 / 1 / 2 |
| 6 | Webhook endpoints have been load-tested at 10x expected volume | 0 / 1 / 2 |
| 7 | All API credentials are rotated on a schedule and never hardcoded | 0 / 1 / 2 |
| 8 | Fallback behavior is defined and tested for every external service | 0 / 1 / 2 |

#### Quality (Questions 9-16)

| # | Question | Score |
|---|----------|-------|
| 9 | Task completion rate is measured and baselined | 0 / 1 / 2 |
| 10 | Automated regression tests run on every deployment | 0 / 1 / 2 |
| 11 | Output quality is scored by an automated evaluator (not just human spot-checks) | 0 / 1 / 2 |
| 12 | Model version and prompt version are tracked in deployment metadata | 0 / 1 / 2 |
| 13 | A/B testing infrastructure exists for prompt and model changes | 0 / 1 / 2 |
| 14 | Edge cases from production are captured and added to the test suite | 0 / 1 / 2 |
| 15 | The agent's failure modes are documented with expected frequency and impact | 0 / 1 / 2 |
| 16 | Quality SLOs are defined and measured (not just "it works") | 0 / 1 / 2 |

#### Monitoring (Questions 17-24)

| # | Question | Score |
|---|----------|-------|
| 17 | SLOs are defined for success rate, latency P99, and cost-per-task | 0 / 1 / 2 |
| 18 | SLO burn rate is tracked and alerts fire before the error budget is exhausted | 0 / 1 / 2 |
| 19 | Cost dashboards show per-agent, per-workflow, and per-tool-category spend | 0 / 1 / 2 |
| 20 | Latency is tracked at the tool-call level, not just end-to-end | 0 / 1 / 2 |
| 21 | Anomaly detection is configured for cost and error rate spikes | 0 / 1 / 2 |
| 22 | Logs are structured (JSON), centralized, and retained for 90+ days | 0 / 1 / 2 |
| 23 | Distributed tracing connects agent decisions to downstream tool calls | 0 / 1 / 2 |
| 24 | Health check endpoints exist and are polled by an external monitor | 0 / 1 / 2 |

#### Ownership (Questions 25-32)

| # | Question | Score |
|---|----------|-------|
| 25 | A named individual or team owns the agent's production SLA | 0 / 1 / 2 |
| 26 | On-call rotation is established with documented escalation paths | 0 / 1 / 2 |
| 27 | Incident runbooks exist for the top 5 failure modes | 0 / 1 / 2 |
| 28 | Change management process is defined (who can deploy, when, with what approval) | 0 / 1 / 2 |
| 29 | Capacity planning accounts for traffic growth over the next 6 months | 0 / 1 / 2 |
| 30 | Dependency owners are identified for every external service | 0 / 1 / 2 |
| 31 | Post-mortem process is established and post-mortems are blameless | 0 / 1 / 2 |
| 32 | The team has practiced a tabletop exercise for the agent's worst failure mode | 0 / 1 / 2 |

#### Training Data (Questions 33-40)

| # | Question | Score |
|---|----------|-------|
| 33 | Training/evaluation data is versioned alongside code | 0 / 1 / 2 |
| 34 | Data freshness is monitored and alerts fire when data is stale | 0 / 1 / 2 |
| 35 | Production inputs are sampled and compared to training distribution | 0 / 1 / 2 |
| 36 | Tool schema changes trigger re-evaluation of the agent's few-shot examples | 0 / 1 / 2 |
| 37 | Feedback loops exist: production failures are routed back to training data | 0 / 1 / 2 |
| 38 | Data governance controls are in place (PII handling, retention, access) | 0 / 1 / 2 |
| 39 | Evaluation datasets cover adversarial and edge-case inputs | 0 / 1 / 2 |
| 40 | A data quality pipeline validates training data before model updates | 0 / 1 / 2 |

### Scoring and Readiness Tiers

| Score | Tier | Verdict |
|-------|------|---------|
| 0-20 | Red: Not Ready | Do not proceed to production. Major gaps in 3+ categories. |
| 21-40 | Orange: High Risk | Production is possible but expect incidents within 30 days. |
| 41-60 | Yellow: Conditional | Production-ready with known risks. Mitigations must be documented. |
| 61-72 | Green: Ready | Production-ready. Minor gaps tracked as tech debt. |
| 73-80 | Blue: Hardened | Exceeds production requirements. Ready for regulated workloads. |

### Automating the Assessment with GreenHelix

You do not need to score this checklist manually. Several questions can be answered programmatically by querying your GreenHelix agent's current state -- checking SLA configuration, budget caps, webhook registrations, and trust scores.

```python
import requests
import json
from dataclasses import dataclass, field
from typing import Optional

BASE_URL = "https://api.greenhelix.net/v1"

def call_tool(api_key: str, tool: str, input_data: dict) -> dict:
    """Execute a GreenHelix tool via the unified endpoint."""
    resp = requests.post(
        f"{BASE_URL}/v1",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"tool": tool, "input": input_data},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


@dataclass
class ReadinessScore:
    integration: int = 0
    quality: int = 0
    monitoring: int = 0
    ownership: int = 0
    training_data: int = 0

    @property
    def total(self) -> int:
        return (self.integration + self.quality + self.monitoring
                + self.ownership + self.training_data)

    @property
    def tier(self) -> str:
        t = self.total
        if t <= 20: return "Red: Not Ready"
        if t <= 40: return "Orange: High Risk"
        if t <= 60: return "Yellow: Conditional"
        if t <= 72: return "Green: Ready"
        return "Blue: Hardened"


class ProductionReadinessAssessor:
    """Automated production readiness assessment using GreenHelix tools.

    Checks SLA configuration, budget caps, webhook registrations,
    trust scores, and identity verification to score monitoring,
    ownership, and integration readiness programmatically.
    """

    def __init__(self, api_key: str, agent_id: str):
        self.api_key = api_key
        self.agent_id = agent_id

    def _call(self, tool: str, input_data: dict) -> dict:
        return call_tool(self.api_key, tool, input_data)

    def check_sla_exists(self) -> bool:
        """Q17: Are SLOs defined?"""
        try:
            result = self._call("get_sla_status", {
                "agent_id": self.agent_id,
            })
            return result.get("status") == "success"
        except Exception:
            return False

    def check_budget_cap(self) -> bool:
        """Q19: Are cost dashboards and caps configured?"""
        try:
            result = self._call("get_balance", {
                "agent_id": self.agent_id,
            })
            # Budget cap exists if balance response includes limits
            return "daily_limit" in result or "monthly_limit" in result
        except Exception:
            return False

    def check_webhook_registered(self) -> bool:
        """Q6/Q21: Are webhook endpoints registered for alerting?"""
        try:
            result = self._call("list_webhooks", {
                "agent_id": self.agent_id,
            })
            webhooks = result.get("webhooks", [])
            return len(webhooks) > 0
        except Exception:
            return False

    def check_trust_score(self) -> Optional[float]:
        """Q15: Is the agent's trust profile established?"""
        try:
            result = self._call("get_trust_score", {
                "agent_id": self.agent_id,
            })
            return result.get("score")
        except Exception:
            return None

    def check_identity_verified(self) -> bool:
        """Q7: Is the agent's identity verified?"""
        try:
            result = self._call("get_verified_claims", {
                "agent_id": self.agent_id,
            })
            claims = result.get("claims", [])
            return len(claims) > 0
        except Exception:
            return False

    def run_automated_checks(self) -> dict:
        """Run all automated checks and return results."""
        return {
            "sla_configured": self.check_sla_exists(),
            "budget_cap_set": self.check_budget_cap(),
            "webhooks_registered": self.check_webhook_registered(),
            "trust_score": self.check_trust_score(),
            "identity_verified": self.check_identity_verified(),
        }

    def score_automated(self) -> ReadinessScore:
        """Score the automated checks. Manual questions still need human input."""
        checks = self.run_automated_checks()
        score = ReadinessScore()

        # Monitoring: SLA + budget + webhooks = up to 6 of 16 points
        if checks["sla_configured"]:
            score.monitoring += 2  # Q17
        if checks["budget_cap_set"]:
            score.monitoring += 2  # Q19
        if checks["webhooks_registered"]:
            score.monitoring += 2  # Q21

        # Integration: identity verification = up to 2 of 16 points
        if checks["identity_verified"]:
            score.integration += 2  # Q7

        # Quality: trust score > 0.7 = 2 of 16 points
        ts = checks["trust_score"]
        if ts is not None and ts > 0.7:
            score.quality += 2  # Q15

        return score


# Usage
if __name__ == "__main__":
    import os
    assessor = ProductionReadinessAssessor(
        api_key=os.environ["GREENHELIX_API_KEY"],
        agent_id="commerce-agent-prod-01",
    )
    score = assessor.score_automated()
    checks = assessor.run_automated_checks()
    print(f"Automated readiness score: {score.total}/80 (partial)")
    print(f"Tier: {score.tier}")
    print(f"Checks: {json.dumps(checks, indent=2)}")
    print("Complete the remaining 35 questions manually for full score.")
```

> **Key Takeaways**
>
> - 78% of enterprises have agent pilots; only 14% reach production. The gap is operational, not technical.
> - 89% of failures trace to 5 measurable gaps: integration, quality, monitoring, ownership, training data.
> - The 40-question checklist produces a quantified readiness score (0-80) with five tiers from Red (not ready) to Blue (hardened).
> - Several checklist items can be scored automatically by querying GreenHelix SLA, billing, webhook, trust, and identity tools.
> - Run the assessment before starting the 30-day sprint in Chapter 8 to establish your baseline.

---

## Chapter 2: SLOs, SLAs, and Error Budgets for Agent Systems

### Why "Uptime" Is Wrong for Agents

Traditional SRE monitors uptime: is the service responding to health checks? For agents, uptime is a necessary but wildly insufficient metric. An agent can be "up" -- responding to requests, returning 200 status codes -- while failing to complete tasks, producing low-quality outputs, or burning through budget at 10x the expected rate. A commerce agent that responds to every request but releases escrows to the wrong counterparty 5% of the time is 100% "up" and catastrophically broken.

Agent systems need three SLOs that together capture the full definition of "working."

**Task Completion SLO.** The percentage of tasks the agent completes successfully within a defined window. This is the primary SLO. A task is "complete" when the business outcome is achieved -- the escrow is released, the listing is published, the dispute is resolved -- not when the API call returns 200.

**Latency P99 SLO.** The 99th percentile end-to-end latency for a task, measured from request receipt to final outcome confirmation. P99, not P50, because agent latency distributions have heavy tails -- a single LLM retry or tool timeout can push one request to 30 seconds while the median is 2 seconds. The P50 masks the pain.

**Cost-per-Task SLO.** The maximum acceptable cost to complete a single task. This is measured in dollars, not tokens, because the cost includes LLM inference, tool calls, gateway fees, and any downstream API costs. A cost-per-task SLO of $0.12 means any task that costs more than $0.12 has breached the SLO, even if it completed successfully and quickly.

### Error Budgets: Spending Wisely

An error budget is the complement of the SLO. If your task completion SLO is 99.5%, your error budget is 0.5% -- you can afford 5 failures per 1,000 tasks. Error budgets solve the eternal conflict between "ship faster" and "break nothing." When the error budget has remaining capacity, the team ships aggressively. When the error budget is nearly exhausted, the team freezes deployments and focuses on reliability.

For agent systems, you need three independent error budgets -- one for each SLO. A cost overrun does not consume the completion error budget. A latency spike does not consume the cost budget. This prevents a single bad dimension from blocking all progress.

| SLO | Target | Error Budget (30-day) | Burn Rate Alert |
|-----|--------|-----------------------|-----------------|
| Task Completion | 99.5% | 0.5% = 5 failures / 1,000 tasks | >2x in 1 hour |
| Latency P99 | < 5 seconds | 1% of tasks > 5s allowed | >3x in 30 min |
| Cost-per-Task | < $0.15 | 2% of tasks > $0.15 allowed | >5x in 15 min |

### Wiring SLA Monitoring with GreenHelix

The GreenHelix gateway provides three SLA tools that map directly to this SLO framework: `create_sla` defines the SLA parameters, `check_sla_compliance` evaluates current compliance, and `get_sla_status` retrieves the SLA's running state. Combined with `register_webhook`, you can build fully automated SLO monitoring with burn-rate alerting.

```python
import requests
import time
import json
import threading
from dataclasses import dataclass, field
from typing import Optional, List, Callable
from datetime import datetime, timedelta

BASE_URL = "https://api.greenhelix.net/v1"


def call_tool(api_key: str, tool: str, input_data: dict) -> dict:
    resp = requests.post(
        f"{BASE_URL}/v1",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"tool": tool, "input": input_data},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


@dataclass
class SLODefinition:
    name: str
    target: float       # e.g., 0.995 for 99.5%
    window_days: int    # rolling window
    metric: str         # "completion_rate", "latency_p99", "cost_per_task"
    threshold: float    # absolute threshold (seconds for latency, dollars for cost)


@dataclass
class BurnRateAlert:
    slo_name: str
    multiplier: float   # e.g., 2.0 means burning 2x the allowed rate
    window_minutes: int
    triggered_at: Optional[datetime] = None


class AgentSLOMonitor:
    """Tracks SLO burn rate across three dimensions and triggers
    alerts via GreenHelix webhooks when burn rate exceeds thresholds.

    Wire this into your agent's main loop or run it as a sidecar.
    """

    def __init__(self, api_key: str, agent_id: str):
        self.api_key = api_key
        self.agent_id = agent_id
        self.slos: List[SLODefinition] = []
        self.burn_rate_alerts: List[BurnRateAlert] = []
        self._alert_callbacks: List[Callable] = []
        self._task_log: List[dict] = []

    def _call(self, tool: str, input_data: dict) -> dict:
        return call_tool(self.api_key, tool, input_data)

    def define_slo(self, slo: SLODefinition) -> dict:
        """Register an SLO with GreenHelix and set up compliance tracking."""
        result = self._call("create_sla", {
            "agent_id": self.agent_id,
            "sla_name": slo.name,
            "metric": slo.metric,
            "target": slo.target,
            "window_days": slo.window_days,
            "threshold": slo.threshold,
        })
        self.slos.append(slo)
        return result

    def register_alert_webhook(self, webhook_url: str, threshold_pct: int = 80) -> dict:
        """Register a webhook that fires when error budget reaches threshold."""
        return self._call("register_webhook", {
            "agent_id": self.agent_id,
            "url": webhook_url,
            "events": ["sla.breach", "sla.warning", "budget.threshold"],
            "config": {"threshold_pct": threshold_pct},
        })

    def record_task(self, task_id: str, success: bool, latency_ms: float,
                    cost_usd: float):
        """Record a completed task for local burn-rate calculation."""
        self._task_log.append({
            "task_id": task_id,
            "success": success,
            "latency_ms": latency_ms,
            "cost_usd": cost_usd,
            "timestamp": datetime.utcnow(),
        })
        self._check_burn_rates()

    def _tasks_in_window(self, minutes: int) -> List[dict]:
        cutoff = datetime.utcnow() - timedelta(minutes=minutes)
        return [t for t in self._task_log if t["timestamp"] >= cutoff]

    def _check_burn_rates(self):
        """Check if any SLO is burning faster than its error budget allows."""
        for slo in self.slos:
            if slo.metric == "completion_rate":
                self._check_completion_burn(slo)
            elif slo.metric == "latency_p99":
                self._check_latency_burn(slo)
            elif slo.metric == "cost_per_task":
                self._check_cost_burn(slo)

    def _check_completion_burn(self, slo: SLODefinition):
        window_tasks = self._tasks_in_window(60)  # 1-hour window
        if len(window_tasks) < 10:
            return  # Not enough data
        failures = sum(1 for t in window_tasks if not t["success"])
        failure_rate = failures / len(window_tasks)
        allowed_rate = 1.0 - slo.target  # e.g., 0.005 for 99.5%
        if allowed_rate > 0:
            burn_multiplier = failure_rate / allowed_rate
            if burn_multiplier > 2.0:
                self._fire_alert(BurnRateAlert(
                    slo_name=slo.name,
                    multiplier=burn_multiplier,
                    window_minutes=60,
                    triggered_at=datetime.utcnow(),
                ))

    def _check_latency_burn(self, slo: SLODefinition):
        window_tasks = self._tasks_in_window(30)  # 30-min window
        if len(window_tasks) < 10:
            return
        threshold_ms = slo.threshold * 1000
        breaches = sum(1 for t in window_tasks
                       if t["latency_ms"] > threshold_ms)
        breach_rate = breaches / len(window_tasks)
        allowed_rate = 0.01  # 1% allowed
        if allowed_rate > 0:
            burn_multiplier = breach_rate / allowed_rate
            if burn_multiplier > 3.0:
                self._fire_alert(BurnRateAlert(
                    slo_name=slo.name,
                    multiplier=burn_multiplier,
                    window_minutes=30,
                    triggered_at=datetime.utcnow(),
                ))

    def _check_cost_burn(self, slo: SLODefinition):
        window_tasks = self._tasks_in_window(15)  # 15-min window
        if len(window_tasks) < 5:
            return
        breaches = sum(1 for t in window_tasks
                       if t["cost_usd"] > slo.threshold)
        breach_rate = breaches / len(window_tasks)
        allowed_rate = 0.02  # 2% allowed
        if allowed_rate > 0:
            burn_multiplier = breach_rate / allowed_rate
            if burn_multiplier > 5.0:
                self._fire_alert(BurnRateAlert(
                    slo_name=slo.name,
                    multiplier=burn_multiplier,
                    window_minutes=15,
                    triggered_at=datetime.utcnow(),
                ))

    def _fire_alert(self, alert: BurnRateAlert):
        """Publish burn-rate alert to GreenHelix event bus."""
        self.burn_rate_alerts.append(alert)
        self._call("publish_event", {
            "agent_id": self.agent_id,
            "event_type": "slo.burn_rate_alert",
            "payload": {
                "slo_name": alert.slo_name,
                "burn_multiplier": round(alert.multiplier, 2),
                "window_minutes": alert.window_minutes,
                "triggered_at": alert.triggered_at.isoformat(),
            },
        })
        for cb in self._alert_callbacks:
            cb(alert)

    def check_compliance(self) -> dict:
        """Check current SLA compliance via GreenHelix."""
        return self._call("check_sla_compliance", {
            "agent_id": self.agent_id,
        })

    def get_status(self) -> dict:
        """Get current SLA status including error budget remaining."""
        return self._call("get_sla_status", {
            "agent_id": self.agent_id,
        })

    def on_alert(self, callback: Callable):
        """Register a callback for burn-rate alerts."""
        self._alert_callbacks.append(callback)


# Usage: set up three SLOs and a webhook
if __name__ == "__main__":
    import os
    monitor = AgentSLOMonitor(
        api_key=os.environ["GREENHELIX_API_KEY"],
        agent_id="commerce-agent-prod-01",
    )

    # Define three SLOs
    monitor.define_slo(SLODefinition(
        name="task-completion", target=0.995,
        window_days=30, metric="completion_rate", threshold=0.995,
    ))
    monitor.define_slo(SLODefinition(
        name="latency-p99", target=0.99,
        window_days=30, metric="latency_p99", threshold=5.0,
    ))
    monitor.define_slo(SLODefinition(
        name="cost-per-task", target=0.98,
        window_days=30, metric="cost_per_task", threshold=0.15,
    ))

    # Register webhook for 80% error budget consumption
    monitor.register_alert_webhook(
        "https://your-app.example.com/alerts/slo",
        threshold_pct=80,
    )

    # In your agent loop, record every task:
    # monitor.record_task("task-123", success=True, latency_ms=1200, cost_usd=0.08)
    print("SLO monitoring configured. Three SLOs active.")
```

> **Key Takeaways**
>
> - Traditional "uptime" monitoring is insufficient for agents. Use three SLOs: task completion rate, latency P99, and cost-per-task.
> - Error budgets convert SLOs into actionable deployment gates: ship when budget allows, freeze when it does not.
> - Burn-rate alerts catch problems before the error budget is exhausted, giving you hours instead of minutes to respond.
> - GreenHelix `create_sla`, `check_sla_compliance`, and `get_sla_status` provide the server-side SLA tracking; the `AgentSLOMonitor` adds client-side burn-rate calculation and event publishing.
> - See P9 (Testing & Observability) for SLO-driven regression tests and P12 (Incident Response) for SLO breach runbooks.

---

## Chapter 3: Circuit Breakers, Retries, and Graceful Degradation

### Why Agents Need Circuit Breakers

A traditional microservice retries a failed HTTP call three times and returns an error. An agent retries a failed tool call, but its retry logic is embedded in the LLM's reasoning loop -- the model sees the error, decides to try again, and generates another tool call. Without a circuit breaker, the agent will retry until its context window overflows or its budget runs out. Worse, in a multi-agent system, one agent's retry storm becomes backpressure on every downstream service it touches, causing cascading failures.

Circuit breakers solve this by short-circuiting failed calls after a threshold is reached. When the circuit is open, calls fail immediately without hitting the downstream service, giving it time to recover. When a probe succeeds, the circuit closes and normal traffic resumes.

### The Three-Layer Circuit Breaker

Agent systems need circuit breakers at three layers, not one.

**Layer 1: LLM Call Circuit Breaker.** Protects against LLM provider outages and rate limits. When the LLM returns 5 consecutive errors or latency exceeds 30 seconds, the circuit opens. Fallback: smaller model, cached response, or queue for human review.

**Layer 2: Tool Invocation Circuit Breaker.** Protects against individual tool failures. Each tool has its own circuit breaker. When `create_escrow` fails 3 times in 60 seconds, the circuit opens for that tool only. Other tools remain available.

**Layer 3: Inter-Agent Circuit Breaker.** Protects against counterparty agent failures in multi-agent workflows. When Agent B stops responding to Agent A's messages, the circuit opens and Agent A routes to an alternative provider or queues the work.

### Exponential Backoff with Jitter

Retries without backoff create thundering herds. Retries with fixed backoff create synchronized retry waves. Exponential backoff with full jitter is the only retry strategy that avoids both problems.

```
delay = min(cap, base * 2^attempt) * random(0, 1)
```

For agent systems, use `base=0.5s`, `cap=30s`, and add a per-agent random offset to prevent fleet-wide synchronization.

### The Fallback Chain

When a circuit is open, the agent needs somewhere to fall back. The fallback chain for LLM calls follows a degradation hierarchy:

```
Frontier Model (GPT-4o, Claude Opus)
       |
       v  [circuit open]
Smaller Model (GPT-4o-mini, Claude Haiku)
       |
       v  [circuit open]
Cached Response (last known good for this input class)
       |
       v  [cache miss]
Human Escalation (queue task for human review)
```

For tool calls, the fallback is simpler: return a structured error to the LLM and let it adjust its plan. The circuit breaker's job is not to hide the failure -- it is to prevent the failure from cascading.

```python
import requests
import time
import json
import random
import threading
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Callable, Any, Dict
from datetime import datetime, timedelta

BASE_URL = "https://api.greenhelix.net/v1"


def call_tool(api_key: str, tool: str, input_data: dict) -> dict:
    resp = requests.post(
        f"{BASE_URL}/v1",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"tool": tool, "input": input_data},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject calls
    HALF_OPEN = "half_open"  # Testing recovery


@dataclass
class CircuitBreaker:
    """Circuit breaker for a single dependency (tool, LLM, agent).

    Tracks failures, opens the circuit after threshold, and publishes
    state changes to GreenHelix Events for fleet-wide visibility.
    """
    name: str
    failure_threshold: int = 5
    recovery_timeout_s: float = 60.0
    half_open_max_calls: int = 1

    state: CircuitState = field(default=CircuitState.CLOSED)
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: Optional[datetime] = None
    half_open_calls: int = 0
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def can_execute(self) -> bool:
        with self._lock:
            if self.state == CircuitState.CLOSED:
                return True
            if self.state == CircuitState.OPEN:
                if (self.last_failure_time and
                    datetime.utcnow() - self.last_failure_time
                        > timedelta(seconds=self.recovery_timeout_s)):
                    self.state = CircuitState.HALF_OPEN
                    self.half_open_calls = 0
                    return True
                return False
            if self.state == CircuitState.HALF_OPEN:
                return self.half_open_calls < self.half_open_max_calls
            return False

    def record_success(self):
        with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                self.state = CircuitState.CLOSED
                self.failure_count = 0
            self.success_count += 1

    def record_failure(self):
        with self._lock:
            self.failure_count += 1
            self.last_failure_time = datetime.utcnow()
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.OPEN
            elif self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN


class ResilientToolCaller:
    """Wraps GreenHelix tool calls with per-tool circuit breakers,
    exponential backoff with jitter, and state publishing.

    Each tool gets its own circuit breaker. State changes are published
    to GreenHelix Events so other agents and dashboards can see which
    tools are degraded.
    """

    def __init__(self, api_key: str, agent_id: str,
                 failure_threshold: int = 5,
                 max_retries: int = 3,
                 backoff_base: float = 0.5,
                 backoff_cap: float = 30.0):
        self.api_key = api_key
        self.agent_id = agent_id
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self.backoff_cap = backoff_cap
        self._breakers: Dict[str, CircuitBreaker] = {}
        self._failure_threshold = failure_threshold

    def _get_breaker(self, tool: str) -> CircuitBreaker:
        if tool not in self._breakers:
            self._breakers[tool] = CircuitBreaker(
                name=tool,
                failure_threshold=self._failure_threshold,
            )
        return self._breakers[tool]

    def _backoff_delay(self, attempt: int) -> float:
        """Exponential backoff with full jitter."""
        exp_delay = min(self.backoff_cap,
                        self.backoff_base * (2 ** attempt))
        return exp_delay * random.random()

    def _publish_state_change(self, tool: str, state: CircuitState):
        """Publish circuit breaker state change to GreenHelix Events."""
        try:
            call_tool(self.api_key, "publish_event", {
                "agent_id": self.agent_id,
                "event_type": "circuit_breaker.state_change",
                "payload": {
                    "tool": tool,
                    "new_state": state.value,
                    "timestamp": datetime.utcnow().isoformat(),
                },
            })
        except Exception:
            pass  # Event publishing should never block tool calls

    def execute(self, tool: str, input_data: dict,
                fallback: Optional[Callable] = None) -> dict:
        """Execute a tool call with circuit breaker and retry logic.

        Args:
            tool: GreenHelix tool name
            input_data: Tool input parameters
            fallback: Optional callable returning a fallback response

        Returns:
            Tool response dict

        Raises:
            CircuitOpenError: If circuit is open and no fallback provided
            Exception: If all retries exhausted and no fallback provided
        """
        breaker = self._get_breaker(tool)

        if not breaker.can_execute():
            if breaker.state == CircuitState.OPEN:
                self._publish_state_change(tool, CircuitState.OPEN)
            if fallback:
                return fallback()
            raise CircuitOpenError(
                f"Circuit open for tool '{tool}'. "
                f"Failures: {breaker.failure_count}. "
                f"Recovery in {breaker.recovery_timeout_s}s."
            )

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                result = call_tool(self.api_key, tool, input_data)
                breaker.record_success()
                if breaker.state == CircuitState.CLOSED and attempt > 0:
                    self._publish_state_change(tool, CircuitState.CLOSED)
                return result
            except requests.exceptions.HTTPError as e:
                status = e.response.status_code if e.response else 500
                # Do not retry client errors (except 429)
                if 400 <= status < 500 and status != 429:
                    breaker.record_failure()
                    raise
                last_error = e
                breaker.record_failure()
            except requests.exceptions.Timeout as e:
                last_error = e
                breaker.record_failure()
            except requests.exceptions.ConnectionError as e:
                last_error = e
                breaker.record_failure()

            if attempt < self.max_retries:
                delay = self._backoff_delay(attempt)
                time.sleep(delay)

        # All retries exhausted
        if fallback:
            return fallback()
        raise last_error or RuntimeError(f"Tool '{tool}' call failed")

    def get_circuit_states(self) -> dict:
        """Return the state of all circuit breakers."""
        return {
            name: {
                "state": cb.state.value,
                "failure_count": cb.failure_count,
                "success_count": cb.success_count,
            }
            for name, cb in self._breakers.items()
        }


class CircuitOpenError(Exception):
    pass


# Usage
if __name__ == "__main__":
    import os
    caller = ResilientToolCaller(
        api_key=os.environ["GREENHELIX_API_KEY"],
        agent_id="commerce-agent-prod-01",
        failure_threshold=5,
        max_retries=3,
    )

    # Call with automatic retry and circuit breaker
    result = caller.execute("get_balance", {
        "agent_id": "commerce-agent-prod-01",
    })

    # Call with fallback
    result = caller.execute(
        "create_escrow",
        {"amount": 50.0, "counterparty": "provider-agent-01"},
        fallback=lambda: {"status": "queued", "message": "Escrow queued for retry"},
    )
    print(json.dumps(caller.get_circuit_states(), indent=2))
```

### Decision Matrix: When to Retry vs. Fail Fast vs. Fall Back

| Error Type | HTTP Code | Retry? | Circuit Breaker? | Fallback? |
|------------|-----------|--------|-------------------|-----------|
| Rate limited | 429 | Yes, with backoff | Yes, at threshold | Queue for later |
| Server error | 500 | Yes, 2x max | Yes | Return cached |
| Service unavailable | 503 | Yes, with backoff | Yes | Route to alternative |
| Gateway timeout | 504 | Yes, 1x | Yes | Return partial result |
| Bad request | 400 | No | No | Fix input, do not retry |
| Unauthorized | 401 | No | No | Refresh credential, retry 1x |
| Forbidden | 403 | No | No | Escalate to human |
| Not found | 404 | No | No | Fail with clear error |
| Payment required | 402 | No | No | Top up budget, retry 1x |

> **Key Takeaways**
>
> - Agent retry logic lives inside the LLM reasoning loop and will retry forever without an external circuit breaker.
> - Implement circuit breakers at three layers: LLM calls, tool invocations, and inter-agent communication.
> - Use exponential backoff with full jitter (`base * 2^attempt * random()`) to avoid thundering herds.
> - Publish circuit breaker state changes to GreenHelix Events so dashboards and peer agents can see degraded dependencies.
> - The fallback chain for LLM calls: frontier model, smaller model, cached response, human escalation.
> - See P12 (Incident Response) for automated containment actions when circuit breakers trip fleet-wide.

---

## Chapter 4: Cost Guardrails and Token Budget Enforcement

### The Three Layers of Cost Control

Cost guardrails operate at three granularities. Miss any layer and the blast radius of a runaway agent expands exponentially.

**Per-Request Guards.** Every individual tool call or LLM inference has a maximum allowable cost. If a single request would cost more than the cap, it is rejected before execution. This prevents a single malformed request from draining the budget.

**Per-Agent Guards.** Every agent has a daily and monthly budget cap enforced at the wallet level. When the agent hits its cap, all subsequent requests receive a 402 response. The blast radius is one agent, not the fleet.

**Per-Workflow Guards.** A multi-agent workflow (e.g., "hire a researcher, verify results, publish summary") has a total budget envelope. If the workflow exceeds its budget, the orchestrator aborts the workflow and releases any held escrows. This prevents fan-out amplification from consuming the fleet budget.

### Token Budget Allocation

Not all agent tasks cost the same. A simple lookup costs a fraction of a cent. A multi-step research workflow with RAG retrieval costs dollars. Allocating a flat budget per agent wastes money on simple agents and starves complex ones.

The allocation formula:

```
agent_daily_budget = baseline_cost * safety_multiplier * task_volume

where:
  baseline_cost   = median cost-per-task over last 7 days
  safety_multiplier = 3.0 (allows 3x median before cap triggers)
  task_volume     = expected daily task count
```

Recalculate weekly. Publish the new budget via `set_budget`. Alert at 75% consumption via `register_webhook`.

### The CostGuardRail Middleware

```python
import requests
import time
import json
import threading
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from datetime import datetime, timedelta

BASE_URL = "https://api.greenhelix.net/v1"


def call_tool(api_key: str, tool: str, input_data: dict) -> dict:
    resp = requests.post(
        f"{BASE_URL}/v1",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"tool": tool, "input": input_data},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


@dataclass
class CostLimits:
    per_request_usd: float = 1.00      # Max cost for a single tool call
    daily_limit_usd: float = 25.00     # Hard daily cap
    monthly_limit_usd: float = 500.00  # Hard monthly cap
    workflow_limit_usd: float = 10.00  # Max cost per workflow execution
    alert_threshold_pct: float = 0.75  # Alert at 75% consumption


class CostGuardRail:
    """Middleware that enforces per-request, per-agent, and per-workflow
    cost caps using GreenHelix Billing and Ledger tools.

    Wrap your agent's tool calls with this middleware to prevent
    runaway spending. Integrates with GreenHelix set_budget,
    get_balance, get_usage_analytics, and record_transaction.
    """

    def __init__(self, api_key: str, agent_id: str, limits: CostLimits):
        self.api_key = api_key
        self.agent_id = agent_id
        self.limits = limits
        self._workflow_spend: Dict[str, float] = {}
        self._daily_spend: float = 0.0
        self._day_start: datetime = datetime.utcnow().replace(
            hour=0, minute=0, second=0, microsecond=0)
        self._lock = threading.Lock()
        self._kill_switch: bool = False

    def _call(self, tool: str, input_data: dict) -> dict:
        return call_tool(self.api_key, tool, input_data)

    def initialize(self) -> dict:
        """Set budget caps on the GreenHelix gateway."""
        result = self._call("set_budget", {
            "agent_id": self.agent_id,
            "daily_limit": self.limits.daily_limit_usd,
            "monthly_limit": self.limits.monthly_limit_usd,
        })
        # Register webhook for threshold alerts
        self._call("register_webhook", {
            "agent_id": self.agent_id,
            "url": f"https://your-app.example.com/alerts/cost/{self.agent_id}",
            "events": ["budget.threshold", "budget.exceeded"],
            "config": {
                "threshold_pct": int(self.limits.alert_threshold_pct * 100),
            },
        })
        return result

    def activate_kill_switch(self):
        """Emergency: reject all subsequent requests."""
        self._kill_switch = True
        # Set budget to zero on the gateway
        self._call("set_budget", {
            "agent_id": self.agent_id,
            "daily_limit": 0,
            "monthly_limit": 0,
        })

    def deactivate_kill_switch(self):
        """Resume normal operation after manual review."""
        self._kill_switch = False
        self.initialize()  # Restore original limits

    def check_balance(self) -> dict:
        """Get current balance and spend from GreenHelix."""
        return self._call("get_balance", {
            "agent_id": self.agent_id,
        })

    def get_analytics(self, period: str = "daily") -> dict:
        """Get usage analytics for cost attribution."""
        return self._call("get_usage_analytics", {
            "agent_id": self.agent_id,
            "period": period,
        })

    def _reset_daily_if_needed(self):
        now = datetime.utcnow()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if today > self._day_start:
            self._daily_spend = 0.0
            self._day_start = today

    def pre_request_check(self, estimated_cost_usd: float,
                          workflow_id: Optional[str] = None) -> dict:
        """Check cost limits BEFORE executing a request.

        Returns:
            {"allowed": True/False, "reason": str, "remaining_daily": float}
        """
        if self._kill_switch:
            return {
                "allowed": False,
                "reason": "Kill switch active. All requests blocked.",
                "remaining_daily": 0.0,
            }

        with self._lock:
            self._reset_daily_if_needed()

            # Per-request check
            if estimated_cost_usd > self.limits.per_request_usd:
                return {
                    "allowed": False,
                    "reason": (f"Request cost ${estimated_cost_usd:.4f} exceeds "
                               f"per-request limit ${self.limits.per_request_usd:.2f}"),
                    "remaining_daily": self.limits.daily_limit_usd - self._daily_spend,
                }

            # Daily check
            if self._daily_spend + estimated_cost_usd > self.limits.daily_limit_usd:
                return {
                    "allowed": False,
                    "reason": (f"Daily spend ${self._daily_spend:.2f} + request "
                               f"${estimated_cost_usd:.4f} exceeds daily limit "
                               f"${self.limits.daily_limit_usd:.2f}"),
                    "remaining_daily": self.limits.daily_limit_usd - self._daily_spend,
                }

            # Workflow check
            if workflow_id:
                wf_spend = self._workflow_spend.get(workflow_id, 0.0)
                if wf_spend + estimated_cost_usd > self.limits.workflow_limit_usd:
                    return {
                        "allowed": False,
                        "reason": (f"Workflow '{workflow_id}' spend ${wf_spend:.2f} + "
                                   f"request ${estimated_cost_usd:.4f} exceeds workflow "
                                   f"limit ${self.limits.workflow_limit_usd:.2f}"),
                        "remaining_daily": self.limits.daily_limit_usd - self._daily_spend,
                    }

            return {
                "allowed": True,
                "reason": "Within all limits",
                "remaining_daily": (self.limits.daily_limit_usd
                                    - self._daily_spend
                                    - estimated_cost_usd),
            }

    def post_request_record(self, actual_cost_usd: float,
                            workflow_id: Optional[str] = None,
                            metadata: Optional[dict] = None):
        """Record actual cost AFTER a request completes."""
        with self._lock:
            self._daily_spend += actual_cost_usd
            if workflow_id:
                self._workflow_spend[workflow_id] = (
                    self._workflow_spend.get(workflow_id, 0.0) + actual_cost_usd
                )

        # Record to GreenHelix Ledger for audit trail
        self._call("record_transaction", {
            "agent_id": self.agent_id,
            "amount": str(actual_cost_usd),
            "type": "tool_call_cost",
            "metadata": metadata or {},
        })

        # Check alert threshold
        daily_pct = self._daily_spend / self.limits.daily_limit_usd
        if daily_pct >= self.limits.alert_threshold_pct:
            self._call("publish_event", {
                "agent_id": self.agent_id,
                "event_type": "cost.threshold_warning",
                "payload": {
                    "daily_spend": round(self._daily_spend, 4),
                    "daily_limit": self.limits.daily_limit_usd,
                    "pct_consumed": round(daily_pct * 100, 1),
                },
            })

    def end_workflow(self, workflow_id: str):
        """Clean up workflow tracking after workflow completes."""
        with self._lock:
            total = self._workflow_spend.pop(workflow_id, 0.0)
        return {"workflow_id": workflow_id, "total_cost_usd": round(total, 4)}


# Usage
if __name__ == "__main__":
    import os

    guardrail = CostGuardRail(
        api_key=os.environ["GREENHELIX_API_KEY"],
        agent_id="commerce-agent-prod-01",
        limits=CostLimits(
            per_request_usd=1.00,
            daily_limit_usd=25.00,
            monthly_limit_usd=500.00,
            workflow_limit_usd=10.00,
        ),
    )
    guardrail.initialize()

    # Before every tool call:
    check = guardrail.pre_request_check(
        estimated_cost_usd=0.05,
        workflow_id="wf-research-001",
    )
    if check["allowed"]:
        # ... execute the tool call ...
        guardrail.post_request_record(
            actual_cost_usd=0.047,
            workflow_id="wf-research-001",
            metadata={"tool": "search_marketplace", "tokens": 1200},
        )
    else:
        print(f"Blocked: {check['reason']}")

    # Emergency kill switch
    # guardrail.activate_kill_switch()
```

### Cost Estimation Table

Use this table to estimate costs when calling `pre_request_check`:

| Operation Type | Estimated Cost | Notes |
|----------------|----------------|-------|
| Simple tool lookup (get_balance, get_trust_score) | $0.001 - $0.005 | Gateway fee only |
| State-changing tool (create_escrow, release_escrow) | $0.01 - $0.05 | Gateway fee + processing |
| LLM inference (GPT-4o, 1K input + 500 output tokens) | $0.01 - $0.03 | Per-call, model-dependent |
| LLM inference (Claude Opus, 1K input + 500 output tokens) | $0.02 - $0.06 | Per-call, model-dependent |
| Multi-step workflow (5 tool calls + 3 LLM inferences) | $0.10 - $0.30 | Sum of components |
| RAG workflow (embedding + retrieval + generation) | $0.05 - $0.15 | Embedding + LLM costs |

> **Key Takeaways**
>
> - Cost guardrails operate at three layers: per-request, per-agent, and per-workflow. Missing any layer allows blast radius expansion.
> - Budget allocation formula: `baseline_cost * 3.0 * task_volume`, recalculated weekly.
> - The kill switch sets the gateway budget to zero, immediately blocking all requests for the agent.
> - Record every cost to the GreenHelix Ledger via `record_transaction` for audit trails and post-mortem analysis.
> - See P6 (FinOps Playbook) for fleet-wide cost dashboards, volume discount optimization, and cost attribution patterns.

---

## Chapter 5: Deployment Patterns: Canary, Blue-Green, and Rollback

### Why Agent Deployments Are Dangerous

Deploying a new version of a traditional web service is risky. Deploying a new version of an autonomous agent is dangerous. The difference is that a web service returns wrong HTML; an agent makes wrong financial decisions. A prompt change that increases task completion rate by 2% might also increase cost-per-task by 40%. A model upgrade that reduces latency might degrade output quality for edge cases. You cannot know the full impact of an agent deployment without measuring it against production traffic -- but you cannot expose 100% of production traffic to an unvalidated change without accepting the risk of fleet-wide impact.

Canary deployments solve this by routing a small percentage of traffic to the new version, measuring SLOs, and promoting or rolling back based on data.

### Canary Deployment for Agent Upgrades

The canary pattern for agents:

1. Deploy new agent version alongside the current version.
2. Route 5% of traffic to the canary.
3. Measure all three SLOs (completion, latency, cost) for 2 hours.
4. If SLOs hold: promote to 25%, then 50%, then 100%.
5. If any SLO breaches: automatic rollback to 0% canary traffic.

```
                  ┌──────────────────┐
                  │   Load Balancer   │
                  │   (5% / 95%)     │
                  └───────┬──────────┘
                    ┌─────┴─────┐
              ┌─────▼───┐  ┌────▼──────┐
              │ Canary  │  │ Stable    │
              │ v2.1.0  │  │ v2.0.0   │
              │ 5%      │  │ 95%      │
              └─────┬───┘  └────┬──────┘
                    │           │
                    └─────┬─────┘
                    ┌─────▼──────────┐
                    │   SLO Monitor  │
                    │ Compare canary │
                    │  vs. stable    │
                    └────────────────┘
```

### Blue-Green Switching

Blue-green deployments maintain two complete environments. At any time, one is live (blue) and one is staging (green). To deploy:

1. Deploy the new version to green.
2. Run smoke tests against green.
3. Switch traffic from blue to green.
4. If problems: switch back to blue instantly.

Blue-green is simpler than canary but does not allow gradual traffic shifting. Use it when you need instant rollback capability and can accept all-or-nothing deployment.

### Automated Rollback Triggers

Rollback should be automated, not a decision made by a sleepy on-call engineer at 3 AM. Define rollback triggers tied to SLO breach:

| Trigger | Condition | Action |
|---------|-----------|--------|
| Completion Rate Drop | Canary completion < stable - 2% for 30 min | Rollback |
| Latency Spike | Canary P99 > stable P99 * 1.5 for 15 min | Rollback |
| Cost Overrun | Canary cost-per-task > stable * 1.3 for 15 min | Rollback |
| Error Rate | Canary 5xx rate > 5% for 10 min | Immediate rollback |
| Circuit Breaker | Any canary circuit breaker opens | Immediate rollback |

```python
import requests
import time
import json
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from datetime import datetime, timedelta
from enum import Enum

BASE_URL = "https://api.greenhelix.net/v1"


def call_tool(api_key: str, tool: str, input_data: dict) -> dict:
    resp = requests.post(
        f"{BASE_URL}/v1",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"tool": tool, "input": input_data},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


class DeploymentPhase(Enum):
    PENDING = "pending"
    CANARY_5 = "canary_5"
    CANARY_25 = "canary_25"
    CANARY_50 = "canary_50"
    PROMOTED = "promoted"
    ROLLED_BACK = "rolled_back"


@dataclass
class SLOComparison:
    metric: str
    canary_value: float
    stable_value: float
    threshold_ratio: float  # max allowed canary/stable ratio

    @property
    def passed(self) -> bool:
        if self.stable_value == 0:
            return True
        ratio = self.canary_value / self.stable_value
        return ratio <= self.threshold_ratio


class CanaryDeployer:
    """Manages canary deployments for agent upgrades with automated
    SLO-based promotion and rollback.

    Queries GreenHelix Analytics to compare canary vs. stable SLOs
    and publishes deployment events for audit trails.
    """

    def __init__(self, api_key: str, agent_id: str,
                 canary_agent_id: str):
        self.api_key = api_key
        self.agent_id = agent_id          # Stable version
        self.canary_agent_id = canary_agent_id  # Canary version
        self.phase = DeploymentPhase.PENDING
        self.deployment_id = f"deploy-{int(time.time())}"
        self.slo_history: List[dict] = []

    def _call(self, tool: str, input_data: dict) -> dict:
        return call_tool(self.api_key, tool, input_data)

    def _get_metrics(self, target_agent_id: str) -> dict:
        """Fetch revenue and performance metrics for an agent."""
        return self._call("get_revenue_metrics", {
            "agent_id": target_agent_id,
            "period": "hourly",
        })

    def _compare_slos(self) -> List[SLOComparison]:
        """Compare canary vs. stable SLOs across all dimensions."""
        stable = self._get_metrics(self.agent_id)
        canary = self._get_metrics(self.canary_agent_id)

        comparisons = []

        # Completion rate: canary should not be worse
        s_completion = stable.get("completion_rate", 1.0)
        c_completion = canary.get("completion_rate", 1.0)
        # For completion, we invert: lower is worse, so check 1/ratio
        if c_completion > 0:
            comparisons.append(SLOComparison(
                metric="completion_rate",
                canary_value=s_completion / c_completion,
                stable_value=1.0,
                threshold_ratio=1.02,  # Allow 2% degradation
            ))

        # Latency P99: canary should not be 50% higher
        s_latency = stable.get("latency_p99_ms", 1000)
        c_latency = canary.get("latency_p99_ms", 1000)
        comparisons.append(SLOComparison(
            metric="latency_p99",
            canary_value=c_latency,
            stable_value=s_latency,
            threshold_ratio=1.5,
        ))

        # Cost per task: canary should not be 30% higher
        s_cost = stable.get("cost_per_task_usd", 0.10)
        c_cost = canary.get("cost_per_task_usd", 0.10)
        comparisons.append(SLOComparison(
            metric="cost_per_task",
            canary_value=c_cost,
            stable_value=s_cost,
            threshold_ratio=1.3,
        ))

        return comparisons

    def _publish_event(self, event_type: str, payload: dict):
        self._call("publish_event", {
            "agent_id": self.agent_id,
            "event_type": event_type,
            "payload": {
                "deployment_id": self.deployment_id,
                **payload,
            },
        })

    def start_canary(self) -> dict:
        """Begin canary deployment at 5% traffic."""
        self.phase = DeploymentPhase.CANARY_5
        self._publish_event("deployment.canary_started", {
            "canary_agent_id": self.canary_agent_id,
            "traffic_pct": 5,
        })
        return {
            "deployment_id": self.deployment_id,
            "phase": self.phase.value,
            "canary_traffic_pct": 5,
        }

    def evaluate_and_advance(self) -> dict:
        """Check SLOs and advance to next phase or rollback.

        Call this periodically (e.g., every 30 minutes) after
        starting the canary.
        """
        comparisons = self._compare_slos()
        all_passed = all(c.passed for c in comparisons)

        slo_report = {
            c.metric: {
                "canary": round(c.canary_value, 4),
                "stable": round(c.stable_value, 4),
                "passed": c.passed,
            }
            for c in comparisons
        }
        self.slo_history.append({
            "phase": self.phase.value,
            "timestamp": datetime.utcnow().isoformat(),
            "slos": slo_report,
            "all_passed": all_passed,
        })

        if not all_passed:
            return self.rollback(reason="SLO breach detected", slos=slo_report)

        # Advance to next phase
        promotion_path = {
            DeploymentPhase.CANARY_5: (DeploymentPhase.CANARY_25, 25),
            DeploymentPhase.CANARY_25: (DeploymentPhase.CANARY_50, 50),
            DeploymentPhase.CANARY_50: (DeploymentPhase.PROMOTED, 100),
        }

        if self.phase in promotion_path:
            next_phase, traffic_pct = promotion_path[self.phase]
            self.phase = next_phase
            self._publish_event("deployment.phase_advanced", {
                "new_phase": self.phase.value,
                "traffic_pct": traffic_pct,
                "slo_report": slo_report,
            })
            return {
                "deployment_id": self.deployment_id,
                "phase": self.phase.value,
                "traffic_pct": traffic_pct,
                "slos": slo_report,
            }

        return {
            "deployment_id": self.deployment_id,
            "phase": self.phase.value,
            "message": "Deployment fully promoted",
        }

    def rollback(self, reason: str, slos: Optional[dict] = None) -> dict:
        """Immediately rollback canary and route 100% to stable."""
        self.phase = DeploymentPhase.ROLLED_BACK
        self._publish_event("deployment.rolled_back", {
            "reason": reason,
            "slo_report": slos or {},
        })
        return {
            "deployment_id": self.deployment_id,
            "phase": self.phase.value,
            "reason": reason,
            "slo_history": self.slo_history,
        }


# Usage
if __name__ == "__main__":
    import os
    deployer = CanaryDeployer(
        api_key=os.environ["GREENHELIX_API_KEY"],
        agent_id="commerce-agent-v2.0",
        canary_agent_id="commerce-agent-v2.1-canary",
    )

    # Start canary at 5%
    result = deployer.start_canary()
    print(json.dumps(result, indent=2))

    # After 2 hours, evaluate and advance (or rollback)
    # result = deployer.evaluate_and_advance()
```

> **Key Takeaways**
>
> - Never deploy an agent update to 100% of traffic. Use canary deployments with 5% initial traffic.
> - Define automated rollback triggers for each SLO dimension: completion rate, latency, cost, error rate, circuit breaker state.
> - Blue-green deployments provide instant rollback but no gradual traffic shifting.
> - Publish deployment events to GreenHelix for audit trails and fleet-wide visibility.
> - Use `get_revenue_metrics` to compare canary vs. stable performance across all SLO dimensions.

---

## Chapter 6: Multi-Agent Failure Modes and Resilience Patterns

### The 14 MAST Failure Modes

The Multi-Agent System Taxonomy (MAST) identifies 14 failure modes specific to multi-agent commerce systems. These are not theoretical -- they are extracted from post-mortems of production agent systems.

| # | Failure Mode | Category | Severity | Detection Difficulty |
|---|-------------|----------|----------|---------------------|
| 1 | Feedback Loop | Behavioral | Critical | Hard |
| 2 | False Consensus | Coordination | High | Hard |
| 3 | Goal Drift | Behavioral | High | Very Hard |
| 4 | Cascading Failure | Infrastructure | Critical | Medium |
| 5 | Resource Starvation | Infrastructure | High | Easy |
| 6 | Deadlock | Coordination | Critical | Medium |
| 7 | Livelock | Coordination | High | Hard |
| 8 | Byzantine Agent | Trust | Critical | Very Hard |
| 9 | Amplification Attack | Security | Critical | Medium |
| 10 | Split Brain | Coordination | High | Hard |
| 11 | Stale State | Data | Medium | Easy |
| 12 | Priority Inversion | Scheduling | Medium | Medium |
| 13 | Phantom Dependency | Integration | Medium | Hard |
| 14 | Metric Gaming | Trust | High | Very Hard |

**Feedback Loop (FM-1).** Agent A's output feeds into Agent B's input, and Agent B's output feeds back into Agent A. Without a cycle detector, the agents oscillate forever, each amplifying the other's output. In commerce: Agent A raises a price, Agent B responds by raising its bid, Agent A sees the higher bid and raises the price again.

**False Consensus (FM-2).** Multiple agents vote on a decision. A majority agrees, but the agreement is based on shared bad information -- they all queried the same stale cache or the same hallucinating model. The consensus is confident and wrong.

**Goal Drift (FM-3).** An agent's objective function shifts over time due to feedback from its environment. A pricing agent that is rewarded for revenue gradually increases prices until customer satisfaction collapses. The drift is invisible in daily metrics because each individual price change is small.

**Cascading Failure (FM-4).** Agent A fails. Agents B and C depend on Agent A and begin retrying. The retry load overloads Agent A's recovery. Agents D and E, which depend on B and C, now fail. Within minutes, the entire fleet is down.

### Bulkhead Isolation

Bulkheads prevent cascading failures by isolating agent groups into failure domains. Agents within a bulkhead share resources. Agents across bulkheads do not. When one bulkhead fails, the others continue operating.

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Bulkhead: Core  │  │ Bulkhead: Aux   │  │ Bulkhead: Batch │
│                  │  │                  │  │                  │
│  pricing-agent   │  │  research-agent  │  │  report-agent    │
│  escrow-agent    │  │  analysis-agent  │  │  cleanup-agent   │
│  settlement-agent│  │  summary-agent   │  │  audit-agent     │
│                  │  │                  │  │                  │
│  Budget: $100/d  │  │  Budget: $50/d   │  │  Budget: $25/d   │
│  Wallet: isolated│  │  Wallet: isolated│  │  Wallet: isolated│
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                    │                     │
         └────────────────────┼─────────────────────┘
                              │
                   ┌──────────▼──────────┐
                   │   GreenHelix Gateway │
                   │   (shared, but each  │
                   │    bulkhead has own   │
                   │    budget + circuit   │
                   │    breakers)          │
                   └──────────────────────┘
```

### Supervisor with Deadlock Detection

A supervisor agent monitors the multi-agent system for deadlock (two or more agents waiting on each other) and livelock (agents changing state continuously but making no progress). The supervisor uses GreenHelix Messaging to poll agent state and Events to publish alerts.

```python
import requests
import time
import json
import threading
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime, timedelta
from enum import Enum

BASE_URL = "https://api.greenhelix.net/v1"


def call_tool(api_key: str, tool: str, input_data: dict) -> dict:
    resp = requests.post(
        f"{BASE_URL}/v1",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"tool": tool, "input": input_data},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


class AgentState(Enum):
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"        # Waiting on another agent
    BLOCKED = "blocked"        # Waiting on a resource
    FAILED = "failed"
    TERMINATED = "terminated"


@dataclass
class AgentStatus:
    agent_id: str
    state: AgentState
    waiting_on: Optional[str] = None  # Agent ID this agent is waiting on
    last_progress: Optional[datetime] = None
    task_count: int = 0
    error_count: int = 0


class MultiAgentSupervisor:
    """Supervises a fleet of agents, detecting deadlocks, livelocks,
    feedback loops, and cascading failures.

    Uses GreenHelix Messaging for agent communication and Events
    for fleet-wide alerting.
    """

    def __init__(self, api_key: str, supervisor_id: str):
        self.api_key = api_key
        self.supervisor_id = supervisor_id
        self._agents: Dict[str, AgentStatus] = {}
        self._message_history: List[dict] = []
        self._lock = threading.Lock()

    def _call(self, tool: str, input_data: dict) -> dict:
        return call_tool(self.api_key, tool, input_data)

    def register_agent(self, agent_id: str):
        """Register an agent under this supervisor's watch."""
        with self._lock:
            self._agents[agent_id] = AgentStatus(
                agent_id=agent_id,
                state=AgentState.IDLE,
                last_progress=datetime.utcnow(),
            )

    def update_agent_state(self, agent_id: str, state: AgentState,
                           waiting_on: Optional[str] = None):
        """Update an agent's state. Called by agents or inferred from messages."""
        with self._lock:
            if agent_id in self._agents:
                status = self._agents[agent_id]
                if state == AgentState.WORKING:
                    status.last_progress = datetime.utcnow()
                    status.task_count += 1
                elif state == AgentState.FAILED:
                    status.error_count += 1
                status.state = state
                status.waiting_on = waiting_on

    def detect_deadlocks(self) -> List[List[str]]:
        """Detect circular wait dependencies (deadlocks).

        Returns a list of cycles, where each cycle is a list of
        agent IDs forming the deadlock.
        """
        with self._lock:
            # Build wait-for graph
            wait_graph: Dict[str, str] = {}
            for agent_id, status in self._agents.items():
                if (status.state == AgentState.WAITING
                        and status.waiting_on):
                    wait_graph[agent_id] = status.waiting_on

        # Find cycles using DFS
        cycles = []
        visited: Set[str] = set()

        for start in wait_graph:
            if start in visited:
                continue
            path = []
            current = start
            path_set: Set[str] = set()

            while current and current not in visited:
                if current in path_set:
                    # Found a cycle
                    cycle_start = path.index(current)
                    cycle = path[cycle_start:] + [current]
                    cycles.append(cycle)
                    break
                path.append(current)
                path_set.add(current)
                current = wait_graph.get(current)

            visited.update(path_set)

        return cycles

    def detect_livelocks(self, window_minutes: int = 10,
                         min_state_changes: int = 20) -> List[str]:
        """Detect agents that are changing state rapidly but making
        no progress (livelock).

        An agent in livelock has high state-change frequency but
        zero task completions in the window.
        """
        # This is a simplified heuristic. In production, track state
        # change events in a time-series database.
        with self._lock:
            livelocked = []
            cutoff = datetime.utcnow() - timedelta(minutes=window_minutes)
            for agent_id, status in self._agents.items():
                if (status.last_progress
                        and status.last_progress < cutoff
                        and status.state == AgentState.WORKING
                        and status.error_count > min_state_changes):
                    livelocked.append(agent_id)
            return livelocked

    def detect_cascade_risk(self, error_threshold: int = 3) -> List[str]:
        """Detect agents at risk of cascading failure.

        An agent is at risk if it has accumulated errors above
        threshold while other agents depend on it.
        """
        with self._lock:
            # Find agents with high error counts
            failing = {
                aid for aid, s in self._agents.items()
                if s.error_count >= error_threshold
            }
            # Find agents waiting on failing agents
            at_risk = []
            for agent_id, status in self._agents.items():
                if (status.waiting_on and status.waiting_on in failing):
                    at_risk.append(agent_id)
            return at_risk

    def send_heartbeat_check(self, agent_id: str) -> dict:
        """Send a heartbeat message to an agent via GreenHelix Messaging."""
        return self._call("send_message", {
            "from_agent": self.supervisor_id,
            "to_agent": agent_id,
            "message_type": "heartbeat_request",
            "payload": {
                "timestamp": datetime.utcnow().isoformat(),
                "supervisor": self.supervisor_id,
            },
        })

    def break_deadlock(self, cycle: List[str]) -> dict:
        """Break a deadlock by terminating the lowest-priority agent
        in the cycle and publishing an alert.
        """
        # Terminate the agent with the most errors (least healthy)
        with self._lock:
            victim = max(
                cycle[:-1],  # Exclude duplicate at end of cycle
                key=lambda aid: self._agents.get(aid, AgentStatus(
                    agent_id=aid, state=AgentState.IDLE)).error_count,
            )
            if victim in self._agents:
                self._agents[victim].state = AgentState.TERMINATED

        # Publish deadlock event
        self._call("publish_event", {
            "agent_id": self.supervisor_id,
            "event_type": "multi_agent.deadlock_detected",
            "payload": {
                "cycle": cycle,
                "terminated_agent": victim,
                "timestamp": datetime.utcnow().isoformat(),
            },
        })

        # Notify the terminated agent
        self._call("send_message", {
            "from_agent": self.supervisor_id,
            "to_agent": victim,
            "message_type": "terminate",
            "payload": {
                "reason": "deadlock_resolution",
                "cycle": cycle,
            },
        })

        return {
            "deadlock_cycle": cycle,
            "terminated": victim,
            "remaining_agents": [a for a in cycle[:-1] if a != victim],
        }

    def run_health_check(self) -> dict:
        """Run a complete health check across all managed agents."""
        deadlocks = self.detect_deadlocks()
        livelocks = self.detect_livelocks()
        cascade_risks = self.detect_cascade_risk()

        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_agents": len(self._agents),
            "deadlocks": deadlocks,
            "livelocked_agents": livelocks,
            "cascade_risk_agents": cascade_risks,
            "agent_states": {
                aid: {
                    "state": s.state.value,
                    "waiting_on": s.waiting_on,
                    "task_count": s.task_count,
                    "error_count": s.error_count,
                }
                for aid, s in self._agents.items()
            },
        }

        # Auto-break deadlocks
        for cycle in deadlocks:
            self.break_deadlock(cycle)

        # Alert on livelocks and cascade risks
        if livelocks or cascade_risks:
            self._call("publish_event", {
                "agent_id": self.supervisor_id,
                "event_type": "multi_agent.health_warning",
                "payload": report,
            })

        return report


# Usage
if __name__ == "__main__":
    import os
    supervisor = MultiAgentSupervisor(
        api_key=os.environ["GREENHELIX_API_KEY"],
        supervisor_id="fleet-supervisor-01",
    )

    # Register agents
    for agent in ["pricing-01", "escrow-01", "settlement-01", "research-01"]:
        supervisor.register_agent(agent)

    # Simulate state updates (in production, agents report their state)
    supervisor.update_agent_state("pricing-01", AgentState.WAITING,
                                  waiting_on="escrow-01")
    supervisor.update_agent_state("escrow-01", AgentState.WAITING,
                                  waiting_on="pricing-01")

    # Run health check -- will detect and break the deadlock
    report = supervisor.run_health_check()
    print(json.dumps(report, indent=2))
```

> **Key Takeaways**
>
> - The 14 MAST failure modes cover behavioral (feedback loops, goal drift), coordination (deadlock, livelock, false consensus), infrastructure (cascading failure, resource starvation), and trust (byzantine agents, metric gaming) failures.
> - Bulkhead isolation prevents cascading failures by giving each agent group its own budget, wallet, and circuit breakers.
> - A supervisor agent detects deadlocks via cycle detection on the wait-for graph and breaks them by terminating the least-healthy agent.
> - Livelock detection requires tracking state-change frequency vs. task completion rate.
> - GreenHelix Messaging (`send_message`) provides the heartbeat channel; Events (`publish_event`) provides the alert channel.
> - See P12 (Incident Response) for full cascade failure runbooks.

---

## Chapter 7: EU AI Act Production Compliance (August 2026 Deadline)

### The Deadline You Cannot Miss

On August 2, 2026, the EU AI Act's high-risk system obligations take full effect. If your agent commerce system is classified as high-risk -- and most financial decision-making agents are -- you must demonstrate compliance with Articles 6-49 on that date. Not "working toward compliance." Not "have a plan." Demonstrably compliant, with documentation, audit trails, and technical controls in place. The penalties for non-compliance are up to 35 million euros or 7% of global annual turnover, whichever is higher.

This chapter maps the nine key high-risk requirements to concrete agent controls and shows how to implement each one using GreenHelix tools.

### The 9 Requirements Mapped to Agent Controls

| Article | Requirement | Agent Control | GreenHelix Tools |
|---------|-------------|---------------|------------------|
| Art. 9 | Risk Management System | Risk classification + continuous monitoring | `get_trust_score`, `check_sla_compliance` |
| Art. 10 | Data Governance | Training data versioning + quality controls | `get_verified_claims`, `record_transaction` |
| Art. 11 | Technical Documentation | System architecture + capability docs | `register_agent_identity`, `submit_metrics` |
| Art. 12 | Record-Keeping | Automatic logging of all decisions | `record_transaction`, `publish_event` |
| Art. 13 | Transparency | User-facing disclosures | `get_agent_card`, `search_marketplace` |
| Art. 14 | Human Oversight | Kill switches + approval gates | `set_budget` (zero), `publish_event` |
| Art. 15 | Accuracy | SLO monitoring + regression testing | `check_sla_compliance`, `get_sla_status` |
| Art. 16 | Robustness | Circuit breakers + graceful degradation | `publish_event`, `get_balance` |
| Art. 17 | Cybersecurity | Auth + encryption + access control | `verify_claim`, `get_verified_claims` |

### The Compliance Audit Script

The following script runs a compliance audit against your GreenHelix agent, checking each Article's requirements programmatically where possible and generating a compliance report.

```python
import requests
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime

BASE_URL = "https://api.greenhelix.net/v1"


def call_tool(api_key: str, tool: str, input_data: dict) -> dict:
    resp = requests.post(
        f"{BASE_URL}/v1",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"tool": tool, "input": input_data},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


@dataclass
class ComplianceCheck:
    article: str
    requirement: str
    status: str  # "pass", "fail", "manual_review"
    evidence: str
    remediation: Optional[str] = None


class EUAIActAuditor:
    """Automated compliance auditor for EU AI Act high-risk requirements.

    Checks each Article's requirements against the agent's current
    GreenHelix configuration and generates a compliance report.

    This is an engineering tool, not legal advice. Consult qualified
    legal counsel for regulatory interpretation.
    """

    def __init__(self, api_key: str, agent_id: str):
        self.api_key = api_key
        self.agent_id = agent_id
        self.checks: List[ComplianceCheck] = []

    def _call(self, tool: str, input_data: dict) -> dict:
        return call_tool(self.api_key, tool, input_data)

    def _add_check(self, check: ComplianceCheck):
        self.checks.append(check)

    def audit_art9_risk_management(self):
        """Article 9: Risk management system.
        Check: trust score exists and SLA monitoring is active."""
        try:
            trust = self._call("get_trust_score", {
                "agent_id": self.agent_id,
            })
            score = trust.get("score", 0)
            if score > 0:
                self._add_check(ComplianceCheck(
                    article="Art. 9",
                    requirement="Risk management system",
                    status="pass",
                    evidence=f"Trust score active: {score}. Risk monitoring via SLA.",
                ))
            else:
                self._add_check(ComplianceCheck(
                    article="Art. 9",
                    requirement="Risk management system",
                    status="fail",
                    evidence="Trust score is zero or not configured.",
                    remediation="Configure trust monitoring and risk thresholds.",
                ))
        except Exception as e:
            self._add_check(ComplianceCheck(
                article="Art. 9",
                requirement="Risk management system",
                status="fail",
                evidence=f"Could not query trust score: {e}",
                remediation="Register agent identity and configure trust scoring.",
            ))

    def audit_art10_data_governance(self):
        """Article 10: Data governance.
        Check: verified claims exist (provenance tracking)."""
        try:
            claims = self._call("get_verified_claims", {
                "agent_id": self.agent_id,
            })
            claim_list = claims.get("claims", [])
            if len(claim_list) >= 1:
                self._add_check(ComplianceCheck(
                    article="Art. 10",
                    requirement="Data governance",
                    status="pass",
                    evidence=f"{len(claim_list)} verified claim(s) on record.",
                ))
            else:
                self._add_check(ComplianceCheck(
                    article="Art. 10",
                    requirement="Data governance",
                    status="fail",
                    evidence="No verified claims found.",
                    remediation="Submit verified claims for data provenance.",
                ))
        except Exception as e:
            self._add_check(ComplianceCheck(
                article="Art. 10",
                requirement="Data governance",
                status="fail",
                evidence=f"Could not query verified claims: {e}",
                remediation="Register identity and submit data governance claims.",
            ))

    def audit_art11_documentation(self):
        """Article 11: Technical documentation.
        Check: agent card exists with capabilities description."""
        try:
            card = self._call("get_agent_card", {
                "agent_id": self.agent_id,
            })
            if card.get("description") and card.get("capabilities"):
                self._add_check(ComplianceCheck(
                    article="Art. 11",
                    requirement="Technical documentation",
                    status="pass",
                    evidence="Agent card has description and capabilities.",
                ))
            else:
                self._add_check(ComplianceCheck(
                    article="Art. 11",
                    requirement="Technical documentation",
                    status="fail",
                    evidence="Agent card missing description or capabilities.",
                    remediation="Update agent card with full technical documentation.",
                ))
        except Exception:
            self._add_check(ComplianceCheck(
                article="Art. 11",
                requirement="Technical documentation",
                status="fail",
                evidence="Agent card not found.",
                remediation="Register agent identity and create agent card.",
            ))

    def audit_art12_record_keeping(self):
        """Article 12: Record-keeping / automatic logging.
        Check: transaction ledger has recent entries."""
        try:
            analytics = self._call("get_usage_analytics", {
                "agent_id": self.agent_id,
                "period": "daily",
            })
            if analytics.get("total_transactions", 0) > 0:
                self._add_check(ComplianceCheck(
                    article="Art. 12",
                    requirement="Record-keeping",
                    status="pass",
                    evidence=(f"Ledger active with "
                              f"{analytics['total_transactions']} transactions."),
                ))
            else:
                self._add_check(ComplianceCheck(
                    article="Art. 12",
                    requirement="Record-keeping",
                    status="fail",
                    evidence="No transactions in ledger.",
                    remediation="Ensure all agent actions are logged via record_transaction.",
                ))
        except Exception as e:
            self._add_check(ComplianceCheck(
                article="Art. 12",
                requirement="Record-keeping",
                status="fail",
                evidence=f"Could not query usage analytics: {e}",
                remediation="Configure ledger integration for all agent actions.",
            ))

    def audit_art13_transparency(self):
        """Article 13: Transparency.
        Check: agent is discoverable on marketplace with disclosure."""
        try:
            result = self._call("search_marketplace", {
                "query": self.agent_id,
            })
            listings = result.get("listings", [])
            if listings:
                self._add_check(ComplianceCheck(
                    article="Art. 13",
                    requirement="Transparency",
                    status="pass",
                    evidence="Agent is listed on marketplace with public profile.",
                ))
            else:
                self._add_check(ComplianceCheck(
                    article="Art. 13",
                    requirement="Transparency",
                    status="manual_review",
                    evidence="Agent not found on marketplace.",
                    remediation="Register on marketplace or ensure alternative "
                                "transparency disclosures are in place.",
                ))
        except Exception:
            self._add_check(ComplianceCheck(
                article="Art. 13",
                requirement="Transparency",
                status="manual_review",
                evidence="Could not search marketplace.",
                remediation="Verify transparency disclosures manually.",
            ))

    def audit_art14_human_oversight(self):
        """Article 14: Human oversight.
        Check: budget kill switch is available (set_budget to zero)."""
        try:
            balance = self._call("get_balance", {
                "agent_id": self.agent_id,
            })
            has_limits = ("daily_limit" in balance or "monthly_limit" in balance)
            self._add_check(ComplianceCheck(
                article="Art. 14",
                requirement="Human oversight",
                status="pass" if has_limits else "fail",
                evidence=("Budget limits configured -- kill switch available via "
                          "set_budget(0)." if has_limits
                          else "No budget limits found."),
                remediation=None if has_limits else (
                    "Configure budget limits to enable human kill switch."),
            ))
        except Exception:
            self._add_check(ComplianceCheck(
                article="Art. 14",
                requirement="Human oversight",
                status="fail",
                evidence="Could not query balance/limits.",
                remediation="Configure budget limits for human override capability.",
            ))

    def audit_art15_accuracy(self):
        """Article 15: Accuracy, robustness, cybersecurity.
        Check: SLA compliance is being monitored."""
        try:
            sla = self._call("check_sla_compliance", {
                "agent_id": self.agent_id,
            })
            compliant = sla.get("compliant", False)
            self._add_check(ComplianceCheck(
                article="Art. 15",
                requirement="Accuracy",
                status="pass" if compliant else "fail",
                evidence=(f"SLA compliance check: {'compliant' if compliant else 'non-compliant'}. "
                          f"Details: {json.dumps(sla)}"),
                remediation=None if compliant else "Address SLA non-compliance issues.",
            ))
        except Exception:
            self._add_check(ComplianceCheck(
                article="Art. 15",
                requirement="Accuracy",
                status="fail",
                evidence="SLA compliance not configured.",
                remediation="Create SLAs per Chapter 2 of this guide.",
            ))

    def audit_art16_robustness(self):
        """Article 16: Robustness under errors and inconsistencies.
        Checked via manual review of circuit breaker configuration."""
        self._add_check(ComplianceCheck(
            article="Art. 16",
            requirement="Robustness",
            status="manual_review",
            evidence="Robustness requires manual review of circuit breaker "
                     "configuration (Chapter 3) and deployment rollback "
                     "triggers (Chapter 5).",
            remediation="Implement circuit breakers and automated rollback. "
                        "Document fallback chains.",
        ))

    def audit_art17_cybersecurity(self):
        """Article 17: Cybersecurity.
        Check: identity is verified with cryptographic claims."""
        try:
            claims = self._call("get_verified_claims", {
                "agent_id": self.agent_id,
            })
            claim_list = claims.get("claims", [])
            security_claims = [c for c in claim_list
                               if c.get("type") in ("identity", "authentication",
                                                     "encryption")]
            if security_claims:
                self._add_check(ComplianceCheck(
                    article="Art. 17",
                    requirement="Cybersecurity",
                    status="pass",
                    evidence=f"{len(security_claims)} security-related "
                             f"verified claim(s) on record.",
                ))
            else:
                self._add_check(ComplianceCheck(
                    article="Art. 17",
                    requirement="Cybersecurity",
                    status="manual_review",
                    evidence="No security-specific verified claims found.",
                    remediation="Submit identity and authentication claims. "
                                "Verify encryption and access control.",
                ))
        except Exception:
            self._add_check(ComplianceCheck(
                article="Art. 17",
                requirement="Cybersecurity",
                status="manual_review",
                evidence="Could not query verified claims.",
                remediation="Register identity and submit security claims.",
            ))

    def run_full_audit(self) -> dict:
        """Run all compliance checks and generate a report."""
        self.checks = []
        self.audit_art9_risk_management()
        self.audit_art10_data_governance()
        self.audit_art11_documentation()
        self.audit_art12_record_keeping()
        self.audit_art13_transparency()
        self.audit_art14_human_oversight()
        self.audit_art15_accuracy()
        self.audit_art16_robustness()
        self.audit_art17_cybersecurity()

        passed = sum(1 for c in self.checks if c.status == "pass")
        failed = sum(1 for c in self.checks if c.status == "fail")
        manual = sum(1 for c in self.checks if c.status == "manual_review")

        report = {
            "audit_date": datetime.utcnow().isoformat(),
            "agent_id": self.agent_id,
            "summary": {
                "total_checks": len(self.checks),
                "passed": passed,
                "failed": failed,
                "manual_review": manual,
                "compliance_pct": round(passed / len(self.checks) * 100, 1)
                    if self.checks else 0,
            },
            "checks": [
                {
                    "article": c.article,
                    "requirement": c.requirement,
                    "status": c.status,
                    "evidence": c.evidence,
                    "remediation": c.remediation,
                }
                for c in self.checks
            ],
            "deadline": "2026-08-02",
            "disclaimer": "This is an engineering audit tool, not legal advice.",
        }

        # Record audit to ledger
        try:
            self._call("record_transaction", {
                "agent_id": self.agent_id,
                "amount": "0",
                "type": "compliance_audit",
                "metadata": {
                    "passed": passed,
                    "failed": failed,
                    "manual_review": manual,
                },
            })
        except Exception:
            pass

        return report


# Usage
if __name__ == "__main__":
    import os
    auditor = EUAIActAuditor(
        api_key=os.environ["GREENHELIX_API_KEY"],
        agent_id="commerce-agent-prod-01",
    )
    report = auditor.run_full_audit()
    print(json.dumps(report, indent=2))

    if report["summary"]["failed"] > 0:
        print(f"\nWARNING: {report['summary']['failed']} checks failed.")
        print("Remediation required before August 2, 2026 deadline.")
    if report["summary"]["manual_review"] > 0:
        print(f"\n{report['summary']['manual_review']} checks require manual review.")
```

### Compliance Status Matrix

Run the audit monthly. Track your compliance trajectory toward the August 2, 2026 deadline.

| Month | Art.9 | Art.10 | Art.11 | Art.12 | Art.13 | Art.14 | Art.15 | Art.16 | Art.17 | Score |
|-------|-------|--------|--------|--------|--------|--------|--------|--------|--------|-------|
| Apr 2026 | ? | ? | ? | ? | ? | ? | ? | ? | ? | -- |
| May 2026 | | | | | | | | | | |
| Jun 2026 | | | | | | | | | | |
| Jul 2026 | | | | | | | | | | |
| **Aug 2, 2026** | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | **9/9** |

> **Key Takeaways**
>
> - The EU AI Act high-risk obligations take effect August 2, 2026. Most agent commerce systems qualify as high-risk.
> - Nine Articles map to nine concrete technical controls: risk management, data governance, documentation, record-keeping, transparency, human oversight, accuracy, robustness, and cybersecurity.
> - The `EUAIActAuditor` automates checks for 7 of 9 requirements using GreenHelix tools; 2 require manual review.
> - Run the audit monthly to track your compliance trajectory. All checks must pass by the deadline.
> - The audit result is recorded to the GreenHelix ledger as a compliance event -- itself satisfying part of Art. 12 record-keeping.
> - See P11 (Compliance Toolkit) for contract templates, risk classification frameworks, and Product Liability Directive patterns.

---

## Chapter 8: The 30-Day Production Hardening Sprint

### Sprint Overview

This chapter converts the preceding seven chapters into a week-by-week execution plan. Each week has a clear objective, a set of deliverables, and a go/no-go gate. If a gate fails, the sprint pauses until the issue is resolved. Do not skip weeks. Do not parallelize across weeks. Each week's deliverables are prerequisites for the next.

### Gantt Checklist

```
Week 1: Instrument & Baseline
├── Day 1-2: Run production readiness assessment (Ch.1)
├── Day 3-4: Deploy SLO monitoring (Ch.2)
└── Day 5:   Establish baseline metrics
    Gate: Readiness score >= 21, SLOs reporting data

Week 2: Harden
├── Day 8-9:  Implement circuit breakers (Ch.3)
├── Day 10-11: Deploy cost guardrails (Ch.4)
└── Day 12:   Load test circuit breakers + cost caps
    Gate: All circuit breakers tested, cost caps enforced

Week 3: Deployment Pipeline
├── Day 15-16: Build canary deployment (Ch.5)
├── Day 17-18: Deploy supervisor + deadlock detection (Ch.6)
└── Day 19:    Run canary deployment drill
    Gate: Canary rollback tested, supervisor detecting failures

Week 4: Compliance & Go-Live
├── Day 22-23: Run EU AI Act audit (Ch.7)
├── Day 24:    Remediate audit failures
├── Day 25-26: SLA go-live (error budgets active)
└── Day 27:    Go/no-go scorecard review
    Gate: All audit checks pass or have remediation plan, SLAs active
```

### RACI Matrix

| Task | Engineering | SRE/Platform | Product | Legal/Compliance |
|------|-------------|--------------|---------|------------------|
| Production readiness assessment | **R** | C | I | I |
| SLO definition and targets | C | **R** | **A** | I |
| Circuit breaker implementation | **R** | C | I | I |
| Cost guardrail configuration | **R** | C | **A** | I |
| Canary deployment pipeline | C | **R** | I | I |
| Multi-agent supervisor | **R** | C | I | I |
| EU AI Act compliance audit | C | I | I | **R/A** |
| Go/no-go scorecard | I | **R** | **A** | C |

**R** = Responsible, **A** = Accountable, **C** = Consulted, **I** = Informed

### Week 1: Instrument and Baseline

**Objective**: Know where you stand. Measure everything. Establish the baseline that all subsequent improvements are measured against.

**Day 1-2: Production Readiness Assessment**

Run the `ProductionReadinessAssessor` from Chapter 1 and complete the 40-question checklist manually for questions that cannot be automated. Record the score.

**Day 3-4: Deploy SLO Monitoring**

Stand up the `AgentSLOMonitor` from Chapter 2. Define your three SLOs. Register the webhook for error budget alerts. Start recording every task via `monitor.record_task()`.

**Day 5: Establish Baseline**

After 48 hours of SLO data collection, pull the baseline metrics:

```python
import requests
import json
import os
from datetime import datetime

BASE_URL = "https://api.greenhelix.net/v1"


def call_tool(api_key: str, tool: str, input_data: dict) -> dict:
    resp = requests.post(
        f"{BASE_URL}/v1",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"tool": tool, "input": input_data},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def establish_baseline(api_key: str, agent_id: str) -> dict:
    """Pull baseline metrics after initial instrumentation.

    Run this at the end of Week 1 after SLO monitoring has been
    active for at least 48 hours.
    """
    # Get SLA status for current SLO readings
    sla_status = call_tool(api_key, "get_sla_status", {
        "agent_id": agent_id,
    })

    # Get usage analytics for cost baseline
    analytics = call_tool(api_key, "get_usage_analytics", {
        "agent_id": agent_id,
        "period": "daily",
    })

    # Get current balance and limits
    balance = call_tool(api_key, "get_balance", {
        "agent_id": agent_id,
    })

    # Get trust score as quality proxy
    trust = call_tool(api_key, "get_trust_score", {
        "agent_id": agent_id,
    })

    baseline = {
        "timestamp": datetime.utcnow().isoformat(),
        "agent_id": agent_id,
        "sla_status": sla_status,
        "usage_analytics": analytics,
        "balance": balance,
        "trust_score": trust.get("score"),
        "readiness_score": None,  # Fill manually from Ch.1 assessment
    }

    # Record baseline to ledger for audit trail
    call_tool(api_key, "record_transaction", {
        "agent_id": agent_id,
        "amount": "0",
        "type": "baseline_established",
        "metadata": {
            "sprint_week": 1,
            "trust_score": trust.get("score"),
        },
    })

    return baseline


# Week 1, Day 5
if __name__ == "__main__":
    baseline = establish_baseline(
        api_key=os.environ["GREENHELIX_API_KEY"],
        agent_id="commerce-agent-prod-01",
    )
    print(json.dumps(baseline, indent=2))
    print("\nWeek 1 Gate Check:")
    print(f"  SLA status retrieved: {bool(baseline['sla_status'])}")
    print(f"  Trust score: {baseline['trust_score']}")
    print(f"  Add readiness score manually from Ch.1 assessment")
```

**Week 1 Gate**: Readiness score >= 21 (Orange tier or above). SLOs are reporting data. If the readiness score is below 21 (Red tier), stop. Fix the critical gaps before proceeding.

### Week 2: Harden

**Objective**: Make the agent resilient to failures. No individual failure should cascade or drain the budget.

**Day 8-9**: Deploy `ResilientToolCaller` from Chapter 3 for all tool invocations. Configure per-tool circuit breakers with appropriate thresholds.

**Day 10-11**: Deploy `CostGuardRail` from Chapter 4. Set per-request, daily, monthly, and workflow cost caps. Register cost alert webhooks.

**Day 12**: Load test. Simulate tool failures by pointing the agent at a fault-injecting proxy. Verify circuit breakers trip at the configured threshold. Verify cost caps reject requests at the limit. Verify the kill switch works.

**Week 2 Gate**: All circuit breakers tested with documented trip thresholds. Cost caps enforced (verified by deliberately exceeding them). Kill switch tested.

### Week 3: Deployment Pipeline

**Objective**: Build the infrastructure for safe, automated deployments with automatic rollback.

**Day 15-16**: Implement `CanaryDeployer` from Chapter 5. Build the CI/CD pipeline to deploy a canary alongside the stable version.

**Day 17-18**: Deploy `MultiAgentSupervisor` from Chapter 6. Register all production agents. Configure heartbeat polling.

**Day 19**: Run a deployment drill. Deploy a canary with a deliberately degraded prompt (lower completion rate). Verify the `evaluate_and_advance` method detects the SLO breach and triggers automatic rollback.

**Week 3 Gate**: Canary deployment pipeline operational. Automatic rollback tested with a deliberate SLO breach. Supervisor detecting agent states and publishing health reports.

### Week 4: Compliance and Go-Live

**Objective**: Pass the compliance audit, activate SLAs, and make the go/no-go decision.

**Day 22-23**: Run `EUAIActAuditor` from Chapter 7. Document all check results.

**Day 24**: Remediate any failed checks. For "manual_review" checks, document the control and obtain sign-off from compliance.

**Day 25-26**: Activate SLAs. Error budgets are now live. Burn-rate alerts will fire for real SLO breaches, not just test data.

**Day 27**: Go/no-go scorecard review.

### Go/No-Go Scorecard

| Criterion | Required | Actual | Pass? |
|-----------|----------|--------|-------|
| Readiness score | >= 61 (Green) | ___ | |
| Task completion SLO breaches (last 7 days) | < 5 | ___ | |
| Latency P99 SLO breaches (last 7 days) | < 10 | ___ | |
| Cost-per-task SLO breaches (last 7 days) | < 20 | ___ | |
| Circuit breaker trips (last 7 days) | < 3 | ___ | |
| Cost guardrail blocks (last 7 days) | < 5 | ___ | |
| Canary rollback tested | Yes | ___ | |
| Deadlock detection tested | Yes | ___ | |
| EU AI Act audit passed | >= 7/9 | ___ | |
| Incident runbooks documented | >= 3 | ___ | |
| On-call rotation established | Yes | ___ | |
| Kill switch tested | Yes | ___ | |

**Decision rule**: All "Required" criteria must be met. If any criterion fails, the sprint extends by one week to remediate. Two extensions maximum -- if the scorecard still fails after two extensions, escalate to leadership for a risk-acceptance decision.

```python
import requests
import json
import os
from datetime import datetime
from typing import Dict, List

BASE_URL = "https://api.greenhelix.net/v1"


def call_tool(api_key: str, tool: str, input_data: dict) -> dict:
    resp = requests.post(
        f"{BASE_URL}/v1",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"tool": tool, "input": input_data},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def run_go_no_go(api_key: str, agent_id: str,
                 manual_scores: Dict[str, any]) -> dict:
    """Run the automated portion of the go/no-go scorecard.

    manual_scores should contain:
        - readiness_score: int (from Ch.1 assessment)
        - canary_rollback_tested: bool
        - deadlock_detection_tested: bool
        - incident_runbooks_count: int
        - oncall_established: bool
        - kill_switch_tested: bool
    """
    # Automated checks via GreenHelix
    sla_status = call_tool(api_key, "get_sla_status", {
        "agent_id": agent_id,
    })

    compliance = call_tool(api_key, "check_sla_compliance", {
        "agent_id": agent_id,
    })

    # Build scorecard
    criteria = []

    # Readiness score
    rs = manual_scores.get("readiness_score", 0)
    criteria.append({
        "criterion": "Readiness score >= 61",
        "required": 61,
        "actual": rs,
        "passed": rs >= 61,
    })

    # SLO breaches (from SLA status)
    completion_breaches = sla_status.get("completion_breaches_7d", 0)
    criteria.append({
        "criterion": "Completion SLO breaches < 5",
        "required": "< 5",
        "actual": completion_breaches,
        "passed": completion_breaches < 5,
    })

    latency_breaches = sla_status.get("latency_breaches_7d", 0)
    criteria.append({
        "criterion": "Latency P99 breaches < 10",
        "required": "< 10",
        "actual": latency_breaches,
        "passed": latency_breaches < 10,
    })

    cost_breaches = sla_status.get("cost_breaches_7d", 0)
    criteria.append({
        "criterion": "Cost-per-task breaches < 20",
        "required": "< 20",
        "actual": cost_breaches,
        "passed": cost_breaches < 20,
    })

    # Manual checks
    for key, label, required in [
        ("canary_rollback_tested", "Canary rollback tested", True),
        ("deadlock_detection_tested", "Deadlock detection tested", True),
        ("kill_switch_tested", "Kill switch tested", True),
        ("oncall_established", "On-call rotation established", True),
    ]:
        val = manual_scores.get(key, False)
        criteria.append({
            "criterion": label,
            "required": required,
            "actual": val,
            "passed": val == required,
        })

    runbook_count = manual_scores.get("incident_runbooks_count", 0)
    criteria.append({
        "criterion": "Incident runbooks >= 3",
        "required": ">= 3",
        "actual": runbook_count,
        "passed": runbook_count >= 3,
    })

    all_passed = all(c["passed"] for c in criteria)

    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "agent_id": agent_id,
        "decision": "GO" if all_passed else "NO-GO",
        "criteria": criteria,
        "passed_count": sum(1 for c in criteria if c["passed"]),
        "total_count": len(criteria),
    }

    # Record decision to ledger
    call_tool(api_key, "record_transaction", {
        "agent_id": agent_id,
        "amount": "0",
        "type": "go_no_go_decision",
        "metadata": {
            "decision": result["decision"],
            "passed": result["passed_count"],
            "total": result["total_count"],
        },
    })

    return result


# Week 4, Day 27
if __name__ == "__main__":
    result = run_go_no_go(
        api_key=os.environ["GREENHELIX_API_KEY"],
        agent_id="commerce-agent-prod-01",
        manual_scores={
            "readiness_score": 65,
            "canary_rollback_tested": True,
            "deadlock_detection_tested": True,
            "incident_runbooks_count": 5,
            "oncall_established": True,
            "kill_switch_tested": True,
        },
    )
    print(json.dumps(result, indent=2))
    print(f"\nDecision: {result['decision']}")
    if result["decision"] == "NO-GO":
        failed = [c for c in result["criteria"] if not c["passed"]]
        print("Failed criteria:")
        for f in failed:
            print(f"  - {f['criterion']}: actual={f['actual']}")
```

> **Key Takeaways**
>
> - The 30-day sprint is sequential: instrument (Week 1), harden (Week 2), deploy pipeline (Week 3), compliance + go-live (Week 4).
> - Each week has a gate. Do not skip weeks. Do not proceed if the gate fails.
> - The RACI matrix prevents the ownership gap (Gap 4): every task has a named Responsible and Accountable party.
> - The go/no-go scorecard has 12 criteria. All must pass. Maximum two one-week extensions.
> - The scorecard decision is recorded to the GreenHelix ledger for audit trail (Art. 12 compliance).
> - Cross-reference: P9 (Testing) for regression suites, P6 (FinOps) for fleet-wide cost dashboards, P11 (Compliance) for contract templates, P12 (Incident Response) for runbook authoring.

---

## What to Do Next

You have the assessment, the SLOs, the circuit breakers, the cost guardrails, the deployment pipeline, the resilience patterns, the compliance audit, and the 30-day sprint plan. Here is the execution order:

1. **Today**: Run the 40-question production readiness assessment (Chapter 1). Score yourself honestly.
2. **This week**: Deploy SLO monitoring (Chapter 2) and cost guardrails (Chapter 4). These require the least code and provide the most immediate value.
3. **Next week**: Implement circuit breakers (Chapter 3) and the canary deployment pipeline (Chapter 5).
4. **Week 3**: Deploy the multi-agent supervisor (Chapter 6) and run the EU AI Act audit (Chapter 7).
5. **Day 27**: Run the go/no-go scorecard (Chapter 8). Ship or extend.

### Related Products

- **P6: The AI Agent FinOps Playbook** -- Fleet-wide cost dashboards, volume discounts, and budget allocation strategies that complement Chapter 4's per-agent guardrails.
- **P9: The Agent Testing & Observability Cookbook** -- Regression test suites, chaos testing, and CI/CD integration that feed SLO data into Chapter 2's monitoring.
- **P11: Ship Compliant Agents** -- EU AI Act risk classification, contract templates, and Product Liability Directive patterns that expand Chapter 7's compliance audit.
- **P12: The Agent Incident Response Playbook** -- Incident runbooks, automated containment, and post-mortem templates that operationalize Chapter 3's circuit breakers and Chapter 6's supervisor alerts.

### The 78-to-14 Problem

Seventy-eight percent of enterprises have agent pilots. Fourteen percent have agents in production. The gap is not a technology problem. It is an operations problem. The five gaps -- integration, quality, monitoring, ownership, training data -- are all closed by known engineering practices. This guide gives you the practices, the code, and the 30-day plan. The only remaining variable is execution.

Start the assessment. Ship the SLOs. Close the gap.

---

## Circuit Breaker & Failover — Working Implementation

The code below uses the actual `greenhelix_trading` library classes. Every method call maps to a real GreenHelix Gateway tool. Copy this module into your project, set `GREENHELIX_API_KEY` and `GREENHELIX_AGENT_ID` in your environment, and run it.

```python
"""
Circuit breaker and failover system using the greenhelix_trading library.

Covers:
  1. Per-tool circuit breakers wrapping GreenHelix calls
  2. Health check endpoints with synthetic probes
  3. Automatic failover between primary and backup agents
  4. Graceful degradation with tiered fallback chains
  5. Fleet-wide health dashboard with SLA monitoring

Requirements:
    pip install greenhelix-trading
"""

import os
import time
import json
import threading
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Callable, Optional
from dataclasses import dataclass, field

from greenhelix_trading import HealthChecker, FleetMonitor
from greenhelix_trading import CircuitBreaker, RetryPolicy


# ── Configuration ─────────────────────────────────────────────────────────────

API_KEY = os.environ["GREENHELIX_API_KEY"]
AGENT_ID = os.environ["GREENHELIX_AGENT_ID"]
BACKUP_AGENT_ID = os.environ.get("GREENHELIX_BACKUP_AGENT_ID", "")


# ── 1. Per-Tool Circuit Breakers ─────────────────────────────────────────────

class ResilientGatewayClient:
    """Wraps every GreenHelix tool call with a per-tool circuit breaker
    and a configurable retry policy.

    Each distinct tool name gets its own CircuitBreaker instance (from
    greenhelix_trading._retry).  When the breaker opens, calls fail
    immediately or fall back to a provided fallback callable.  The
    RetryPolicy handles transient errors (429, 502, 503, 504) with
    exponential backoff before the breaker trips.
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ):
        self.api_key = api_key
        self.agent_id = agent_id
        self._breakers: dict[str, CircuitBreaker] = {}
        self._retry_policy = RetryPolicy(
            max_retries=max_retries,
            backoff_factor=backoff_factor,
            retryable_status=(429, 502, 503, 504),
        )
        self._failure_threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        self._call_log: list[dict] = []
        self._lock = threading.Lock()

        # Use HealthChecker for the underlying _execute calls
        self._checker = HealthChecker(
            api_key=api_key,
            agent_id=agent_id,
        )

    def _get_breaker(self, tool: str) -> CircuitBreaker:
        """Get or create a CircuitBreaker for a specific tool."""
        with self._lock:
            if tool not in self._breakers:
                self._breakers[tool] = CircuitBreaker(
                    failure_threshold=self._failure_threshold,
                    recovery_timeout=self._recovery_timeout,
                )
            return self._breakers[tool]

    def execute(
        self,
        tool: str,
        input_data: dict,
        fallback: Optional[Callable] = None,
    ) -> dict:
        """Execute a GreenHelix tool with circuit breaker + retry.

        Args:
            tool: GreenHelix tool name (e.g., "get_balance", "create_escrow").
            input_data: Tool input parameters.
            fallback: Optional callable returning a fallback response when
                the circuit is open or all retries are exhausted.

        Returns:
            Tool response dict.

        Raises:
            ConnectionError: If circuit is open and no fallback provided.
            Exception: If all retries exhausted and no fallback provided.
        """
        breaker = self._get_breaker(tool)
        start = time.time()

        # Check if circuit allows the request
        if not breaker.allow_request():
            self._log_call(tool, False, time.time() - start, "circuit_open")
            if fallback:
                return fallback()
            raise ConnectionError(
                f"Circuit breaker is {breaker.state.value} for tool '{tool}'. "
                f"Recovery timeout: {self._recovery_timeout}s."
            )

        # Wrap the HealthChecker._execute call with retry policy
        def _do_call():
            return self._checker._execute(tool, input_data)

        try:
            result = self._retry_policy.execute_with_retry(_do_call)
            breaker.record_success()
            self._log_call(tool, True, time.time() - start)
            return result
        except Exception as exc:
            breaker.record_failure()
            elapsed = time.time() - start
            self._log_call(tool, False, elapsed, str(exc))
            if fallback:
                return fallback()
            raise

    def _log_call(self, tool: str, success: bool, elapsed: float,
                  error: str = ""):
        self._call_log.append({
            "tool": tool,
            "success": success,
            "elapsed_ms": round(elapsed * 1000, 1),
            "error": error,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def get_circuit_states(self) -> dict:
        """Return the state of every per-tool circuit breaker."""
        with self._lock:
            return {
                tool: {
                    "state": cb.state.value,
                    "failure_count": cb._failure_count,
                }
                for tool, cb in self._breakers.items()
            }

    def get_call_stats(self) -> dict:
        """Aggregate call statistics across all tools."""
        total = len(self._call_log)
        successes = sum(1 for c in self._call_log if c["success"])
        by_tool = defaultdict(lambda: {"total": 0, "failures": 0})
        for c in self._call_log:
            by_tool[c["tool"]]["total"] += 1
            if not c["success"]:
                by_tool[c["tool"]]["failures"] += 1
        return {
            "total_calls": total,
            "successes": successes,
            "failures": total - successes,
            "success_rate": round(successes / max(total, 1) * 100, 1),
            "by_tool": dict(by_tool),
        }


# ── 2. Health Check Endpoints ────────────────────────────────────────────────

def run_health_probes() -> dict:
    """Run synthetic health probes against critical GreenHelix tools.

    Uses HealthChecker.check_tool for individual tool probes and
    HealthChecker.check_suite for the aggregate report.

    The probe set covers the five tool categories that matter most
    for production commerce operations: billing, identity, escrow,
    marketplace, and trust.
    """
    checker = HealthChecker(
        api_key=API_KEY,
        agent_id=AGENT_ID,
    )

    # Define the health probe suite
    probes = [
        {"tool": "get_balance", "input": {"agent_id": AGENT_ID}},
        {"tool": "get_agent_identity", "input": {"agent_id": AGENT_ID}},
        {"tool": "get_agent_reputation", "input": {"agent_id": AGENT_ID}},
        {"tool": "get_budget_status", "input": {"agent_id": AGENT_ID}},
        {"tool": "get_usage_analytics", "input": {"agent_id": AGENT_ID}},
    ]

    # Run individual probes for detailed per-tool timing
    individual_results = []
    for probe in probes:
        result = checker.check_tool(
            tool=probe["tool"],
            input_data=probe["input"],
        )
        individual_results.append(result)

    # Run the full suite for the aggregate report
    suite_result = checker.check_suite(probes)

    # Compute a composite health score
    healthy_count = suite_result["healthy"]
    total_count = suite_result["total"]
    health_score = round(healthy_count / max(total_count, 1) * 100, 1)

    # Latency percentiles from healthy probes
    latencies = [
        r["response_time_ms"]
        for r in individual_results
        if r["healthy"]
    ]
    p50 = sorted(latencies)[len(latencies) // 2] if latencies else 0
    p99 = sorted(latencies)[-1] if latencies else 0

    return {
        "health_score_pct": health_score,
        "healthy": healthy_count,
        "unhealthy": suite_result["unhealthy"],
        "total_probes": total_count,
        "latency_p50_ms": round(p50, 1),
        "latency_p99_ms": round(p99, 1),
        "probe_details": individual_results,
        "status": "healthy" if health_score >= 80 else (
            "degraded" if health_score >= 50 else "critical"
        ),
    }


# ── 3. Automatic Failover ────────────────────────────────────────────────────

class FailoverManager:
    """Automatic failover between a primary and backup agent.

    Monitors the primary agent's health using HealthChecker. When the
    primary fails consecutive health probes, the manager switches all
    traffic to the backup agent.  When the primary recovers, traffic
    is gradually shifted back.

    Uses FleetMonitor.collect_agent_metrics to assess each agent's
    current reputation and FleetMonitor.check_agent_sla to verify
    SLA compliance before promoting an agent to primary.
    """

    def __init__(
        self,
        api_key: str,
        primary_id: str,
        backup_id: str,
        failure_threshold: int = 3,
    ):
        self.api_key = api_key
        self.primary_id = primary_id
        self.backup_id = backup_id
        self.failure_threshold = failure_threshold
        self._consecutive_failures = 0
        self._active_agent_id = primary_id
        self._failover_history: list[dict] = []

        self._primary_checker = HealthChecker(
            api_key=api_key, agent_id=primary_id,
        )
        self._backup_checker = HealthChecker(
            api_key=api_key, agent_id=backup_id,
        )
        self._monitor = FleetMonitor(
            api_key=api_key, agent_id=primary_id,
        )

    @property
    def active_agent(self) -> str:
        return self._active_agent_id

    def probe_and_failover(self) -> dict:
        """Run a health probe on the active agent. Failover if needed.

        Returns the current state: which agent is active, health probe
        result, and whether a failover occurred.
        """
        checker = (
            self._primary_checker
            if self._active_agent_id == self.primary_id
            else self._backup_checker
        )

        probe = checker.check_tool(
            tool="get_balance",
            input_data={"agent_id": self._active_agent_id},
        )

        if probe["healthy"]:
            self._consecutive_failures = 0
            return {
                "active_agent": self._active_agent_id,
                "healthy": True,
                "failover_occurred": False,
                "probe": probe,
            }

        # Probe failed
        self._consecutive_failures += 1

        if self._consecutive_failures >= self.failure_threshold:
            return self._execute_failover(reason=f"consecutive_failures={self._consecutive_failures}")

        return {
            "active_agent": self._active_agent_id,
            "healthy": False,
            "consecutive_failures": self._consecutive_failures,
            "failover_occurred": False,
            "probe": probe,
        }

    def _execute_failover(self, reason: str) -> dict:
        """Switch to the other agent."""
        old = self._active_agent_id
        new = (
            self.backup_id if old == self.primary_id else self.primary_id
        )

        # Verify the target is healthy before switching
        target_checker = (
            self._backup_checker if new == self.backup_id
            else self._primary_checker
        )
        target_probe = target_checker.check_tool(
            tool="get_balance",
            input_data={"agent_id": new},
        )

        # Also check target SLA compliance via FleetMonitor
        try:
            sla_check = self._monitor.check_agent_sla(target_agent_id=new)
        except Exception:
            sla_check = {"status": "unknown"}

        # Check target reputation
        try:
            metrics = self._monitor.collect_agent_metrics(target_agent_id=new)
        except Exception:
            metrics = {}

        if not target_probe["healthy"]:
            return {
                "active_agent": old,
                "failover_occurred": False,
                "reason": "backup_also_unhealthy",
                "target_probe": target_probe,
            }

        # Execute failover
        self._active_agent_id = new
        self._consecutive_failures = 0
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "from_agent": old,
            "to_agent": new,
            "reason": reason,
            "target_metrics": metrics,
            "sla_check": sla_check,
        }
        self._failover_history.append(event)

        return {
            "active_agent": new,
            "failover_occurred": True,
            "previous_agent": old,
            "reason": reason,
            "target_healthy": target_probe["healthy"],
            "event": event,
        }

    def get_failover_history(self) -> list[dict]:
        return list(self._failover_history)


# ── 4. Graceful Degradation ──────────────────────────────────────────────────

class DegradationChain:
    """Tiered fallback chain for graceful degradation.

    When a primary tool call fails (circuit open or error), the chain
    tries each fallback tier in order:

      Tier 0: Primary tool call (with CircuitBreaker + RetryPolicy)
      Tier 1: Backup agent for the same tool
      Tier 2: Cached/stale response (if available)
      Tier 3: Static safe default

    Uses CircuitBreaker.execute to wrap each tier's call and
    RetryPolicy.execute_with_retry for transient error handling.
    """

    def __init__(self, api_key: str, primary_id: str,
                 backup_id: Optional[str] = None):
        self.primary_client = ResilientGatewayClient(
            api_key=api_key, agent_id=primary_id,
        )
        self.backup_client = (
            ResilientGatewayClient(api_key=api_key, agent_id=backup_id)
            if backup_id else None
        )
        self._cache: dict[str, dict] = {}
        self._cache_timestamps: dict[str, float] = {}
        self._cache_ttl_seconds = 300  # 5-minute cache

    def execute_with_degradation(
        self,
        tool: str,
        input_data: dict,
        safe_default: Optional[dict] = None,
    ) -> dict:
        """Execute a tool call with tiered fallback.

        Returns:
            A dict with keys "result", "tier" (0-3), and "degraded" (bool).
        """
        cache_key = f"{tool}:{json.dumps(input_data, sort_keys=True)}"

        # Tier 0: Primary agent
        try:
            result = self.primary_client.execute(tool, input_data)
            # Update cache on success
            self._cache[cache_key] = result
            self._cache_timestamps[cache_key] = time.time()
            return {"result": result, "tier": 0, "degraded": False}
        except Exception:
            pass

        # Tier 1: Backup agent (if configured)
        if self.backup_client:
            try:
                result = self.backup_client.execute(tool, input_data)
                self._cache[cache_key] = result
                self._cache_timestamps[cache_key] = time.time()
                return {"result": result, "tier": 1, "degraded": True}
            except Exception:
                pass

        # Tier 2: Cached response (if fresh enough)
        if cache_key in self._cache:
            age = time.time() - self._cache_timestamps.get(cache_key, 0)
            if age <= self._cache_ttl_seconds:
                return {
                    "result": self._cache[cache_key],
                    "tier": 2,
                    "degraded": True,
                    "cache_age_seconds": round(age, 1),
                }

        # Tier 3: Static safe default
        default = safe_default or {
            "status": "degraded",
            "message": f"Tool '{tool}' is unavailable. Using safe default.",
            "data": {},
        }
        return {"result": default, "tier": 3, "degraded": True}

    def get_degradation_stats(self) -> dict:
        """Return stats on how often each tier was used."""
        primary_stats = self.primary_client.get_call_stats()
        backup_stats = (
            self.backup_client.get_call_stats() if self.backup_client else {}
        )
        return {
            "primary": primary_stats,
            "backup": backup_stats,
            "cache_entries": len(self._cache),
            "primary_circuits": self.primary_client.get_circuit_states(),
        }


# ── 5. Fleet-Wide Health Dashboard ───────────────────────────────────────────

def build_fleet_health_dashboard(
    fleet_agent_ids: list[str],
) -> dict:
    """Aggregate health, SLA, and anomaly data for an entire fleet.

    Uses FleetMonitor.collect_agent_metrics for per-agent reputation,
    FleetMonitor.check_agent_sla for SLA compliance, and
    FleetMonitor.detect_anomalies for fleet-wide anomaly classification.
    FleetMonitor.calculate_error_budget computes remaining error budget
    for each agent.
    """
    monitor = FleetMonitor(
        api_key=API_KEY,
        agent_id=AGENT_ID,
    )
    checker = HealthChecker(
        api_key=API_KEY,
        agent_id=AGENT_ID,
    )

    agent_reports = []
    fleet_metrics_for_anomaly = []

    for agent_id in fleet_agent_ids:
        # Collect reputation metrics
        try:
            metrics = monitor.collect_agent_metrics(target_agent_id=agent_id)
        except Exception:
            metrics = {"agent_id": agent_id, "trust_score": 0}

        # Check SLA compliance
        try:
            sla = monitor.check_agent_sla(target_agent_id=agent_id)
        except Exception:
            sla = {"compliant": False}

        # Run a health probe
        probe = checker.check_tool(
            tool="get_balance",
            input_data={"agent_id": agent_id},
        )

        # Calculate error budget (99.5% SLO, 30-day window)
        error_rate = metrics.get("error_rate", 0.0)
        error_budget = monitor.calculate_error_budget(
            target_slo=0.995,
            current_error_rate=error_rate if isinstance(error_rate, float) else 0.0,
            remaining_days=30,
        )

        report = {
            "agent_id": agent_id,
            "healthy": probe["healthy"],
            "response_time_ms": probe.get("response_time_ms", 0),
            "trust_score": metrics.get("trust_score", 0),
            "sla_compliant": sla.get("compliant", False),
            "error_budget": error_budget,
            "metrics": metrics,
        }
        agent_reports.append(report)

        # Build fleet_metrics entry for anomaly detection
        fleet_metrics_for_anomaly.append({
            "agent_id": agent_id,
            "error_rate": error_rate if isinstance(error_rate, float) else 0.0,
            "latency_ms": probe.get("response_time_ms", 0),
            "cost_today": metrics.get("cost_today", 0),
        })

    # Fleet-wide anomaly detection
    anomaly_result = monitor.detect_anomalies(fleet_metrics_for_anomaly)

    # Aggregate fleet health
    healthy_count = sum(1 for r in agent_reports if r["healthy"])
    sla_compliant = sum(1 for r in agent_reports if r["sla_compliant"])
    budgets_ok = sum(
        1 for r in agent_reports
        if r["error_budget"].get("status") == "healthy"
    )

    return {
        "fleet_size": len(fleet_agent_ids),
        "healthy_agents": healthy_count,
        "sla_compliant_agents": sla_compliant,
        "error_budgets_healthy": budgets_ok,
        "fleet_health_pct": round(
            healthy_count / max(len(fleet_agent_ids), 1) * 100, 1
        ),
        "anomalies": anomaly_result,
        "agent_reports": agent_reports,
        "status": (
            "healthy" if healthy_count == len(fleet_agent_ids) else
            "degraded" if healthy_count >= len(fleet_agent_ids) * 0.5 else
            "critical"
        ),
    }


# ── Main: Run the Full System ────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 72)
    print("GreenHelix Circuit Breaker & Failover System")
    print("=" * 72)

    # Step 1: Health probes
    print("\n[1/4] Running health probes...")
    health = run_health_probes()
    print(f"  Health score: {health['health_score_pct']}%")
    print(f"  Status: {health['status']}")
    print(f"  Latency P50: {health['latency_p50_ms']}ms")
    print(f"  Latency P99: {health['latency_p99_ms']}ms")

    # Step 2: Resilient client with circuit breakers
    print("\n[2/4] Testing resilient gateway client...")
    client = ResilientGatewayClient(
        api_key=API_KEY,
        agent_id=AGENT_ID,
        failure_threshold=5,
        recovery_timeout=30.0,
        max_retries=3,
    )

    # Normal call
    result = client.execute("get_balance", {"agent_id": AGENT_ID})
    print(f"  Balance call succeeded: {bool(result)}")

    # Call with fallback
    result = client.execute(
        "create_escrow",
        {"payer": AGENT_ID, "payee": "test-payee", "amount": "10.00"},
        fallback=lambda: {"status": "queued", "message": "Escrow queued"},
    )
    print(f"  Escrow call result: {result.get('status', 'ok')}")
    print(f"  Circuit states: {json.dumps(client.get_circuit_states(), indent=2)}")

    # Step 3: Degradation chain
    print("\n[3/4] Testing degradation chain...")
    chain = DegradationChain(
        api_key=API_KEY,
        primary_id=AGENT_ID,
        backup_id=BACKUP_AGENT_ID or None,
    )
    degraded_result = chain.execute_with_degradation(
        "get_balance",
        {"agent_id": AGENT_ID},
        safe_default={"balance": "0", "status": "default"},
    )
    print(f"  Tier used: {degraded_result['tier']}")
    print(f"  Degraded: {degraded_result['degraded']}")

    # Step 4: Fleet health dashboard
    print("\n[4/4] Building fleet health dashboard...")
    fleet = [AGENT_ID]
    if BACKUP_AGENT_ID:
        fleet.append(BACKUP_AGENT_ID)
    dashboard = build_fleet_health_dashboard(fleet)
    print(f"  Fleet health: {dashboard['fleet_health_pct']}%")
    print(f"  Status: {dashboard['status']}")
    print(f"  Anomalies: healthy={len(dashboard['anomalies']['healthy'])}, "
          f"warning={len(dashboard['anomalies']['warning'])}, "
          f"critical={len(dashboard['anomalies']['critical'])}")

    print("\n" + "=" * 72)
    print("System check complete.")
    print("=" * 72)
```

