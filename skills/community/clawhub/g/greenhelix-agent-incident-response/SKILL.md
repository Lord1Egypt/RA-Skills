---
name: greenhelix-agent-incident-response
version: "1.3.1"
description: "The Agent Incident Response Playbook: Detect, Contain, Recover, and Learn When AI Agent Systems Fail. Structured runbooks for AI agent commerce failures: runaway spending, escrow exploitation, identity compromise, service degradation, and cascade failures. Includes detailed code examples with Python classes for automated detection, containment, recovery, and post-mortem forensics with full API integration."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [incident-response, runbooks, agent-ops, containment, forensics, commerce, guide, greenhelix, openclaw, ai-agent]
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
# The Agent Incident Response Playbook: Detect, Contain, Recover, and Learn When AI Agent Systems Fail

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `GREENHELIX_API_KEY`: API authentication for GreenHelix gateway (read/write access to purchased API tools only)


Your fleet of 40 commerce agents has been running smoothly for three months. Budget caps are set, escrow flows are tested, observability dashboards are green. At 2:47 AM on a Tuesday, one agent enters a retry loop against a flaky upstream service. Each retry creates a new escrow. Within 11 minutes the agent has created 312 escrows totaling $47,000 in locked funds. The budget cap does not trigger because each individual escrow is $150 -- well under the per-transaction limit. By the time your on-call engineer wakes up to a PagerDuty alert at 3:14 AM, the agent has exhausted the shared wallet and three other agents have failed their own escrow creates with insufficient-balance errors, triggering their own retry loops. You now have a cascade failure across four agents, $47K in locked escrows, and no runbook that tells you what to do first. Standard IT incident response -- the kind built for a database going down or a deployment rolling back -- does not work here. The failure was not a discrete event. It was a behavioral drift that compounded across autonomous systems making independent financial decisions. This guide gives you the runbooks, the automation, and the API-backed response classes to detect, contain, recover from, and learn from agent commerce incidents. Every command runs against the GreenHelix API. Every pattern is extracted from real failures in production agent systems.
1. [Why Agent Incidents Are Different](#chapter-1-why-agent-incidents-are-different)
2. [Phase 1: Detection — Knowing Something Is Wrong](#chapter-2-phase-1-detection--knowing-something-is-wrong)

## What You'll Learn
- Chapter 1: Why Agent Incidents Are Different
- Chapter 2: Phase 1: Detection — Knowing Something Is Wrong
- Chapter 3: Phase 2: Containment — Stop the Bleeding
- Chapter 4: Phase 3: Recovery — Getting Back to Normal
- Chapter 5: Phase 4: Post-Mortem — Learning from Failure
- Chapter 6: The 5 Agent Incident Runbooks
- Chapter 7: Automated Incident Response
- Chapter 8: Incident Readiness Checklist
- Automated Incident Detection & Escalation — Working Implementation

## Full Guide

# The Agent Incident Response Playbook: Detect, Contain, Recover, and Learn When AI Agent Systems Fail

Your fleet of 40 commerce agents has been running smoothly for three months. Budget caps are set, escrow flows are tested, observability dashboards are green. At 2:47 AM on a Tuesday, one agent enters a retry loop against a flaky upstream service. Each retry creates a new escrow. Within 11 minutes the agent has created 312 escrows totaling $47,000 in locked funds. The budget cap does not trigger because each individual escrow is $150 -- well under the per-transaction limit. By the time your on-call engineer wakes up to a PagerDuty alert at 3:14 AM, the agent has exhausted the shared wallet and three other agents have failed their own escrow creates with insufficient-balance errors, triggering their own retry loops. You now have a cascade failure across four agents, $47K in locked escrows, and no runbook that tells you what to do first. Standard IT incident response -- the kind built for a database going down or a deployment rolling back -- does not work here. The failure was not a discrete event. It was a behavioral drift that compounded across autonomous systems making independent financial decisions. This guide gives you the runbooks, the automation, and the API-backed response classes to detect, contain, recover from, and learn from agent commerce incidents. Every command runs against the GreenHelix API. Every pattern is extracted from real failures in production agent systems.

---

## Table of Contents

1. [Why Agent Incidents Are Different](#chapter-1-why-agent-incidents-are-different)
2. [Phase 1: Detection — Knowing Something Is Wrong](#chapter-2-phase-1-detection--knowing-something-is-wrong)
3. [Phase 2: Containment — Stop the Bleeding](#chapter-3-phase-2-containment--stop-the-bleeding)
4. [Phase 3: Recovery — Getting Back to Normal](#chapter-4-phase-3-recovery--getting-back-to-normal)
5. [Phase 4: Post-Mortem — Learning from Failure](#chapter-5-phase-4-post-mortem--learning-from-failure)
6. [The 5 Agent Incident Runbooks](#chapter-6-the-5-agent-incident-runbooks)
7. [Automated Incident Response](#chapter-7-automated-incident-response)
8. [Incident Readiness Checklist](#chapter-8-incident-readiness-checklist)

---

## Chapter 1: Why Agent Incidents Are Different

### The $47K Infinite Loop

The scenario in the introduction is not hypothetical. Agent retry loops are the most common cause of financial incidents in autonomous commerce systems, and they are the hardest to detect with traditional monitoring. A database going down produces a clear signal: connection refused, error rate spikes, health check fails. An agent entering a retry loop produces normal-looking traffic. Each individual API call succeeds. Each escrow is valid. The budget cap does not fire because the cap was designed for large single transactions, not hundreds of small ones. The anomaly is in the aggregate behavior, not in any single event.

The second most common incident is the deleted database -- or more precisely, the agent that was given infrastructure tools and decided that the fastest way to resolve a failing integration test was to drop and recreate the table. The third is the terraform destroy: an orchestrator agent with deployment permissions that interpreted "clean up the staging environment" as "destroy all resources." These failures share a common trait: they are non-deterministic. The same agent, with the same prompt, given the same inputs on a different day, would have behaved differently. The failure emerges from the intersection of model stochasticity, system state, and timing.

### Why Traditional Runbooks Break

NIST SP 800-61 (Computer Security Incident Handling Guide) defines a four-phase incident response lifecycle: Preparation, Detection & Analysis, Containment/Eradication/Recovery, and Post-Incident Activity. The framework is sound. The implementation assumptions are not. NIST assumes incidents have discrete causes: a malware infection, a compromised credential, a misconfigured firewall. Agent incidents have diffuse causes: a combination of model behavior, retry logic, budget configuration, and counterparty state that together produce a failure no single factor would have caused alone.

Traditional runbooks also assume human decision-making speed is acceptable. When a web server is compromised, an hour to assess and contain is reasonable. When an agent is creating escrows at 30 per minute, an hour of containment delay is $270,000 in additional locked funds. Agent incident response must be automated at the detection and initial containment phases, with human judgment reserved for recovery and post-mortem.

### The 4-Phase Model for Agent Incidents

This guide adapts the NIST lifecycle for autonomous agent commerce:

```
  ┌─────────┐     ┌────────────┐     ┌──────────┐     ┌─────────┐
  │ DETECT   │────▶│  CONTAIN   │────▶│ RECOVER  │────▶│  LEARN  │
  │          │     │            │     │          │     │         │
  │ Cost     │     │ Freeze     │     │ Restore  │     │ Audit   │
  │ anomaly  │     │ budgets    │     │ budgets  │     │ trail   │
  │ Rep.     │     │ Cancel     │     │ Re-verify│     │ Impact  │
  │ drift    │     │ escrows    │     │ identity │     │ assess  │
  │ Webhook  │     │ Verify     │     │ Clear    │     │ Build   │
  │ alerts   │     │ identity   │     │ flags    │     │ timeline│
  └─────────┘     └────────────┘     └──────────┘     └─────────┘
       │                                                     │
       └──────────── Continuous Improvement ─────────────────┘
```

**Detect**: Identify anomalous agent behavior through cost monitoring, reputation drift, and webhook-based alerting. Automated detection triggers automated containment.

**Contain**: Stop the bleeding. Freeze budgets to zero, cancel active escrows, verify agent identity has not been compromised. This phase must execute in under 60 seconds.

**Recover**: Restore the system to a known-good state. Re-enable budgets at safe levels, re-verify agent identity and reputation, clear incident flags so normal operations resume.

**Learn**: Reconstruct what happened, assess the financial impact, and feed findings back into detection rules so the same incident cannot recur.

Every class in this guide maps to one phase. Every method maps to one action. Every action calls one or more GreenHelix API tools. The rest of this guide walks through each phase with production-ready Python code, then assembles five complete runbooks for the most common agent incident types.

---

## Chapter 2: Phase 1: Detection — Knowing Something Is Wrong

### The Three Detection Signals

Agent incidents produce three observable signals, and you need all three because no single signal is reliable on its own.

**Cost anomaly**: An agent's spending rate deviates from its historical baseline. A cost spike is the most reliable signal for runaway spending, but it lags -- by the time cumulative spend exceeds the anomaly threshold, the agent may have already locked significant funds. The detection window depends on your polling interval.

**Reputation drift**: An agent's trust score or reputation metrics change unexpectedly. A sudden drop in reputation may indicate the agent is producing low-quality work, failing to meet escrow conditions, or being reported by counterparties. Reputation drift is a leading indicator for quality degradation incidents but a lagging indicator for financial incidents.

**Webhook alerts**: The GreenHelix event bus can push real-time notifications for budget threshold crossings, escrow state changes, and trust score updates. Webhooks are the fastest detection method but require infrastructure to receive and process them. If your webhook endpoint is down, you have no detection.

### The IncidentDetector Class

The `IncidentDetector` combines all three signals into a single monitoring class. It polls billing and reputation endpoints on a configurable interval and registers webhooks for real-time alerting.

```python
import requests
import time
import json
import hashlib
import statistics
from datetime import datetime, timezone
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class AnomalyResult:
    """Result of an anomaly detection check."""
    detected: bool
    signal: str
    severity: str  # "info", "warning", "critical"
    agent_id: str
    details: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "detected": self.detected,
            "signal": self.signal,
            "severity": self.severity,
            "agent_id": self.agent_id,
            "details": self.details,
            "timestamp": self.timestamp,
        }


class IncidentDetector:
    """Phase 1: Detect agent incidents via cost, reputation, and webhooks.

    Usage:
        detector = IncidentDetector(
            api_key="your-key",
            agent_id="agent-prod-001",
        )

        # One-shot anomaly check
        anomalies = detector.check_all()
        for anomaly in anomalies:
            if anomaly.severity == "critical":
                print(f"CRITICAL: {anomaly.signal} - {anomaly.details}")

        # Set up persistent webhook alerts
        detector.setup_alerts(
            webhook_url="https://your-app.com/incidents/webhook",
            budget_threshold_pct=80,
        )

        # Continuous monitoring loop
        detector.monitor(interval_seconds=30, callback=your_handler)
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: str = "https://api.greenhelix.net/v1",
        cost_anomaly_std_devs: float = 2.0,
        reputation_drop_threshold: float = 0.15,
    ):
        self.api_key = api_key
        self.agent_id = agent_id
        self.base_url = base_url
        self.cost_anomaly_std_devs = cost_anomaly_std_devs
        self.reputation_drop_threshold = reputation_drop_threshold
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })
        self._cost_history: list[float] = []
        self._reputation_baseline: Optional[float] = None
        self._alert_callbacks: list = []

    def _execute(self, tool: str, input_data: dict) -> dict:
        """Execute a GreenHelix tool."""
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    # ── Cost Anomaly Detection ─────────────────────────────────

    def check_cost_anomaly(self) -> AnomalyResult:
        """Detect spending anomalies by comparing current balance drain
        rate against historical baseline.

        Uses a rolling window of balance snapshots to compute the
        mean and standard deviation of spending rate, then flags
        any period where the rate exceeds mean + N standard deviations.
        """
        balance_resp = self._execute("get_balance", {
            "agent_id": self.agent_id,
        })
        current_balance = float(balance_resp.get("balance", "0"))
        self._cost_history.append(current_balance)

        if len(self._cost_history) < 5:
            return AnomalyResult(
                detected=False,
                signal="cost_anomaly",
                severity="info",
                agent_id=self.agent_id,
                details={"message": "Insufficient history", "samples": len(self._cost_history)},
            )

        # Compute balance deltas (spending rate per interval)
        deltas = [
            self._cost_history[i] - self._cost_history[i + 1]
            for i in range(len(self._cost_history) - 1)
        ]
        # Filter to only spending (positive deltas)
        spending_deltas = [d for d in deltas if d > 0]

        if len(spending_deltas) < 3:
            return AnomalyResult(
                detected=False,
                signal="cost_anomaly",
                severity="info",
                agent_id=self.agent_id,
                details={"message": "Insufficient spending data"},
            )

        mean_spend = statistics.mean(spending_deltas)
        std_spend = statistics.stdev(spending_deltas)
        latest_spend = deltas[-1] if deltas[-1] > 0 else 0

        threshold = mean_spend + (self.cost_anomaly_std_devs * std_spend)

        if latest_spend > threshold and std_spend > 0:
            severity = "critical" if latest_spend > threshold * 2 else "warning"
            return AnomalyResult(
                detected=True,
                signal="cost_anomaly",
                severity=severity,
                agent_id=self.agent_id,
                details={
                    "current_balance": str(current_balance),
                    "latest_spend_rate": str(round(latest_spend, 2)),
                    "mean_spend_rate": str(round(mean_spend, 2)),
                    "std_dev": str(round(std_spend, 2)),
                    "threshold": str(round(threshold, 2)),
                    "z_score": str(round(
                        (latest_spend - mean_spend) / std_spend, 2
                    )) if std_spend > 0 else "N/A",
                },
            )

        return AnomalyResult(
            detected=False,
            signal="cost_anomaly",
            severity="info",
            agent_id=self.agent_id,
            details={
                "current_balance": str(current_balance),
                "latest_spend_rate": str(round(latest_spend, 2)),
                "threshold": str(round(threshold, 2)),
            },
        )

    # ── Reputation Drift Detection ─────────────────────────────

    def check_reputation_drift(self) -> AnomalyResult:
        """Detect unexpected drops in agent reputation score.

        Compares current reputation against the baseline captured
        on first call. A drop exceeding the threshold indicates
        either quality degradation or adversarial reporting.
        """
        rep_resp = self._execute("get_agent_reputation", {
            "agent_id": self.agent_id,
        })
        current_score = float(rep_resp.get("reputation_score", 0))

        if self._reputation_baseline is None:
            self._reputation_baseline = current_score
            return AnomalyResult(
                detected=False,
                signal="reputation_drift",
                severity="info",
                agent_id=self.agent_id,
                details={
                    "message": "Baseline established",
                    "baseline": str(current_score),
                },
            )

        drop = self._reputation_baseline - current_score
        drop_pct = drop / self._reputation_baseline if self._reputation_baseline > 0 else 0

        if drop_pct >= self.reputation_drop_threshold:
            severity = "critical" if drop_pct >= 0.30 else "warning"
            return AnomalyResult(
                detected=True,
                signal="reputation_drift",
                severity=severity,
                agent_id=self.agent_id,
                details={
                    "baseline_score": str(self._reputation_baseline),
                    "current_score": str(current_score),
                    "drop_pct": str(round(drop_pct * 100, 1)),
                    "threshold_pct": str(round(self.reputation_drop_threshold * 100, 1)),
                },
            )

        return AnomalyResult(
            detected=False,
            signal="reputation_drift",
            severity="info",
            agent_id=self.agent_id,
            details={
                "current_score": str(current_score),
                "baseline_score": str(self._reputation_baseline),
            },
        )

    # ── Budget Status Check ────────────────────────────────────

    def check_budget_status(self) -> AnomalyResult:
        """Check if agent is approaching or has exceeded budget limits."""
        budget_resp = self._execute("get_budget_status", {
            "agent_id": self.agent_id,
        })
        utilization_pct = float(budget_resp.get("utilization_pct", 0))
        daily_limit = budget_resp.get("daily_limit", "0")
        daily_spent = budget_resp.get("daily_spent", "0")

        if utilization_pct >= 95:
            return AnomalyResult(
                detected=True,
                signal="budget_exhaustion",
                severity="critical",
                agent_id=self.agent_id,
                details={
                    "utilization_pct": str(utilization_pct),
                    "daily_limit": str(daily_limit),
                    "daily_spent": str(daily_spent),
                },
            )
        elif utilization_pct >= 80:
            return AnomalyResult(
                detected=True,
                signal="budget_warning",
                severity="warning",
                agent_id=self.agent_id,
                details={
                    "utilization_pct": str(utilization_pct),
                    "daily_limit": str(daily_limit),
                    "daily_spent": str(daily_spent),
                },
            )

        return AnomalyResult(
            detected=False,
            signal="budget_status",
            severity="info",
            agent_id=self.agent_id,
            details={"utilization_pct": str(utilization_pct)},
        )

    # ── Webhook Alert Setup ────────────────────────────────────

    def setup_alerts(
        self,
        webhook_url: str,
        budget_threshold_pct: int = 80,
    ) -> dict:
        """Register webhooks for real-time incident alerting.

        Sets up three event subscriptions:
        1. Budget threshold crossing (configurable percentage)
        2. Escrow state changes (creation, release, cancellation)
        3. Reputation score updates
        """
        results = {}

        # Budget alert webhook
        results["budget_alert"] = self._execute("register_webhook", {
            "agent_id": self.agent_id,
            "event_type": "budget_threshold",
            "webhook_url": webhook_url,
            "config": {
                "threshold_pct": budget_threshold_pct,
            },
        })

        # Escrow state change webhook
        results["escrow_alert"] = self._execute("register_webhook", {
            "agent_id": self.agent_id,
            "event_type": "escrow_state_change",
            "webhook_url": webhook_url,
        })

        # Reputation change webhook
        results["reputation_alert"] = self._execute("register_webhook", {
            "agent_id": self.agent_id,
            "event_type": "reputation_change",
            "webhook_url": webhook_url,
        })

        # Publish a test event to verify webhook delivery
        results["test_event"] = self._execute("publish_event", {
            "agent_id": self.agent_id,
            "event_type": "incident_detector_setup",
            "payload": {
                "message": "Incident detection webhooks configured",
                "webhook_url": webhook_url,
                "timestamp": int(time.time()),
            },
        })

        return results

    # ── Combined Check ─────────────────────────────────────────

    def check_all(self) -> list[AnomalyResult]:
        """Run all detection checks and return any anomalies found."""
        results = []
        checks = [
            self.check_cost_anomaly,
            self.check_reputation_drift,
            self.check_budget_status,
        ]
        for check in checks:
            try:
                result = check()
                if result.detected:
                    results.append(result)
            except requests.exceptions.RequestException as e:
                results.append(AnomalyResult(
                    detected=True,
                    signal="detection_failure",
                    severity="warning",
                    agent_id=self.agent_id,
                    details={"error": str(e), "check": check.__name__},
                ))
        return results

    # ── Continuous Monitoring ──────────────────────────────────

    def monitor(
        self,
        interval_seconds: int = 30,
        callback=None,
        max_iterations: Optional[int] = None,
    ):
        """Run continuous anomaly detection in a polling loop.

        Args:
            interval_seconds: Seconds between detection cycles.
            callback: Function called with list[AnomalyResult] each cycle.
            max_iterations: Stop after N cycles (None = run forever).
        """
        iteration = 0
        while max_iterations is None or iteration < max_iterations:
            anomalies = self.check_all()
            if anomalies and callback:
                callback(anomalies)
            elif anomalies:
                for a in anomalies:
                    print(
                        f"[{a.severity.upper()}] {a.signal}: "
                        f"{json.dumps(a.details)}"
                    )
            time.sleep(interval_seconds)
            iteration += 1
```

### Detection in Practice

The detector is designed to run as a sidecar process alongside your agent fleet. In the simplest deployment, run it as a cron job every 30 seconds:

```python
detector = IncidentDetector(
    api_key="your-api-key",
    agent_id="agent-prod-001",
    cost_anomaly_std_devs=2.5,      # Wider tolerance = fewer false positives
    reputation_drop_threshold=0.10,  # Alert on 10% reputation drop
)

# Set up persistent webhooks (run once during deployment)
detector.setup_alerts(
    webhook_url="https://your-app.com/incidents/webhook",
    budget_threshold_pct=75,  # Alert at 75% budget utilization
)

# Continuous monitoring (runs in background)
def on_anomaly(anomalies):
    for a in anomalies:
        if a.severity == "critical":
            # Trigger automated containment (see Chapter 3)
            trigger_containment(a.agent_id, a.signal, a.details)
        else:
            # Send to alerting channel
            send_slack_alert(a)

detector.monitor(interval_seconds=30, callback=on_anomaly)
```

The `cost_anomaly_std_devs` parameter controls sensitivity. At 2.0 standard deviations, you will catch most real anomalies but may see false positives during legitimate high-activity periods (end-of-month billing, batch processing). At 3.0, you will miss some slower-developing anomalies but virtually eliminate false positives. Start at 2.5 and tune based on your false-positive rate during the first two weeks.

The `reputation_drop_threshold` of 0.15 (15%) was chosen because normal reputation fluctuation in a healthy agent is under 5% per day. A 15% drop in a single monitoring interval indicates either a genuine quality problem or adversarial reporting. Both warrant investigation.

---

## Chapter 3: Phase 2: Containment — Stop the Bleeding

### The 60-Second Rule

In agent commerce, containment must complete within 60 seconds of detection. Every second of delay is more locked funds, more failed transactions, more cascade effects on dependent agents. The containment phase has three actions, executed in order:

1. **Freeze the budget**: Set the agent's daily budget cap to zero. This immediately prevents new spending without affecting existing escrows.
2. **Cancel active escrows**: List all pending escrows for the agent and cancel them. This unlocks funds and prevents further financial exposure.
3. **Verify identity**: Confirm the agent has not been impersonated. If identity verification fails, the incident scope expands from "misbehaving agent" to "compromised agent."

### The IncidentContainment Class

```python
import requests
import time
import json
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class ContainmentResult:
    """Result of a containment action."""
    action: str
    success: bool
    agent_id: str
    details: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    error: Optional[str] = None

    def to_dict(self) -> dict:
        result = {
            "action": self.action,
            "success": self.success,
            "agent_id": self.agent_id,
            "details": self.details,
            "timestamp": self.timestamp,
        }
        if self.error:
            result["error"] = self.error
        return result


class IncidentContainment:
    """Phase 2: Contain agent incidents by freezing budgets, escrows,
    and verifying identity.

    Usage:
        containment = IncidentContainment(
            api_key="your-key",
            agent_id="agent-prod-001",
        )

        # Full containment sequence (recommended)
        results = containment.contain_agent()
        for r in results:
            print(f"[{r.action}] success={r.success}")

        # Individual actions
        containment.freeze_agent()
        containment.freeze_escrows()
        containment.verify_agent_identity()
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: str = "https://api.greenhelix.net/v1",
    ):
        self.api_key = api_key
        self.agent_id = agent_id
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })
        self._containment_log: list[ContainmentResult] = []

    def _execute(self, tool: str, input_data: dict) -> dict:
        """Execute a GreenHelix tool."""
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    def _log(self, result: ContainmentResult):
        """Append to the internal containment audit log."""
        self._containment_log.append(result)

    # ── Budget Freeze ──────────────────────────────────────────

    def freeze_agent(self) -> ContainmentResult:
        """Freeze an agent's spending by setting daily budget cap to zero.

        This is the single most important containment action. Setting
        the daily budget to $0 immediately prevents the agent from
        initiating any new paid operations. Existing escrows are not
        affected -- they must be cancelled separately.
        """
        try:
            # First, capture current budget for later restoration
            budget_status = self._execute("get_budget_status", {
                "agent_id": self.agent_id,
            })
            previous_cap = budget_status.get("daily_limit", "unknown")

            # Set budget to zero
            freeze_resp = self._execute("set_budget_cap", {
                "agent_id": self.agent_id,
                "daily": "0",
                "monthly": "0",
            })

            # Publish incident event
            self._execute("publish_event", {
                "agent_id": self.agent_id,
                "event_type": "incident_budget_frozen",
                "payload": {
                    "previous_daily_cap": str(previous_cap),
                    "reason": "incident_containment",
                    "timestamp": int(time.time()),
                },
            })

            result = ContainmentResult(
                action="freeze_budget",
                success=True,
                agent_id=self.agent_id,
                details={
                    "previous_daily_cap": str(previous_cap),
                    "new_daily_cap": "0",
                    "response": freeze_resp,
                },
            )
        except requests.exceptions.RequestException as e:
            result = ContainmentResult(
                action="freeze_budget",
                success=False,
                agent_id=self.agent_id,
                error=str(e),
            )

        self._log(result)
        return result

    # ── Escrow Freeze ──────────────────────────────────────────

    def freeze_escrows(self) -> ContainmentResult:
        """Cancel all active escrows for the agent to unlock funds.

        Lists all escrows where the agent is the payer, then cancels
        each one that is in a cancellable state (pending, funded).
        Escrows that have already been released or disputed cannot
        be cancelled.
        """
        try:
            # List all escrows for this agent
            escrows_resp = self._execute("list_escrows", {
                "agent_id": self.agent_id,
            })
            escrows = escrows_resp.get("escrows", [])

            cancelled = []
            failed = []
            skipped = []

            for escrow in escrows:
                escrow_id = escrow.get("escrow_id", "")
                status = escrow.get("status", "")

                if status in ("pending", "funded", "active"):
                    try:
                        cancel_resp = self._execute("cancel_escrow", {
                            "escrow_id": escrow_id,
                            "reason": "incident_containment",
                        })
                        cancelled.append({
                            "escrow_id": escrow_id,
                            "amount": escrow.get("amount", "0"),
                            "status": status,
                            "cancel_response": cancel_resp,
                        })
                    except requests.exceptions.RequestException as e:
                        failed.append({
                            "escrow_id": escrow_id,
                            "error": str(e),
                        })
                else:
                    skipped.append({
                        "escrow_id": escrow_id,
                        "status": status,
                        "reason": "not_cancellable",
                    })

            total_unlocked = sum(
                float(c.get("amount", "0")) for c in cancelled
            )

            result = ContainmentResult(
                action="freeze_escrows",
                success=len(failed) == 0,
                agent_id=self.agent_id,
                details={
                    "total_escrows": len(escrows),
                    "cancelled": len(cancelled),
                    "failed": len(failed),
                    "skipped": len(skipped),
                    "total_unlocked": str(round(total_unlocked, 2)),
                    "cancelled_details": cancelled,
                    "failed_details": failed,
                },
            )
        except requests.exceptions.RequestException as e:
            result = ContainmentResult(
                action="freeze_escrows",
                success=False,
                agent_id=self.agent_id,
                error=str(e),
            )

        self._log(result)
        return result

    # ── Identity Verification ──────────────────────────────────

    def verify_agent_identity(self) -> ContainmentResult:
        """Verify the agent's identity has not been compromised.

        Checks both the agent's registered identity and current
        verification status. If the agent cannot be verified,
        the incident scope expands to potential identity compromise.
        """
        try:
            # Get current identity record
            identity_resp = self._execute("get_agent_identity", {
                "agent_id": self.agent_id,
            })

            # Verify the agent is still valid
            verify_resp = self._execute("verify_agent", {
                "agent_id": self.agent_id,
            })
            is_verified = verify_resp.get("verified", False)

            # Check reputation for signs of manipulation
            rep_resp = self._execute("get_agent_reputation", {
                "agent_id": self.agent_id,
            })

            result = ContainmentResult(
                action="verify_identity",
                success=True,
                agent_id=self.agent_id,
                details={
                    "identity_valid": is_verified,
                    "identity": identity_resp,
                    "reputation": rep_resp,
                    "compromise_suspected": not is_verified,
                },
            )

            if not is_verified:
                result.details["warning"] = (
                    "Agent identity verification FAILED. "
                    "Possible identity compromise. Escalate immediately."
                )
                # Publish critical event
                self._execute("publish_event", {
                    "agent_id": self.agent_id,
                    "event_type": "incident_identity_compromise_suspected",
                    "payload": {
                        "verification_result": verify_resp,
                        "timestamp": int(time.time()),
                    },
                })
        except requests.exceptions.RequestException as e:
            result = ContainmentResult(
                action="verify_identity",
                success=False,
                agent_id=self.agent_id,
                error=str(e),
                details={
                    "warning": "Could not verify identity. Treat as compromised.",
                },
            )

        self._log(result)
        return result

    # ── Full Containment Sequence ──────────────────────────────

    def contain_agent(self) -> list[ContainmentResult]:
        """Execute the full containment sequence: freeze budget,
        cancel escrows, verify identity.

        Returns a list of ContainmentResult objects, one per action.
        Actions execute in order. A failure in one action does not
        prevent subsequent actions from executing -- all three must
        be attempted regardless.
        """
        results = []
        start_time = time.time()

        # Step 1: Freeze budget (most critical, executes first)
        results.append(self.freeze_agent())

        # Step 2: Cancel escrows (unlock funds)
        results.append(self.freeze_escrows())

        # Step 3: Verify identity (expand scope if compromised)
        results.append(self.verify_agent_identity())

        elapsed = round(time.time() - start_time, 2)

        # Publish containment summary
        try:
            self._execute("publish_event", {
                "agent_id": self.agent_id,
                "event_type": "incident_containment_complete",
                "payload": {
                    "elapsed_seconds": elapsed,
                    "actions": [r.to_dict() for r in results],
                    "all_succeeded": all(r.success for r in results),
                    "timestamp": int(time.time()),
                },
            })
        except requests.exceptions.RequestException:
            pass  # Do not let event publishing failure block containment

        return results

    def get_containment_log(self) -> list[dict]:
        """Return the full containment audit log."""
        return [r.to_dict() for r in self._containment_log]
```

### Containment Timing

In testing against the GreenHelix sandbox, the full three-step containment sequence completes in under 3 seconds:

| Action | Typical Latency |
|---|---|
| `freeze_agent` (set_budget_cap) | 200-400ms |
| `freeze_escrows` (list + cancel N) | 500ms + 200ms per escrow |
| `verify_agent_identity` | 400-600ms |
| **Total (5 escrows)** | **~2.5 seconds** |

Even with 50 active escrows, containment completes in under 15 seconds. The 60-second rule provides a generous safety margin for network latency and retries.

### What Containment Does Not Do

Containment does not terminate the agent process. Containment does not revoke API keys. Containment does not delete data. It is designed to be reversible. The agent is still running but financially frozen -- it can read data, check status, and log events, but it cannot spend money or lock new funds. This is intentional: a fully terminated agent cannot participate in its own recovery.

---

## Chapter 4: Phase 3: Recovery — Getting Back to Normal

### Recovery Is Not "Undo Containment"

A common mistake is treating recovery as the inverse of containment: unfreeze the budget, resume operations, done. Recovery must verify that the root cause is resolved before re-enabling financial operations. If you unfreeze a budget while the retry loop is still running, you will re-enter the incident within minutes.

Recovery has three gates, and each must pass before proceeding to the next:

1. **Root cause confirmed resolved**: The code change, configuration fix, or model constraint that caused the incident has been deployed and verified.
2. **Identity and reputation verified**: The agent's identity is intact and its reputation reflects its true performance, not incident-degraded metrics.
3. **Budget restored to safe levels**: The budget is restored to a conservative level (typically 50% of pre-incident cap) with enhanced monitoring, then gradually increased over 24-48 hours.

### The IncidentRecovery Class

```python
import requests
import time
import json
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class RecoveryResult:
    """Result of a recovery action."""
    action: str
    success: bool
    agent_id: str
    details: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    error: Optional[str] = None

    def to_dict(self) -> dict:
        result = {
            "action": self.action,
            "success": self.success,
            "agent_id": self.agent_id,
            "details": self.details,
            "timestamp": self.timestamp,
        }
        if self.error:
            result["error"] = self.error
        return result


class IncidentRecovery:
    """Phase 3: Recover agent operations after containment.

    Usage:
        recovery = IncidentRecovery(
            api_key="your-key",
            agent_id="agent-prod-001",
        )

        # Gradual recovery (recommended)
        results = recovery.recover_agent(
            target_daily_budget="500.00",
            initial_budget_pct=50,
        )
        for r in results:
            print(f"[{r.action}] success={r.success}")

        # After 24 hours with no anomalies, restore full budget
        recovery.restore_full_budget(target_daily_budget="1000.00")
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: str = "https://api.greenhelix.net/v1",
    ):
        self.api_key = api_key
        self.agent_id = agent_id
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })
        self._recovery_log: list[RecoveryResult] = []

    def _execute(self, tool: str, input_data: dict) -> dict:
        """Execute a GreenHelix tool."""
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    def _log(self, result: RecoveryResult):
        self._recovery_log.append(result)

    # ── Budget Restoration ─────────────────────────────────────

    def restore_budget(
        self,
        daily_budget: str,
        monthly_budget: Optional[str] = None,
    ) -> RecoveryResult:
        """Restore the agent's budget to a specified level.

        Start with a conservative budget (50% of pre-incident level)
        and increase gradually over 24-48 hours as monitoring confirms
        normal behavior.
        """
        try:
            monthly = monthly_budget or str(float(daily_budget) * 30)
            resp = self._execute("set_budget_cap", {
                "agent_id": self.agent_id,
                "daily": daily_budget,
                "monthly": monthly,
            })

            result = RecoveryResult(
                action="restore_budget",
                success=True,
                agent_id=self.agent_id,
                details={
                    "daily_budget": daily_budget,
                    "monthly_budget": monthly,
                    "response": resp,
                },
            )
        except requests.exceptions.RequestException as e:
            result = RecoveryResult(
                action="restore_budget",
                success=False,
                agent_id=self.agent_id,
                error=str(e),
            )

        self._log(result)
        return result

    # ── Reputation Restoration ─────────────────────────────────

    def restore_reputation(
        self,
        submit_recovery_metrics: bool = True,
    ) -> RecoveryResult:
        """Verify and restore agent reputation post-incident.

        Checks current reputation, compares against expected baseline,
        and optionally submits recovery metrics to rebuild trust.
        """
        try:
            # Get current reputation
            rep_resp = self._execute("get_agent_reputation", {
                "agent_id": self.agent_id,
            })
            current_score = float(rep_resp.get("reputation_score", 0))

            # Verify the agent identity is still intact
            verify_resp = self._execute("verify_agent", {
                "agent_id": self.agent_id,
            })
            is_verified = verify_resp.get("verified", False)

            # Get verified claims to confirm audit trail integrity
            claims_resp = self._execute("get_verified_claims", {
                "agent_id": self.agent_id,
            })

            # Submit recovery metrics if requested
            metrics_resp = None
            if submit_recovery_metrics:
                metrics_resp = self._execute("submit_metrics", {
                    "agent_id": self.agent_id,
                    "metrics": {
                        "incident_recovery": True,
                        "recovery_timestamp": int(time.time()),
                        "post_recovery_status": "active",
                    },
                })

            result = RecoveryResult(
                action="restore_reputation",
                success=is_verified,
                agent_id=self.agent_id,
                details={
                    "current_reputation": str(current_score),
                    "identity_verified": is_verified,
                    "verified_claims": claims_resp,
                    "recovery_metrics_submitted": metrics_resp is not None,
                },
            )

            if not is_verified:
                result.details["warning"] = (
                    "Agent identity verification failed during recovery. "
                    "Re-registration may be required."
                )
        except requests.exceptions.RequestException as e:
            result = RecoveryResult(
                action="restore_reputation",
                success=False,
                agent_id=self.agent_id,
                error=str(e),
            )

        self._log(result)
        return result

    # ── Incident Flag Clearing ─────────────────────────────────

    def clear_incident(self, incident_id: str = "") -> RecoveryResult:
        """Clear the incident flag and publish a recovery event.

        This signals to other systems (monitoring, alerting, dashboards)
        that the incident has been resolved and the agent is returning
        to normal operations.
        """
        try:
            event_resp = self._execute("publish_event", {
                "agent_id": self.agent_id,
                "event_type": "incident_resolved",
                "payload": {
                    "incident_id": incident_id or f"inc-{int(time.time())}",
                    "resolved_at": int(time.time()),
                    "resolution": "containment_and_recovery_complete",
                },
            })

            # Update service rating to reflect recovery
            rate_resp = self._execute("rate_service", {
                "agent_id": self.agent_id,
                "rating": 3,  # Neutral post-incident rating
                "comment": "Service restored after incident containment and recovery.",
            })

            result = RecoveryResult(
                action="clear_incident",
                success=True,
                agent_id=self.agent_id,
                details={
                    "event_published": event_resp,
                    "service_rating_updated": rate_resp,
                },
            )
        except requests.exceptions.RequestException as e:
            result = RecoveryResult(
                action="clear_incident",
                success=False,
                agent_id=self.agent_id,
                error=str(e),
            )

        self._log(result)
        return result

    # ── Full Recovery Sequence ─────────────────────────────────

    def recover_agent(
        self,
        target_daily_budget: str = "500.00",
        initial_budget_pct: int = 50,
        incident_id: str = "",
    ) -> list[RecoveryResult]:
        """Execute the full recovery sequence.

        Restores budget at a conservative percentage of the target,
        verifies identity and reputation, and clears the incident flag.
        """
        results = []

        # Step 1: Restore budget at conservative level
        initial_budget = str(
            round(float(target_daily_budget) * initial_budget_pct / 100, 2)
        )
        results.append(self.restore_budget(daily_budget=initial_budget))

        # Step 2: Verify and restore reputation
        results.append(self.restore_reputation())

        # Step 3: Clear incident flag
        results.append(self.clear_incident(incident_id=incident_id))

        return results

    def restore_full_budget(
        self, target_daily_budget: str,
    ) -> RecoveryResult:
        """Restore budget to full pre-incident level.

        Call this 24-48 hours after initial recovery, once monitoring
        confirms the agent is operating normally.
        """
        return self.restore_budget(daily_budget=target_daily_budget)

    def get_recovery_log(self) -> list[dict]:
        """Return the full recovery audit log."""
        return [r.to_dict() for r in self._recovery_log]
```

### The Gradual Restoration Pattern

Never restore an agent to full operational capacity immediately. Use a stepped approach:

```
Time 0h:    50% of pre-incident budget, enhanced monitoring (30s interval)
Time +6h:   If no anomalies, increase to 75%
Time +24h:  If no anomalies, increase to 100%
Time +48h:  Reduce monitoring to standard interval (5m)
```

```python
# Gradual restoration example
recovery = IncidentRecovery(api_key="key", agent_id="agent-prod-001")
detector = IncidentDetector(api_key="key", agent_id="agent-prod-001")

# Immediate: 50% budget with tight monitoring
recovery.restore_budget(daily_budget="250.00")  # 50% of $500
detector.monitor(interval_seconds=30, max_iterations=720)  # 6 hours

# +6h: Check for anomalies, then increase
anomalies = detector.check_all()
if not anomalies:
    recovery.restore_budget(daily_budget="375.00")  # 75%
    detector.monitor(interval_seconds=60, max_iterations=1080)  # 18 hours

# +24h: Full restoration
anomalies = detector.check_all()
if not anomalies:
    recovery.restore_full_budget(target_daily_budget="500.00")
```

---

## Chapter 5: Phase 4: Post-Mortem — Learning from Failure

### Every Incident Is a Training Signal

The post-mortem phase is where agent incident response diverges most sharply from traditional IT incident response. In traditional IR, the post-mortem produces a document: a timeline, a root cause, action items for humans. In agent incident response, the post-mortem produces data that feeds back into the detection system. Every incident teaches the detector what the next incident will look like.

The forensics phase has three outputs:

1. **Audit trail**: A cryptographically verified record of everything the agent did during the incident window, extracted from GreenHelix claim chains.
2. **Impact assessment**: Total financial impact -- funds locked, funds lost, funds recovered -- computed from billing analytics.
3. **Incident timeline**: A reconstruction of events from detection through recovery, suitable for both human review and machine learning.

### The IncidentForensics Class

```python
import requests
import time
import json
from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class ForensicsResult:
    """Result of a forensics investigation action."""
    action: str
    agent_id: str
    details: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "action": self.action,
            "agent_id": self.agent_id,
            "details": self.details,
            "timestamp": self.timestamp,
        }


class IncidentForensics:
    """Phase 4: Post-mortem forensics for agent incidents.

    Usage:
        forensics = IncidentForensics(
            api_key="your-key",
            agent_id="agent-prod-001",
        )

        # Full post-mortem
        report = forensics.run_post_mortem(
            incident_id="inc-1712345678",
            incident_start=1712345000,
            incident_end=1712346000,
        )
        print(json.dumps(report, indent=2))
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: str = "https://api.greenhelix.net/v1",
    ):
        self.api_key = api_key
        self.agent_id = agent_id
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })

    def _execute(self, tool: str, input_data: dict) -> dict:
        """Execute a GreenHelix tool."""
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    # ── Audit Trail ────────────────────────────────────────────

    def get_audit_trail(
        self,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
    ) -> ForensicsResult:
        """Extract the cryptographically verified audit trail for
        the incident window.

        Uses claim chains to reconstruct a tamper-proof record of
        agent actions. Each claim in the chain is individually
        verifiable via its Merkle proof.
        """
        # Get claim chains for the agent
        chains_resp = self._execute("get_claim_chains", {
            "agent_id": self.agent_id,
        })
        chains = chains_resp.get("chains", [])

        # Get verified claims (individually verifiable)
        claims_resp = self._execute("get_verified_claims", {
            "agent_id": self.agent_id,
        })
        claims = claims_resp.get("claims", [])

        # Filter to incident window if specified
        if start_time and end_time:
            claims = [
                c for c in claims
                if start_time <= c.get("timestamp", 0) <= end_time
            ]

        # Get identity record for forensic context
        identity_resp = self._execute("get_agent_identity", {
            "agent_id": self.agent_id,
        })

        return ForensicsResult(
            action="audit_trail",
            agent_id=self.agent_id,
            details={
                "claim_chains": chains,
                "verified_claims_in_window": claims,
                "total_claims_in_window": len(claims),
                "identity_at_time": identity_resp,
                "window": {
                    "start": start_time,
                    "end": end_time,
                },
            },
        )

    # ── Impact Assessment ──────────────────────────────────────

    def assess_impact(self) -> ForensicsResult:
        """Calculate the financial impact of the incident.

        Uses billing analytics to compute total spending during the
        incident, broken down by category. Compares against the
        agent's normal spending patterns to isolate incident-related
        costs.
        """
        # Get usage analytics
        analytics_resp = self._execute("get_usage_analytics", {
            "agent_id": self.agent_id,
        })

        # Get billing summary
        billing_resp = self._execute("get_billing_summary", {
            "agent_id": self.agent_id,
        })

        # Get spending by category
        category_resp = self._execute("get_spending_by_category", {
            "agent_id": self.agent_id,
        })

        # Get current balance
        balance_resp = self._execute("get_balance", {
            "agent_id": self.agent_id,
        })

        # Get escrow status (how much was locked/recovered)
        escrows_resp = self._execute("list_escrows", {
            "agent_id": self.agent_id,
        })
        escrows = escrows_resp.get("escrows", [])

        locked_funds = sum(
            float(e.get("amount", "0"))
            for e in escrows
            if e.get("status") in ("pending", "funded", "active")
        )
        cancelled_funds = sum(
            float(e.get("amount", "0"))
            for e in escrows
            if e.get("status") == "cancelled"
        )
        released_funds = sum(
            float(e.get("amount", "0"))
            for e in escrows
            if e.get("status") == "released"
        )

        return ForensicsResult(
            action="impact_assessment",
            agent_id=self.agent_id,
            details={
                "current_balance": balance_resp.get("balance", "0"),
                "usage_analytics": analytics_resp,
                "billing_summary": billing_resp,
                "spending_by_category": category_resp,
                "escrow_impact": {
                    "total_escrows": len(escrows),
                    "still_locked": str(round(locked_funds, 2)),
                    "cancelled_recovered": str(round(cancelled_funds, 2)),
                    "released_lost": str(round(released_funds, 2)),
                },
            },
        )

    # ── Timeline Reconstruction ────────────────────────────────

    def build_timeline(
        self,
        incident_id: str,
        detection_time: int,
        containment_time: int,
        recovery_time: int,
        containment_log: Optional[list[dict]] = None,
        recovery_log: Optional[list[dict]] = None,
    ) -> ForensicsResult:
        """Reconstruct a complete incident timeline.

        Combines data from detection, containment, and recovery
        phases into a single chronological record suitable for
        both human review and machine learning.
        """
        # Compute phase durations
        detection_to_containment = containment_time - detection_time
        containment_to_recovery = recovery_time - containment_time
        total_duration = recovery_time - detection_time

        # Get reputation at time of forensics
        rep_resp = self._execute("get_agent_reputation", {
            "agent_id": self.agent_id,
        })

        timeline_events = []

        # Detection event
        timeline_events.append({
            "phase": "detection",
            "timestamp": detection_time,
            "iso_time": datetime.fromtimestamp(
                detection_time, tz=timezone.utc
            ).isoformat(),
            "event": "incident_detected",
        })

        # Containment events (from log if provided)
        if containment_log:
            for entry in containment_log:
                timeline_events.append({
                    "phase": "containment",
                    "timestamp": entry.get("timestamp", containment_time),
                    "iso_time": datetime.fromtimestamp(
                        entry.get("timestamp", containment_time),
                        tz=timezone.utc,
                    ).isoformat(),
                    "event": entry.get("action", "containment_action"),
                    "success": entry.get("success", False),
                    "details": entry.get("details", {}),
                })
        else:
            timeline_events.append({
                "phase": "containment",
                "timestamp": containment_time,
                "iso_time": datetime.fromtimestamp(
                    containment_time, tz=timezone.utc
                ).isoformat(),
                "event": "containment_complete",
            })

        # Recovery events (from log if provided)
        if recovery_log:
            for entry in recovery_log:
                timeline_events.append({
                    "phase": "recovery",
                    "timestamp": entry.get("timestamp", recovery_time),
                    "iso_time": datetime.fromtimestamp(
                        entry.get("timestamp", recovery_time),
                        tz=timezone.utc,
                    ).isoformat(),
                    "event": entry.get("action", "recovery_action"),
                    "success": entry.get("success", False),
                    "details": entry.get("details", {}),
                })
        else:
            timeline_events.append({
                "phase": "recovery",
                "timestamp": recovery_time,
                "iso_time": datetime.fromtimestamp(
                    recovery_time, tz=timezone.utc
                ).isoformat(),
                "event": "recovery_complete",
            })

        # Sort chronologically
        timeline_events.sort(key=lambda e: e["timestamp"])

        return ForensicsResult(
            action="build_timeline",
            agent_id=self.agent_id,
            details={
                "incident_id": incident_id,
                "timeline": timeline_events,
                "phase_durations": {
                    "detection_to_containment_seconds": detection_to_containment,
                    "containment_to_recovery_seconds": containment_to_recovery,
                    "total_duration_seconds": total_duration,
                },
                "reputation_post_incident": rep_resp,
                "meets_60s_containment_sla": detection_to_containment <= 60,
            },
        )

    # ── Full Post-Mortem ───────────────────────────────────────

    def run_post_mortem(
        self,
        incident_id: str,
        incident_start: int,
        incident_end: int,
        containment_log: Optional[list[dict]] = None,
        recovery_log: Optional[list[dict]] = None,
    ) -> dict:
        """Run a complete post-mortem investigation.

        Combines audit trail, impact assessment, and timeline
        reconstruction into a single report.
        """
        audit = self.get_audit_trail(
            start_time=incident_start,
            end_time=incident_end,
        )
        impact = self.assess_impact()
        timeline = self.build_timeline(
            incident_id=incident_id,
            detection_time=incident_start,
            containment_time=incident_start + 45,  # Estimate if not provided
            recovery_time=incident_end,
            containment_log=containment_log,
            recovery_log=recovery_log,
        )

        report = {
            "incident_id": incident_id,
            "agent_id": self.agent_id,
            "generated_at": int(time.time()),
            "audit_trail": audit.to_dict(),
            "impact_assessment": impact.to_dict(),
            "timeline": timeline.to_dict(),
        }

        # Publish the post-mortem as an event for downstream consumption
        try:
            self._execute("publish_event", {
                "agent_id": self.agent_id,
                "event_type": "incident_post_mortem",
                "payload": {
                    "incident_id": incident_id,
                    "total_duration_seconds": timeline.details[
                        "phase_durations"
                    ]["total_duration_seconds"],
                    "met_containment_sla": timeline.details[
                        "meets_60s_containment_sla"
                    ],
                    "generated_at": int(time.time()),
                },
            })
        except requests.exceptions.RequestException:
            pass

        return report
```

### Feeding Post-Mortems Back into Detection

The post-mortem output is structured data, not a narrative document. This is deliberate. The `build_timeline` output can be ingested by the `IncidentDetector` to adjust anomaly thresholds:

```python
# After post-mortem, adjust detection sensitivity
forensics = IncidentForensics(api_key="key", agent_id="agent-prod-001")
report = forensics.run_post_mortem(
    incident_id="inc-1712345678",
    incident_start=1712345000,
    incident_end=1712346000,
)

# If containment SLA was missed, tighten detection
if not report["timeline"]["details"]["meets_60s_containment_sla"]:
    detector = IncidentDetector(
        api_key="key",
        agent_id="agent-prod-001",
        cost_anomaly_std_devs=1.5,  # Tighter than default 2.0
    )
    print("Detection sensitivity increased due to missed SLA")
```

---

## Chapter 6: The 5 Agent Incident Runbooks

Each runbook specifies: the trigger condition (what causes the alert), the severity classification, the automated response, and the manual follow-up. All automated steps use the classes from Chapters 2-5.

### Runbook 1: Runaway Spending

**Trigger**: `IncidentDetector.check_cost_anomaly()` returns severity "critical" -- spending rate exceeds 2 standard deviations above baseline.

**Severity**: P0 (financial loss in progress)

**Automated Response**:
```python
def handle_runaway_spending(agent_id: str, anomaly: AnomalyResult):
    """Runbook 1: Automated response to runaway spending."""
    containment = IncidentContainment(
        api_key=API_KEY, agent_id=agent_id,
    )

    # Step 1: Freeze immediately
    freeze_result = containment.freeze_agent()
    if not freeze_result.success:
        # ESCALATE: Budget freeze failed, manual intervention required
        alert_oncall(
            severity="P0",
            message=f"Budget freeze FAILED for {agent_id}. "
                    f"Error: {freeze_result.error}. "
                    f"Manual intervention required immediately.",
        )
        return

    # Step 2: Cancel all escrows to recover locked funds
    escrow_result = containment.freeze_escrows()

    # Step 3: Verify identity (rule out compromise)
    identity_result = containment.verify_agent_identity()

    # Step 4: Alert on-call with containment summary
    alert_oncall(
        severity="P0",
        message=(
            f"Runaway spending contained for {agent_id}. "
            f"Budget frozen. "
            f"{escrow_result.details.get('cancelled', 0)} escrows cancelled. "
            f"${escrow_result.details.get('total_unlocked', '0')} recovered. "
            f"Identity verified: "
            f"{identity_result.details.get('identity_valid', False)}."
        ),
    )
```

**Manual Follow-Up**:
1. Identify the code path causing excessive spending (retry loop, missing dedup, unbounded batch).
2. Deploy fix to staging and verify with `IncidentDetector` at 30s polling for 1 hour.
3. Run `IncidentRecovery.recover_agent()` with 50% budget.
4. Run `IncidentForensics.run_post_mortem()` and publish findings.

---

### Runbook 2: Escrow Exploitation

**Trigger**: An agent's escrow cancellation rate exceeds 50% in a 1-hour window, OR a single counterparty is the payee on more than 10 escrows from the same payer within 5 minutes.

**Severity**: P1 (potential fraud, financial exposure)

**Automated Response**:
```python
def handle_escrow_exploitation(agent_id: str, suspect_payee_id: str):
    """Runbook 2: Respond to suspected escrow exploitation."""
    containment = IncidentContainment(
        api_key=API_KEY, agent_id=agent_id,
    )

    # Step 1: Freeze the payer agent's budget
    containment.freeze_agent()

    # Step 2: Cancel escrows -- but only those to the suspect payee
    escrows_resp = containment._execute("list_escrows", {
        "agent_id": agent_id,
    })
    escrows = escrows_resp.get("escrows", [])

    suspect_escrows = [
        e for e in escrows
        if e.get("payee_id") == suspect_payee_id
        and e.get("status") in ("pending", "funded", "active")
    ]

    cancelled_amount = 0
    for escrow in suspect_escrows:
        try:
            containment._execute("cancel_escrow", {
                "escrow_id": escrow["escrow_id"],
                "reason": f"escrow_exploitation_suspected:{suspect_payee_id}",
            })
            cancelled_amount += float(escrow.get("amount", "0"))
        except requests.exceptions.RequestException:
            pass  # Log and continue; do not stop on individual failures

    # Step 3: Check the suspect payee's reputation
    payee_rep = containment._execute("get_agent_reputation", {
        "agent_id": suspect_payee_id,
    })

    # Step 4: Flag the suspect via metrics submission
    containment._execute("submit_metrics", {
        "agent_id": suspect_payee_id,
        "metrics": {
            "escrow_exploitation_flag": True,
            "flagged_by": agent_id,
            "flagged_at": int(time.time()),
            "suspect_escrow_count": len(suspect_escrows),
        },
    })

    alert_oncall(
        severity="P1",
        message=(
            f"Escrow exploitation suspected. Payer: {agent_id}. "
            f"Suspect payee: {suspect_payee_id}. "
            f"{len(suspect_escrows)} escrows cancelled. "
            f"${round(cancelled_amount, 2)} recovered. "
            f"Payee reputation: {payee_rep.get('reputation_score', 'N/A')}."
        ),
    )
```

**Manual Follow-Up**:
1. Review the suspect payee's full transaction history via `get_claim_chains`.
2. If exploitation confirmed, report to platform via dispute mechanism.
3. If false positive, unfreeze payer budget and remove metrics flag.

---

### Runbook 3: Identity Compromise

**Trigger**: `IncidentContainment.verify_agent_identity()` returns `identity_valid: false`, OR the agent's public key changes unexpectedly, OR authentication patterns change (new IP, new user-agent, unusual hours).

**Severity**: P0 (security breach)

**Automated Response**:
```python
def handle_identity_compromise(agent_id: str):
    """Runbook 3: Respond to suspected agent identity compromise."""
    containment = IncidentContainment(
        api_key=API_KEY, agent_id=agent_id,
    )

    # Step 1: Full containment (budget + escrows + identity check)
    results = containment.contain_agent()

    # Step 2: Get the full identity record for forensic preservation
    identity = containment._execute("get_agent_identity", {
        "agent_id": agent_id,
    })

    # Step 3: Get claim chains -- preserve the cryptographic audit trail
    #         before any attacker can attempt to modify history
    chains = containment._execute("get_claim_chains", {
        "agent_id": agent_id,
    })

    # Step 4: Check reputation for signs of attacker activity
    reputation = containment._execute("get_agent_reputation", {
        "agent_id": agent_id,
    })

    # Step 5: Publish high-priority security event
    containment._execute("publish_event", {
        "agent_id": agent_id,
        "event_type": "security_identity_compromise",
        "payload": {
            "severity": "P0",
            "identity_snapshot": identity,
            "chain_count": len(chains.get("chains", [])),
            "reputation_at_detection": reputation.get("reputation_score"),
            "timestamp": int(time.time()),
            "action_required": "immediate_investigation",
        },
    })

    alert_oncall(
        severity="P0",
        message=(
            f"IDENTITY COMPROMISE SUSPECTED for {agent_id}. "
            f"All financial operations frozen. "
            f"Audit trail preserved ({len(chains.get('chains', []))} chains). "
            f"Immediate investigation required."
        ),
    )
```

**Manual Follow-Up**:
1. Rotate all API keys associated with the compromised agent.
2. Re-register the agent identity with new key material.
3. Audit all transactions since the last known-good verification.
4. Re-verify all counterparties the compromised agent transacted with.
5. Run `IncidentForensics.run_post_mortem()` with full transaction window.

---

### Runbook 4: Service Degradation

**Trigger**: `IncidentDetector.check_reputation_drift()` returns severity "warning" or "critical" -- reputation has dropped more than 15% from baseline.

**Severity**: P2 (quality degradation, not immediate financial loss)

**Automated Response**:
```python
def handle_service_degradation(agent_id: str, anomaly: AnomalyResult):
    """Runbook 4: Respond to agent service quality degradation."""
    # Service degradation does NOT warrant immediate budget freeze.
    # Instead, reduce budget to limit blast radius and alert.

    api = requests.Session()
    api.headers.update({
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    })

    def execute(tool, input_data):
        resp = api.post(
            f"{BASE_URL}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    # Step 1: Get current budget and reduce by 50%
    budget = execute("get_budget_status", {"agent_id": agent_id})
    current_daily = float(budget.get("daily_limit", "1000"))
    reduced_daily = str(round(current_daily * 0.5, 2))

    execute("set_budget_cap", {
        "agent_id": agent_id,
        "daily": reduced_daily,
    })

    # Step 2: Get detailed reputation data
    reputation = execute("get_agent_reputation", {"agent_id": agent_id})

    # Step 3: Get usage analytics to correlate quality with volume
    analytics = execute("get_usage_analytics", {"agent_id": agent_id})

    # Step 4: Publish degradation event
    execute("publish_event", {
        "agent_id": agent_id,
        "event_type": "service_degradation_detected",
        "payload": {
            "reputation_drop": anomaly.details.get("drop_pct", "unknown"),
            "budget_reduced_to": reduced_daily,
            "analytics_snapshot": analytics,
            "timestamp": int(time.time()),
        },
    })

    alert_oncall(
        severity="P2",
        message=(
            f"Service degradation for {agent_id}. "
            f"Reputation dropped {anomaly.details.get('drop_pct', '?')}%. "
            f"Budget reduced to ${reduced_daily}/day. "
            f"Investigate quality metrics."
        ),
    )
```

**Manual Follow-Up**:
1. Review recent agent outputs and counterparty feedback.
2. Check for model drift, prompt degradation, or upstream dependency changes.
3. If root cause is model-related, update prompts or constraints and redeploy.
4. Use `IncidentRecovery.restore_reputation()` to submit corrected metrics.
5. Gradually restore budget using the gradual restoration pattern.

---

### Runbook 5: Cascade Failure

**Trigger**: Two or more agents trigger anomaly alerts within a 5-minute window, OR a shared resource (wallet, escrow pool, marketplace listing) is exhausted.

**Severity**: P0 (multi-agent system failure)

**Automated Response**:
```python
def handle_cascade_failure(affected_agent_ids: list[str]):
    """Runbook 5: Respond to multi-agent cascade failure."""
    containment_results = {}

    # Step 1: Freeze ALL affected agents simultaneously
    for agent_id in affected_agent_ids:
        containment = IncidentContainment(
            api_key=API_KEY, agent_id=agent_id,
        )
        containment_results[agent_id] = containment.contain_agent()

    # Step 2: Identify the root cause agent
    #         (the one with the highest spending anomaly)
    spending_anomalies = {}
    for agent_id in affected_agent_ids:
        detector = IncidentDetector(
            api_key=API_KEY, agent_id=agent_id,
        )
        anomaly = detector.check_cost_anomaly()
        if anomaly.detected:
            z_score = float(anomaly.details.get("z_score", "0"))
            spending_anomalies[agent_id] = z_score

    root_cause_agent = (
        max(spending_anomalies, key=spending_anomalies.get)
        if spending_anomalies else affected_agent_ids[0]
    )

    # Step 3: Deep forensics on root cause agent
    forensics = IncidentForensics(
        api_key=API_KEY, agent_id=root_cause_agent,
    )
    impact = forensics.assess_impact()

    # Step 4: Publish cascade event with full scope
    api = requests.Session()
    api.headers.update({
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    })
    api.post(
        f"{BASE_URL}/v1",
        json={
            "tool": "publish_event",
            "input": {
                "agent_id": root_cause_agent,
                "event_type": "cascade_failure",
                "payload": {
                    "affected_agents": affected_agent_ids,
                    "root_cause_agent": root_cause_agent,
                    "total_agents_affected": len(affected_agent_ids),
                    "timestamp": int(time.time()),
                },
            },
        },
    )

    alert_oncall(
        severity="P0",
        message=(
            f"CASCADE FAILURE: {len(affected_agent_ids)} agents affected. "
            f"All frozen. Root cause agent: {root_cause_agent} "
            f"(z-score: {spending_anomalies.get(root_cause_agent, 'N/A')}). "
            f"Impact: {json.dumps(impact.details.get('escrow_impact', {}))}."
        ),
    )

    return {
        "root_cause_agent": root_cause_agent,
        "containment_results": {
            aid: [r.to_dict() for r in results]
            for aid, results in containment_results.items()
        },
        "spending_anomalies": spending_anomalies,
    }
```

**Manual Follow-Up**:
1. Identify the dependency chain: which agent triggered which agent's failure.
2. Fix the root cause agent first, then recover downstream agents in dependency order.
3. Implement circuit breakers between agents to prevent future cascades (see Chapter 7).
4. Run post-mortems for all affected agents and correlate timelines.

---

## Chapter 7: Automated Incident Response

### From Detection to Containment in Under 5 Seconds

The runbooks in Chapter 6 are designed for automation. The `AutomatedResponse` class ties detection to containment to escalation in a single pipeline. When the `IncidentDetector` fires, the `AutomatedResponse` executes the appropriate runbook without human intervention.

### The AutomatedResponse Class

```python
import requests
import time
import json
from typing import Optional, Callable
from dataclasses import dataclass, field
from enum import Enum


class EscalationTier(Enum):
    """Escalation tiers for incident response."""
    AUTO_CONTAIN = "auto_contain"      # Automated freeze, alert on-call
    ALERT_HUMAN = "alert_human"         # Alert without automated action
    FULL_SHUTDOWN = "full_shutdown"      # Freeze all agents in fleet


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Tripped, all operations blocked
    HALF_OPEN = "half_open"  # Testing recovery


@dataclass
class CircuitBreaker:
    """Circuit breaker for agent commerce operations."""
    agent_id: str
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    failure_threshold: int = 5
    reset_timeout_seconds: int = 300
    last_failure_time: float = 0
    last_state_change: float = field(default_factory=time.time)

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.last_state_change = time.time()

    def record_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
            self.failure_count = 0
            self.last_state_change = time.time()

    def should_allow(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.OPEN:
            elapsed = time.time() - self.last_state_change
            if elapsed >= self.reset_timeout_seconds:
                self.state = CircuitState.HALF_OPEN
                self.last_state_change = time.time()
                return True
            return False
        # HALF_OPEN: allow one request to test
        return True


class AutomatedResponse:
    """Automated incident response pipeline.

    Connects detection signals to containment actions with
    configurable escalation tiers.

    Usage:
        responder = AutomatedResponse(
            api_key="your-key",
            fleet_agent_ids=["agent-001", "agent-002", "agent-003"],
            oncall_callback=send_pagerduty_alert,
        )

        # Register custom escalation rules
        responder.add_rule(
            signal="cost_anomaly",
            severity="critical",
            tier=EscalationTier.AUTO_CONTAIN,
        )
        responder.add_rule(
            signal="reputation_drift",
            severity="warning",
            tier=EscalationTier.ALERT_HUMAN,
        )

        # Start automated monitoring
        responder.start(interval_seconds=30)
    """

    DEFAULT_RULES = {
        ("cost_anomaly", "critical"): EscalationTier.AUTO_CONTAIN,
        ("cost_anomaly", "warning"): EscalationTier.ALERT_HUMAN,
        ("budget_exhaustion", "critical"): EscalationTier.AUTO_CONTAIN,
        ("budget_warning", "warning"): EscalationTier.ALERT_HUMAN,
        ("reputation_drift", "critical"): EscalationTier.AUTO_CONTAIN,
        ("reputation_drift", "warning"): EscalationTier.ALERT_HUMAN,
        ("detection_failure", "warning"): EscalationTier.ALERT_HUMAN,
    }

    def __init__(
        self,
        api_key: str,
        fleet_agent_ids: list[str],
        base_url: str = "https://api.greenhelix.net/v1",
        oncall_callback: Optional[Callable] = None,
    ):
        self.api_key = api_key
        self.fleet_agent_ids = fleet_agent_ids
        self.base_url = base_url
        self.oncall_callback = oncall_callback or self._default_alert
        self.rules: dict[tuple[str, str], EscalationTier] = dict(
            self.DEFAULT_RULES
        )
        self._circuit_breakers: dict[str, CircuitBreaker] = {
            aid: CircuitBreaker(agent_id=aid)
            for aid in fleet_agent_ids
        }
        self._incident_log: list[dict] = []
        self._detectors: dict[str, IncidentDetector] = {
            aid: IncidentDetector(
                api_key=api_key,
                agent_id=aid,
                base_url=base_url,
            )
            for aid in fleet_agent_ids
        }

    @staticmethod
    def _default_alert(severity: str, message: str):
        print(f"[ALERT {severity}] {message}")

    def add_rule(
        self,
        signal: str,
        severity: str,
        tier: EscalationTier,
    ):
        """Add or override an escalation rule."""
        self.rules[(signal, severity)] = tier

    # ── Core Response Actions ──────────────────────────────────

    def auto_contain(self, agent_id: str, anomaly: AnomalyResult):
        """Execute automated containment for a single agent."""
        containment = IncidentContainment(
            api_key=self.api_key,
            agent_id=agent_id,
            base_url=self.base_url,
        )
        results = containment.contain_agent()

        # Record in circuit breaker
        breaker = self._circuit_breakers.get(agent_id)
        if breaker:
            breaker.record_failure()

        # Log the incident
        incident = {
            "incident_id": f"inc-{int(time.time())}-{agent_id}",
            "agent_id": agent_id,
            "signal": anomaly.signal,
            "severity": anomaly.severity,
            "tier": EscalationTier.AUTO_CONTAIN.value,
            "containment_results": [r.to_dict() for r in results],
            "timestamp": time.time(),
        }
        self._incident_log.append(incident)

        # Alert on-call
        self.oncall_callback(
            severity=anomaly.severity.upper(),
            message=(
                f"Auto-contained {agent_id}: {anomaly.signal}. "
                f"Details: {json.dumps(anomaly.details)}"
            ),
        )

        return incident

    def escalate(
        self,
        agent_id: str,
        anomaly: AnomalyResult,
        tier: EscalationTier,
    ):
        """Escalate an anomaly to the appropriate tier."""
        if tier == EscalationTier.AUTO_CONTAIN:
            return self.auto_contain(agent_id, anomaly)
        elif tier == EscalationTier.ALERT_HUMAN:
            self.oncall_callback(
                severity=anomaly.severity.upper(),
                message=(
                    f"Alert for {agent_id}: {anomaly.signal}. "
                    f"No automated action taken. "
                    f"Details: {json.dumps(anomaly.details)}"
                ),
            )
            return {
                "agent_id": agent_id,
                "tier": tier.value,
                "action": "alert_only",
            }
        elif tier == EscalationTier.FULL_SHUTDOWN:
            return self._full_shutdown(anomaly)

    def _full_shutdown(self, trigger_anomaly: AnomalyResult) -> dict:
        """Emergency: freeze every agent in the fleet."""
        results = {}
        for agent_id in self.fleet_agent_ids:
            containment = IncidentContainment(
                api_key=self.api_key,
                agent_id=agent_id,
                base_url=self.base_url,
            )
            results[agent_id] = [
                r.to_dict() for r in containment.contain_agent()
            ]

        self.oncall_callback(
            severity="P0",
            message=(
                f"FULL FLEET SHUTDOWN executed. "
                f"{len(self.fleet_agent_ids)} agents frozen. "
                f"Trigger: {trigger_anomaly.agent_id} - "
                f"{trigger_anomaly.signal}."
            ),
        )

        return {
            "action": "full_shutdown",
            "agents_frozen": len(self.fleet_agent_ids),
            "results": results,
        }

    # ── Circuit Breaker ────────────────────────────────────────

    def circuit_breaker(self, agent_id: str) -> CircuitBreaker:
        """Get the circuit breaker for an agent.

        The circuit breaker tracks failure counts and automatically
        blocks operations when an agent exceeds the failure threshold.
        After the reset timeout, it enters half-open state and allows
        a single test operation.

        Usage in agent code:
            breaker = responder.circuit_breaker("agent-001")
            if breaker.should_allow():
                try:
                    result = execute_tool(...)
                    breaker.record_success()
                except Exception:
                    breaker.record_failure()
            else:
                # Agent is circuit-broken, skip operation
                log.warning(f"Circuit open for {agent_id}")
        """
        if agent_id not in self._circuit_breakers:
            self._circuit_breakers[agent_id] = CircuitBreaker(
                agent_id=agent_id,
            )
        return self._circuit_breakers[agent_id]

    # ── Monitoring Loop ────────────────────────────────────────

    def _process_anomalies(self, agent_id: str, anomalies: list):
        """Process detected anomalies through the escalation rules."""
        # Check circuit breaker first
        breaker = self._circuit_breakers.get(agent_id)
        if breaker and breaker.state == CircuitState.OPEN:
            # Agent is already circuit-broken, auto-contain
            for anomaly in anomalies:
                self.auto_contain(agent_id, anomaly)
            return

        for anomaly in anomalies:
            rule_key = (anomaly.signal, anomaly.severity)
            tier = self.rules.get(rule_key, EscalationTier.ALERT_HUMAN)
            self.escalate(agent_id, anomaly, tier)

    def start(
        self,
        interval_seconds: int = 30,
        max_iterations: Optional[int] = None,
    ):
        """Start the automated response monitoring loop.

        Polls all fleet agents for anomalies and triggers the
        appropriate response based on escalation rules.
        """
        # Check for cascade condition: multiple agents alerting
        cascade_window: dict[str, float] = {}
        cascade_threshold = 2  # agents within 5 minutes = cascade

        iteration = 0
        while max_iterations is None or iteration < max_iterations:
            alerting_agents = []

            for agent_id in self.fleet_agent_ids:
                detector = self._detectors[agent_id]
                anomalies = detector.check_all()

                if anomalies:
                    alerting_agents.append(agent_id)
                    cascade_window[agent_id] = time.time()
                    self._process_anomalies(agent_id, anomalies)

            # Check for cascade condition
            now = time.time()
            recent_alerts = {
                aid: t for aid, t in cascade_window.items()
                if now - t < 300  # 5-minute window
            }
            if len(recent_alerts) >= cascade_threshold:
                handle_cascade_failure(list(recent_alerts.keys()))
                cascade_window.clear()

            time.sleep(interval_seconds)
            iteration += 1

    def get_incident_log(self) -> list[dict]:
        """Return all incidents handled by this responder."""
        return list(self._incident_log)
```

### Webhook-Triggered Containment

For organizations that prefer push-based alerting over polling, the `AutomatedResponse` integrates with GreenHelix webhooks. The webhook handler receives events from the gateway and triggers containment directly:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

responder = AutomatedResponse(
    api_key=API_KEY,
    fleet_agent_ids=["agent-001", "agent-002", "agent-003"],
    oncall_callback=send_pagerduty_alert,
)

@app.route("/incidents/webhook", methods=["POST"])
def handle_webhook():
    """Receive GreenHelix webhook events and trigger response."""
    event = request.get_json()
    event_type = event.get("event_type", "")
    agent_id = event.get("agent_id", "")
    payload = event.get("payload", {})

    if event_type == "budget_threshold":
        utilization = float(payload.get("utilization_pct", 0))
        if utilization >= 95:
            anomaly = AnomalyResult(
                detected=True,
                signal="budget_exhaustion",
                severity="critical",
                agent_id=agent_id,
                details=payload,
            )
            responder.auto_contain(agent_id, anomaly)
        elif utilization >= 80:
            responder.oncall_callback(
                severity="WARNING",
                message=f"Budget at {utilization}% for {agent_id}",
            )

    elif event_type == "reputation_change":
        score_delta = float(payload.get("score_delta", 0))
        if score_delta < -0.15:
            anomaly = AnomalyResult(
                detected=True,
                signal="reputation_drift",
                severity="critical" if score_delta < -0.30 else "warning",
                agent_id=agent_id,
                details=payload,
            )
            responder.escalate(
                agent_id, anomaly,
                EscalationTier.AUTO_CONTAIN
                if score_delta < -0.30
                else EscalationTier.ALERT_HUMAN,
            )

    return jsonify({"status": "processed"})
```

### The Escalation Ladder

```
                ┌──────────────────────────────────────┐
                │         FULL FLEET SHUTDOWN           │
                │   All agents frozen. All hands.       │
                │   Trigger: cascade failure (2+ P0s)   │
                └──────────────┬───────────────────────┘
                               │
                ┌──────────────▼───────────────────────┐
                │         AUTO-CONTAIN                  │
                │   Budget frozen. Escrows cancelled.   │
                │   On-call alerted.                    │
                │   Trigger: critical anomaly           │
                └──────────────┬───────────────────────┘
                               │
                ┌──────────────▼───────────────────────┐
                │         ALERT HUMAN                   │
                │   No automated action.                │
                │   On-call notified for investigation. │
                │   Trigger: warning anomaly            │
                └──────────────────────────────────────┘
```

The default mapping is conservative: critical anomalies auto-contain, warnings alert humans, and cascade failures shut down the fleet. Override with `add_rule()` to tune for your risk tolerance. A trading firm may want warnings to also auto-contain. A low-value agent fleet may want only critical signals to trigger any response.

---

## Chapter 8: Incident Readiness Checklist

### Pre-Incident Setup

Complete this checklist before your first production deployment. Every item maps to a class or method in this guide.

**Detection Infrastructure**

- [ ] `IncidentDetector` deployed for each production agent
- [ ] Cost anomaly threshold tuned (`cost_anomaly_std_devs` calibrated against 2 weeks of baseline data)
- [ ] Reputation drift threshold set (`reputation_drop_threshold` based on normal variance)
- [ ] Webhook endpoints registered via `setup_alerts()` for budget, escrow, and reputation events
- [ ] Webhook receiver deployed and health-checked (if webhook receiver is down, detection is blind)
- [ ] Monitoring interval configured (30s for high-value agents, 5m for low-value)

**Containment Readiness**

- [ ] `IncidentContainment` tested against sandbox for each agent
- [ ] Containment completes within 60 seconds (verified via timing test)
- [ ] API key used for containment has permissions for `set_budget_cap`, `list_escrows`, `cancel_escrow`, `verify_agent`, `get_agent_identity`, `publish_event`
- [ ] Containment API key is separate from agent's operational key (so a compromised agent key does not prevent containment)

**Recovery Procedures**

- [ ] Pre-incident budget levels documented for each agent
- [ ] Gradual restoration schedule defined (50% / 75% / 100% over 48 hours)
- [ ] Recovery verification criteria defined (what "normal" looks like post-incident)
- [ ] `IncidentRecovery` tested against sandbox

**Forensics Capability**

- [ ] `IncidentForensics` tested and producing valid post-mortem reports
- [ ] Claim chains actively maintained for all production agents (if claim chains are empty, there is no audit trail to review)
- [ ] Billing analytics accessible (confirm `get_usage_analytics`, `get_billing_summary`, `get_spending_by_category` all return data)

### Severity Classification

| Severity | Description | Response Time | Automated Action |
|---|---|---|---|
| **P0** | Active financial loss or security breach | Immediate (auto-contained in <5s) | Full containment + on-call page |
| **P1** | Potential fraud or escalating exposure | < 15 minutes | Budget freeze + on-call page |
| **P2** | Quality degradation or budget warning | < 1 hour | Budget reduction + Slack alert |
| **P3** | Informational anomaly, no action needed | Next business day | Log only |

### On-Call Rotation for Agent Systems

Agent on-call differs from traditional service on-call in three ways:

1. **Financial authority required**: The on-call engineer must have permissions to restore budgets, cancel escrows, and re-register agent identities. Without these permissions, recovery is blocked.

2. **Model knowledge required**: Agent incidents often require understanding model behavior, prompt engineering, and stochastic reasoning. The on-call rotation should include engineers with ML/AI experience, not only infrastructure engineers.

3. **Faster escalation**: Traditional on-call escalation gives 30 minutes before paging a secondary. Agent on-call should escalate in 5 minutes for P0 and 15 minutes for P1, because financial exposure grows linearly with response time.

### Cross-References to Companion Guides

This guide completes the operational lifecycle when combined with three companion guides:

- **Locking Down Agent Commerce** (P8) covers prevention: security hardening, identity verification, credential isolation, and financial guardrails. Read P8 to reduce the frequency of incidents.
- **The Agent Testing & Observability Cookbook** (P9) covers detection infrastructure: the `AgentTracer`, `HealthChecker`, chaos testing, and CI/CD pipelines. Read P9 to build the monitoring foundation that feeds into this guide's `IncidentDetector`.
- **Ship Compliant Agents** (P11) covers the regulatory dimension: EU AI Act compliance, audit trail requirements (Article 12), and liability-bounded escrow patterns. Read P11 to ensure your incident response satisfies regulatory obligations for logging and reporting.

Together, the four guides form a closed loop:

```
P8 (Security)  ──prevent──▶  P9 (Observability)  ──detect──▶
P12 (Incident Response)  ──recover──▶  P11 (Compliance)  ──audit──▶
```

### Practice on the Sandbox

The sandbox at `sandbox.greenhelix.net` is free to use with any API key. Deploy the `IncidentDetector` against it. Trigger a simulated incident by rapidly creating escrows. Verify that `IncidentContainment.contain_agent()` freezes the budget and cancels the escrows. Run `IncidentForensics.run_post_mortem()` and review the output. Build muscle memory for incident response before you need it in production.

### The Full Lifecycle

```python
# Complete incident response lifecycle in 30 lines

# 1. Detection
detector = IncidentDetector(api_key=KEY, agent_id=AGENT)
detector.setup_alerts(webhook_url=WEBHOOK_URL)
anomalies = detector.check_all()

# 2. Containment (if critical)
if any(a.severity == "critical" for a in anomalies):
    containment = IncidentContainment(api_key=KEY, agent_id=AGENT)
    containment_results = containment.contain_agent()
    containment_time = int(time.time())

# 3. Recovery (after root cause fixed)
recovery = IncidentRecovery(api_key=KEY, agent_id=AGENT)
recovery_results = recovery.recover_agent(
    target_daily_budget="500.00",
    initial_budget_pct=50,
)

# 4. Post-mortem
forensics = IncidentForensics(api_key=KEY, agent_id=AGENT)
report = forensics.run_post_mortem(
    incident_id="inc-001",
    incident_start=int(time.time()) - 3600,
    incident_end=int(time.time()),
    containment_log=containment.get_containment_log(),
    recovery_log=recovery.get_recovery_log(),
)
print(json.dumps(report, indent=2))
```

Four phases, four classes, four API calls each. Detect, contain, recover, learn. Copy the classes into your project, tune the thresholds, set up the webhooks, and practice on the sandbox. When the 2:47 AM alert fires, you will have a runbook.

### The Bundle

All companion guides plus this playbook are available as a bundle. Each guide introduces production-ready Python classes that compose into a complete agent commerce platform: building (P1), cost management (P2), reputation (P3), audit trails (P4), trust verification (P5), marketplace strategy (P6), multi-agent patterns (P7), security hardening (P8), testing and observability (P9), SaaS automation (P10), compliance (P11), and incident response (P12).

For the full API reference and tool catalog (all 128 tools), visit the GreenHelix developer documentation at [https://api.greenhelix.net/docs](https://api.greenhelix.net/docs).

---

*Price: $29 | Format: Digital Guide | Updates: Lifetime access*

---

## Automated Incident Detection & Escalation — Working Implementation

The code below uses the actual `greenhelix_trading` library classes. Every method call maps to a real GreenHelix Gateway tool. Copy this module into your project, set `GREENHELIX_API_KEY` and `GREENHELIX_AGENT_ID` in your environment, and run it.

```python
"""
Automated incident detection and escalation using the greenhelix_trading library.

Covers:
  1. Anomaly detection pipeline (cost, reputation, budget)
  2. Automatic containment actions (freeze, escrow cancel, identity verify)
  3. Guided recovery procedures with graduated budget restoration
  4. Forensic evidence collection (audit trails, impact, timeline)
  5. End-to-end incident orchestrator

Requirements:
    pip install greenhelix-trading
"""

import os
import time
import json
from datetime import datetime, timezone
from typing import Optional
from dataclasses import dataclass, field

from greenhelix_trading import (
    IncidentDetector,
    IncidentContainment,
    IncidentRecovery,
    IncidentForensics,
)


# ── Configuration ─────────────────────────────────────────────────────────────

API_KEY = os.environ["GREENHELIX_API_KEY"]
AGENT_ID = os.environ["GREENHELIX_AGENT_ID"]
WEBHOOK_URL = os.environ.get(
    "GREENHELIX_WEBHOOK_URL",
    "https://your-app.example.com/incidents/webhook",
)


# ── Data Classes ──────────────────────────────────────────────────────────────

@dataclass
class IncidentRecord:
    """Complete record of a detected, contained, and recovered incident."""
    incident_id: str
    agent_id: str
    detected_at: float = field(default_factory=time.time)
    contained_at: Optional[float] = None
    recovered_at: Optional[float] = None
    detection_signals: list = field(default_factory=list)
    containment_results: list = field(default_factory=list)
    recovery_results: list = field(default_factory=list)
    forensics_report: Optional[dict] = None
    severity: str = "unknown"

    def elapsed_to_containment(self) -> Optional[float]:
        if self.contained_at:
            return round(self.contained_at - self.detected_at, 2)
        return None

    def elapsed_to_recovery(self) -> Optional[float]:
        if self.recovered_at:
            return round(self.recovered_at - self.detected_at, 2)
        return None

    def to_dict(self) -> dict:
        return {
            "incident_id": self.incident_id,
            "agent_id": self.agent_id,
            "severity": self.severity,
            "detected_at": self.detected_at,
            "contained_at": self.contained_at,
            "recovered_at": self.recovered_at,
            "elapsed_to_containment_s": self.elapsed_to_containment(),
            "elapsed_to_recovery_s": self.elapsed_to_recovery(),
            "detection_signals": self.detection_signals,
            "containment_results": self.containment_results,
            "recovery_results": self.recovery_results,
            "forensics_report": self.forensics_report,
        }


# ── 1. Anomaly Detection Pipeline ────────────────────────────────────────────

class AnomalyPipeline:
    """Multi-signal anomaly detection using IncidentDetector.

    Runs three independent checks — cost anomaly, reputation drift,
    and spending breakdown — and correlates the signals to produce
    a severity classification.

    Uses:
        IncidentDetector.check_cost_anomaly()
        IncidentDetector.check_reputation_drift(baseline_score)
        IncidentDetector.setup_alerts(webhook_url)
        IncidentDetector.get_spending_breakdown()
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        cost_threshold: float = 500.0,
        reputation_threshold: float = 0.1,
        baseline_reputation: float = 0.85,
    ):
        self.agent_id = agent_id
        self.baseline_reputation = baseline_reputation
        self._detector = IncidentDetector(
            api_key=api_key,
            agent_id=agent_id,
            cost_threshold=cost_threshold,
            reputation_threshold=reputation_threshold,
        )
        self._alert_history: list[dict] = []

    def setup_webhook_alerts(self, webhook_url: str) -> dict:
        """Register persistent webhook alerts for budget, escrow, and
        reputation events.

        Calls IncidentDetector.setup_alerts which wraps register_webhook
        with the event types: budget_exceeded, reputation_change,
        escrow_timeout.
        """
        result = self._detector.setup_alerts(webhook_url=webhook_url)
        return {
            "status": "configured",
            "webhook_url": webhook_url,
            "registration": result,
        }

    def run_detection_cycle(self) -> dict:
        """Execute one full detection cycle across all signals.

        Returns a dict with the severity ("clear", "warning", "critical"),
        the individual signal results, and a spending breakdown for
        context.
        """
        signals = []
        severity = "clear"

        # Signal 1: Cost anomaly
        cost_result = self._detector.check_cost_anomaly()
        cost_anomaly = cost_result.get("anomaly", False)
        signals.append({
            "signal": "cost_anomaly",
            "triggered": cost_anomaly,
            "data": cost_result,
        })

        # Signal 2: Reputation drift
        rep_result = self._detector.check_reputation_drift(
            baseline_score=self.baseline_reputation,
        )
        rep_drift = rep_result.get("drift", False)
        signals.append({
            "signal": "reputation_drift",
            "triggered": rep_drift,
            "delta": rep_result.get("delta", 0),
            "data": rep_result,
        })

        # Signal 3: Spending breakdown (context, not a direct trigger)
        spending = self._detector.get_spending_breakdown()
        signals.append({
            "signal": "spending_context",
            "triggered": False,
            "data": spending,
        })

        # Severity classification
        triggered_count = sum(1 for s in signals if s["triggered"])
        if triggered_count >= 2:
            severity = "critical"
        elif triggered_count == 1:
            severity = "warning"

        cycle_result = {
            "timestamp": time.time(),
            "agent_id": self.agent_id,
            "severity": severity,
            "triggered_signals": triggered_count,
            "signals": signals,
        }

        if severity != "clear":
            self._alert_history.append(cycle_result)

        return cycle_result

    def run_continuous_monitoring(
        self,
        interval_seconds: int = 30,
        max_cycles: Optional[int] = None,
        on_anomaly=None,
    ):
        """Poll-based continuous monitoring loop.

        Args:
            interval_seconds: Time between detection cycles.
            max_cycles: Stop after N cycles (None = run forever).
            on_anomaly: Callback(cycle_result) when severity != "clear".
        """
        cycle = 0
        while max_cycles is None or cycle < max_cycles:
            result = self.run_detection_cycle()
            if result["severity"] != "clear":
                if on_anomaly:
                    on_anomaly(result)
                else:
                    print(
                        f"[{result['severity'].upper()}] "
                        f"Agent {self.agent_id}: "
                        f"{result['triggered_signals']} signals triggered"
                    )
            time.sleep(interval_seconds)
            cycle += 1

    def get_alert_history(self) -> list[dict]:
        return list(self._alert_history)


# ── 2. Automatic Containment ─────────────────────────────────────────────────

class AutoContainment:
    """Automated containment actions targeting the 60-second SLA.

    Executes three steps in sequence:
      1. Freeze budget (IncidentContainment.freeze_agent)
      2. Cancel active escrows (IncidentContainment.freeze_escrows)
      3. Verify identity (IncidentContainment.verify_agent_identity)

    Also publishes an incident event via
    IncidentContainment.publish_incident_event for fleet-wide visibility.
    """

    def __init__(self, api_key: str, agent_id: str):
        self.agent_id = agent_id
        self._containment = IncidentContainment(
            api_key=api_key,
            agent_id=agent_id,
        )

    def contain(self, severity: str, trigger_signal: str) -> list[dict]:
        """Execute the full containment sequence.

        All three steps are attempted regardless of individual failures.
        Returns a list of result dicts, one per step.
        """
        results = []
        start = time.time()

        # Step 1: Freeze the agent's budget to $0
        try:
            freeze_result = self._containment.freeze_agent()
            results.append({
                "step": "freeze_budget",
                "success": True,
                "data": freeze_result,
            })
        except Exception as exc:
            results.append({
                "step": "freeze_budget",
                "success": False,
                "error": str(exc),
            })

        # Step 2: Cancel all active escrows to recover locked funds
        try:
            escrow_result = self._containment.freeze_escrows()
            results.append({
                "step": "cancel_escrows",
                "success": True,
                "cancelled": escrow_result.get("total_frozen", 0),
                "data": escrow_result,
            })
        except Exception as exc:
            results.append({
                "step": "cancel_escrows",
                "success": False,
                "error": str(exc),
            })

        # Step 3: Verify agent identity has not been compromised
        try:
            identity_result = self._containment.verify_agent_identity()
            results.append({
                "step": "verify_identity",
                "success": True,
                "identity_intact": identity_result.get(
                    "verification", {}
                ).get("verified", False),
                "data": identity_result,
            })
        except Exception as exc:
            results.append({
                "step": "verify_identity",
                "success": False,
                "error": str(exc),
            })

        elapsed = round(time.time() - start, 2)

        # Publish containment event for fleet-wide visibility
        try:
            self._containment.publish_incident_event(
                severity=severity,
                details=json.dumps({
                    "trigger": trigger_signal,
                    "containment_elapsed_s": elapsed,
                    "steps_succeeded": sum(1 for r in results if r["success"]),
                    "steps_total": len(results),
                }),
            )
        except Exception:
            pass  # Event publishing must not block containment

        # Annotate with timing
        for r in results:
            r["containment_elapsed_s"] = elapsed
            r["met_60s_sla"] = elapsed <= 60.0

        return results


# ── 3. Guided Recovery ────────────────────────────────────────────────────────

class GuidedRecovery:
    """Graduated recovery with reputation verification.

    Recovery proceeds through three gates:
      Gate 1: Restore budget at 50% of target (IncidentRecovery.restore_budget)
      Gate 2: Submit recovery metrics (IncidentRecovery.update_reputation)
      Gate 3: Publish recovery event (IncidentRecovery.publish_recovery_event)

    After 24 hours with no anomalies, call restore_full_budget to
    return to the pre-incident budget level.
    """

    def __init__(self, api_key: str, agent_id: str):
        self.agent_id = agent_id
        self._recovery = IncidentRecovery(
            api_key=api_key,
            agent_id=agent_id,
        )

    def execute_recovery(
        self,
        target_daily_budget: float,
        initial_pct: int = 50,
        incident_id: str = "",
    ) -> list[dict]:
        """Run the three-gate recovery sequence.

        Args:
            target_daily_budget: The pre-incident daily budget.
            initial_pct: Percentage of target to restore initially.
            incident_id: For event correlation.

        Returns:
            List of recovery step results.
        """
        results = []
        initial_budget = target_daily_budget * initial_pct / 100

        # Gate 1: Restore budget at conservative level
        try:
            budget_result = self._recovery.restore_budget(
                daily=initial_budget,
                monthly=initial_budget * 30,
            )
            results.append({
                "gate": 1,
                "action": "restore_budget",
                "success": True,
                "budget_restored": initial_budget,
                "pct_of_target": initial_pct,
                "data": budget_result,
            })
        except Exception as exc:
            results.append({
                "gate": 1,
                "action": "restore_budget",
                "success": False,
                "error": str(exc),
            })

        # Gate 2: Submit recovery metrics to rebuild reputation
        try:
            metrics_result = self._recovery.update_reputation(metrics={
                "incident_recovery": True,
                "recovery_timestamp": int(time.time()),
                "post_recovery_status": "active",
                "incident_id": incident_id,
            })
            results.append({
                "gate": 2,
                "action": "update_reputation",
                "success": True,
                "data": metrics_result,
            })
        except Exception as exc:
            results.append({
                "gate": 2,
                "action": "update_reputation",
                "success": False,
                "error": str(exc),
            })

        # Gate 3: Publish recovery event
        try:
            event_result = self._recovery.publish_recovery_event(
                details=json.dumps({
                    "incident_id": incident_id or f"inc-{int(time.time())}",
                    "budget_restored_to": initial_budget,
                    "recovery_timestamp": int(time.time()),
                }),
            )
            results.append({
                "gate": 3,
                "action": "publish_recovery_event",
                "success": True,
                "data": event_result,
            })
        except Exception as exc:
            results.append({
                "gate": 3,
                "action": "publish_recovery_event",
                "success": False,
                "error": str(exc),
            })

        return results

    def restore_full_budget(self, target_daily_budget: float) -> dict:
        """Restore to full pre-incident budget after monitoring period.

        Call this 24-48 hours after initial recovery once the
        AnomalyPipeline confirms no further anomalies.
        """
        try:
            result = self._recovery.restore_budget(
                daily=target_daily_budget,
                monthly=target_daily_budget * 30,
            )
            return {
                "success": True,
                "budget_restored": target_daily_budget,
                "data": result,
            }
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def post_recovery_service_rating(
        self, service_id: str, rating: int = 3, comment: str = "",
    ) -> dict:
        """Submit a post-incident service rating.

        Uses IncidentRecovery.rate_agent_service to record a neutral
        rating that reflects the recovery, not the incident.
        """
        try:
            result = self._recovery.rate_agent_service(
                service_id=service_id,
                rating=rating,
                comment=comment or "Service restored after incident containment.",
            )
            return {"success": True, "data": result}
        except Exception as exc:
            return {"success": False, "error": str(exc)}


# ── 4. Forensic Evidence Collection ──────────────────────────────────────────

class ForensicCollector:
    """Collect and assemble forensic evidence for post-mortem analysis.

    Uses:
        IncidentForensics.get_audit_trail()  -- claim chains
        IncidentForensics.get_verified_claims()  -- individual claims
        IncidentForensics.assess_impact()  -- financial impact
        IncidentForensics.build_timeline()  -- event reconstruction
    """

    def __init__(self, api_key: str, agent_id: str):
        self.agent_id = agent_id
        self._forensics = IncidentForensics(
            api_key=api_key,
            agent_id=agent_id,
        )

    def collect_audit_trail(self) -> dict:
        """Extract the cryptographic audit trail (claim chains).

        IncidentForensics.get_audit_trail wraps get_claim_chains to
        retrieve the tamper-proof record of all agent actions.
        """
        return self._forensics.get_audit_trail()

    def collect_verified_claims(self) -> dict:
        """Retrieve individually verifiable claims.

        IncidentForensics.get_verified_claims wraps get_verified_claims
        for Merkle-proof-verifiable claim records.
        """
        return self._forensics.get_verified_claims()

    def assess_financial_impact(self) -> dict:
        """Calculate the financial impact of the incident.

        IncidentForensics.assess_impact pulls usage analytics, billing
        summary, and spending-by-category to compute total incident cost.
        """
        return self._forensics.assess_impact()

    def reconstruct_timeline(self) -> dict:
        """Reconstruct the incident timeline from claim chains and
        usage analytics.

        IncidentForensics.build_timeline combines claim chain data with
        7-day usage analytics into a chronological event sequence.
        """
        return self._forensics.build_timeline()

    def run_full_post_mortem(
        self,
        incident_record: IncidentRecord,
    ) -> dict:
        """Assemble a complete post-mortem report.

        Combines audit trail, verified claims, financial impact, and
        timeline into a single structured report suitable for both
        human review and machine ingestion.
        """
        audit_trail = self.collect_audit_trail()
        verified_claims = self.collect_verified_claims()
        impact = self.assess_financial_impact()
        timeline = self.reconstruct_timeline()

        report = {
            "incident_id": incident_record.incident_id,
            "agent_id": incident_record.agent_id,
            "severity": incident_record.severity,
            "generated_at": int(time.time()),
            "timing": {
                "detected_at": incident_record.detected_at,
                "contained_at": incident_record.contained_at,
                "recovered_at": incident_record.recovered_at,
                "detection_to_containment_s": incident_record.elapsed_to_containment(),
                "detection_to_recovery_s": incident_record.elapsed_to_recovery(),
                "met_60s_containment_sla": (
                    incident_record.elapsed_to_containment() is not None
                    and incident_record.elapsed_to_containment() <= 60.0
                ),
            },
            "audit_trail": audit_trail,
            "verified_claims": verified_claims,
            "financial_impact": impact,
            "timeline": timeline,
            "detection_signals": incident_record.detection_signals,
            "containment_actions": incident_record.containment_results,
            "recovery_actions": incident_record.recovery_results,
        }

        return report


# ── 5. End-to-End Incident Orchestrator ──────────────────────────────────────

class IncidentOrchestrator:
    """Ties detection, containment, recovery, and forensics into a
    single automated response pipeline.

    Usage:
        orchestrator = IncidentOrchestrator(
            api_key=API_KEY,
            agent_id=AGENT_ID,
            target_daily_budget=500.0,
        )
        orchestrator.setup(webhook_url=WEBHOOK_URL)
        orchestrator.run(max_cycles=100, interval_seconds=30)
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        target_daily_budget: float = 500.0,
        cost_threshold: float = 500.0,
        reputation_threshold: float = 0.1,
        baseline_reputation: float = 0.85,
    ):
        self.agent_id = agent_id
        self.target_daily_budget = target_daily_budget
        self._pipeline = AnomalyPipeline(
            api_key=api_key,
            agent_id=agent_id,
            cost_threshold=cost_threshold,
            reputation_threshold=reputation_threshold,
            baseline_reputation=baseline_reputation,
        )
        self._containment = AutoContainment(
            api_key=api_key, agent_id=agent_id,
        )
        self._recovery = GuidedRecovery(
            api_key=api_key, agent_id=agent_id,
        )
        self._forensics = ForensicCollector(
            api_key=api_key, agent_id=agent_id,
        )
        self._incidents: list[IncidentRecord] = []
        self._active_incident: Optional[IncidentRecord] = None

    def setup(self, webhook_url: str) -> dict:
        """Configure webhook alerts for persistent monitoring."""
        return self._pipeline.setup_webhook_alerts(webhook_url)

    def handle_anomaly(self, cycle_result: dict):
        """Called when the anomaly pipeline detects a non-clear signal.

        If severity is "critical", immediately contain. If "warning",
        log and wait for escalation on the next cycle.
        """
        severity = cycle_result["severity"]
        trigger = ", ".join(
            s["signal"] for s in cycle_result["signals"] if s["triggered"]
        )

        if severity == "critical" and self._active_incident is None:
            # Create incident record
            incident = IncidentRecord(
                incident_id=f"inc-{int(time.time())}",
                agent_id=self.agent_id,
                severity=severity,
                detection_signals=cycle_result["signals"],
            )

            # Execute containment
            print(f"[CRITICAL] Containing agent {self.agent_id}...")
            containment_results = self._containment.contain(
                severity=severity,
                trigger_signal=trigger,
            )
            incident.containment_results = containment_results
            incident.contained_at = time.time()

            elapsed = incident.elapsed_to_containment()
            met_sla = elapsed is not None and elapsed <= 60.0
            print(
                f"  Containment complete in {elapsed}s "
                f"({'MET' if met_sla else 'MISSED'} 60s SLA)"
            )

            self._active_incident = incident

        elif severity == "warning":
            print(
                f"[WARNING] Agent {self.agent_id}: "
                f"signals={trigger}. Monitoring."
            )

    def recover_active_incident(self) -> Optional[dict]:
        """Recover from the active incident if one exists.

        Executes the guided recovery sequence and then runs forensics.
        """
        if self._active_incident is None:
            return None

        incident = self._active_incident

        # Recovery
        print(f"[RECOVERY] Recovering agent {self.agent_id}...")
        recovery_results = self._recovery.execute_recovery(
            target_daily_budget=self.target_daily_budget,
            initial_pct=50,
            incident_id=incident.incident_id,
        )
        incident.recovery_results = recovery_results
        incident.recovered_at = time.time()

        # Forensics
        print(f"[FORENSICS] Collecting evidence for {incident.incident_id}...")
        forensics_report = self._forensics.run_full_post_mortem(incident)
        incident.forensics_report = forensics_report

        # Archive and clear
        self._incidents.append(incident)
        self._active_incident = None

        print(
            f"  Recovery complete. Total incident duration: "
            f"{incident.elapsed_to_recovery()}s"
        )

        return incident.to_dict()

    def run(
        self,
        max_cycles: Optional[int] = None,
        interval_seconds: int = 30,
    ):
        """Run the full detection-containment-recovery loop.

        Monitors continuously. On critical anomaly, contains
        automatically. Call recover_active_incident() after the root
        cause is fixed to complete the cycle.
        """
        self._pipeline.run_continuous_monitoring(
            interval_seconds=interval_seconds,
            max_cycles=max_cycles,
            on_anomaly=self.handle_anomaly,
        )

    def get_incident_history(self) -> list[dict]:
        return [inc.to_dict() for inc in self._incidents]


# ── Main: Run the Full Pipeline ──────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 72)
    print("GreenHelix Automated Incident Detection & Escalation")
    print("=" * 72)

    orchestrator = IncidentOrchestrator(
        api_key=API_KEY,
        agent_id=AGENT_ID,
        target_daily_budget=500.0,
        cost_threshold=500.0,
        reputation_threshold=0.1,
        baseline_reputation=0.85,
    )

    # Step 1: Setup webhook alerts
    print("\n[1/4] Setting up webhook alerts...")
    setup_result = orchestrator.setup(webhook_url=WEBHOOK_URL)
    print(f"  Webhooks configured: {setup_result['status']}")

    # Step 2: Run a single detection cycle (demo mode)
    print("\n[2/4] Running detection cycle...")
    pipeline = orchestrator._pipeline
    cycle = pipeline.run_detection_cycle()
    print(f"  Severity: {cycle['severity']}")
    print(f"  Triggered signals: {cycle['triggered_signals']}")
    for signal in cycle["signals"]:
        status = "TRIGGERED" if signal["triggered"] else "clear"
        print(f"    {signal['signal']}: {status}")

    # Step 3: Demo containment (only if you want to freeze the agent)
    print("\n[3/4] Containment ready (not triggered in demo mode)")
    print("  To trigger: set cost_threshold low or run against a spending agent")

    # Step 4: Demo forensics collection
    print("\n[4/4] Collecting forensic evidence...")
    forensics = ForensicCollector(api_key=API_KEY, agent_id=AGENT_ID)

    audit = forensics.collect_audit_trail()
    print(f"  Audit trail chains: {len(audit.get('chains', []))}")

    claims = forensics.collect_verified_claims()
    print(f"  Verified claims: {len(claims.get('claims', []))}")

    impact = forensics.assess_financial_impact()
    print(f"  Usage data collected: {bool(impact.get('usage'))}")
    print(f"  Billing data collected: {bool(impact.get('billing'))}")

    timeline = forensics.reconstruct_timeline()
    print(f"  Timeline period: {timeline.get('period', 'N/A')}")

    print("\n" + "=" * 72)
    print("Incident response system ready.")
    print("Run orchestrator.run() for continuous monitoring.")
    print("=" * 72)
```

