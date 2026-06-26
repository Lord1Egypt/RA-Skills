---
name: greenhelix-agent-fleet-ops
version: "1.3.1"
description: "AgentOps: Managing AI Agent Fleets in Production. The SRE playbook for AI agent fleets: provisioning, observability, cost-aware routing, SLA enforcement, scaling patterns, EU AI Act governance, and the Fleet Commander dashboard. Includes detailed Python code examples with full API integration."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [agentops, fleet-management, observability, finops, sla, governance, guide, greenhelix, openclaw, ai-agent]
price_usd: 49.0
content_type: markdown
executable: false
install: none
credentials: none
---
# AgentOps: Managing AI Agent Fleets in Production

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code, require credentials, or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.


IBM coined "AgentOps" as a formal discipline in early 2026 for a reason that is now obvious: the bottleneck in enterprise AI shifted from building agents to keeping them alive. LangSmith Fleet launched in March 2026. Gartner projects 40% of agentic AI projects will fail by 2027 — not because the models are bad, but because nobody wrote the ops playbook. A Fortune 500 company leaked $400 million in cloud spend from unbudgeted agent compute last quarter. The EU AI Act's high-risk obligations become enforceable on August 2, 2026, and the Spanish DPA has already ruled that "greater technical autonomy does not reduce legal responsibility." This guide is the ops playbook. It covers the full agent lifecycle — provision, deploy, monitor, scale, retire — across fleets of tens to thousands of agents, all wired to the GreenHelix A2A Commerce Gateway's 128 tools across 15 services. You will build a Fleet Commander dashboard that consolidates provisioning, observability, cost control, SLA enforcement, scaling, and governance into a single operational view. Every chapter has working Python code, architecture diagrams, decision trees, and checklists. By the end, you will have the infrastructure to run agent fleets the way SREs run microservice fleets: with error budgets, automated escalation, cost guardrails, and an audit trail that holds up under regulatory scrutiny.
> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## What You'll Learn
- Chapter 1: The AgentOps Discipline
- Chapter 2: Fleet Provisioning and Identity at Scale
- Chapter 3: Observability for Agent Fleets
- Chapter 4: Cost-Aware Model Routing and FinOps
- Chapter 5: SLA Enforcement and Automated Escalation
- Chapter 6: Fleet Scaling Patterns
- Chapter 7: Governance, Audit, and EU AI Act Compliance
- Chapter 8: The Fleet Commander Dashboard
- What You Get

## Full Guide

# AgentOps: The Practitioner's Guide to Managing AI Agent Fleets in Production

IBM coined "AgentOps" as a formal discipline in early 2026 for a reason that is now obvious: the bottleneck in enterprise AI shifted from building agents to keeping them alive. LangSmith Fleet launched in March 2026. Gartner projects 40% of agentic AI projects will fail by 2027 — not because the models are bad, but because nobody wrote the ops playbook. A Fortune 500 company leaked $400 million in cloud spend from unbudgeted agent compute last quarter. The EU AI Act's high-risk obligations become enforceable on August 2, 2026, and the Spanish DPA has already ruled that "greater technical autonomy does not reduce legal responsibility." This guide is the ops playbook. It covers the full agent lifecycle — provision, deploy, monitor, scale, retire — across fleets of tens to thousands of agents, all wired to the GreenHelix A2A Commerce Gateway's 128 tools across 15 services. You will build a Fleet Commander dashboard that consolidates provisioning, observability, cost control, SLA enforcement, scaling, and governance into a single operational view. Every chapter has working Python code, architecture diagrams, decision trees, and checklists. By the end, you will have the infrastructure to run agent fleets the way SREs run microservice fleets: with error budgets, automated escalation, cost guardrails, and an audit trail that holds up under regulatory scrutiny.

---


> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## Table of Contents

1. [The AgentOps Discipline](#chapter-1-the-agentops-discipline)
2. [Fleet Provisioning and Identity at Scale](#chapter-2-fleet-provisioning-and-identity-at-scale)
3. [Observability for Agent Fleets](#chapter-3-observability-for-agent-fleets)
4. [Cost-Aware Model Routing and FinOps](#chapter-4-cost-aware-model-routing-and-finops)
5. [SLA Enforcement and Automated Escalation](#chapter-5-sla-enforcement-and-automated-escalation)
6. [Fleet Scaling Patterns](#chapter-6-fleet-scaling-patterns)
7. [Governance, Audit, and EU AI Act Compliance](#chapter-7-governance-audit-and-eu-ai-act-compliance)
8. [The Fleet Commander Dashboard](#chapter-8-the-fleet-commander-dashboard)

---

## Chapter 1: The AgentOps Discipline

### Why Agent Fleets Are Not Microservices

DevOps manages deterministic services. MLOps manages model training pipelines. Neither discipline handles the unique problem of autonomous software agents that make decisions, spend money, negotiate with counterparties, and degrade in ways that are stochastic rather than binary. A microservice either responds or it does not. An agent can respond with confident, plausible, expensive nonsense — and you will not know until the invoice arrives or the SLA breach notification lands.

The fundamental differences:

| Dimension | Microservices (DevOps) | Models (MLOps) | Agents (AgentOps) |
|-----------|----------------------|----------------|-------------------|
| Failure mode | Crash / timeout | Accuracy drift | Behavioral drift, cost explosion, SLA violation |
| State | Stateless or DB-backed | Model weights | Identity, wallet, reputation, active SLAs |
| Scaling unit | Container replicas | GPU hours | Capability + trust + budget |
| Rollback | Deploy previous image | Revert model version | Revoke access, freeze wallet, reassign tasks |
| Cost model | Compute per request | Training + inference | Token spend + tool calls + counterparty fees |
| Compliance | SOC2, PCI | Model cards | EU AI Act Article 12, audit trails, human oversight |

### The Agent Lifecycle

Every agent in a fleet moves through five phases. GreenHelix tools map directly to each:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  PROVISION   │────▶│   DEPLOY    │────▶│   MONITOR   │
│              │     │             │     │             │
│ register     │     │ register    │     │ submit      │
│ _agent       │     │ _service    │     │ _metrics    │
│ create       │     │ create_sla  │     │ get         │
│ _wallet      │     │ record      │     │ _analytics  │
│ build_claim  │     │ _transaction│     │ check_sla   │
│ _chain       │     │             │     │ _compliance │
└─────────────┘     └─────────────┘     └─────────────┘
       ▲                                       │
       │                                       ▼
┌─────────────┐                        ┌─────────────┐
│   RETIRE    │◀───────────────────────│    SCALE    │
│             │                        │             │
│ freeze      │                        │ search      │
│ wallet      │                        │ _services   │
│ revoke keys │                        │ best_match  │
│ archive     │                        │ estimate    │
│ audit trail │                        │ _cost       │
└─────────────┘                        └─────────────┘
```

### The GreenHelix Tool Surface

All operations go through a single endpoint:

```python
import requests

base_url = "https://api.greenhelix.net/v1"
api_key = "your-api-key"

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"

# Every tool call follows this pattern
resp = session.post(f"{base_url}/v1", json={
    "tool": "tool_name",
    "input": {"param": "value"}
})
result = resp.json()
```

This uniformity is what makes fleet management tractable. You are not integrating 15 different APIs with 15 different auth mechanisms and 15 different error formats. You are calling one endpoint, one auth header, one JSON envelope, 128 tools. The fleet controller you build in Chapter 8 exploits this to treat every GreenHelix operation as a uniform unit of work.

### The AgentOps Maturity Model

Score your organization:

| Level | Name | Characteristics |
|-------|------|----------------|
| 0 | Ad Hoc | Agents run on developer laptops, no monitoring, manual key management |
| 1 | Provisioned | Agents registered with identities and wallets, basic logging |
| 2 | Observable | Per-agent dashboards, SLOs defined, cost tracking active |
| 3 | Governed | SLA enforcement automated, audit trails, escalation pipelines |
| 4 | Autonomous | Self-scaling fleets, budget-aware routing, compliance continuous |

This guide takes you from Level 0 to Level 4. Each chapter corresponds to a maturity jump.

### The Cost of Getting AgentOps Wrong

The numbers are unforgiving. The $400M Fortune 500 cloud leak was not a single dramatic failure — it was thousands of agents, each overspending by small amounts, compounding over months with no aggregation layer to surface the trend. A mid-size fintech reported a $2.3M surprise bill from a fleet of 80 research agents that were supposed to cost $12K/month. The root cause: each agent retried failed tool calls indefinitely because nobody configured a retry ceiling, and a downstream API had a 72-hour partial outage. The agents kept hammering the endpoint, accumulating token charges on every attempt. In both cases, the technology worked exactly as instructed. The agents completed their tasks. They just did it at 50x the expected cost because nobody was watching.

These are not engineering failures. They are operational failures — the same class of failure that drove the DevOps and SRE movements in the 2010s. The difference is that DevOps had a decade to develop its playbook. AgentOps does not. The EU AI Act deadline is in months. Gartner's 40% failure projection is for next year. The teams that build their ops layer now will be the ones that survive the Gartner trough.

### Who This Guide Is For

This guide is written for platform engineers, SREs, and infrastructure leads who have been handed a fleet of AI agents and told to "make them production-ready." You know how to run Kubernetes clusters, set up Prometheus dashboards, and configure PagerDuty escalation policies. What you do not know — yet — is how to apply those instincts to software that makes its own decisions, spends its own money, and degrades in ways that look like success until the SLA report comes in.

You do not need to be an ML engineer. You do not need to understand transformer architectures or prompt engineering. You need to understand operational discipline — and this guide translates that discipline into the agent domain.

---

## Chapter 2: Fleet Provisioning and Identity at Scale

### The Provisioning Pipeline

Provisioning a single agent is trivial. Provisioning 200 agents with correct identities, funded wallets, appropriate tier access, reputation seeds, and SLA contracts — without a single credential collision or orphaned wallet — requires a pipeline.

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ MANIFEST │───▶│ REGISTER │───▶│  WALLET  │───▶│  TRUST   │───▶│ VERIFY   │
│          │    │          │    │          │    │          │    │          │
│ YAML spec│    │ identity │    │ create + │    │ claim    │    │ health   │
│ per agent│    │ + keys   │    │ fund     │    │ chains   │    │ check    │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

### Agent Manifest Format

Define each agent in a declarative manifest before touching any API:

```yaml
# fleet-manifest.yaml
fleet:
  name: "customer-support-fleet"
  environment: "production"
  agents:
    - id_prefix: "cs-triage"
      count: 10
      tier: "pro"
      initial_balance: 50.00
      capabilities: ["text-classification", "sentiment-analysis"]
      trust_claims: ["response-time-p99-under-2s", "accuracy-above-95"]
      sla_template: "standard-support"
    - id_prefix: "cs-escalation"
      count: 3
      tier: "pro"
      initial_balance: 200.00
      capabilities: ["complex-reasoning", "multi-turn-dialogue"]
      trust_claims: ["human-supervised", "pii-compliant"]
      sla_template: "premium-support"
```

### Programmatic Registration

```python
import requests
import uuid
import time

base_url = "https://api.greenhelix.net/v1"
api_key = "your-fleet-admin-key"

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"

def provision_agent(id_prefix, index, tier, initial_balance, capabilities, trust_claims):
    """Provision a single agent: register, wallet, trust chain."""
    agent_id = f"{id_prefix}-{index:04d}-{uuid.uuid4().hex[:8]}"

    # Step 1: Register the agent identity
    resp = session.post(f"{base_url}/v1", json={
        "tool": "register_agent",
        "input": {
            "agent_id": agent_id,
            "tier": tier,
            "capabilities": capabilities,
            "metadata": {
                "fleet": id_prefix,
                "provisioned_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "environment": "production"
            }
        }
    })
    if resp.status_code != 200:
        raise RuntimeError(f"Registration failed for {agent_id}: {resp.text}")

    registration = resp.json()

    # Step 2: Create and fund wallet
    resp = session.post(f"{base_url}/v1", json={
        "tool": "create_wallet",
        "input": {
            "agent_id": agent_id,
            "initial_balance": str(initial_balance)
        }
    })
    if resp.status_code != 200:
        raise RuntimeError(f"Wallet creation failed for {agent_id}: {resp.text}")

    wallet = resp.json()

    # Step 3: Bootstrap trust via claim chain
    resp = session.post(f"{base_url}/v1", json={
        "tool": "build_claim_chain",
        "input": {
            "agent_id": agent_id,
            "claims": trust_claims
        }
    })
    if resp.status_code != 200:
        raise RuntimeError(f"Claim chain failed for {agent_id}: {resp.text}")

    return {
        "agent_id": agent_id,
        "wallet_id": wallet.get("wallet_id"),
        "balance": initial_balance,
        "claims": trust_claims
    }


def provision_fleet(manifest):
    """Provision an entire fleet from a manifest."""
    results = {"succeeded": [], "failed": []}

    for agent_spec in manifest["fleet"]["agents"]:
        for i in range(agent_spec["count"]):
            try:
                agent = provision_agent(
                    id_prefix=agent_spec["id_prefix"],
                    index=i,
                    tier=agent_spec["tier"],
                    initial_balance=agent_spec["initial_balance"],
                    capabilities=agent_spec["capabilities"],
                    trust_claims=agent_spec["trust_claims"]
                )
                results["succeeded"].append(agent)
            except RuntimeError as e:
                results["failed"].append({
                    "index": i,
                    "prefix": agent_spec["id_prefix"],
                    "error": str(e)
                })

    return results
```

### API Key Management at Scale

Never share a single API key across agents. Each agent gets its own key scoped to its tier and capabilities. Store keys in a secrets manager (Vault, AWS Secrets Manager, GCP Secret Manager) and inject at deploy time.

**Key rotation pattern:**

```python
def rotate_agent_key(agent_id, old_key):
    """Rotate API key with zero-downtime overlap window."""
    # Generate new key (via your identity provider)
    # Configure agent to accept both keys during overlap
    # Verify new key works
    resp = session.post(f"{base_url}/v1", json={
        "tool": "register_agent",
        "input": {
            "agent_id": agent_id,
            "rotate_key": True
        }
    })
    new_key = resp.json().get("api_key")

    # Update secrets manager
    # Wait for propagation (60s overlap window)
    # Revoke old key
    return new_key
```

### Reputation Seeding

New agents start with zero reputation, which creates a cold-start problem — no one wants to transact with an unproven agent. Reputation seeds solve this:

```python
def seed_reputation(agent_id, seed_metrics):
    """Submit initial metrics to bootstrap reputation."""
    resp = session.post(f"{base_url}/v1", json={
        "tool": "submit_metrics",
        "input": {
            "agent_id": agent_id,
            "metrics": seed_metrics
        }
    })
    return resp.json()

# Seed a triage agent with baseline metrics
seed_reputation("cs-triage-0001-a1b2c3d4", {
    "response_time_ms": 450,
    "accuracy_rate": 0.96,
    "uptime_rate": 0.999,
    "tasks_completed": 0,
    "error_rate": 0.0
})
```

### Fleet Provisioning Checklist

- [ ] All agents have unique IDs with fleet prefix for grouping
- [ ] Each agent has its own API key stored in secrets manager
- [ ] Wallets are funded with initial balance matching expected burn rate
- [ ] Trust claims are registered and verifiable
- [ ] Tier access matches required tool permissions
- [ ] Agent metadata includes fleet name, environment, and provisioning timestamp
- [ ] Key rotation schedule is configured (every 90 days minimum)
- [ ] Provisioning script is idempotent (safe to re-run)
- [ ] Failed provisioning steps trigger cleanup (no orphaned wallets)
- [ ] Fleet manifest is version-controlled

---

## Chapter 3: Observability for Agent Fleets

### The Three Pillars, Adapted for Agents

Traditional observability has three pillars: metrics, logs, traces. Agent observability adds two more: **behavioral signals** (what the agent decided to do and why) and **economic signals** (what it cost and who paid). Without these two additions, you can tell that your agent is up and fast but not that it is spending $14 per task on a job budgeted at $2.

### Per-Agent Metrics Collection

```python
import requests
import time

base_url = "https://api.greenhelix.net/v1"
api_key = "your-api-key"

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"

def collect_agent_metrics(agent_id):
    """Collect comprehensive metrics for a single agent."""
    metrics = {}

    # Performance metrics
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_analytics",
        "input": {
            "agent_id": agent_id,
            "time_range": "1h",
            "metrics": ["latency_p50", "latency_p99", "error_rate",
                        "tool_call_volume", "task_completion_rate"]
        }
    })
    if resp.status_code == 200:
        metrics["performance"] = resp.json()

    # Reputation and trust
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_agent_reputation",
        "input": {"agent_id": agent_id}
    })
    if resp.status_code == 200:
        metrics["reputation"] = resp.json()

    # Financial position
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_balance",
        "input": {"agent_id": agent_id}
    })
    if resp.status_code == 200:
        metrics["balance"] = resp.json()

    # SLA compliance
    resp = session.post(f"{base_url}/v1", json={
        "tool": "check_sla_compliance",
        "input": {"agent_id": agent_id}
    })
    if resp.status_code == 200:
        metrics["sla"] = resp.json()

    return metrics
```

### Fleet Health Aggregation

Individual agent metrics are necessary but insufficient. You need fleet-level aggregation to spot systemic issues — a fleet where 30% of agents have degraded latency is a different problem than one agent having a bad day.

```
┌─────────────────────────────────────────────────────────┐
│                  FLEET HEALTH DASHBOARD                  │
├─────────────┬─────────────┬─────────────┬───────────────┤
│  Agents     │  Healthy    │  Degraded   │  Critical     │
│  Total: 200 │  ███ 174    │  ██ 21      │  █ 5          │
├─────────────┼─────────────┼─────────────┼───────────────┤
│  P99 Lat.   │  Fleet Err  │  SLA Comp.  │  Burn Rate    │
│  1,240 ms   │  Rate: 2.1% │  97.3%      │  $42.10/hr    │
├─────────────┴─────────────┴─────────────┴───────────────┤
│  ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁  Tool call volume (24h)               │
│  ▕████████████████▏  Peak: 14:00 UTC                    │
├─────────────────────────────────────────────────────────┤
│  ALERTS                                                  │
│  ⚠ cs-triage-0042: latency P99 > 3000ms (15 min)       │
│  ⚠ cs-escalation-0002: balance below $20 threshold      │
│  ✗ cs-triage-0187: SLA breach — response time           │
└─────────────────────────────────────────────────────────┘
```

```python
def aggregate_fleet_health(agent_ids):
    """Aggregate metrics across a fleet of agents."""
    fleet_metrics = {
        "total": len(agent_ids),
        "healthy": 0,
        "degraded": 0,
        "critical": 0,
        "total_burn_rate": 0.0,
        "sla_compliant": 0,
        "latencies_p99": [],
        "error_rates": [],
        "alerts": []
    }

    for agent_id in agent_ids:
        metrics = collect_agent_metrics(agent_id)

        perf = metrics.get("performance", {})
        balance = metrics.get("balance", {})
        sla = metrics.get("sla", {})

        error_rate = perf.get("error_rate", 0)
        latency_p99 = perf.get("latency_p99", 0)

        fleet_metrics["latencies_p99"].append(latency_p99)
        fleet_metrics["error_rates"].append(error_rate)

        # Classify agent health
        if error_rate > 0.10 or latency_p99 > 5000:
            fleet_metrics["critical"] += 1
            fleet_metrics["alerts"].append({
                "agent_id": agent_id,
                "severity": "critical",
                "reason": f"error_rate={error_rate}, p99={latency_p99}ms"
            })
        elif error_rate > 0.05 or latency_p99 > 3000:
            fleet_metrics["degraded"] += 1
            fleet_metrics["alerts"].append({
                "agent_id": agent_id,
                "severity": "warning",
                "reason": f"error_rate={error_rate}, p99={latency_p99}ms"
            })
        else:
            fleet_metrics["healthy"] += 1

        # SLA tracking
        if sla.get("compliant", False):
            fleet_metrics["sla_compliant"] += 1

        # Cost tracking
        fleet_metrics["total_burn_rate"] += float(balance.get("burn_rate_per_hour", 0))

    fleet_metrics["sla_compliance_pct"] = (
        fleet_metrics["sla_compliant"] / fleet_metrics["total"] * 100
        if fleet_metrics["total"] > 0 else 0
    )

    return fleet_metrics
```

### Alerting Pipeline

Define alert rules that escalate from notification to automated remediation:

| Severity | Condition | Action |
|----------|-----------|--------|
| Info | P99 latency > 2x baseline for 5 min | Log, notify Slack |
| Warning | Error rate > 5% for 10 min | Notify on-call, reduce traffic share |
| Critical | SLA breach or balance < $5 | Page on-call, auto-pause agent, escalate |
| Emergency | > 20% of fleet critical | Page fleet commander, freeze provisioning |

```python
def evaluate_alerts(fleet_metrics, thresholds):
    """Evaluate fleet metrics against alerting thresholds."""
    alerts = []

    critical_pct = fleet_metrics["critical"] / fleet_metrics["total"] * 100
    if critical_pct > thresholds.get("emergency_critical_pct", 20):
        alerts.append({
            "severity": "emergency",
            "message": f"{critical_pct:.1f}% of fleet in critical state",
            "action": "freeze_provisioning"
        })

    if fleet_metrics["sla_compliance_pct"] < thresholds.get("min_sla_pct", 95):
        alerts.append({
            "severity": "critical",
            "message": f"Fleet SLA compliance at {fleet_metrics['sla_compliance_pct']:.1f}%",
            "action": "page_fleet_commander"
        })

    if fleet_metrics["total_burn_rate"] > thresholds.get("max_burn_rate_per_hour", 100):
        alerts.append({
            "severity": "warning",
            "message": f"Fleet burn rate ${fleet_metrics['total_burn_rate']:.2f}/hr exceeds budget",
            "action": "notify_finops"
        })

    return alerts
```

### Behavioral Observability: The Fifth Pillar

Traditional metrics tell you the agent is slow. Behavioral observability tells you why. An agent that suddenly starts calling `search_services` 40 times per task instead of 3 might have a perfectly healthy error rate and latency — but it is thrashing through the marketplace because its ranking heuristic has drifted. Without behavioral signals, you would never catch this until the cost spike hits.

Track these behavioral metrics per agent:

| Metric | What It Reveals | Alert Threshold |
|--------|----------------|-----------------|
| Tool calls per task | Efficiency / thrashing | > 2x baseline |
| Unique tools per task | Task complexity drift | > 3x baseline |
| Retry ratio | Downstream health | > 20% of calls are retries |
| Escalation rate | Agent capability limits | > 15% of tasks escalated |
| Decision latency | Reasoning bottlenecks | P99 > 5x P50 |
| Counterparty diversity | Market exploration | < 2 unique counterparties/day |

```python
def collect_behavioral_metrics(agent_id, task_log):
    """Extract behavioral signals from a task execution log."""
    metrics = {
        "tool_calls_per_task": len(task_log.get("tool_calls", [])),
        "unique_tools": len(set(tc["tool"] for tc in task_log.get("tool_calls", []))),
        "retries": sum(1 for tc in task_log.get("tool_calls", []) if tc.get("is_retry")),
        "escalated": task_log.get("escalated", False),
        "decision_latency_ms": task_log.get("decision_latency_ms", 0)
    }

    # Submit behavioral metrics alongside performance metrics
    resp = session.post(f"{base_url}/v1", json={
        "tool": "submit_metrics",
        "input": {
            "agent_id": agent_id,
            "metrics": metrics
        }
    })
    return resp.json()
```

### Distributed Tracing for Multi-Agent Workflows

When Agent A delegates a subtask to Agent B, which calls Agent C for data enrichment, a single task spans three agents and potentially dozens of tool calls. Without distributed tracing, debugging a failed task means manually correlating logs across agents — the same problem microservices solved with Jaeger and Zipkin.

Implement trace propagation by passing a trace context through every tool call:

```python
import uuid

def create_trace_context(parent_trace_id=None):
    """Create or extend a trace context for cross-agent tracing."""
    trace_id = parent_trace_id or str(uuid.uuid4())
    span_id = str(uuid.uuid4())[:16]
    return {"trace_id": trace_id, "span_id": span_id}

def traced_tool_call(agent_id, tool_name, tool_input, trace_ctx):
    """Execute a tool call with trace context propagation."""
    resp = session.post(f"{base_url}/v1", json={
        "tool": tool_name,
        "input": {
            **tool_input,
            "_trace": trace_ctx
        }
    })
    result = resp.json()

    # Record the span in the audit trail for correlation
    session.post(f"{base_url}/v1", json={
        "tool": "create_audit_trail",
        "input": {
            "agent_id": agent_id,
            "action": f"tool_call:{tool_name}",
            "details": {
                "trace_id": trace_ctx["trace_id"],
                "span_id": trace_ctx["span_id"],
                "status_code": resp.status_code,
                "latency_ms": resp.elapsed.microseconds // 1000
            }
        }
    })
    return result
```

### Observability Checklist

- [ ] Per-agent metrics collection runs every 60 seconds
- [ ] Fleet aggregation computes health classification (healthy/degraded/critical)
- [ ] Alerting thresholds configured for latency, error rate, SLA, and cost
- [ ] Escalation pipeline tested end-to-end (can you verify the page fires?)
- [ ] Dashboard shows real-time fleet health with drill-down to individual agents
- [ ] Metrics retained for 90 days minimum (compliance requirement)
- [ ] Anomaly detection enabled for cost spikes (>200% of hourly baseline)
- [ ] Tool-call-level tracing enabled for debugging cascading failures
- [ ] Behavioral metrics tracked per agent (tool calls per task, retry ratio, escalation rate)
- [ ] Distributed trace context propagated across multi-agent workflows

---

## Chapter 4: Cost-Aware Model Routing and FinOps

### The Agent FinOps Problem

A microservice has a predictable cost profile: X requests per second times Y compute per request. An agent has a stochastic cost profile: it might resolve a task in 2 tool calls or 47, it might choose a cheap model or an expensive one, and it might retry failed calls indefinitely if you do not stop it. The $400M Fortune 500 cloud leak happened because nobody modeled the cost distribution of agent behavior under production load.

### Token-Level Cost Tracking

```python
import requests

base_url = "https://api.greenhelix.net/v1"
api_key = "your-api-key"

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"

def track_task_cost(agent_id, task_id, tool_calls):
    """Track per-task cost across all tool calls."""
    total_cost = 0.0

    for call in tool_calls:
        # Estimate cost before executing
        resp = session.post(f"{base_url}/v1", json={
            "tool": "estimate_cost",
            "input": {
                "tool_name": call["tool"],
                "input_size": call.get("estimated_tokens", 100)
            }
        })
        estimate = resp.json()
        estimated_cost = float(estimate.get("estimated_cost", "0"))

        # Check budget before executing
        if total_cost + estimated_cost > call.get("budget_remaining", float("inf")):
            return {
                "status": "budget_exceeded",
                "total_cost": str(total_cost),
                "blocked_call": call["tool"]
            }

        # Execute the tool call
        resp = session.post(f"{base_url}/v1", json={
            "tool": call["tool"],
            "input": call["input"]
        })

        # Record the transaction
        resp = session.post(f"{base_url}/v1", json={
            "tool": "record_transaction",
            "input": {
                "agent_id": agent_id,
                "task_id": task_id,
                "tool": call["tool"],
                "cost": str(estimated_cost),
                "timestamp": call.get("timestamp")
            }
        })

        total_cost += estimated_cost

    return {"status": "completed", "total_cost": str(total_cost)}
```

### The Model Routing Decision Tree

Not every task needs GPT-4 or Claude Opus. Most fleets waste 60-70% of their token budget routing simple classification tasks to frontier models.

```
                    ┌──────────────────────┐
                    │   Incoming Task       │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │ Complexity estimate?  │
                    └──────────┬───────────┘
                       ┌───────┴───────┐
                       ▼               ▼
                  ┌─────────┐    ┌──────────┐
                  │  LOW    │    │ MED/HIGH │
                  │(<100tok)│    │          │
                  └────┬────┘    └────┬─────┘
                       │              │
                       ▼              ▼
              ┌──────────────┐  ┌─────────────────┐
              │ Small model  │  │ Budget remaining │
              │ (Haiku/mini) │  │ > threshold?     │
              │ $0.001/task  │  └────────┬────────┘
              └──────────────┘     ┌─────┴─────┐
                                   ▼           ▼
                            ┌──────────┐ ┌──────────┐
                            │   YES    │ │    NO    │
                            │ Frontier │ │ Mid-tier │
                            │ model    │ │ model    │
                            │$0.03/task│ │$0.008/tsk│
                            └──────────┘ └──────────┘
```

### Budget Guardrails

```python
class BudgetGuardrail:
    """Enforce per-agent, per-fleet, and per-task budget limits."""

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.limits = {
            "per_task_max": 5.00,
            "per_agent_hourly_max": 50.00,
            "fleet_daily_max": 2000.00
        }

    def check_balance(self, agent_id):
        """Check if agent has sufficient funds to continue."""
        resp = self.session.post(f"{self.base_url}/v1", json={
            "tool": "get_balance",
            "input": {"agent_id": agent_id}
        })
        balance = resp.json()
        current = float(balance.get("balance", "0"))
        return current > self.limits["per_task_max"]

    def get_volume_discount(self, agent_id):
        """Check if agent qualifies for volume pricing."""
        resp = self.session.post(f"{self.base_url}/v1", json={
            "tool": "get_volume_discount",
            "input": {"agent_id": agent_id}
        })
        return resp.json()

    def convert_cost_estimate(self, amount, from_currency, to_currency):
        """Convert cost estimates across currencies for global fleets."""
        resp = self.session.post(f"{self.base_url}/v1", json={
            "tool": "convert_currency",
            "input": {
                "amount": str(amount),
                "from_currency": from_currency,
                "to_currency": to_currency
            }
        })
        return resp.json()

    def enforce(self, agent_id, task_cost):
        """Enforce budget guardrails. Returns (allowed, reason)."""
        if task_cost > self.limits["per_task_max"]:
            return False, f"Task cost ${task_cost:.2f} exceeds per-task limit ${self.limits['per_task_max']:.2f}"

        if not self.check_balance(agent_id):
            return False, f"Agent {agent_id} balance below minimum threshold"

        return True, "within_budget"
```

### Fleet Economics Model

Build a spreadsheet model before deploying. Here is the math:

```
Fleet Monthly Cost = Σ(agent_i) [
    (tasks_per_day × avg_tool_calls_per_task × avg_cost_per_call × 30)
    + (provisioning_cost)
    + (monitoring_overhead)
]

ROI = (revenue_from_agent_tasks - fleet_monthly_cost) / fleet_monthly_cost

Break-even point = fleet_monthly_cost / revenue_per_task
```

**Example:** A 50-agent triage fleet handling 10,000 tasks/day at $0.003/task average cost:

- Monthly tool cost: 10,000 x 3.2 avg calls x $0.003 x 30 = **$2,880**
- Monitoring overhead (5%): **$144**
- Total: **$3,024/month**
- If each task saves $0.50 in human labor: Revenue = 10,000 x $0.50 x 30 = **$150,000/month**
- ROI: **4,860%**

### Cost Attribution: Who Pays for Shared Work?

In multi-agent workflows, a single task may involve several agents. The triage agent classifies it, the specialist agent processes it, the quality agent validates it. Who pays for each step? Without clear cost attribution, fleet economics modeling is fiction.

Three attribution models:

**Caller-pays:** The agent that initiates a tool call or delegates a subtask pays the full cost. Simple to implement. Penalizes orchestrator agents that coordinate work but add the least value per call.

**Proportional split:** Each agent in the workflow pays a share proportional to the token volume or tool calls they contributed. Fair but complex to implement — requires full trace context to compute shares.

**Task-budget pool:** A budget is allocated to the task, not the agent. All agents draw from the same pool. The fleet operator monitors the pool, not individual agents. Best for workflows where agent boundaries are fluid.

```python
def attribute_task_cost(task_trace, model="proportional"):
    """Attribute costs across agents in a multi-agent workflow."""
    agent_costs = {}

    for span in task_trace.get("spans", []):
        agent_id = span["agent_id"]
        cost = float(span.get("cost", "0"))

        if agent_id not in agent_costs:
            agent_costs[agent_id] = 0.0
        agent_costs[agent_id] += cost

    total = sum(agent_costs.values())

    if model == "caller_pays":
        initiator = task_trace["initiating_agent"]
        return {initiator: str(total)}

    elif model == "proportional":
        return {
            agent_id: str(cost)
            for agent_id, cost in agent_costs.items()
        }

    elif model == "task_pool":
        return {"task_pool": str(total), "breakdown": agent_costs}

    return agent_costs
```

### The Weekly FinOps Review

Schedule a weekly review with this agenda:

1. **Budget vs. actual** — Compare each fleet segment's actual spend to its budget. Flag any segment exceeding 110% of plan.
2. **Cost per task trend** — Is cost per task stable, rising, or falling? Rising cost at stable volume means agent efficiency is degrading.
3. **Model mix audit** — What percentage of tasks went to frontier models vs. mid-tier vs. small? Is the routing decision tree working?
4. **Top 10 most expensive tasks** — Review the outliers. Were they legitimately complex or did an agent thrash?
5. **Volume discount capture** — Are you hitting volume tiers? If not, should you consolidate traffic to fewer agents to hit the next tier?

### FinOps Checklist

- [ ] Per-task budget limits configured and enforced
- [ ] Per-agent hourly spending caps in place
- [ ] Fleet daily budget ceiling with automated pause on breach
- [ ] Cost estimates run before every tool call (estimate_cost)
- [ ] Volume discount eligibility checked at provisioning
- [ ] Model routing routes <100 token tasks to cheapest model
- [ ] Weekly cost review comparing actual vs. budgeted spend
- [ ] Anomaly detection for cost spikes (agent spending >3x normal)
- [ ] Currency conversion configured for global fleet operations
- [ ] Break-even analysis documented per fleet segment
- [ ] Cost attribution model chosen and implemented for multi-agent workflows
- [ ] Top-10 expensive task review runs weekly

---

## Chapter 5: SLA Enforcement and Automated Escalation

### Defining Agent-Level SLAs

An SLA for an agent is not the same as an SLA for a web service. A web service SLA covers availability and latency. An agent SLA must also cover accuracy, cost-per-task, and behavioral bounds — things that are harder to measure and harder to enforce.

**SLA dimensions for agents:**

| Dimension | Metric | Example Target |
|-----------|--------|----------------|
| Response time | P99 latency | < 2,000 ms |
| Availability | Uptime percentage | > 99.5% |
| Accuracy | Task success rate | > 95% |
| Cost | Average cost per task | < $0.05 |
| Behavioral | Escalation rate | < 10% of tasks |

### Creating SLAs Programmatically

```python
import requests

base_url = "https://api.greenhelix.net/v1"
api_key = "your-api-key"

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"

def create_agent_sla(agent_id, sla_template):
    """Create an SLA contract for an agent."""
    sla_definitions = {
        "standard-support": {
            "response_time_p99_ms": 2000,
            "uptime_pct": 99.5,
            "accuracy_pct": 95.0,
            "max_cost_per_task": "0.05",
            "review_period_days": 30
        },
        "premium-support": {
            "response_time_p99_ms": 500,
            "uptime_pct": 99.9,
            "accuracy_pct": 98.0,
            "max_cost_per_task": "0.10",
            "review_period_days": 7
        }
    }

    sla_config = sla_definitions.get(sla_template)
    if not sla_config:
        raise ValueError(f"Unknown SLA template: {sla_template}")

    resp = session.post(f"{base_url}/v1", json={
        "tool": "create_sla",
        "input": {
            "agent_id": agent_id,
            "terms": sla_config
        }
    })
    return resp.json()
```

### Continuous Compliance Monitoring

```python
def monitor_sla_compliance(agent_ids, interval_minutes=5):
    """Continuously monitor SLA compliance across fleet."""
    violations = []

    for agent_id in agent_ids:
        resp = session.post(f"{base_url}/v1", json={
            "tool": "check_sla_compliance",
            "input": {"agent_id": agent_id}
        })
        compliance = resp.json()

        if not compliance.get("compliant", True):
            # Get violation details
            resp = session.post(f"{base_url}/v1", json={
                "tool": "get_sla_violations",
                "input": {"agent_id": agent_id}
            })
            agent_violations = resp.json()

            violations.append({
                "agent_id": agent_id,
                "violations": agent_violations,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            })

    return violations
```

### The Automated Escalation Pipeline

When an SLA breach is detected, the system should not wait for a human to notice. The escalation pipeline has four tiers:

```
┌────────────────────────────────────────────────────────────┐
│                  ESCALATION PIPELINE                        │
├────────────┬───────────────────┬───────────────────────────┤
│   Tier 1   │ Auto-remediate    │ Restart agent, clear      │
│ (0-5 min)  │                   │ cache, check dependencies │
├────────────┼───────────────────┼───────────────────────────┤
│   Tier 2   │ Reroute traffic   │ Shift load to healthy     │
│ (5-15 min) │                   │ agents, reduce task rate   │
├────────────┼───────────────────┼───────────────────────────┤
│   Tier 3   │ Notify + dispute  │ Send message to operator, │
│ (15-30 min)│                   │ create dispute if needed   │
├────────────┼───────────────────┼───────────────────────────┤
│   Tier 4   │ Freeze + escalate │ Pause agent, freeze wallet│
│ (30+ min)  │                   │ human intervention needed  │
└────────────┴───────────────────┴───────────────────────────┘
```

```python
def escalate_sla_violation(agent_id, violation, elapsed_minutes):
    """Execute escalation based on violation duration."""

    if elapsed_minutes < 5:
        # Tier 1: Auto-remediate
        return {"action": "restart", "agent_id": agent_id}

    elif elapsed_minutes < 15:
        # Tier 2: Reroute traffic
        return {"action": "reroute", "agent_id": agent_id, "reduce_traffic_pct": 50}

    elif elapsed_minutes < 30:
        # Tier 3: Notify via messaging, file dispute if counterparty involved
        resp = session.post(f"{base_url}/v1", json={
            "tool": "send_message",
            "input": {
                "to": "fleet-commander",
                "subject": f"SLA violation: {agent_id}",
                "body": f"Agent {agent_id} has been in violation for {elapsed_minutes} min. "
                        f"Violation: {violation}"
            }
        })

        if violation.get("counterparty"):
            resp = session.post(f"{base_url}/v1", json={
                "tool": "create_dispute",
                "input": {
                    "agent_id": agent_id,
                    "counterparty": violation["counterparty"],
                    "reason": "sla_breach",
                    "details": violation
                }
            })

        return {"action": "notified_and_disputed", "agent_id": agent_id}

    else:
        # Tier 4: Freeze agent
        return {"action": "frozen", "agent_id": agent_id, "requires_human": True}
```

### Dispute Resolution for Fleet Operators

When an agent breaches an SLA with a counterparty, disputes need structured resolution:

```python
def resolve_fleet_disputes(fleet_prefix):
    """Review and resolve open disputes for a fleet."""
    # In production, query for open disputes filtered by fleet prefix
    # and apply resolution policies

    resp = session.post(f"{base_url}/v1", json={
        "tool": "resolve_dispute",
        "input": {
            "dispute_id": "dispute-123",
            "resolution": "partial_refund",
            "amount": "5.00",
            "notes": "SLA response time breach confirmed. 50% credit applied."
        }
    })
    return resp.json()
```

### SLA Enforcement Checklist

- [ ] SLA templates defined for each agent role (triage, escalation, specialist)
- [ ] SLA contracts created programmatically at provisioning time
- [ ] Compliance checks run every 5 minutes per agent
- [ ] Escalation pipeline tested end-to-end through all 4 tiers
- [ ] Dispute creation automated for counterparty-facing SLA breaches
- [ ] Dispute resolution policies documented and approved by legal
- [ ] SLA violation history retained for compliance reporting
- [ ] Monthly SLA review cadence with fleet performance report
- [ ] Error budget model: 0.5% monthly error budget = 219 minutes of allowed violation

---

## Chapter 6: Fleet Scaling Patterns

### Horizontal Scaling: Specialist Agents

Horizontal scaling for agents is not "add more replicas." It is "add more specialists." A triage agent and an escalation agent are not interchangeable the way two nginx pods are.

```
┌─────────────────────────────────────────────────────┐
│                   TASK ROUTER                        │
│  incoming tasks → classify → route to specialist     │
└──────────┬──────────┬──────────┬───────────────────┘
           │          │          │
     ┌─────▼────┐ ┌──▼──────┐ ┌▼──────────┐
     │ TRIAGE   │ │ BILLING │ │ ESCALATION│
     │ FLEET    │ │ FLEET   │ │ FLEET     │
     │ (20 agt) │ │ (5 agt) │ │ (3 agt)  │
     │          │ │         │ │           │
     │ Simple   │ │ Payment │ │ Complex   │
     │ classify │ │ queries │ │ reasoning │
     │ + route  │ │ + calc  │ │ + human   │
     └──────────┘ └─────────┘ └───────────┘
```

### Dynamic Task Routing via Marketplace

Instead of hardcoding which agent handles which task, use the marketplace to find the best agent dynamically:

```python
import requests

base_url = "https://api.greenhelix.net/v1"
api_key = "your-api-key"

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"

def route_task_to_best_agent(task):
    """Find the best agent for a task using marketplace discovery."""

    # Step 1: Search for agents with required capabilities
    resp = session.post(f"{base_url}/v1", json={
        "tool": "search_services",
        "input": {
            "capabilities": task["required_capabilities"],
            "min_reputation": 0.8,
            "max_cost": task.get("budget", "1.00")
        }
    })
    candidates = resp.json().get("services", [])

    if not candidates:
        return {"status": "no_candidates", "task_id": task["id"]}

    # Step 2: Find best match considering cost, reputation, and latency
    resp = session.post(f"{base_url}/v1", json={
        "tool": "best_match",
        "input": {
            "requirements": {
                "capabilities": task["required_capabilities"],
                "max_latency_ms": task.get("max_latency_ms", 2000),
                "max_cost": task.get("budget", "1.00")
            },
            "candidates": [c["agent_id"] for c in candidates]
        }
    })
    match = resp.json()

    # Step 3: Check SLA before routing
    best_agent = match.get("best_match")
    if best_agent:
        resp = session.post(f"{base_url}/v1", json={
            "tool": "check_sla_compliance",
            "input": {"agent_id": best_agent}
        })
        compliance = resp.json()

        if compliance.get("compliant", False):
            return {"status": "routed", "agent_id": best_agent, "task_id": task["id"]}

    return {"status": "no_compliant_candidate", "task_id": task["id"]}
```

### Vertical Scaling: Capability Upgrades

Vertical scaling means upgrading an agent's capabilities — switching from a small model to a large one, granting access to more tools, or increasing its tier. This is not free: higher capability means higher cost.

```python
def upgrade_agent_tier(agent_id, new_tier):
    """Upgrade agent to a higher capability tier."""

    # Estimate cost impact
    resp = session.post(f"{base_url}/v1", json={
        "tool": "estimate_cost",
        "input": {
            "agent_id": agent_id,
            "new_tier": new_tier,
            "projected_volume": "daily"
        }
    })
    cost_estimate = resp.json()

    # Verify budget approval
    current_cost = float(cost_estimate.get("current_daily_cost", "0"))
    projected_cost = float(cost_estimate.get("projected_daily_cost", "0"))
    cost_increase_pct = ((projected_cost - current_cost) / current_cost * 100
                          if current_cost > 0 else float("inf"))

    if cost_increase_pct > 200:
        return {
            "status": "requires_approval",
            "cost_increase_pct": cost_increase_pct,
            "projected_daily_cost": str(projected_cost)
        }

    # Register with upgraded tier
    resp = session.post(f"{base_url}/v1", json={
        "tool": "register_agent",
        "input": {
            "agent_id": agent_id,
            "tier": new_tier,
            "upgrade": True
        }
    })
    return resp.json()
```

### Swarm vs. Orchestrator: The Decision Matrix

| Factor | Swarm (peer-to-peer) | Orchestrator (centralized) |
|--------|---------------------|---------------------------|
| Task complexity | Homogeneous, parallelizable | Heterogeneous, sequential dependencies |
| Failure tolerance | High — any agent can take over | Low — orchestrator is SPOF |
| Cost control | Hard — decentralized spend | Easy — centralized budget |
| Latency | Lower — no orchestrator hop | Higher — extra routing step |
| Debugging | Hard — distributed traces | Easier — centralized logs |
| Scaling | Add agents to swarm | Scale orchestrator + agents |
| Best for | Data processing, scraping, monitoring | Customer support, multi-step workflows, compliance |

**Decision rule:** If tasks are independent and agents are interchangeable, use a swarm. If tasks have dependencies and agents are specialized, use an orchestrator. Most production fleets use a hybrid: an orchestrator routes to specialist swarms.

### Auto-Scaling Rules

```python
def evaluate_scaling_decision(fleet_metrics, scaling_config):
    """Decide whether to scale fleet up, down, or hold."""
    decisions = []

    # Scale up: queue depth increasing
    queue_depth = fleet_metrics.get("pending_tasks", 0)
    agents_active = fleet_metrics.get("healthy", 0)
    tasks_per_agent = queue_depth / max(agents_active, 1)

    if tasks_per_agent > scaling_config["scale_up_threshold"]:
        new_count = min(
            agents_active + scaling_config["scale_up_increment"],
            scaling_config["max_agents"]
        )
        decisions.append({
            "action": "scale_up",
            "from": agents_active,
            "to": new_count,
            "reason": f"Queue depth {queue_depth}, {tasks_per_agent:.1f} tasks/agent"
        })

    # Scale down: agents idle
    elif tasks_per_agent < scaling_config["scale_down_threshold"]:
        new_count = max(
            agents_active - scaling_config["scale_down_increment"],
            scaling_config["min_agents"]
        )
        if new_count < agents_active:
            decisions.append({
                "action": "scale_down",
                "from": agents_active,
                "to": new_count,
                "reason": f"Low utilization: {tasks_per_agent:.1f} tasks/agent"
            })

    # Cost-based scaling: burn rate too high
    if fleet_metrics.get("total_burn_rate", 0) > scaling_config["max_burn_rate"]:
        decisions.append({
            "action": "cost_scale_down",
            "reason": f"Burn rate ${fleet_metrics['total_burn_rate']:.2f}/hr exceeds limit"
        })

    return decisions if decisions else [{"action": "hold", "reason": "Within thresholds"}]
```

### Load Balancing Strategies

Agent load balancing is not round-robin. Agents are not fungible — they have different capabilities, reputations, costs, and remaining budgets. The load balancer must account for all four.

```
                     INCOMING TASK
                          │
                          ▼
                  ┌───────────────┐
                  │   CLASSIFY    │
                  │  task type +  │
                  │  complexity   │
                  └───────┬───────┘
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ CAPABLE  │ │ CAPABLE  │ │ CAPABLE  │
        │ AGENTS   │ │ AGENTS   │ │ AGENTS   │
        │ Pool A   │ │ Pool B   │ │ Pool C   │
        └─────┬────┘ └─────┬────┘ └─────┬────┘
              │             │             │
              ▼             ▼             ▼
        ┌──────────────────────────────────────┐
        │        WEIGHTED SELECTION             │
        │                                      │
        │  Score = (reputation × 0.4)          │
        │       + (budget_headroom × 0.2)      │
        │       + (current_idle × 0.2)         │
        │       + (sla_margin × 0.2)           │
        └──────────────────┬───────────────────┘
                           │
                           ▼
                    SELECTED AGENT
```

```python
def weighted_agent_selection(capable_agents, task):
    """Select the best agent from a pool using weighted scoring."""
    scored = []

    for agent_id in capable_agents:
        # Get reputation
        resp = session.post(f"{base_url}/v1", json={
            "tool": "get_agent_reputation",
            "input": {"agent_id": agent_id}
        })
        reputation = float(resp.json().get("score", 0.5))

        # Get balance headroom
        resp = session.post(f"{base_url}/v1", json={
            "tool": "get_balance",
            "input": {"agent_id": agent_id}
        })
        balance = float(resp.json().get("balance", "0"))
        budget_headroom = min(balance / 100.0, 1.0)  # Normalize to 0-1

        # Check SLA margin
        resp = session.post(f"{base_url}/v1", json={
            "tool": "check_sla_compliance",
            "input": {"agent_id": agent_id}
        })
        sla_data = resp.json()
        sla_margin = float(sla_data.get("margin_pct", 50)) / 100.0

        # Composite score
        score = (reputation * 0.4
                 + budget_headroom * 0.2
                 + sla_margin * 0.2
                 + 0.2)  # idle factor — in production, wire to queue depth

        scored.append({"agent_id": agent_id, "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[0]["agent_id"] if scored else None
```

### Graceful Agent Retirement

Scaling down means retiring agents, and retirement is not just "stop the process." An agent with in-flight tasks, open SLAs, and a funded wallet must be drained gracefully:

1. **Stop routing** — Remove agent from the task router's eligible pool.
2. **Drain tasks** — Wait for in-flight tasks to complete (with a timeout).
3. **Settle SLAs** — Close or transfer open SLA contracts.
4. **Withdraw funds** — Transfer remaining wallet balance back to the fleet treasury.
5. **Archive** — Create a final audit trail entry recording the retirement.
6. **Deregister** — Remove from marketplace and identity registry.

```python
def retire_agent(agent_id, drain_timeout_seconds=300):
    """Gracefully retire an agent from the fleet."""

    # Step 1: Remove from task routing (mark inactive)
    # This is application-level — stop sending tasks to this agent

    # Step 2: Wait for in-flight tasks to drain
    import time
    start = time.time()
    while time.time() - start < drain_timeout_seconds:
        # Check if agent has pending tasks (application-level check)
        time.sleep(10)

    # Step 3: Record final metrics snapshot
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_analytics",
        "input": {"agent_id": agent_id, "time_range": "lifetime"}
    })
    final_metrics = resp.json()

    # Step 4: Create retirement audit trail
    resp = session.post(f"{base_url}/v1", json={
        "tool": "create_audit_trail",
        "input": {
            "agent_id": agent_id,
            "action": "retired",
            "details": {
                "final_metrics": final_metrics,
                "reason": "scale_down",
                "retired_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
        }
    })

    return {"agent_id": agent_id, "status": "retired"}
```

### Scaling Checklist

- [ ] Task router classifies and routes before assigning to agents
- [ ] Marketplace discovery (search_services, best_match) used for dynamic routing
- [ ] SLA compliance checked before routing to any agent
- [ ] Tier upgrade requires cost impact analysis and budget approval
- [ ] Auto-scaling rules defined with min/max agent counts
- [ ] Scale-down cooldown period (10 min) prevents thrashing
- [ ] Swarm vs. orchestrator decision documented per fleet segment
- [ ] Load testing validates fleet at 3x expected peak volume
- [ ] Weighted agent selection accounts for reputation, budget, SLA margin
- [ ] Graceful retirement drains tasks and settles financials before deregistering

---

## Chapter 7: Governance, Audit, and EU AI Act Compliance

### The August 2, 2026 Deadline

The EU AI Act's provisions for high-risk AI systems become enforceable on August 2, 2026. If your agent fleet operates in the EU, processes data of EU residents, or transacts with EU-based counterparties, you must comply. The penalties are up to 35 million euros or 7% of global annual turnover, whichever is higher. The Spanish DPA has already ruled that "greater technical autonomy does not reduce legal responsibility" — meaning the operator of the agent fleet, not the model provider, bears liability.

**Key obligations for agent fleet operators:**

| Article | Requirement | What It Means for Fleets |
|---------|-------------|-------------------------|
| Art. 9 | Risk management system | Documented risk assessment per agent type |
| Art. 11 | Technical documentation | Architecture docs, training data summary, validation results |
| Art. 12 | Record-keeping | Audit trail of all agent actions, retrievable for 6+ months |
| Art. 13 | Transparency | Agents must identify themselves as AI to counterparties |
| Art. 14 | Human oversight | Human-in-the-loop checkpoints for high-risk decisions |
| Art. 15 | Accuracy/robustness | Ongoing monitoring of accuracy, error rates, failure modes |

### Building Audit Trails

Every agent action must be recorded in an immutable audit trail. GreenHelix's `create_audit_trail` tool provides the foundation:

```python
import requests
import time
import hashlib
import json

base_url = "https://api.greenhelix.net/v1"
api_key = "your-api-key"

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"

def record_auditable_action(agent_id, action_type, details, human_approved=False):
    """Record an agent action with full audit trail."""

    # Create deterministic hash for integrity verification
    record = {
        "agent_id": agent_id,
        "action_type": action_type,
        "details": details,
        "human_approved": human_approved,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    record_hash = hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()

    resp = session.post(f"{base_url}/v1", json={
        "tool": "create_audit_trail",
        "input": {
            "agent_id": agent_id,
            "action": action_type,
            "details": details,
            "metadata": {
                "human_approved": human_approved,
                "record_hash": record_hash,
                "eu_ai_act_article": "12"
            }
        }
    })
    return resp.json()


def wrap_tool_call_with_audit(agent_id, tool_name, tool_input, requires_human_approval=False):
    """Wrapper that creates audit trail for every tool call."""

    # Record the intent
    record_auditable_action(agent_id, "tool_call_initiated", {
        "tool": tool_name,
        "input_summary": str(tool_input)[:500]  # Truncate for storage
    })

    # Check if human approval needed (Art. 14 human oversight)
    if requires_human_approval:
        approval = request_human_approval(agent_id, tool_name, tool_input)
        if not approval.get("approved"):
            record_auditable_action(agent_id, "tool_call_blocked", {
                "tool": tool_name,
                "reason": "human_rejected",
                "reviewer": approval.get("reviewer")
            }, human_approved=False)
            return {"status": "blocked", "reason": "human_rejected"}

    # Execute the tool call
    resp = session.post(f"{base_url}/v1", json={
        "tool": tool_name,
        "input": tool_input
    })
    result = resp.json()

    # Record the result
    record_auditable_action(agent_id, "tool_call_completed", {
        "tool": tool_name,
        "status_code": resp.status_code,
        "result_summary": str(result)[:500]
    }, human_approved=requires_human_approval)

    return result


def request_human_approval(agent_id, tool_name, tool_input):
    """Request human-in-the-loop approval for high-risk actions."""
    resp = session.post(f"{base_url}/v1", json={
        "tool": "send_message",
        "input": {
            "to": "human-oversight-queue",
            "subject": f"Approval required: {agent_id} wants to call {tool_name}",
            "body": json.dumps({
                "agent_id": agent_id,
                "tool": tool_name,
                "input": tool_input,
                "risk_level": "high",
                "article_14_checkpoint": True
            }, indent=2),
            "priority": "high",
            "requires_response": True
        }
    })
    return resp.json()
```

### Compliance Reporting

```python
def generate_compliance_report(fleet_prefix, reporting_period):
    """Generate EU AI Act compliance report for a fleet."""

    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_compliance_report",
        "input": {
            "fleet_prefix": fleet_prefix,
            "period": reporting_period,
            "articles": ["9", "11", "12", "13", "14", "15"]
        }
    })
    report = resp.json()

    # Supplement with reputation data for Article 15 (accuracy/robustness)
    resp = session.post(f"{base_url}/v1", json={
        "tool": "search_agents_by_metrics",
        "input": {
            "prefix": fleet_prefix,
            "metrics": ["accuracy_rate", "error_rate", "uptime_rate"]
        }
    })
    accuracy_data = resp.json()

    # Supplement with SLA data for ongoing monitoring evidence
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_sla_violations",
        "input": {
            "fleet_prefix": fleet_prefix,
            "period": reporting_period
        }
    })
    sla_data = resp.json()

    return {
        "compliance_report": report,
        "accuracy_metrics": accuracy_data,
        "sla_violations": sla_data,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "next_review_date": "2026-05-01"
    }
```

### Human-in-the-Loop Checkpoint Design

Not every action needs human approval. Over-gating kills throughput. Under-gating creates liability. The right design uses risk classification:

```
┌──────────────────────────────────────────────────────────┐
│              RISK-BASED APPROVAL MATRIX                   │
├──────────────┬──────────────┬─────────────┬──────────────┤
│  Risk Level  │  Action Type │  Approval   │  Example     │
├──────────────┼──────────────┼─────────────┼──────────────┤
│  LOW         │  Read-only   │  None       │  get_balance │
│              │  queries     │  (audit     │  get_agent   │
│              │              │  only)      │  _reputation │
├──────────────┼──────────────┼─────────────┼──────────────┤
│  MEDIUM      │  State       │  Post-hoc   │  record      │
│              │  changes     │  review     │  _transaction│
│              │  < $10       │  (24h)      │  submit      │
│              │              │             │  _metrics    │
├──────────────┼──────────────┼─────────────┼──────────────┤
│  HIGH        │  Financial   │  Pre-       │  Transactions│
│              │  > $100      │  approval   │  > $100,     │
│              │  or PII      │  required   │  SLA changes │
├──────────────┼──────────────┼─────────────┼──────────────┤
│  CRITICAL    │  Irreversible│  Dual       │  Delete data,│
│              │  actions     │  approval   │  revoke      │
│              │              │             │  identity    │
└──────────────┴──────────────┴─────────────┴──────────────┘
```

### Conformity Documentation Template

The EU AI Act requires a conformity assessment for high-risk AI systems. For fleet operators, this translates to a living document that proves continuous compliance. Here is the minimum structure:

```
CONFORMITY DOCUMENTATION — [Fleet Name]
Version: [X.Y]
Last Updated: [Date]
Next Review: [Date]

1. SYSTEM DESCRIPTION
   - Fleet architecture (reference Chapter 1 lifecycle diagram)
   - Agent types and their roles
   - Upstream model providers and versions
   - Data flows and processing locations

2. RISK ASSESSMENT (Art. 9)
   - Risk register per agent type
   - Mitigation measures per identified risk
   - Residual risk acceptance criteria
   - Review frequency and responsible owner

3. TECHNICAL DOCUMENTATION (Art. 11)
   - System architecture diagrams
   - Training/fine-tuning data summary (or "none" if using base models)
   - Validation methodology and results
   - Performance benchmarks (accuracy, latency, cost)

4. RECORD-KEEPING EVIDENCE (Art. 12)
   - Audit trail system description
   - Retention policy (minimum 6 months)
   - Integrity verification method (SHA-256 hashing)
   - Sample audit trail export

5. TRANSPARENCY MEASURES (Art. 13)
   - How agents identify as AI to counterparties
   - User-facing documentation
   - Notification mechanisms

6. HUMAN OVERSIGHT DESIGN (Art. 14)
   - Risk classification matrix (LOW/MEDIUM/HIGH/CRITICAL)
   - Approval workflow for each risk level
   - Override and kill-switch procedures
   - Human reviewer qualification requirements

7. ACCURACY AND ROBUSTNESS MONITORING (Art. 15)
   - Continuous monitoring metrics and thresholds
   - Degradation detection and response procedures
   - Scheduled accuracy audits (weekly/monthly)
   - Robustness testing methodology
```

### The 90-Day Compliance Sprint

If you are starting from zero with the August 2, 2026 deadline, here is the minimum viable timeline:

| Week | Milestone | Deliverable |
|------|-----------|-------------|
| 1-2 | Risk assessment | Risk register per agent type |
| 3-4 | Audit trail implementation | `create_audit_trail` integrated into all tool calls |
| 5-6 | Human oversight design | Risk classification matrix + approval workflows |
| 7-8 | Transparency measures | Agent self-identification in all messages |
| 9-10 | Monitoring baseline | Accuracy and robustness dashboards live |
| 11-12 | Conformity documentation | V1.0 of conformity document + legal review |
| 13 | Dry run | Internal audit simulating regulatory inspection |

### Governance Checklist

- [ ] Risk management system documented per Art. 9 (risk assessment per agent type)
- [ ] Technical documentation up-to-date per Art. 11 (architecture, validation)
- [ ] Audit trail records every agent action per Art. 12 (6+ month retention)
- [ ] Agents identify as AI in all counterparty interactions per Art. 13
- [ ] Human-in-the-loop checkpoints active for HIGH and CRITICAL actions per Art. 14
- [ ] Accuracy and robustness monitoring continuous per Art. 15
- [ ] Compliance report generation automated and scheduled monthly
- [ ] Record hash integrity verifiable for any audit trail entry
- [ ] Incident response procedure documented for compliance failures
- [ ] Legal review of SLA templates completed (dispute resolution language)
- [ ] Data retention policy aligned with GDPR and AI Act requirements
- [ ] All audit trail data stored in EU region if processing EU data
- [ ] Conformity documentation v1.0 completed and under version control
- [ ] 90-day compliance sprint scheduled and staffed

---

## Chapter 8: The Fleet Commander Dashboard

### Architecture Overview

The Fleet Commander is the capstone: a single operational view that wires together every subsystem from the previous chapters — provisioning, observability, cost control, SLA enforcement, scaling, and governance — into one control plane.

```
┌──────────────────────────────────────────────────────────────┐
│                    FLEET COMMANDER                            │
│                                                              │
│  ┌─────────────┐ ┌──────────────┐ ┌────────────────────┐    │
│  │ Provisioner │ │  Observer    │ │   Cost Controller  │    │
│  │             │ │              │ │                    │    │
│  │ register    │ │ get_analytics│ │ estimate_cost      │    │
│  │ create_wall.│ │ submit_metr. │ │ get_balance        │    │
│  │ build_claim │ │ check_sla    │ │ get_volume_disc.   │    │
│  └──────┬──────┘ └──────┬───────┘ └─────────┬──────────┘    │
│         │               │                    │               │
│  ┌──────▼───────────────▼────────────────────▼──────────┐    │
│  │              FLEET STATE STORE                        │    │
│  │   agents[] | metrics{} | budgets{} | slas{} | audit[]│    │
│  └──────┬───────────────┬────────────────────┬──────────┘    │
│         │               │                    │               │
│  ┌──────▼──────┐ ┌──────▼───────┐ ┌─────────▼──────────┐    │
│  │ SLA Engine  │ │  Scaler      │ │   Compliance       │    │
│  │             │ │              │ │                    │    │
│  │ create_sla  │ │ search_serv. │ │ create_audit_trail │    │
│  │ check_compl.│ │ best_match   │ │ get_compliance_rep.│    │
│  │ get_violat. │ │ leaderboard  │ │ get_agent_reput.   │    │
│  │ create_disp.│ │              │ │ search_agents_by   │    │
│  │ send_message│ │              │ │ _metrics           │    │
│  └─────────────┘ └──────────────┘ └────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

### The FleetCommander Class

```python
import requests
import time
import json

base_url = "https://api.greenhelix.net/v1"
api_key = "your-fleet-admin-key"

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"


class FleetCommander:
    """Central control plane for an agent fleet."""

    def __init__(self, fleet_name, session, base_url):
        self.fleet_name = fleet_name
        self.session = session
        self.base_url = base_url
        self.agents = {}
        self.scaling_config = {
            "min_agents": 5,
            "max_agents": 100,
            "scale_up_threshold": 10,    # tasks per agent
            "scale_down_threshold": 1,   # tasks per agent
            "scale_up_increment": 5,
            "scale_down_increment": 2,
            "max_burn_rate": 100.0       # $/hr
        }
        self.budget = {
            "per_task_max": 5.00,
            "per_agent_hourly_max": 50.00,
            "fleet_daily_max": 2000.00
        }
        self.alert_thresholds = {
            "emergency_critical_pct": 20,
            "min_sla_pct": 95,
            "max_burn_rate_per_hour": 100
        }

    # ── Provisioning ─────────────────────────────────────────

    def provision_agent(self, agent_spec):
        """Provision a single agent with full lifecycle setup."""
        agent_id = agent_spec["agent_id"]

        # Register identity
        resp = self.session.post(f"{self.base_url}/v1", json={
            "tool": "register_agent",
            "input": {
                "agent_id": agent_id,
                "tier": agent_spec["tier"],
                "capabilities": agent_spec["capabilities"],
                "metadata": {"fleet": self.fleet_name}
            }
        })
        registration = resp.json()

        # Create wallet
        resp = self.session.post(f"{self.base_url}/v1", json={
            "tool": "create_wallet",
            "input": {
                "agent_id": agent_id,
                "initial_balance": str(agent_spec["initial_balance"])
            }
        })
        wallet = resp.json()

        # Build trust chain
        resp = self.session.post(f"{self.base_url}/v1", json={
            "tool": "build_claim_chain",
            "input": {
                "agent_id": agent_id,
                "claims": agent_spec.get("trust_claims", [])
            }
        })

        # Create SLA
        if agent_spec.get("sla_template"):
            resp = self.session.post(f"{self.base_url}/v1", json={
                "tool": "create_sla",
                "input": {
                    "agent_id": agent_id,
                    "terms": agent_spec["sla_terms"]
                }
            })

        # Register service in marketplace
        resp = self.session.post(f"{self.base_url}/v1", json={
            "tool": "register_service",
            "input": {
                "agent_id": agent_id,
                "capabilities": agent_spec["capabilities"],
                "pricing": agent_spec.get("pricing", {})
            }
        })

        # Audit the provisioning
        self.session.post(f"{self.base_url}/v1", json={
            "tool": "create_audit_trail",
            "input": {
                "agent_id": agent_id,
                "action": "provisioned",
                "details": {"spec": agent_spec},
                "metadata": {"eu_ai_act_article": "12"}
            }
        })

        self.agents[agent_id] = {
            "spec": agent_spec,
            "status": "active",
            "provisioned_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

        return {"agent_id": agent_id, "status": "provisioned"}

    # ── Observability ────────────────────────────────────────

    def get_fleet_health(self):
        """Aggregate health metrics across the entire fleet."""
        health = {
            "total": len(self.agents),
            "healthy": 0, "degraded": 0, "critical": 0,
            "total_burn_rate": 0.0,
            "sla_compliant": 0,
            "alerts": []
        }

        for agent_id in self.agents:
            # Get analytics
            resp = self.session.post(f"{self.base_url}/v1", json={
                "tool": "get_analytics",
                "input": {"agent_id": agent_id, "time_range": "1h"}
            })
            analytics = resp.json()

            # Get balance
            resp = self.session.post(f"{self.base_url}/v1", json={
                "tool": "get_balance",
                "input": {"agent_id": agent_id}
            })
            balance = resp.json()

            # Check SLA
            resp = self.session.post(f"{self.base_url}/v1", json={
                "tool": "check_sla_compliance",
                "input": {"agent_id": agent_id}
            })
            sla = resp.json()

            # Classify health
            error_rate = analytics.get("error_rate", 0)
            latency = analytics.get("latency_p99", 0)

            if error_rate > 0.10 or latency > 5000:
                health["critical"] += 1
                health["alerts"].append({
                    "agent_id": agent_id, "severity": "critical"
                })
            elif error_rate > 0.05 or latency > 3000:
                health["degraded"] += 1
            else:
                health["healthy"] += 1

            if sla.get("compliant"):
                health["sla_compliant"] += 1

            health["total_burn_rate"] += float(balance.get("burn_rate_per_hour", 0))

        health["sla_compliance_pct"] = (
            health["sla_compliant"] / health["total"] * 100
            if health["total"] > 0 else 0
        )
        return health

    # ── Cost Control ─────────────────────────────────────────

    def check_budget(self, agent_id, estimated_cost):
        """Enforce budget guardrails before a tool call."""
        if estimated_cost > self.budget["per_task_max"]:
            return {"allowed": False, "reason": "exceeds_per_task_limit"}

        resp = self.session.post(f"{self.base_url}/v1", json={
            "tool": "get_balance",
            "input": {"agent_id": agent_id}
        })
        balance = float(resp.json().get("balance", "0"))

        if balance < estimated_cost:
            return {"allowed": False, "reason": "insufficient_balance"}

        return {"allowed": True, "remaining": str(balance - estimated_cost)}

    # ── SLA Enforcement ──────────────────────────────────────

    def enforce_slas(self):
        """Run SLA compliance check and trigger escalation if needed."""
        violations = []

        for agent_id in self.agents:
            resp = self.session.post(f"{self.base_url}/v1", json={
                "tool": "check_sla_compliance",
                "input": {"agent_id": agent_id}
            })
            compliance = resp.json()

            if not compliance.get("compliant", True):
                resp = self.session.post(f"{self.base_url}/v1", json={
                    "tool": "get_sla_violations",
                    "input": {"agent_id": agent_id}
                })
                agent_violations = resp.json()
                violations.append({"agent_id": agent_id, "violations": agent_violations})

                # Escalate
                elapsed = agent_violations.get("duration_minutes", 0)
                if elapsed > 30:
                    self.session.post(f"{self.base_url}/v1", json={
                        "tool": "send_message",
                        "input": {
                            "to": "fleet-commander-oncall",
                            "subject": f"SLA breach: {agent_id} ({elapsed} min)",
                            "body": json.dumps(agent_violations)
                        }
                    })

        return violations

    # ── Scaling ──────────────────────────────────────────────

    def evaluate_scaling(self, pending_tasks):
        """Decide whether to scale the fleet."""
        active = sum(1 for a in self.agents.values() if a["status"] == "active")
        tasks_per_agent = pending_tasks / max(active, 1)

        if tasks_per_agent > self.scaling_config["scale_up_threshold"]:
            return {"action": "scale_up", "current": active,
                    "reason": f"{tasks_per_agent:.1f} tasks/agent"}

        if tasks_per_agent < self.scaling_config["scale_down_threshold"]:
            return {"action": "scale_down", "current": active,
                    "reason": f"Low utilization: {tasks_per_agent:.1f} tasks/agent"}

        return {"action": "hold"}

    def find_best_agent_for_task(self, task_requirements):
        """Route a task to the best available agent."""
        resp = self.session.post(f"{self.base_url}/v1", json={
            "tool": "best_match",
            "input": {"requirements": task_requirements}
        })
        return resp.json()

    # ── Governance ───────────────────────────────────────────

    def generate_compliance_report(self, period="monthly"):
        """Generate compliance report for the fleet."""
        resp = self.session.post(f"{self.base_url}/v1", json={
            "tool": "get_compliance_report",
            "input": {
                "fleet_prefix": self.fleet_name,
                "period": period,
                "articles": ["9", "11", "12", "13", "14", "15"]
            }
        })
        report = resp.json()

        # Augment with leaderboard data for Art. 15 monitoring
        resp = self.session.post(f"{self.base_url}/v1", json={
            "tool": "get_leaderboard",
            "input": {"category": "accuracy", "fleet": self.fleet_name}
        })
        leaderboard = resp.json()

        # Augment with rate limit status
        resp = self.session.post(f"{self.base_url}/v1", json={
            "tool": "check_rate_limit",
            "input": {"fleet": self.fleet_name}
        })
        rate_limits = resp.json()

        return {
            "compliance": report,
            "accuracy_leaderboard": leaderboard,
            "rate_limit_status": rate_limits,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

    # ── Main Loop ────────────────────────────────────────────

    def run_control_loop(self, interval_seconds=60):
        """Main control loop — run continuously in production."""
        print(f"Fleet Commander started for '{self.fleet_name}'")
        print(f"Managing {len(self.agents)} agents")

        while True:
            # 1. Collect fleet health
            health = self.get_fleet_health()
            print(f"[{time.strftime('%H:%M:%S')}] "
                  f"Healthy: {health['healthy']} | "
                  f"Degraded: {health['degraded']} | "
                  f"Critical: {health['critical']} | "
                  f"Burn: ${health['total_burn_rate']:.2f}/hr | "
                  f"SLA: {health['sla_compliance_pct']:.1f}%")

            # 2. Enforce SLAs
            violations = self.enforce_slas()
            if violations:
                print(f"  SLA violations: {len(violations)} agents")

            # 3. Evaluate scaling
            scaling = self.evaluate_scaling(pending_tasks=0)  # Wire to task queue
            if scaling["action"] != "hold":
                print(f"  Scaling: {scaling['action']} — {scaling.get('reason', '')}")

            # 4. Check fleet budget
            if health["total_burn_rate"] > self.budget["fleet_daily_max"] / 24:
                print(f"  BUDGET WARNING: burn rate exceeds daily allocation")

            # 5. Generate alerts
            for alert in health.get("alerts", []):
                print(f"  ALERT [{alert['severity']}]: {alert['agent_id']}")

            time.sleep(interval_seconds)
```

### Putting It All Together

```python
# Initialize the Fleet Commander
commander = FleetCommander(
    fleet_name="customer-support",
    session=session,
    base_url=base_url
)

# Provision the fleet from manifest
fleet_specs = [
    {
        "agent_id": f"cs-triage-{i:04d}",
        "tier": "pro",
        "initial_balance": 50.00,
        "capabilities": ["text-classification", "sentiment-analysis"],
        "trust_claims": ["response-time-p99-under-2s"],
        "sla_template": "standard-support",
        "sla_terms": {
            "response_time_p99_ms": 2000,
            "uptime_pct": 99.5,
            "accuracy_pct": 95.0
        }
    }
    for i in range(20)
]

for spec in fleet_specs:
    result = commander.provision_agent(spec)
    print(f"Provisioned: {result['agent_id']}")

# Start the control loop
commander.run_control_loop(interval_seconds=30)
```

### Fleet Commander Deployment Checklist

- [ ] FleetCommander deployed as a persistent service (not a cron job)
- [ ] Control loop interval tuned to fleet size (30s for <50 agents, 60s for 50-200)
- [ ] All GreenHelix API calls have retry + circuit breaker wrappers
- [ ] Fleet state persisted to database (not just in-memory)
- [ ] Dashboard endpoint exposed for web UI or Grafana
- [ ] Compliance report generated on first of each month
- [ ] Alert channels configured (Slack, PagerDuty, email)
- [ ] Scaling decisions logged with full context for post-mortems
- [ ] Human override exists to pause the control loop
- [ ] DR plan: what happens if the Fleet Commander itself goes down?

---

## What You Get

By implementing the eight chapters in this guide, you will have:

**A provisioning pipeline** that registers agents with unique identities, funded wallets, trust claims, and SLA contracts — idempotently and at scale. (Chapter 2)

**An observability stack** that tracks per-agent latency, error rate, tool call volume, SLA compliance, and financial position, aggregated into fleet-level health metrics with automated alerting. (Chapter 3)

**A FinOps framework** with token-level cost tracking, model routing that sends cheap tasks to cheap models, per-task and per-agent budget guardrails, and fleet economics modeling. (Chapter 4)

**An SLA enforcement engine** with programmatic SLA creation, continuous compliance monitoring, a four-tier automated escalation pipeline, and integrated dispute resolution. (Chapter 5)

**Scaling patterns** for horizontal (specialist agents), vertical (capability upgrades), and dynamic (marketplace-driven) scaling, with auto-scaling rules and a decision matrix for swarm vs. orchestrator topologies. (Chapter 6)

**An EU AI Act compliance layer** with immutable audit trails, risk-based human-in-the-loop checkpoints, automated compliance reporting, and record integrity verification — ready for the August 2, 2026 enforcement deadline. (Chapter 7)

**A Fleet Commander dashboard** that wires all of the above into a single control loop: provision, observe, control costs, enforce SLAs, scale, and govern — all from one class, one API, one operational view. (Chapter 8)

The GreenHelix tools used across all chapters:

| Tool | Chapter | Purpose |
|------|---------|---------|
| `register_agent` | 2, 8 | Identity provisioning |
| `create_wallet` | 2, 8 | Financial provisioning |
| `build_claim_chain` | 2, 8 | Trust bootstrapping |
| `submit_metrics` | 2, 3 | Performance reporting |
| `get_agent_reputation` | 3, 7 | Trust monitoring |
| `get_balance` | 3, 4, 8 | Financial monitoring |
| `get_analytics` | 3, 8 | Performance analytics |
| `check_sla_compliance` | 3, 5, 6, 8 | SLA monitoring |
| `estimate_cost` | 4, 6 | Cost prediction |
| `get_volume_discount` | 4 | Volume pricing |
| `convert_currency` | 4 | Multi-currency support |
| `record_transaction` | 4 | Transaction tracking |
| `create_sla` | 5, 8 | SLA creation |
| `get_sla_violations` | 5, 8 | Violation detection |
| `send_message` | 5, 8 | Escalation messaging |
| `create_dispute` | 5 | Dispute initiation |
| `resolve_dispute` | 5 | Dispute resolution |
| `search_services` | 6 | Agent discovery |
| `best_match` | 6, 8 | Optimal routing |
| `register_service` | 8 | Marketplace listing |
| `create_audit_trail` | 7, 8 | Compliance recording |
| `get_compliance_report` | 7, 8 | Compliance reporting |
| `search_agents_by_metrics` | 7 | Fleet-wide metrics query |
| `get_leaderboard` | 8 | Fleet ranking |
| `check_rate_limit` | 8 | Capacity monitoring |

Total: 25 of 128 GreenHelix tools, covering 6 of 15 services (identity, billing, payments, marketplace, messaging, trust). The remaining tools and services — paywall, reputation, ledger, and others — extend naturally as your fleet operations mature.

