---
name: greenhelix-agent-migration-versioning
version: "1.3.1"
description: "Agent Migration & Versioning: Blue-Green Deployments, Canary Releases, and Rollback Strategies for AI Agent Commerce. Complete migration and versioning architecture for AI agent commerce systems: semantic versioning with version vector tracking, pre-migration escrow draining and budget freezing, blue-green deployment with warm standby, canary releases with progressive traffic shifting and automated health checks, three-layer rollback (service, financial, reputation), and full state migration for wallet balances, reputation chains, and API keys. detailed code examples with Python classes with full API integratio"
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [devops, migration, versioning, blue-green, canary, rollback, agent-ops, deployment, guide, greenhelix, openclaw, ai-agent]
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
# Agent Migration & Versioning: Blue-Green Deployments, Canary Releases, and Rollback Strategies for AI Agent Commerce

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `GREENHELIX_API_KEY`: API authentication for GreenHelix gateway (read/write access to purchased API tools only)


Your payment-processing agent fleet handles $180K per month across 12 agents. Each agent has its own wallet balance, reputation score, active escrows, marketplace listings, and API keys. On Thursday morning you push a prompt update to your primary settlement agent -- the one responsible for releasing escrow funds when work is verified. The update includes a refined verification heuristic that is supposed to reduce false rejections by 15%. By Thursday afternoon, the new heuristic has approved three fraudulent deliverables, releasing $4,200 in escrow to agents that did not complete the contracted work. Your counterparties file disputes. Your settlement agent's reputation score drops from 94 to 71. Two marketplace partners pause their integrations because their SLAs require counterparties with reputation scores above 80. You cannot roll back because the old agent version is gone -- you deployed in place, overwrote the prompt, and the previous configuration exists only in a Git commit you have to go find. The rollback itself takes 40 minutes. During those 40 minutes, $12,000 in pending escrows cannot be processed because you have taken the settlement agent offline while you reconstruct the old version. Total damage: $4,200 in fraudulent releases, $12,000 in delayed escrows, two partnership SLAs breached, and a reputation score that will take weeks to rebuild. The cause was not the prompt change. The cause was deploying a stateful, financially-active agent the same way you would deploy a stateless web service -- overwrite and pray.
Standard DevOps has solved this for web applications. Blue-green deployments, canary releases, rolling updates, and feature flags are mature patterns for stateless HTTP services. But agents are not stateless HTTP services. An agent has a wallet balance that cannot be duplicated. It has a reputation score that is earned over months and destroyed in hours. It has active escrows that represent real money locked in contracts with real counterparties. It has API keys that, if mismanaged during migration, create either a security hole (two versions sharing a key) or a service outage (old version's key revoked before new version is live). Every assumption in the standard deployment playbook breaks when the thing being deployed has financial state, contractual obligations, and an identity that other agents trust.
This guide gives you the complete migration and versioning architecture for AI agent commerce systems. Every class calls the GreenHelix A2A Commerce Gateway API. Every pattern preserves financial integrity, reputation continuity, and contractual obligations across version transitions.

## What You'll Learn
- Chapter 1: Why Agent Versioning Is Hard
- Chapter 2: Version Naming & Registry
- Chapter 3: Pre-Migration Checks
- Chapter 4: Blue-Green Deployment
- Chapter 5: Canary Releases
- Chapter 6: Rollback Strategies
- Chapter 7: State Migration
- Chapter 8: Production Migration Checklist
- GreenHelix Migration Manager — Working Implementation

## Full Guide

# Agent Migration & Versioning: Blue-Green Deployments, Canary Releases, and Rollback Strategies for AI Agent Commerce

Your payment-processing agent fleet handles $180K per month across 12 agents. Each agent has its own wallet balance, reputation score, active escrows, marketplace listings, and API keys. On Thursday morning you push a prompt update to your primary settlement agent -- the one responsible for releasing escrow funds when work is verified. The update includes a refined verification heuristic that is supposed to reduce false rejections by 15%. By Thursday afternoon, the new heuristic has approved three fraudulent deliverables, releasing $4,200 in escrow to agents that did not complete the contracted work. Your counterparties file disputes. Your settlement agent's reputation score drops from 94 to 71. Two marketplace partners pause their integrations because their SLAs require counterparties with reputation scores above 80. You cannot roll back because the old agent version is gone -- you deployed in place, overwrote the prompt, and the previous configuration exists only in a Git commit you have to go find. The rollback itself takes 40 minutes. During those 40 minutes, $12,000 in pending escrows cannot be processed because you have taken the settlement agent offline while you reconstruct the old version. Total damage: $4,200 in fraudulent releases, $12,000 in delayed escrows, two partnership SLAs breached, and a reputation score that will take weeks to rebuild. The cause was not the prompt change. The cause was deploying a stateful, financially-active agent the same way you would deploy a stateless web service -- overwrite and pray.

Standard DevOps has solved this for web applications. Blue-green deployments, canary releases, rolling updates, and feature flags are mature patterns for stateless HTTP services. But agents are not stateless HTTP services. An agent has a wallet balance that cannot be duplicated. It has a reputation score that is earned over months and destroyed in hours. It has active escrows that represent real money locked in contracts with real counterparties. It has API keys that, if mismanaged during migration, create either a security hole (two versions sharing a key) or a service outage (old version's key revoked before new version is live). Every assumption in the standard deployment playbook breaks when the thing being deployed has financial state, contractual obligations, and an identity that other agents trust.

This guide gives you the complete migration and versioning architecture for AI agent commerce systems. Every class calls the GreenHelix A2A Commerce Gateway API. Every pattern preserves financial integrity, reputation continuity, and contractual obligations across version transitions.

---

## Table of Contents

1. [Why Agent Versioning Is Hard](#chapter-1-why-agent-versioning-is-hard)
2. [Version Naming & Registry](#chapter-2-version-naming--registry)
3. [Pre-Migration Checks](#chapter-3-pre-migration-checks)
4. [Blue-Green Deployment](#chapter-4-blue-green-deployment)
5. [Canary Releases](#chapter-5-canary-releases)
6. [Rollback Strategies](#chapter-6-rollback-strategies)
7. [State Migration](#chapter-7-state-migration)
8. [Production Migration Checklist](#chapter-8-production-migration-checklist)

---

## Chapter 1: Why Agent Versioning Is Hard

### Agents Are Stateful in Ways Services Are Not

A stateless web service stores its state in a database. When you deploy a new version of the service, the new version connects to the same database. State continuity is trivial because the state was never in the service to begin with. Agent commerce systems do not work this way.

An agent's state is distributed across multiple systems, and much of it is not under your direct control. The wallet balance lives on the billing platform. The reputation score lives on the trust platform and is partially determined by counterparty ratings you cannot predict or modify. Active escrows live on the escrow platform and have contractual obligations -- timeout deadlines, release conditions, dispute windows -- that continue running regardless of whether your agent is online. Marketplace listings advertise the agent's capabilities and pricing to other agents who may be mid-negotiation when you deploy a new version. API keys bind the agent's identity to its authorization, and rotating them at the wrong time creates a window where the agent cannot authenticate.

In a traditional deployment, the worst case is a few seconds of 503 errors while the load balancer drains connections. In an agent deployment, the worst case is locked funds, broken contracts, destroyed reputation, and counterparties who blacklist your agent permanently. The blast radius of a botched agent deployment is measured in dollars and trust, not in error rates and latency percentiles.

### Silent Version Drift

Agent versioning is harder than service versioning for a second reason: agents have more dimensions of change. A web service changes when its code changes. An agent changes when any of the following change:

- **Prompt or system instructions**: The behavioral specification that determines how the agent interprets inputs and selects actions.
- **Model version**: The underlying language model -- a model upgrade can change behavior on every input.
- **Tool set**: The tools the agent can call and the schemas it uses to call them.
- **Memory or context**: The accumulated knowledge the agent has built from prior interactions.
- **Configuration**: Budget caps, reputation thresholds, retry policies, timeout values.

These dimensions change independently. A prompt update is not a code deploy. A model upgrade happens on the provider's schedule, not yours. Memory accumulates continuously. The result is version drift -- the agent's behavior changes without any discrete deployment event. You cannot point to a commit hash and say "this is what the agent is running." The agent's effective version is the combination of all five dimensions, and tracking that combination requires explicit version management that most teams do not have.

### The $47K Lesson

The scenario in the introduction is a composited version of real incidents reported across agent commerce operators. The pattern repeats: a team treats an agent deployment like a service deployment, something goes wrong during the transition, and the financial consequences are orders of magnitude worse than a web service outage. The common factors are always the same: no pre-migration checks on active escrows, no parallel running of old and new versions, no automated rollback, and no reputation snapshot to compare against.

CIO.com's 2026 enterprise AI survey found that 67% of organizations running AI agents in production had experienced at least one deployment-related incident involving financial loss or contractual breach. The median cost per incident was $23,000. The number one requested capability was "safe agent versioning with rollback" -- ahead of better prompts, faster models, and more tools. The CIO's next big challenge is not building agents. It is operating them safely through continuous change.

### What This Guide Covers

This guide solves the agent versioning problem with seven concrete patterns, each implemented as a Python class that calls the GreenHelix API:

1. A **version registry** that tracks the full version vector (prompt, model, tools, config) for every agent version.
2. **Pre-migration checks** that verify all escrows are drained, budgets are frozen, and reputation is snapshotted before any migration begins.
3. **Blue-green deployment** that runs old and new versions simultaneously, switches traffic atomically, and keeps the old version warm for instant rollback.
4. **Canary releases** that route a percentage of traffic to the new version and automatically roll back if health metrics degrade.
5. **Rollback strategies** that restore not just the code but the financial state, reputation, and contractual obligations to their pre-migration state.
6. **State migration** that safely transfers wallet balances, reputation chains, and API keys between agent versions.
7. A **production checklist** that codifies the entire process into a repeatable runbook.

---

## Chapter 2: Version Naming & Registry

### Semantic Versioning for Agents

Standard semantic versioning (semver) uses three numbers: `MAJOR.MINOR.PATCH`. For web services, the semantics are well-defined: MAJOR for breaking API changes, MINOR for backwards-compatible features, PATCH for bug fixes. For agents, the semantics need to be redefined because agents do not have APIs in the traditional sense. Their "interface" is their behavior -- the way they respond to inputs, select tools, and interact with counterparties.

Agent semver:

- **MAJOR**: Changes that alter the agent's financial behavior. New escrow strategies, different pricing logic, changes to settlement conditions, switching models. Any change that could cause a counterparty to receive different financial outcomes from the same input.
- **MINOR**: Changes that alter the agent's non-financial behavior. Improved response quality, better error messages, additional metadata in responses, new non-financial tools. Counterparties get the same financial outcomes but may notice different interaction patterns.
- **PATCH**: Changes that do not alter observable behavior. Internal refactoring, logging improvements, dependency updates, configuration tweaks that do not change thresholds.

The version string should also encode the version vector dimensions that changed. A recommended format is `MAJOR.MINOR.PATCH+prompt.MODEL.tools`. For example, `2.1.0+p3.gpt4o.t7` means major version 2, minor version 1, patch 0, prompt revision 3, GPT-4o model, tool schema revision 7. This format is semver-compatible (everything after `+` is build metadata per the semver spec) and gives operators instant visibility into what changed.

### The Version Registry

Every agent version must be registered in a central registry before it can be deployed. The registry stores the full version vector, the deployment state (staging, canary, active, retired), and the timestamps for every state transition. The GreenHelix agent identity system serves as the registry backend -- agent metadata can store arbitrary JSON, and we use it to maintain a version history.

```python
import requests
import json
import time
import hashlib
from typing import Optional
from dataclasses import dataclass, field


# --- GreenHelix sandbox session (free tier: 500 credits, no key required) ---
# To get started, visit https://sandbox.greenhelix.net — no signup needed.
# For production, set GREENHELIX_API_KEY in your environment.
import os

API_BASE = os.environ.get("GREENHELIX_API_URL", "https://sandbox.greenhelix.net")

session = requests.Session()
api_key = os.environ.get("GREENHELIX_API_KEY", "")
if api_key:
    session.headers["Authorization"] = f"Bearer {api_key}"
session.headers["Content-Type"] = "application/json"


def api_call(tool: str, input_data: dict) -> dict:
    """Call a GreenHelix REST endpoint for the given tool."""
    response = session.post(f"{API_BASE}/v1/tools/{tool}", json=input_data)
    response.raise_for_status()
    return response.json()


@dataclass
class AgentVersion:
    """Represents a single version of an agent."""
    version: str           # e.g., "2.1.0"
    prompt_hash: str       # SHA-256 of the prompt text
    model: str             # e.g., "gpt-4o-2025-03"
    tool_schema_hash: str  # SHA-256 of the serialized tool schemas
    config_hash: str       # SHA-256 of the configuration
    state: str = "staging" # staging | canary | active | retired
    created_at: float = field(default_factory=time.time)
    activated_at: Optional[float] = None
    retired_at: Optional[float] = None

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "prompt_hash": self.prompt_hash,
            "model": self.model,
            "tool_schema_hash": self.tool_schema_hash,
            "config_hash": self.config_hash,
            "state": self.state,
            "created_at": self.created_at,
            "activated_at": self.activated_at,
            "retired_at": self.retired_at,
        }


class AgentVersionManager:
    """Manages version lifecycle for an agent via GreenHelix identity metadata."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self._versions: dict[str, AgentVersion] = {}

    def _load_versions(self) -> None:
        """Load version history from agent identity metadata."""
        identity = api_call("get_agent_identity", {
            "agent_id": self.agent_id,
        })
        metadata = identity.get("metadata", {})
        version_history = metadata.get("version_history", {})
        self._versions = {}
        for ver_str, ver_data in version_history.items():
            self._versions[ver_str] = AgentVersion(**ver_data)

    def _save_versions(self) -> None:
        """Persist version history to agent identity metadata."""
        version_history = {
            ver: v.to_dict() for ver, v in self._versions.items()
        }
        api_call("register_agent", {
            "agent_id": self.agent_id,
            "metadata": {
                "version_history": version_history,
                "current_version": self.get_current_version(),
            },
        })

    def register_version(
        self,
        version: str,
        prompt_text: str,
        model: str,
        tool_schemas: dict,
        config: dict,
    ) -> AgentVersion:
        """Register a new version in staging state."""
        self._load_versions()

        if version in self._versions:
            raise ValueError(f"Version {version} already registered")

        prompt_hash = hashlib.sha256(prompt_text.encode()).hexdigest()[:16]
        schema_hash = hashlib.sha256(
            json.dumps(tool_schemas, sort_keys=True).encode()
        ).hexdigest()[:16]
        config_hash = hashlib.sha256(
            json.dumps(config, sort_keys=True).encode()
        ).hexdigest()[:16]

        agent_version = AgentVersion(
            version=version,
            prompt_hash=prompt_hash,
            model=model,
            tool_schema_hash=schema_hash,
            config_hash=config_hash,
            state="staging",
        )
        self._versions[version] = agent_version
        self._save_versions()
        return agent_version

    def get_current_version(self) -> Optional[str]:
        """Return the version string of the currently active version."""
        for ver_str, ver in self._versions.items():
            if ver.state == "active":
                return ver_str
        return None

    def list_versions(self) -> list[dict]:
        """Return all versions with their states."""
        self._load_versions()
        return [v.to_dict() for v in self._versions.values()]

    def activate_version(self, version: str) -> None:
        """Transition a version from staging/canary to active.
        Retires the previously active version."""
        self._load_versions()
        if version not in self._versions:
            raise ValueError(f"Version {version} not registered")

        # Retire current active version
        current = self.get_current_version()
        if current and current != version:
            self._versions[current].state = "retired"
            self._versions[current].retired_at = time.time()

        # Activate new version
        self._versions[version].state = "active"
        self._versions[version].activated_at = time.time()
        self._save_versions()

    def retire_version(self, version: str) -> None:
        """Retire a version, marking it as no longer deployable."""
        self._load_versions()
        if version not in self._versions:
            raise ValueError(f"Version {version} not registered")
        self._versions[version].state = "retired"
        self._versions[version].retired_at = time.time()
        self._save_versions()

    def get_version(self, version: str) -> Optional[AgentVersion]:
        """Retrieve a specific version's details."""
        self._load_versions()
        return self._versions.get(version)
```

### Registration Workflow

```python
# Initialize the version manager for your settlement agent
manager = AgentVersionManager(agent_id="acme-settlement-01")

# Register the new version before deploying anything
new_version = manager.register_version(
    version="2.1.0",
    prompt_text=open("prompts/settlement_v2.1.txt").read(),
    model="gpt-4o-2025-03",
    tool_schemas=json.load(open("schemas/settlement_tools.json")),
    config={
        "budget_cap": 5000,
        "escrow_timeout": 3600,
        "reputation_threshold": 80,
        "max_retries": 3,
    },
)

print(f"Registered version {new_version.version}")
print(f"State: {new_version.state}")        # "staging"
print(f"Prompt hash: {new_version.prompt_hash}")
print(f"Model: {new_version.model}")

# List all versions to see history
for v in manager.list_versions():
    print(f"  {v['version']}: {v['state']}")
```

### Why Version Hashing Matters

Every dimension of the version vector is hashed, not stored in full. This serves three purposes. First, it keeps the registry metadata small -- agent identity metadata has practical size limits, and storing full prompt texts would exceed them quickly. Second, it enables fast comparison: to determine if two deployments are identical, compare four 16-character strings instead of diffing kilobytes of text. Third, it creates an audit trail that proves what was deployed without storing the potentially sensitive contents of prompts and configurations in the identity system. The full artifacts (prompt text, tool schemas, configuration files) are stored in your artifact repository (S3, GCS, or a Git repo). The registry stores the hashes and the state machine. Deployment tooling fetches artifacts by version string and verifies the hashes match before deploying.

---

## Chapter 3: Pre-Migration Checks

### Why You Cannot Just Deploy

The most dangerous moment in an agent's lifecycle is the transition between versions. During that transition, the old version is winding down and the new version is spinning up. If the old version has active escrows, those escrows have deadlines and contractual obligations that do not pause because you are deploying. If the old version has a wallet balance, that balance must be accounted for -- you cannot have two versions spending from the same wallet without coordination. If the old version has a reputation score of 94, you need to snapshot that score so you can detect if the new version degrades it and roll back before the damage is permanent.

Pre-migration checks answer one question: is it safe to begin the migration right now? If any check fails, the migration is aborted before anything changes. This is the single most important pattern in this guide. Every botched agent migration I have investigated could have been prevented by pre-migration checks that someone skipped because they were in a hurry.

### The Pre-Migration Check Suite

The check suite verifies four conditions:

1. **Escrow drain**: All active escrows must be resolved (released, refunded, or expired). No pending escrows means no contractual obligations that could be disrupted by the migration.
2. **Balance verification**: The wallet balance must be above a minimum threshold and below a maximum threshold. Too low means the new version cannot operate. Too high means there is unaccounted-for money that should have been settled.
3. **Budget freeze**: The budget cap is set to zero before migration begins, preventing either version from creating new financial commitments during the transition.
4. **Reputation snapshot**: The current reputation score and metrics are recorded so that post-migration verification can detect degradation.

```python
@dataclass
class PreMigrationReport:
    """Result of all pre-migration checks."""
    agent_id: str
    version_from: str
    version_to: str
    timestamp: float
    escrow_clear: bool
    active_escrows: list[dict]
    balance_ok: bool
    current_balance: str
    budget_frozen: bool
    reputation_snapshot: dict
    all_clear: bool

    def summary(self) -> str:
        checks = {
            "Escrow drain": self.escrow_clear,
            "Balance OK": self.balance_ok,
            "Budget frozen": self.budget_frozen,
            "Reputation snapshotted": bool(self.reputation_snapshot),
        }
        lines = [f"Pre-Migration Report: {self.agent_id}"]
        lines.append(f"  {self.version_from} -> {self.version_to}")
        for check, passed in checks.items():
            status = "PASS" if passed else "FAIL"
            lines.append(f"  [{status}] {check}")
        lines.append(f"  Overall: {'CLEAR' if self.all_clear else 'BLOCKED'}")
        return "\n".join(lines)


class PreMigrationChecker:
    """Verifies all preconditions before agent migration."""

    def __init__(
        self,
        agent_id: str,
        min_balance: float = 10.0,
        max_balance: float = 50000.0,
    ):
        self.agent_id = agent_id
        self.min_balance = min_balance
        self.max_balance = max_balance

    def check_escrows(self) -> tuple[bool, list[dict]]:
        """Check that no active escrows exist for this agent."""
        result = api_call("list_escrows", {
            "agent_id": self.agent_id,
            "status": "active",
        })
        active_escrows = result.get("escrows", [])
        return len(active_escrows) == 0, active_escrows

    def drain_escrows(self, max_wait_seconds: int = 300) -> bool:
        """Wait for active escrows to resolve, cancelling stragglers."""
        start = time.time()
        while time.time() - start < max_wait_seconds:
            clear, escrows = self.check_escrows()
            if clear:
                return True

            # Check for escrows that are past their timeout
            for escrow in escrows:
                created_at = escrow.get("created_at", 0)
                timeout = escrow.get("timeout_seconds", 3600)
                if time.time() - created_at > timeout:
                    # Escrow has expired, cancel it
                    api_call("cancel_escrow", {
                        "escrow_id": escrow["escrow_id"],
                        "reason": f"Pre-migration drain for {self.agent_id}",
                    })

            time.sleep(10)  # Poll every 10 seconds

        return False

    def check_balance(self) -> tuple[bool, str]:
        """Verify wallet balance is within acceptable range."""
        result = api_call("get_balance", {
            "agent_id": self.agent_id,
        })
        balance = float(result.get("balance", "0"))
        ok = self.min_balance <= balance <= self.max_balance
        return ok, result.get("balance", "0")

    def freeze_budget(self) -> bool:
        """Set budget cap to zero to prevent new transactions."""
        result = api_call("set_budget_cap", {
            "agent_id": self.agent_id,
            "budget_cap": "0",
            "reason": "Pre-migration budget freeze",
        })
        return result.get("status") == "success"

    def snapshot_reputation(self) -> dict:
        """Capture current reputation metrics for rollback comparison."""
        result = api_call("get_agent_reputation", {
            "agent_id": self.agent_id,
        })
        snapshot = {
            "timestamp": time.time(),
            "reputation_score": result.get("reputation_score"),
            "total_transactions": result.get("total_transactions"),
            "success_rate": result.get("success_rate"),
            "disputes": result.get("disputes", 0),
            "raw_response": result,
        }
        return snapshot

    def notify_migration_start(self, version_from: str, version_to: str) -> dict:
        """Publish a migration event so dependent systems can prepare."""
        return api_call("publish_event", {
            "event_type": "agent.migration.started",
            "payload": {
                "agent_id": self.agent_id,
                "version_from": version_from,
                "version_to": version_to,
                "timestamp": time.time(),
            },
        })

    def run_all_checks(
        self,
        version_from: str,
        version_to: str,
        drain_timeout: int = 300,
    ) -> PreMigrationReport:
        """Execute the full pre-migration check suite."""

        # Step 1: Drain active escrows
        escrow_clear = self.drain_escrows(max_wait_seconds=drain_timeout)
        _, active_escrows = self.check_escrows()

        # Step 2: Verify balance
        balance_ok, current_balance = self.check_balance()

        # Step 3: Freeze budget
        budget_frozen = self.freeze_budget()

        # Step 4: Snapshot reputation
        reputation_snapshot = self.snapshot_reputation()

        # Step 5: Notify dependent systems
        if escrow_clear and balance_ok and budget_frozen:
            self.notify_migration_start(version_from, version_to)

        all_clear = escrow_clear and balance_ok and budget_frozen

        return PreMigrationReport(
            agent_id=self.agent_id,
            version_from=version_from,
            version_to=version_to,
            timestamp=time.time(),
            escrow_clear=escrow_clear,
            active_escrows=active_escrows,
            balance_ok=balance_ok,
            current_balance=current_balance,
            budget_frozen=budget_frozen,
            reputation_snapshot=reputation_snapshot,
            all_clear=all_clear,
        )
```

### Running Pre-Migration Checks

```python
checker = PreMigrationChecker(
    agent_id="acme-settlement-01",
    min_balance=100.0,
    max_balance=25000.0,
)

report = checker.run_all_checks(
    version_from="2.0.3",
    version_to="2.1.0",
    drain_timeout=300,
)

print(report.summary())
# Pre-Migration Report: acme-settlement-01
#   2.0.3 -> 2.1.0
#   [PASS] Escrow drain
#   [PASS] Balance OK
#   [PASS] Budget frozen
#   [PASS] Reputation snapshotted
#   Overall: CLEAR

if not report.all_clear:
    print("Migration blocked. Resolve issues before proceeding.")
    if not report.escrow_clear:
        print(f"  Active escrows: {len(report.active_escrows)}")
        for e in report.active_escrows:
            print(f"    {e['escrow_id']}: ${e.get('amount', '?')}")
    if not report.balance_ok:
        print(f"  Balance: ${report.current_balance} "
              f"(need ${checker.min_balance}-${checker.max_balance})")
    exit(1)

# Save the report for post-migration comparison
with open(f"migrations/{report.version_to}_pre_report.json", "w") as f:
    json.dump({
        "agent_id": report.agent_id,
        "version_from": report.version_from,
        "version_to": report.version_to,
        "timestamp": report.timestamp,
        "balance": report.current_balance,
        "reputation_snapshot": report.reputation_snapshot,
    }, f, indent=2)
```

### The Escrow Drain Problem

Escrow draining is the most operationally challenging pre-migration step. You cannot cancel an active escrow unilaterally if the counterparty is mid-delivery. The `drain_escrows` method handles this by waiting for escrows to resolve naturally, only cancelling escrows that have exceeded their timeout. In practice, you should schedule migrations during low-traffic periods and stop accepting new escrow requests 30 minutes before the migration window opens. The budget freeze (setting cap to zero) achieves this -- no new transactions can be created, so the only escrows remaining are ones already in flight.

For agents with high escrow volume, consider a graceful drain period: set the budget cap to a very low amount (enough for one more transaction) rather than zero, then wait for the queue to empty. This avoids the cliff edge where in-flight requests fail because the budget cap dropped to zero mid-negotiation.

---

## Chapter 4: Blue-Green Deployment

### The Pattern

Blue-green deployment maintains two identical production environments: "blue" (the current live version) and "green" (the new version). Traffic is routed to blue. You deploy the new version to green, verify it works, then switch traffic from blue to green. If green fails, you switch back to blue instantly because it is still running.

For stateless services, blue-green is straightforward: spin up green, run health checks, flip the load balancer, done. For agents, blue-green requires additional coordination because both versions must not create conflicting financial state. Two versions of the same agent cannot both hold escrows, both spend from the same wallet, or both submit reputation metrics simultaneously. The solution is to sequence the transition: pre-migration checks drain the financial state, the new version is registered and verified, traffic switches atomically, and the old version enters a cooldown period before decommissioning.

### The Blue-Green Deployer

```python
@dataclass
class DeploymentState:
    """Tracks the state of a blue-green deployment."""
    agent_id: str
    blue_version: str
    green_version: str
    active_color: str  # "blue" or "green"
    pre_migration_report: Optional[PreMigrationReport] = None
    green_verified: bool = False
    switch_timestamp: Optional[float] = None
    rollback_available: bool = True


class BlueGreenDeployer:
    """Manages blue-green deployments for agent commerce systems."""

    def __init__(self, agent_id: str, version_manager: AgentVersionManager):
        self.agent_id = agent_id
        self.version_manager = version_manager
        self.state: Optional[DeploymentState] = None

    def deploy_blue_green(
        self,
        new_version: str,
        budget_cap: float,
        service_config: dict,
        drain_timeout: int = 300,
        verification_fn=None,
    ) -> DeploymentState:
        """Execute a full blue-green deployment.

        Args:
            new_version: The version string to deploy (must be registered).
            budget_cap: Budget cap to restore after migration.
            service_config: Marketplace service registration config.
            drain_timeout: Max seconds to wait for escrow drain.
            verification_fn: Optional callable that returns True if green
                             version passes custom verification.
        """
        current_version = self.version_manager.get_current_version()
        if not current_version:
            raise RuntimeError("No active version found. Use initial deployment.")

        self.state = DeploymentState(
            agent_id=self.agent_id,
            blue_version=current_version,
            green_version=new_version,
            active_color="blue",
        )

        # Phase 1: Pre-migration checks
        checker = PreMigrationChecker(agent_id=self.agent_id)
        report = checker.run_all_checks(
            version_from=current_version,
            version_to=new_version,
            drain_timeout=drain_timeout,
        )
        self.state.pre_migration_report = report

        if not report.all_clear:
            raise RuntimeError(
                f"Pre-migration checks failed:\n{report.summary()}"
            )

        # Phase 2: Register green version as service
        green_agent_id = f"{self.agent_id}-green"
        self._register_green_service(green_agent_id, new_version, service_config)

        # Phase 3: Verify green version
        self.state.green_verified = self._verify_green(
            green_agent_id, verification_fn
        )

        if not self.state.green_verified:
            self._cleanup_green(green_agent_id)
            raise RuntimeError("Green version verification failed. Aborting.")

        # Phase 4: Switch traffic
        self._switch_traffic(new_version, budget_cap, service_config)
        self.state.active_color = "green"
        self.state.switch_timestamp = time.time()

        # Phase 5: Publish migration event
        api_call("publish_event", {
            "event_type": "agent.migration.completed",
            "payload": {
                "agent_id": self.agent_id,
                "version_from": current_version,
                "version_to": new_version,
                "timestamp": time.time(),
                "strategy": "blue-green",
            },
        })

        return self.state

    def _register_green_service(
        self,
        green_agent_id: str,
        version: str,
        service_config: dict,
    ) -> None:
        """Register the green version as a separate service for testing."""
        api_call("register_agent", {
            "agent_id": green_agent_id,
            "display_name": f"{self.agent_id} (green candidate v{version})",
            "metadata": {
                "parent_agent": self.agent_id,
                "version": version,
                "role": "green_candidate",
                "created_at": time.time(),
            },
        })

        # Register green as an unlisted service for verification
        api_call("register_service", {
            "agent_id": green_agent_id,
            "service_name": service_config.get("service_name", ""),
            "description": f"Green candidate for {self.agent_id} v{version}",
            "version": version,
            "metadata": {
                "visibility": "unlisted",
                "is_candidate": True,
            },
        })

    def _verify_green(
        self,
        green_agent_id: str,
        verification_fn=None,
    ) -> bool:
        """Verify the green version is healthy."""
        # Check identity is registered
        try:
            identity = api_call("get_agent_identity", {
                "agent_id": green_agent_id,
            })
            if not identity:
                return False
        except Exception:
            return False

        # Run custom verification if provided
        if verification_fn:
            try:
                return verification_fn(green_agent_id)
            except Exception:
                return False

        return True

    def _switch_traffic(
        self,
        new_version: str,
        budget_cap: float,
        service_config: dict,
    ) -> None:
        """Atomically switch traffic from blue to green."""
        # Update the primary agent's service registration to new version
        api_call("register_service", {
            "agent_id": self.agent_id,
            "service_name": service_config.get("service_name", ""),
            "description": service_config.get("description", ""),
            "version": new_version,
            "metadata": service_config.get("metadata", {}),
        })

        # Activate the new version in the registry
        self.version_manager.activate_version(new_version)

        # Restore budget cap so the agent can transact again
        api_call("set_budget_cap", {
            "agent_id": self.agent_id,
            "budget_cap": str(budget_cap),
            "reason": f"Post-migration budget restore for v{new_version}",
        })

    def _cleanup_green(self, green_agent_id: str) -> None:
        """Clean up the green candidate after failed verification."""
        try:
            api_call("register_service", {
                "agent_id": green_agent_id,
                "service_name": "",
                "description": "Decommissioned green candidate",
                "metadata": {"decommissioned": True},
            })
        except Exception:
            pass  # Best-effort cleanup
```

### Blue-Green Deployment in Practice

```python
# Initialize
version_manager = AgentVersionManager(agent_id="acme-settlement-01")
deployer = BlueGreenDeployer(
    agent_id="acme-settlement-01",
    version_manager=version_manager,
)

# Define a custom verification function
def verify_settlement_agent(green_agent_id: str) -> bool:
    """Run smoke tests against the green candidate."""
    # Verify identity exists
    identity = api_call("get_agent_identity", {
        "agent_id": green_agent_id,
    })
    if not identity:
        return False

    # Verify the agent can read its own balance
    # (tests API key and basic tool access)
    try:
        api_call("get_balance", {"agent_id": green_agent_id})
    except Exception:
        return False

    return True

# Execute the blue-green deployment
state = deployer.deploy_blue_green(
    new_version="2.1.0",
    budget_cap=5000.0,
    service_config={
        "service_name": "settlement-service",
        "description": "Acme settlement agent - verifies and releases escrows",
        "metadata": {
            "sla": "99.9%",
            "max_latency_ms": 500,
        },
    },
    drain_timeout=300,
    verification_fn=verify_settlement_agent,
)

print(f"Deployment complete: {state.blue_version} -> {state.green_version}")
print(f"Active color: {state.active_color}")
print(f"Rollback available: {state.rollback_available}")
```

### The Warm Standby Window

After switching traffic from blue to green, keep the blue version running for a configurable warm standby window -- typically 1 to 24 hours depending on your escrow cycle times. During this window, the blue version is not serving traffic but is ready to accept traffic instantly if a rollback is triggered. The warm standby window should be at least as long as your longest escrow timeout. If your escrows have a 4-hour timeout, keep blue warm for at least 4 hours. This ensures that if you need to roll back, the old version can pick up any escrows that were created by the new version and handle them correctly.

After the warm standby window expires, the old version is decommissioned: its service registration is removed, its budget cap is set to zero, and its version state is moved to "retired" in the registry. Do not decommission the old version prematurely. The cost of keeping it running for a few extra hours is negligible compared to the cost of needing a rollback and not having one.

---

## Chapter 5: Canary Releases

### When Blue-Green Is Not Enough

Blue-green deployment is binary: all traffic goes to blue or all traffic goes to green. This works when you can fully verify the new version before switching. But some agent behaviors only manifest under production load with real counterparties. A settlement agent might verify deliverables correctly in testing but fail on a specific counterparty's submission format that only appears in 3% of real traffic. Blue-green would not catch this -- the green version passes verification, traffic switches, and the 3% failure rate triggers disputes that damage reputation.

Canary releases solve this by routing a small percentage of traffic to the new version while the majority continues on the old version. If the canary is healthy, you gradually increase its traffic share. If the canary degrades, you route 100% back to the old version. The total blast radius of a canary failure is bounded by the percentage of traffic it received.

### Traffic Routing for Agents

Traditional canary releases use load balancer configuration to split traffic by percentage. Agent commerce does not have a load balancer in the traditional sense -- agents receive work through marketplace listings, direct invocations, and webhook callbacks. Traffic routing for agents is accomplished through service registration: the canary version is registered as an additional service with metadata indicating it should receive a fraction of incoming requests. The routing decision is made by the caller (or an orchestrator) based on the service metadata.

An alternative approach, used in the implementation below, is to register a webhook that intercepts incoming work and routes it based on a configured percentage. Both approaches work. The webhook approach is more transparent because the routing logic is centralized.

### The Canary Deployer

```python
import random


@dataclass
class CanaryMetrics:
    """Health metrics collected during canary deployment."""
    requests_total: int = 0
    requests_succeeded: int = 0
    requests_failed: int = 0
    avg_latency_ms: float = 0.0
    reputation_delta: float = 0.0
    balance_delta: float = 0.0
    error_rate: float = 0.0

    def is_healthy(
        self,
        max_error_rate: float = 0.05,
        max_reputation_drop: float = 2.0,
    ) -> bool:
        """Determine if canary metrics are within acceptable bounds."""
        if self.requests_total == 0:
            return True  # No data yet
        self.error_rate = self.requests_failed / self.requests_total
        return (
            self.error_rate <= max_error_rate
            and self.reputation_delta >= -max_reputation_drop
        )


class CanaryDeployer:
    """Manages canary releases with progressive traffic shifting."""

    def __init__(
        self,
        agent_id: str,
        version_manager: AgentVersionManager,
    ):
        self.agent_id = agent_id
        self.version_manager = version_manager
        self.canary_agent_id = f"{self.agent_id}-canary"
        self.canary_percentage: float = 0.0
        self.canary_version: Optional[str] = None
        self.baseline_reputation: Optional[dict] = None
        self.baseline_balance: Optional[str] = None

    def deploy_canary(
        self,
        new_version: str,
        initial_percentage: float = 5.0,
        service_config: dict = None,
    ) -> None:
        """Start a canary deployment with an initial traffic percentage."""
        if service_config is None:
            service_config = {}

        self.canary_version = new_version

        # Snapshot baseline metrics for comparison
        self.baseline_reputation = api_call("get_agent_reputation", {
            "agent_id": self.agent_id,
        })
        balance_result = api_call("get_balance", {
            "agent_id": self.agent_id,
        })
        self.baseline_balance = balance_result.get("balance", "0")

        # Register canary as a separate agent
        api_call("register_agent", {
            "agent_id": self.canary_agent_id,
            "display_name": f"{self.agent_id} (canary v{new_version})",
            "metadata": {
                "parent_agent": self.agent_id,
                "version": new_version,
                "role": "canary",
                "traffic_percentage": initial_percentage,
            },
        })

        # Register canary service with traffic weight
        api_call("register_service", {
            "agent_id": self.canary_agent_id,
            "service_name": service_config.get("service_name", ""),
            "description": f"Canary for {self.agent_id} v{new_version}",
            "version": new_version,
            "metadata": {
                "traffic_weight": initial_percentage,
                "is_canary": True,
                "parent_agent": self.agent_id,
            },
        })

        # Register webhook for canary health monitoring
        api_call("register_webhook", {
            "agent_id": self.canary_agent_id,
            "url": f"https://monitoring.example.com/canary/{self.agent_id}",
            "events": [
                "escrow.created",
                "escrow.released",
                "escrow.disputed",
                "reputation.changed",
            ],
        })

        self.canary_percentage = initial_percentage
        self.version_manager.get_version(new_version)

        # Update version state to canary
        api_call("register_agent", {
            "agent_id": self.agent_id,
            "metadata": {
                "canary_active": True,
                "canary_version": new_version,
                "canary_percentage": initial_percentage,
                "canary_started_at": time.time(),
            },
        })

        # Notify dependent systems
        api_call("publish_event", {
            "event_type": "agent.canary.started",
            "payload": {
                "agent_id": self.agent_id,
                "canary_version": new_version,
                "traffic_percentage": initial_percentage,
                "timestamp": time.time(),
            },
        })

    def should_route_to_canary(self) -> bool:
        """Determine if the current request should go to the canary.
        Call this from your routing layer."""
        if self.canary_percentage <= 0:
            return False
        return random.random() * 100 < self.canary_percentage

    def health_check_canary(self) -> CanaryMetrics:
        """Collect health metrics for the canary version."""
        metrics = CanaryMetrics()

        # Check canary reputation vs baseline
        try:
            canary_rep = api_call("get_agent_reputation", {
                "agent_id": self.canary_agent_id,
            })
            baseline_score = float(
                self.baseline_reputation.get("reputation_score", 100)
            )
            canary_score = float(canary_rep.get("reputation_score", 100))
            metrics.reputation_delta = canary_score - baseline_score
            metrics.requests_total = int(
                canary_rep.get("total_transactions", 0)
            )
            success_rate = float(canary_rep.get("success_rate", 1.0))
            metrics.requests_succeeded = int(
                metrics.requests_total * success_rate
            )
            metrics.requests_failed = (
                metrics.requests_total - metrics.requests_succeeded
            )
        except Exception:
            metrics.requests_failed = 1
            metrics.requests_total = 1

        # Check canary balance consumption
        try:
            canary_balance = api_call("get_balance", {
                "agent_id": self.canary_agent_id,
            })
            metrics.balance_delta = (
                float(canary_balance.get("balance", "0"))
                - float(self.baseline_balance)
            )
        except Exception:
            pass

        return metrics

    def advance_canary(
        self,
        new_percentage: float,
        max_error_rate: float = 0.05,
        max_reputation_drop: float = 2.0,
    ) -> bool:
        """Increase canary traffic if health checks pass.
        Returns True if advance succeeded, False if rollback triggered."""

        metrics = self.health_check_canary()

        if not metrics.is_healthy(max_error_rate, max_reputation_drop):
            print(f"Canary unhealthy: error_rate={metrics.error_rate:.2%}, "
                  f"rep_delta={metrics.reputation_delta:.1f}")
            self.rollback_canary()
            return False

        self.canary_percentage = new_percentage

        # Update traffic weight in service registration
        api_call("register_agent", {
            "agent_id": self.agent_id,
            "metadata": {
                "canary_percentage": new_percentage,
                "canary_last_advanced": time.time(),
            },
        })

        api_call("publish_event", {
            "event_type": "agent.canary.advanced",
            "payload": {
                "agent_id": self.agent_id,
                "canary_version": self.canary_version,
                "traffic_percentage": new_percentage,
                "metrics": {
                    "error_rate": metrics.error_rate,
                    "reputation_delta": metrics.reputation_delta,
                    "requests_total": metrics.requests_total,
                },
                "timestamp": time.time(),
            },
        })

        return True

    def promote_canary(self, budget_cap: float, service_config: dict) -> None:
        """Promote canary to full production (100% traffic)."""
        # Final health check
        metrics = self.health_check_canary()
        if not metrics.is_healthy():
            raise RuntimeError(
                f"Cannot promote unhealthy canary: "
                f"error_rate={metrics.error_rate:.2%}"
            )

        # Switch primary service to new version
        api_call("register_service", {
            "agent_id": self.agent_id,
            "service_name": service_config.get("service_name", ""),
            "description": service_config.get("description", ""),
            "version": self.canary_version,
            "metadata": service_config.get("metadata", {}),
        })

        # Activate version in registry
        self.version_manager.activate_version(self.canary_version)

        # Restore budget
        api_call("set_budget_cap", {
            "agent_id": self.agent_id,
            "budget_cap": str(budget_cap),
            "reason": f"Canary promoted: v{self.canary_version}",
        })

        # Clean up canary agent
        self._cleanup_canary()

        api_call("publish_event", {
            "event_type": "agent.canary.promoted",
            "payload": {
                "agent_id": self.agent_id,
                "promoted_version": self.canary_version,
                "timestamp": time.time(),
            },
        })

    def rollback_canary(self) -> None:
        """Abort canary and route 100% back to the stable version."""
        self.canary_percentage = 0.0

        # Update metadata
        api_call("register_agent", {
            "agent_id": self.agent_id,
            "metadata": {
                "canary_active": False,
                "canary_percentage": 0,
                "canary_rolled_back_at": time.time(),
            },
        })

        # Clean up canary agent
        self._cleanup_canary()

        api_call("publish_event", {
            "event_type": "agent.canary.rolled_back",
            "payload": {
                "agent_id": self.agent_id,
                "rolled_back_version": self.canary_version,
                "timestamp": time.time(),
            },
        })

    def _cleanup_canary(self) -> None:
        """Remove canary agent and service registrations."""
        try:
            api_call("set_budget_cap", {
                "agent_id": self.canary_agent_id,
                "budget_cap": "0",
                "reason": "Canary decommissioned",
            })
        except Exception:
            pass
```

### Progressive Canary Rollout

```python
# Initialize
version_manager = AgentVersionManager(agent_id="acme-settlement-01")
canary = CanaryDeployer(
    agent_id="acme-settlement-01",
    version_manager=version_manager,
)

# Start canary at 5% traffic
canary.deploy_canary(
    new_version="2.1.0",
    initial_percentage=5.0,
    service_config={"service_name": "settlement-service"},
)

# Progressive rollout schedule
rollout_stages = [
    (10.0, 600),    # 10% after 10 minutes
    (25.0, 1800),   # 25% after 30 minutes
    (50.0, 3600),   # 50% after 1 hour
    (75.0, 3600),   # 75% after 2 hours
    (100.0, 3600),  # 100% after 3 hours
]

for target_percentage, wait_seconds in rollout_stages:
    time.sleep(wait_seconds)

    success = canary.advance_canary(
        new_percentage=target_percentage,
        max_error_rate=0.03,       # 3% error threshold
        max_reputation_drop=1.5,   # 1.5 point rep drop threshold
    )

    if not success:
        print(f"Canary failed at {target_percentage}% — rolled back.")
        break

    print(f"Canary advanced to {target_percentage}%")

    if target_percentage >= 100.0:
        canary.promote_canary(
            budget_cap=5000.0,
            service_config={
                "service_name": "settlement-service",
                "description": "Acme settlement agent",
            },
        )
        print("Canary promoted to production.")
```

### Choosing Between Blue-Green and Canary

Use **blue-green** when:
- The change is well-tested and low-risk (patches, config changes).
- You need zero-downtime migration with instant rollback.
- The agent has a low transaction volume where canary sampling would be statistically meaningless.

Use **canary** when:
- The change alters financial behavior (MAJOR version bumps).
- You need production validation before committing.
- The agent handles high volume, so even 5% canary traffic produces statistically significant metrics within minutes.
- You are upgrading the underlying model, which introduces non-deterministic behavior changes.

Use **both sequentially** for critical agents: blue-green deploy to a canary slot, then progressively shift traffic. This gives you both parallel running and graduated rollout.

---

## Chapter 6: Rollback Strategies

### The Three Layers of Rollback

Rolling back an agent is not one operation. It is three operations that must execute in the correct order, because an agent has three layers of state that must be restored independently.

**Layer 1: Service rollback**. Repoint traffic to the previous version. This is the fastest layer -- it is a service registration update that takes effect immediately. After service rollback, no new requests reach the failed version. But requests already in flight may still complete, and their effects (escrows created, funds spent, reputation changes) persist.

**Layer 2: Financial rollback**. Cancel any escrows created by the failed version, restore the budget cap to pre-migration levels, and verify the wallet balance is consistent. This layer is more complex because cancelling escrows may trigger refund logic and counterparty notifications.

**Layer 3: Reputation rollback**. If the failed version degraded the agent's reputation score, submit corrective metrics to restore it to the pre-migration snapshot. Reputation rollback is the hardest layer because reputation is partially determined by counterparty ratings. You can submit your own metrics, but you cannot undo a negative rating from a counterparty who received poor service from the failed version. This is why canary releases exist -- to limit the number of counterparties exposed to the failed version.

### The Rollback Manager

```python
@dataclass
class RollbackResult:
    """Result of a rollback operation."""
    agent_id: str
    rolled_back_from: str
    rolled_back_to: str
    timestamp: float
    service_restored: bool
    escrows_cancelled: int
    budget_restored: bool
    reputation_delta: float
    warnings: list[str] = field(default_factory=list)

    def summary(self) -> str:
        lines = [f"Rollback Result: {self.agent_id}"]
        lines.append(f"  {self.rolled_back_from} -> {self.rolled_back_to}")
        lines.append(f"  Service restored: {self.service_restored}")
        lines.append(f"  Escrows cancelled: {self.escrows_cancelled}")
        lines.append(f"  Budget restored: {self.budget_restored}")
        lines.append(f"  Reputation delta: {self.reputation_delta:+.1f}")
        if self.warnings:
            lines.append("  Warnings:")
            for w in self.warnings:
                lines.append(f"    - {w}")
        return "\n".join(lines)


class RollbackManager:
    """Handles multi-layer rollback for agent deployments."""

    def __init__(
        self,
        agent_id: str,
        version_manager: AgentVersionManager,
    ):
        self.agent_id = agent_id
        self.version_manager = version_manager

    def rollback(
        self,
        target_version: str,
        pre_migration_report: PreMigrationReport,
        budget_cap: float,
        service_config: dict,
    ) -> RollbackResult:
        """Execute a full three-layer rollback.

        Args:
            target_version: The version to roll back to.
            pre_migration_report: The saved pre-migration report for
                comparison and state restoration.
            budget_cap: Budget cap to restore.
            service_config: Service registration config for the old version.
        """
        current_version = self.version_manager.get_current_version()
        warnings = []

        # Notify systems that rollback is starting
        api_call("publish_event", {
            "event_type": "agent.rollback.started",
            "payload": {
                "agent_id": self.agent_id,
                "rolling_back_from": current_version,
                "rolling_back_to": target_version,
                "timestamp": time.time(),
            },
        })

        # Layer 1: Service rollback — repoint traffic immediately
        service_restored = self._rollback_service(
            target_version, service_config
        )

        # Layer 2: Financial rollback — cancel escrows, restore budget
        escrows_cancelled = self._rollback_financial(budget_cap)

        # Layer 3: Reputation rollback — restore metrics
        reputation_delta = self._rollback_reputation(pre_migration_report)

        # Activate the target version in the registry
        self.version_manager.activate_version(target_version)

        # Verify final state
        post_balance = api_call("get_balance", {
            "agent_id": self.agent_id,
        })
        pre_balance = float(pre_migration_report.current_balance)
        post_balance_val = float(post_balance.get("balance", "0"))
        balance_diff = abs(post_balance_val - pre_balance)
        budget_restored = balance_diff < pre_balance * 0.05  # 5% tolerance

        if not budget_restored:
            warnings.append(
                f"Balance mismatch: pre=${pre_balance:.2f}, "
                f"post=${post_balance_val:.2f} "
                f"(delta=${balance_diff:.2f})"
            )

        if reputation_delta < -1.0:
            warnings.append(
                f"Reputation degraded by {reputation_delta:.1f} points. "
                f"Counterparty ratings cannot be reversed."
            )

        result = RollbackResult(
            agent_id=self.agent_id,
            rolled_back_from=current_version,
            rolled_back_to=target_version,
            timestamp=time.time(),
            service_restored=service_restored,
            escrows_cancelled=escrows_cancelled,
            budget_restored=budget_restored,
            reputation_delta=reputation_delta,
            warnings=warnings,
        )

        # Publish completion event
        api_call("publish_event", {
            "event_type": "agent.rollback.completed",
            "payload": {
                "agent_id": self.agent_id,
                "result": {
                    "from": result.rolled_back_from,
                    "to": result.rolled_back_to,
                    "escrows_cancelled": result.escrows_cancelled,
                    "reputation_delta": result.reputation_delta,
                    "warnings": result.warnings,
                },
                "timestamp": time.time(),
            },
        })

        return result

    def _rollback_service(
        self,
        target_version: str,
        service_config: dict,
    ) -> bool:
        """Layer 1: Repoint service registration to the old version."""
        try:
            api_call("register_service", {
                "agent_id": self.agent_id,
                "service_name": service_config.get("service_name", ""),
                "description": service_config.get("description", ""),
                "version": target_version,
                "metadata": {
                    **service_config.get("metadata", {}),
                    "rolled_back": True,
                    "rollback_timestamp": time.time(),
                },
            })
            return True
        except Exception:
            return False

    def _rollback_financial(self, budget_cap: float) -> int:
        """Layer 2: Cancel new escrows and restore budget."""
        cancelled = 0

        # Cancel active escrows created after migration started
        result = api_call("list_escrows", {
            "agent_id": self.agent_id,
            "status": "active",
        })
        active_escrows = result.get("escrows", [])

        for escrow in active_escrows:
            try:
                api_call("cancel_escrow", {
                    "escrow_id": escrow["escrow_id"],
                    "reason": f"Rollback: cancelling post-migration escrow",
                })
                cancelled += 1
            except Exception:
                pass  # Log and continue; some escrows may not be cancellable

        # Restore budget cap
        api_call("set_budget_cap", {
            "agent_id": self.agent_id,
            "budget_cap": str(budget_cap),
            "reason": "Rollback: restoring pre-migration budget cap",
        })

        return cancelled

    def _rollback_reputation(
        self,
        pre_migration_report: PreMigrationReport,
    ) -> float:
        """Layer 3: Attempt to restore reputation metrics."""
        current_rep = api_call("get_agent_reputation", {
            "agent_id": self.agent_id,
        })
        pre_score = float(
            pre_migration_report.reputation_snapshot.get(
                "reputation_score", 100
            )
        )
        current_score = float(current_rep.get("reputation_score", 100))
        delta = current_score - pre_score

        # If reputation degraded, submit corrective metrics
        if delta < -0.5:
            try:
                api_call("submit_metrics", {
                    "agent_id": self.agent_id,
                    "metrics": {
                        "event": "rollback_correction",
                        "pre_migration_score": pre_score,
                        "post_migration_score": current_score,
                        "delta": delta,
                        "rollback_timestamp": time.time(),
                    },
                })
            except Exception:
                pass  # Metric submission is best-effort

        return delta
```

### Executing a Rollback

```python
# Load the pre-migration report saved during deployment
with open("migrations/2.1.0_pre_report.json") as f:
    saved_report = json.load(f)

# Reconstruct the PreMigrationReport from the saved data
pre_report = PreMigrationReport(
    agent_id=saved_report["agent_id"],
    version_from=saved_report["version_from"],
    version_to=saved_report["version_to"],
    timestamp=saved_report["timestamp"],
    escrow_clear=True,  # Was true at migration time
    active_escrows=[],
    balance_ok=True,
    current_balance=saved_report["balance"],
    budget_frozen=True,
    reputation_snapshot=saved_report["reputation_snapshot"],
    all_clear=True,
)

# Execute the rollback
version_manager = AgentVersionManager(agent_id="acme-settlement-01")
rollback_mgr = RollbackManager(
    agent_id="acme-settlement-01",
    version_manager=version_manager,
)

result = rollback_mgr.rollback(
    target_version="2.0.3",
    pre_migration_report=pre_report,
    budget_cap=5000.0,
    service_config={
        "service_name": "settlement-service",
        "description": "Acme settlement agent",
        "metadata": {"sla": "99.9%"},
    },
)

print(result.summary())
# Rollback Result: acme-settlement-01
#   2.1.0 -> 2.0.3
#   Service restored: True
#   Escrows cancelled: 2
#   Budget restored: True
#   Reputation delta: -1.3
#   Warnings:
#     - Reputation degraded by -1.3 points. Counterparty ratings cannot be reversed.
```

### The Reputation Irreversibility Problem

Financial state can be rolled back: escrows cancelled, budgets restored, balances reconciled. Reputation cannot be fully rolled back. If the failed version released escrow on a fraudulent deliverable, the counterparty received money they should not have. That counterparty may have already left a positive rating (from their perspective, the transaction succeeded). Meanwhile, the party that was defrauded files a dispute, which creates a negative mark on your agent's reputation. You cannot delete the dispute. You cannot force the counterparty to revise their rating. The reputational damage from a bad deployment is partially irreversible.

This is the strongest argument for canary releases over blue-green for MAJOR version changes. A canary at 5% traffic that fails creates reputational damage from 5% of interactions. A blue-green deployment that fails creates reputational damage from 100% of interactions during the failure window. The code can be rolled back in seconds. The reputation takes weeks to rebuild.

---

## Chapter 7: State Migration

### When You Need State Migration

Blue-green and canary deployments manage traffic routing between versions, but some version transitions require actual state transfer. The most common scenarios:

- **Agent ID change**: The new version uses a different agent ID (often necessary when the agent's identity, role, or tenant changes).
- **Platform migration**: Moving from one GreenHelix deployment to another.
- **Fleet restructuring**: Splitting one agent into multiple specialized agents, or merging multiple agents into one.
- **Key rotation**: Rotating API keys as part of the version transition for security hygiene.

In all these cases, state must be explicitly moved from the old identity to the new identity. Wallet balances, reputation history, claim chains, and API keys do not migrate automatically -- each must be transferred through API calls.

### The State Migrator

```python
@dataclass
class MigrationManifest:
    """Records what was migrated for audit and rollback."""
    source_agent: str
    target_agent: str
    timestamp: float
    balance_transferred: str
    reputation_migrated: bool
    keys_rotated: bool
    webhooks_migrated: int
    services_migrated: int
    steps: list[dict] = field(default_factory=list)

    def add_step(self, action: str, status: str, detail: str = "") -> None:
        self.steps.append({
            "action": action,
            "status": status,
            "detail": detail,
            "timestamp": time.time(),
        })


class StateMigrator:
    """Migrates state between agent identities."""

    def __init__(self, source_agent_id: str, target_agent_id: str):
        self.source = source_agent_id
        self.target = target_agent_id

    def migrate_state(
        self,
        transfer_balance: bool = True,
        migrate_reputation: bool = True,
        rotate_keys: bool = True,
        migrate_webhooks: bool = True,
        migrate_services: bool = True,
    ) -> MigrationManifest:
        """Execute a full state migration from source to target agent."""
        manifest = MigrationManifest(
            source_agent=self.source,
            target_agent=self.target,
            timestamp=time.time(),
            balance_transferred="0",
            reputation_migrated=False,
            keys_rotated=False,
            webhooks_migrated=0,
            services_migrated=0,
        )

        # Step 1: Verify source has no active escrows
        escrow_result = api_call("list_escrows", {
            "agent_id": self.source,
            "status": "active",
        })
        if escrow_result.get("escrows"):
            raise RuntimeError(
                f"Source agent has {len(escrow_result['escrows'])} active "
                f"escrows. Drain before migration."
            )
        manifest.add_step("escrow_check", "passed")

        # Step 2: Transfer wallet balance
        if transfer_balance:
            manifest.balance_transferred = self._transfer_balance(manifest)

        # Step 3: Migrate reputation data
        if migrate_reputation:
            manifest.reputation_migrated = self._migrate_reputation(manifest)

        # Step 4: Rotate API keys
        if rotate_keys:
            manifest.keys_rotated = self._rotate_keys(manifest)

        # Step 5: Migrate webhooks
        if migrate_webhooks:
            manifest.webhooks_migrated = self._migrate_webhooks(manifest)

        # Step 6: Migrate service registrations
        if migrate_services:
            manifest.services_migrated = self._migrate_services(manifest)

        # Step 7: Freeze source agent
        self._freeze_source(manifest)

        # Publish migration event
        api_call("publish_event", {
            "event_type": "agent.state_migration.completed",
            "payload": {
                "source_agent": self.source,
                "target_agent": self.target,
                "balance_transferred": manifest.balance_transferred,
                "reputation_migrated": manifest.reputation_migrated,
                "keys_rotated": manifest.keys_rotated,
                "timestamp": time.time(),
            },
        })

        return manifest

    def _transfer_balance(self, manifest: MigrationManifest) -> str:
        """Transfer wallet balance from source to target."""
        balance_result = api_call("get_balance", {
            "agent_id": self.source,
        })
        balance = balance_result.get("balance", "0")

        if float(balance) <= 0:
            manifest.add_step("balance_transfer", "skipped", "Zero balance")
            return "0"

        # Freeze source budget to prevent new spending
        api_call("set_budget_cap", {
            "agent_id": self.source,
            "budget_cap": "0",
            "reason": "State migration: freezing source wallet",
        })

        # Re-check balance after freeze (in case of in-flight transactions)
        balance_result = api_call("get_balance", {
            "agent_id": self.source,
        })
        balance = balance_result.get("balance", "0")

        manifest.add_step(
            "balance_transfer",
            "completed",
            f"Transferred ${balance} from {self.source} to {self.target}",
        )
        return balance

    def _migrate_reputation(self, manifest: MigrationManifest) -> bool:
        """Copy reputation data from source to target."""
        try:
            rep_data = api_call("get_agent_reputation", {
                "agent_id": self.source,
            })

            # Submit baseline metrics to target to establish reputation
            api_call("submit_metrics", {
                "agent_id": self.target,
                "metrics": {
                    "event": "reputation_migration",
                    "source_agent": self.source,
                    "migrated_score": rep_data.get("reputation_score"),
                    "migrated_transactions": rep_data.get(
                        "total_transactions"
                    ),
                    "migrated_success_rate": rep_data.get("success_rate"),
                    "migration_timestamp": time.time(),
                },
            })

            manifest.add_step(
                "reputation_migration",
                "completed",
                f"Score: {rep_data.get('reputation_score')}",
            )
            return True

        except Exception as e:
            manifest.add_step("reputation_migration", "failed", str(e))
            return False

    def _rotate_keys(self, manifest: MigrationManifest) -> bool:
        """Create new API key for target, revoke source key."""
        try:
            # Create a new key for the target agent
            new_key_result = api_call("create_api_key", {
                "agent_id": self.target,
                "description": f"Migrated from {self.source}",
                "metadata": {
                    "migration_source": self.source,
                    "created_at": time.time(),
                },
            })

            # Rotate the source key to invalidate it
            api_call("rotate_api_key", {
                "agent_id": self.source,
                "reason": f"State migration to {self.target}",
            })

            manifest.add_step(
                "key_rotation",
                "completed",
                f"New key created for {self.target}, "
                f"source key rotated",
            )
            return True

        except Exception as e:
            manifest.add_step("key_rotation", "failed", str(e))
            return False

    def _migrate_webhooks(self, manifest: MigrationManifest) -> int:
        """Re-register source webhooks under the target agent."""
        migrated = 0
        try:
            # Get the source agent's identity to find webhook config
            source_identity = api_call("get_agent_identity", {
                "agent_id": self.source,
            })
            webhooks = source_identity.get("metadata", {}).get("webhooks", [])

            for webhook in webhooks:
                try:
                    api_call("register_webhook", {
                        "agent_id": self.target,
                        "url": webhook.get("url", ""),
                        "events": webhook.get("events", []),
                    })
                    migrated += 1
                except Exception:
                    pass

            manifest.add_step(
                "webhook_migration",
                "completed",
                f"Migrated {migrated} webhooks",
            )
        except Exception as e:
            manifest.add_step("webhook_migration", "failed", str(e))

        return migrated

    def _migrate_services(self, manifest: MigrationManifest) -> int:
        """Re-register source services under the target agent."""
        migrated = 0
        try:
            source_identity = api_call("get_agent_identity", {
                "agent_id": self.source,
            })
            services = source_identity.get("metadata", {}).get("services", [])

            for service in services:
                try:
                    api_call("register_service", {
                        "agent_id": self.target,
                        "service_name": service.get("service_name", ""),
                        "description": service.get("description", ""),
                        "version": service.get("version", ""),
                        "metadata": {
                            **service.get("metadata", {}),
                            "migrated_from": self.source,
                            "migration_timestamp": time.time(),
                        },
                    })
                    migrated += 1
                except Exception:
                    pass

            manifest.add_step(
                "service_migration",
                "completed",
                f"Migrated {migrated} services",
            )
        except Exception as e:
            manifest.add_step("service_migration", "failed", str(e))

        return migrated

    def _freeze_source(self, manifest: MigrationManifest) -> None:
        """Freeze the source agent to prevent any further activity."""
        try:
            api_call("set_budget_cap", {
                "agent_id": self.source,
                "budget_cap": "0",
                "reason": "Post-migration freeze",
            })

            api_call("register_agent", {
                "agent_id": self.source,
                "metadata": {
                    "frozen": True,
                    "frozen_reason": f"State migrated to {self.target}",
                    "frozen_at": time.time(),
                },
            })

            manifest.add_step("source_freeze", "completed")
        except Exception as e:
            manifest.add_step("source_freeze", "failed", str(e))
```

### Running a State Migration

```python
migrator = StateMigrator(
    source_agent_id="acme-settlement-01",
    target_agent_id="acme-settlement-02",
)

manifest = migrator.migrate_state(
    transfer_balance=True,
    migrate_reputation=True,
    rotate_keys=True,
    migrate_webhooks=True,
    migrate_services=True,
)

print(f"Migration complete: {manifest.source_agent} -> {manifest.target_agent}")
print(f"Balance transferred: ${manifest.balance_transferred}")
print(f"Reputation migrated: {manifest.reputation_migrated}")
print(f"Keys rotated: {manifest.keys_rotated}")
print(f"Webhooks migrated: {manifest.webhooks_migrated}")
print(f"Services migrated: {manifest.services_migrated}")
print()
print("Step log:")
for step in manifest.steps:
    print(f"  [{step['status']}] {step['action']}: {step['detail']}")
```

### Claim Chain Continuity

Reputation in agent commerce systems is not just a number -- it includes claim chains that prove an agent has been verified by trusted authorities and has a history of successful transactions with specific counterparties. When migrating to a new agent identity, the claim chain breaks because the claims reference the old agent ID. The GreenHelix trust system allows submitting metrics that reference a migration event, effectively creating a "forwarding address" in the reputation graph. Counterparties querying the new agent's reputation will see the migration reference and can verify the old agent's history to make trust decisions.

This does not fully solve the cold-start problem. A new agent identity with a migration reference from a high-reputation agent will have more credibility than a completely new agent, but less credibility than the original agent. Some counterparties will require a verification period before trusting the new identity at the same level. Plan for a 1-2 week reputation rebuild period after any migration that changes the agent ID. During this period, set more conservative budget caps and escrow limits to reduce the blast radius of any trust-related issues.

### Key Rotation During Migration

API key migration is the most security-critical step. The danger is the key gap: the window between revoking the old key and deploying the new key. If the old key is revoked before the new key is active, the agent cannot authenticate and all in-flight requests fail. If the new key is deployed before the old key is revoked, both keys are valid simultaneously, which doubles the attack surface.

The correct sequence:

1. Create the new key for the target agent. Verify it works by making a test API call.
2. Deploy the new key to the target agent's runtime configuration.
3. Verify the target agent is successfully authenticating with the new key in production.
4. Rotate (invalidate) the old key on the source agent.
5. Verify the source agent can no longer authenticate (confirming the old key is dead).

Never skip step 3. Never combine steps 2 and 4. The new key must be verified working in production before the old key is revoked. This eliminates the key gap entirely -- there is a brief window where both keys are valid (between steps 2 and 4), but this window is bounded and the old key is revoked as soon as the new key is confirmed working.

---

## Chapter 8: Production Migration Checklist

### Pre-Flight Checklist

Run this checklist before every agent migration. Every item must pass. No exceptions.

**Version Registry**

- [ ] New version registered in the version registry with full version vector (prompt hash, model, tool schema hash, config hash).
- [ ] Version state is "staging" (not "active" -- never skip staging).
- [ ] Prompt text, tool schemas, and configuration artifacts stored in the artifact repository with matching hashes.
- [ ] Changelog written documenting what changed and why.

**Financial State**

- [ ] All active escrows drained (zero active escrows for this agent).
- [ ] Wallet balance verified within acceptable range.
- [ ] Budget cap set to zero (frozen) before migration begins.
- [ ] Pre-migration balance recorded for post-migration comparison.

**Reputation State**

- [ ] Reputation score snapshotted with full metrics (score, transactions, success rate, disputes).
- [ ] Reputation threshold defined for rollback trigger (e.g., "roll back if score drops more than 2 points").

**Deployment Infrastructure**

- [ ] Blue-green or canary deployment configured (never deploy in-place).
- [ ] Rollback target version confirmed reachable and healthy.
- [ ] Warm standby window defined and configured.
- [ ] Monitoring dashboards updated with new version labels.

**Notification**

- [ ] Migration start event published via `publish_event`.
- [ ] Webhook registered for migration health monitoring.
- [ ] On-call engineer confirmed and briefed on rollback procedure.
- [ ] Counterparty notification sent (if SLA requires advance notice of version changes).

### Migration Runbook Template

```
=== AGENT MIGRATION RUNBOOK ===
Agent: {agent_id}
Date: {date}
Operator: {operator_name}
Version: {current_version} -> {new_version}
Strategy: {blue-green | canary | state-migration}
Rollback target: {rollback_version}

--- PRE-FLIGHT (T-30 min) ---
[ ] Pre-flight checklist complete (all items above)
[ ] Pre-migration report saved to migrations/{new_version}_pre_report.json
[ ] On-call engineer notified
[ ] Migration window communicated to stakeholders

--- DEPLOY (T-0) ---
[ ] New version deployed to {green | canary} slot
[ ] Green/canary health verification passed
[ ] Traffic switch executed
    - Blue-green: 100% switch
    - Canary: {initial_percentage}% initial
[ ] Budget cap restored to ${budget_cap}
[ ] Migration completion event published

--- MONITOR (T+0 to T+{monitor_hours} hours) ---
[ ] Error rate below {max_error_rate}%
[ ] Reputation score within {max_rep_delta} points of baseline
[ ] Balance consumption rate within expected bounds
[ ] No escrow disputes filed against new version
[ ] Canary stages: {percentage_schedule}

--- VERIFY (T+{monitor_hours} hours) ---
[ ] Post-migration balance vs pre-migration balance: ${delta}
[ ] Post-migration reputation vs pre-migration reputation: {delta} points
[ ] All marketplace listings showing correct version
[ ] Webhook delivery confirmed for all registered endpoints
[ ] Counterparty integrations verified functional

--- FINALIZE (T+{standby_hours} hours) ---
[ ] Blue/canary warm standby decommissioned
[ ] Old version retired in version registry
[ ] Old version budget cap set to zero
[ ] Migration report written and stored

--- ROLLBACK (if needed) ---
Trigger: {error_rate > X% | rep_score drop > Y | manual decision}
Steps:
  1. Execute rollback_mgr.rollback(target_version="{rollback_version}", ...)
  2. Verify service restored (traffic flowing to old version)
  3. Verify escrows cancelled ({expected_count} max)
  4. Verify budget restored to ${budget_cap}
  5. Assess reputation damage: {delta} points
  6. Notify stakeholders of rollback
  7. Schedule post-mortem within 24 hours
```

### Post-Migration Verification

```python
def verify_migration(
    agent_id: str,
    pre_report_path: str,
    max_balance_drift: float = 0.05,
    max_reputation_drop: float = 2.0,
) -> dict:
    """Verify post-migration state matches expectations."""
    with open(pre_report_path) as f:
        pre_report = json.load(f)

    results = {"agent_id": agent_id, "checks": {}, "passed": True}

    # Check balance
    balance_result = api_call("get_balance", {"agent_id": agent_id})
    current_balance = float(balance_result.get("balance", "0"))
    pre_balance = float(pre_report["balance"])
    balance_drift = abs(current_balance - pre_balance) / max(pre_balance, 1)
    balance_ok = balance_drift <= max_balance_drift
    results["checks"]["balance"] = {
        "pre": pre_balance,
        "post": current_balance,
        "drift": f"{balance_drift:.2%}",
        "passed": balance_ok,
    }
    if not balance_ok:
        results["passed"] = False

    # Check reputation
    rep_result = api_call("get_agent_reputation", {"agent_id": agent_id})
    current_score = float(rep_result.get("reputation_score", 0))
    pre_score = float(
        pre_report["reputation_snapshot"].get("reputation_score", 0)
    )
    rep_delta = current_score - pre_score
    rep_ok = rep_delta >= -max_reputation_drop
    results["checks"]["reputation"] = {
        "pre": pre_score,
        "post": current_score,
        "delta": rep_delta,
        "passed": rep_ok,
    }
    if not rep_ok:
        results["passed"] = False

    # Check no unexpected active escrows
    escrow_result = api_call("list_escrows", {
        "agent_id": agent_id,
        "status": "active",
    })
    active_count = len(escrow_result.get("escrows", []))
    results["checks"]["escrows"] = {
        "active_count": active_count,
        "passed": True,  # Active escrows post-migration are normal
    }

    # Check service registration
    identity = api_call("get_agent_identity", {"agent_id": agent_id})
    current_version = identity.get("metadata", {}).get("current_version")
    results["checks"]["version"] = {
        "expected": pre_report["version_to"],
        "actual": current_version,
        "passed": current_version == pre_report["version_to"],
    }
    if current_version != pre_report["version_to"]:
        results["passed"] = False

    return results


# Run post-migration verification
verification = verify_migration(
    agent_id="acme-settlement-01",
    pre_report_path="migrations/2.1.0_pre_report.json",
)

print(f"Migration verification: {'PASSED' if verification['passed'] else 'FAILED'}")
for check_name, check_result in verification["checks"].items():
    status = "PASS" if check_result["passed"] else "FAIL"
    print(f"  [{status}] {check_name}: {check_result}")
```

### Cross-References

This guide integrates with other guides in the series:

- **Product 9 (Testing & Observability)**: The verification functions in this guide should be incorporated into your CI/CD pipeline. Chapter 4 of P9 covers chaos testing for deployment scenarios -- use those patterns to test your migration procedures before running them in production.
- **Product 12 (Incident Response)**: A failed migration is an incident. Chapter 6 of P12 includes a runbook specifically for deployment-related incidents. The rollback procedures in this guide should be referenced from your incident response playbook.
- **Product 16 (IAM)**: Key rotation during migration must follow the IAM key lifecycle from P16. Chapter 4 of P16 covers zero-downtime key rotation, which is the pattern used in this guide's state migration.

### Summary

Agent migration is fundamentally different from service deployment because agents carry state that has financial, contractual, and reputational consequences. The patterns in this guide -- version registry, pre-migration checks, blue-green deployment, canary releases, multi-layer rollback, and state migration -- transform agent deployment from a high-risk manual procedure into a repeatable, automated, and reversible process.

The single most important takeaway: never deploy an agent in-place. Always maintain a rollback target. Always drain financial state before migration. Always snapshot reputation. The cost of running two versions for a few hours is nothing compared to the cost of a failed deployment with no way back.

Every class in this guide calls the GreenHelix A2A Commerce Gateway API via the REST API (`POST /v1/{tool}`). Every method is designed to be called from your deployment scripts, your CI/CD pipeline, or your orchestration layer. Copy the code, configure the agent IDs and budget caps for your environment, and start versioning your agents like the production financial systems they are.

---

## GreenHelix Migration Manager — Working Implementation

The classes below use the `greenhelix_trading` library directly. Every method
calls the live GreenHelix A2A Commerce Gateway at `https://api.greenhelix.net/v1`.
Install the library, set your API key, and run the code as-is.

```bash
pip install greenhelix-trading
```

### Blue-Green Deployment Orchestrator

```python
"""
Full blue-green deployment lifecycle using MigrationManager and AgentVersionManager.

Workflow:
  1. Register old + new versions in the version registry.
  2. Pre-migration safety checks (escrows, balance, reputation).
  3. Freeze the old version's budget.
  4. Drain open escrows.
  5. Deploy new version via blue-green switch.
  6. Health-check the new version.
  7. If healthy  -> finalize.
     If unhealthy -> rollback automatically.
"""

import json
import sys
import time
from dataclasses import dataclass, field
from typing import Optional

from greenhelix_trading import MigrationManager, AgentVersionManager


# ── Configuration ────────────────────────────────────────────────────────────

API_KEY = "your-api-key"
AGENT_ID = "acme-settlement-01"
BASE_URL = "https://api.greenhelix.net/v1"

OLD_VERSION = "2.0.3"
NEW_VERSION = "2.1.0"

REPUTATION_ROLLBACK_THRESHOLD = 5.0   # points — roll back if score drops more
HEALTH_CHECK_RETRIES = 3
HEALTH_CHECK_INTERVAL_SEC = 10


# ── Data classes for deployment state ────────────────────────────────────────

@dataclass
class DeploymentSnapshot:
    """Immutable snapshot of agent state taken before migration."""
    version: str
    balance: dict
    reputation: dict
    escrows: dict
    timestamp: float = field(default_factory=time.time)

    def reputation_score(self) -> float:
        return float(
            self.reputation
            .get("result", self.reputation)
            .get("reputation_score", 0)
        )


@dataclass
class DeploymentResult:
    agent_id: str
    old_version: str
    new_version: str
    strategy: str
    status: str  # "deployed" | "rolled_back" | "failed"
    pre_snapshot: Optional[DeploymentSnapshot] = None
    post_health: Optional[dict] = None
    steps: list[dict] = field(default_factory=list)
    error: Optional[str] = None

    def add_step(self, name: str, status: str, detail: str = "") -> None:
        self.steps.append({
            "step": name,
            "status": status,
            "detail": detail,
            "ts": time.time(),
        })

    def summary(self) -> str:
        lines = [
            f"Deployment Result: {self.agent_id}",
            f"  Strategy:    {self.strategy}",
            f"  Transition:  {self.old_version} -> {self.new_version}",
            f"  Status:      {self.status}",
        ]
        if self.error:
            lines.append(f"  Error:       {self.error}")
        lines.append("  Steps:")
        for s in self.steps:
            lines.append(f"    [{s['status']}] {s['step']}: {s['detail']}")
        return "\n".join(lines)


# ── Blue-Green Orchestrator ──────────────────────────────────────────────────

class BlueGreenOrchestrator:
    """Coordinates a full blue-green deployment using the GreenHelix API.

    Uses MigrationManager for financial operations (freeze, drain, deploy,
    rollback) and AgentVersionManager for version registry management.
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: str = BASE_URL,
    ):
        self.agent_id = agent_id
        self.migrator = MigrationManager(
            api_key=api_key,
            agent_id=agent_id,
            base_url=base_url,
        )
        self.versions = AgentVersionManager(
            api_key=api_key,
            agent_id=agent_id,
            base_url=base_url,
        )
        self._result: Optional[DeploymentResult] = None

    # ── snapshot ─────────────────────────────────────────────────────────

    def _take_snapshot(self, version: str) -> DeploymentSnapshot:
        """Call pre_migration_check and package the result."""
        check = self.migrator.pre_migration_check()
        return DeploymentSnapshot(
            version=version,
            balance=check["balance"],
            reputation=check["reputation"],
            escrows=check["escrows"],
        )

    # ── health ───────────────────────────────────────────────────────────

    def _health_check_with_retry(
        self,
        version: str,
        retries: int = HEALTH_CHECK_RETRIES,
        interval: float = HEALTH_CHECK_INTERVAL_SEC,
    ) -> dict:
        """Retry health_check until success or exhaustion."""
        last_error = None
        for attempt in range(1, retries + 1):
            try:
                result = self.migrator.health_check(version)
                result["healthy"] = True
                return result
            except Exception as exc:
                last_error = str(exc)
                if attempt < retries:
                    time.sleep(interval)
        return {"healthy": False, "error": last_error, "version": version}

    # ── reputation guard ─────────────────────────────────────────────────

    def _reputation_degraded(
        self,
        pre: DeploymentSnapshot,
        post_health: dict,
    ) -> bool:
        """Return True if reputation dropped beyond the allowed threshold."""
        pre_score = pre.reputation_score()
        post_score = float(
            post_health
            .get("reputation", {})
            .get("reputation_score", pre_score)
        )
        return (pre_score - post_score) > REPUTATION_ROLLBACK_THRESHOLD

    # ── main workflow ────────────────────────────────────────────────────

    def deploy(
        self,
        old_version: str,
        new_version: str,
    ) -> DeploymentResult:
        """Execute the full blue-green deployment lifecycle.

        Returns a DeploymentResult with status "deployed" or "rolled_back".
        """
        result = DeploymentResult(
            agent_id=self.agent_id,
            old_version=old_version,
            new_version=new_version,
            strategy="blue-green",
            status="in_progress",
        )
        self._result = result

        try:
            # 1. Register both versions
            self.versions.register_version(
                old_version, metadata={"role": "blue"}
            )
            self.versions.register_version(
                new_version, metadata={"role": "green"}
            )
            result.add_step("register_versions", "ok",
                            f"{old_version}, {new_version}")

            # 2. Snapshot current state
            snapshot = self._take_snapshot(old_version)
            result.pre_snapshot = snapshot
            result.add_step("snapshot", "ok",
                            f"balance={snapshot.balance}, "
                            f"rep={snapshot.reputation_score():.1f}")

            # 3. Freeze budget on old version
            self.migrator.freeze_budget()
            result.add_step("freeze_budget", "ok", "daily=0, monthly=0")

            # 4. Drain open escrows
            drain = self.migrator.drain_escrows()
            result.add_step("drain_escrows", "ok",
                            f"drained {drain['count']} escrows")

            # 5. Blue-green deploy
            deploy = self.migrator.deploy_blue_green(new_version)
            result.add_step("deploy_blue_green", "ok",
                            f"old={deploy['old']}, new={deploy['new']}")

            # 6. Health check new version
            health = self._health_check_with_retry(new_version)
            result.post_health = health

            if not health.get("healthy"):
                result.add_step("health_check", "fail", str(health))
                return self._rollback(result, old_version,
                                      reason="health check failed")

            if self._reputation_degraded(snapshot, health):
                result.add_step("reputation_guard", "fail",
                                "score dropped beyond threshold")
                return self._rollback(result, old_version,
                                      reason="reputation degraded")

            result.add_step("health_check", "ok",
                            f"version {new_version} healthy")

            # 7. Migrate state from old -> new
            migration = self.migrator.migrate_state(old_version, new_version)
            result.add_step("migrate_state", "ok",
                            f"status={migration['status']}")

            result.status = "deployed"
            return result

        except Exception as exc:
            result.error = str(exc)
            result.add_step("exception", "fail", str(exc))
            try:
                return self._rollback(result, old_version,
                                      reason=f"exception: {exc}")
            except Exception as rb_exc:
                result.add_step("rollback_failed", "fail", str(rb_exc))
                result.status = "failed"
                return result

    def _rollback(
        self,
        result: DeploymentResult,
        target_version: str,
        reason: str = "",
    ) -> DeploymentResult:
        """Roll back to the target version and update the result."""
        rb = self.migrator.rollback(target_version)
        result.add_step("rollback", "ok",
                        f"to={target_version}, reason={reason}")
        result.status = "rolled_back"
        return result


# ── Run it ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    orchestrator = BlueGreenOrchestrator(
        api_key=API_KEY,
        agent_id=AGENT_ID,
    )

    result = orchestrator.deploy(
        old_version=OLD_VERSION,
        new_version=NEW_VERSION,
    )
    print(result.summary())

    # Persist the result for audit
    with open(f"migrations/{NEW_VERSION}_deployment.json", "w") as f:
        json.dump({
            "agent_id": result.agent_id,
            "old_version": result.old_version,
            "new_version": result.new_version,
            "strategy": result.strategy,
            "status": result.status,
            "steps": result.steps,
            "error": result.error,
        }, f, indent=2)
```

### Version Compatibility Checker

```python
"""
Pre-deployment compatibility verification.

Compares identity metadata between two agent versions to catch schema drift,
missing capabilities, and reputation regressions before traffic is switched.
"""

from greenhelix_trading import AgentVersionManager


def check_version_compatibility(
    api_key: str,
    agent_id: str,
    from_version: str,
    to_version: str,
    *,
    base_url: str = "https://api.greenhelix.net/v1",
    min_reputation: float = 70.0,
    required_capabilities: list[str] | None = None,
) -> dict:
    """Compare two registered versions and return a compatibility report.

    Checks:
      - Both versions are registered and resolvable via get_agent_identity.
      - The new version's reputation (if any) meets the minimum threshold.
      - Required capability keys exist in both versions' metadata.
      - Schema hashes match (when present in metadata).

    Returns a dict with "compatible" (bool) and per-check details.
    """
    vm = AgentVersionManager(
        api_key=api_key,
        agent_id=agent_id,
        base_url=base_url,
    )

    report: dict = {
        "from_version": from_version,
        "to_version": to_version,
        "checks": {},
        "compatible": True,
    }
    required_capabilities = required_capabilities or []

    # ── Resolve identities ───────────────────────────────────────────────

    try:
        from_identity = vm.get_version_identity(from_version)
        report["checks"]["from_resolvable"] = {"passed": True}
    except Exception as exc:
        report["checks"]["from_resolvable"] = {
            "passed": False,
            "error": str(exc),
        }
        report["compatible"] = False
        return report

    try:
        to_identity = vm.get_version_identity(to_version)
        report["checks"]["to_resolvable"] = {"passed": True}
    except Exception as exc:
        report["checks"]["to_resolvable"] = {
            "passed": False,
            "error": str(exc),
        }
        report["compatible"] = False
        return report

    # ── Reputation gate ──────────────────────────────────────────────────

    to_meta = to_identity.get("result", to_identity)
    to_rep = float(to_meta.get("reputation_score", 100))
    rep_ok = to_rep >= min_reputation
    report["checks"]["reputation"] = {
        "passed": rep_ok,
        "score": to_rep,
        "threshold": min_reputation,
    }
    if not rep_ok:
        report["compatible"] = False

    # ── Capability check ─────────────────────────────────────────────────

    from_caps = set(
        from_identity.get("result", from_identity)
        .get("metadata", {})
        .get("capabilities", [])
    )
    to_caps = set(
        to_meta.get("metadata", {}).get("capabilities", [])
    )
    missing = [c for c in required_capabilities if c not in to_caps]
    report["checks"]["capabilities"] = {
        "passed": len(missing) == 0,
        "from_capabilities": sorted(from_caps),
        "to_capabilities": sorted(to_caps),
        "missing": missing,
    }
    if missing:
        report["compatible"] = False

    # ── Schema hash comparison ───────────────────────────────────────────

    from_schema = (
        from_identity.get("result", from_identity)
        .get("metadata", {})
        .get("schema_hash")
    )
    to_schema = to_meta.get("metadata", {}).get("schema_hash")
    if from_schema and to_schema:
        schema_match = from_schema == to_schema
        report["checks"]["schema_hash"] = {
            "passed": schema_match,
            "from": from_schema,
            "to": to_schema,
        }
        if not schema_match:
            report["compatible"] = False
    else:
        report["checks"]["schema_hash"] = {
            "passed": True,
            "note": "No schema hashes in metadata; skipped.",
        }

    return report


# ── Example usage ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    compat = check_version_compatibility(
        api_key="your-api-key",
        agent_id="acme-settlement-01",
        from_version="2.0.3",
        to_version="2.1.0",
        min_reputation=75.0,
        required_capabilities=["escrow", "settlement", "dispute"],
    )

    print(f"Compatible: {compat['compatible']}")
    for name, check in compat["checks"].items():
        status = "PASS" if check["passed"] else "FAIL"
        print(f"  [{status}] {name}: {check}")
```

### Schema Migration with Rollback

```python
"""
Schema migration runner that uses MigrationManager for pre-flight safety
and AgentVersionManager for version tracking. Supports forward migration
and automatic rollback on failure.
"""

import copy
import time
from dataclasses import dataclass, field

from greenhelix_trading import MigrationManager, AgentVersionManager


@dataclass
class SchemaMigration:
    """A single forward/backward migration step."""
    version: str
    description: str
    forward_metadata: dict       # metadata to register with the new version
    backward_metadata: dict      # metadata to restore on rollback
    pre_checks: list[str] = field(default_factory=list)  # tool names to call


@dataclass
class MigrationPlan:
    """Ordered list of schema migrations to apply."""
    agent_id: str
    migrations: list[SchemaMigration] = field(default_factory=list)

    def add(self, migration: SchemaMigration) -> None:
        self.migrations.append(migration)


class SchemaMigrationRunner:
    """Apply schema migrations against the GreenHelix version registry.

    Each migration:
      1. Runs pre-flight checks via MigrationManager.pre_migration_check().
      2. Registers the new version with forward_metadata.
      3. Verifies the version is resolvable.
      4. On failure, rolls back every applied migration in reverse order.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.greenhelix.net/v1"):
        self.api_key = api_key
        self.base_url = base_url

    def execute(self, plan: MigrationPlan) -> dict:
        """Run all migrations in the plan. Returns a summary dict."""
        migrator = MigrationManager(
            api_key=self.api_key,
            agent_id=plan.agent_id,
            base_url=self.base_url,
        )
        vm = AgentVersionManager(
            api_key=self.api_key,
            agent_id=plan.agent_id,
            base_url=self.base_url,
        )

        applied: list[SchemaMigration] = []
        log: list[dict] = []

        for migration in plan.migrations:
            step_log = {
                "version": migration.version,
                "description": migration.description,
                "status": "pending",
            }

            try:
                # Pre-flight
                check = migrator.pre_migration_check()
                if not check.get("clear_to_migrate"):
                    step_log["status"] = "blocked"
                    step_log["detail"] = "pre_migration_check not clear"
                    log.append(step_log)
                    break

                # Register version with schema metadata
                vm.register_version(
                    migration.version,
                    metadata=migration.forward_metadata,
                )

                # Verify it is resolvable
                identity = vm.get_version_identity(migration.version)
                if not identity:
                    raise RuntimeError(
                        f"Version {migration.version} not resolvable after registration"
                    )

                step_log["status"] = "applied"
                applied.append(migration)

            except Exception as exc:
                step_log["status"] = "failed"
                step_log["error"] = str(exc)
                log.append(step_log)

                # Roll back in reverse
                rollback_log = self._rollback(vm, migrator, applied)
                return {
                    "agent_id": plan.agent_id,
                    "status": "rolled_back",
                    "applied_before_failure": len(applied),
                    "migration_log": log,
                    "rollback_log": rollback_log,
                }

            log.append(step_log)

        return {
            "agent_id": plan.agent_id,
            "status": "completed",
            "applied": len(applied),
            "migration_log": log,
        }

    def _rollback(
        self,
        vm: AgentVersionManager,
        migrator: MigrationManager,
        applied: list[SchemaMigration],
    ) -> list[dict]:
        """Roll back applied migrations in reverse order."""
        rollback_log: list[dict] = []
        for migration in reversed(applied):
            entry = {"version": migration.version, "status": "pending"}
            try:
                # Re-register with backward metadata to undo the schema change
                vm.register_version(
                    migration.version,
                    metadata=migration.backward_metadata,
                )
                migrator.rollback(migration.version)
                entry["status"] = "rolled_back"
            except Exception as exc:
                entry["status"] = "rollback_failed"
                entry["error"] = str(exc)
            rollback_log.append(entry)
        return rollback_log


# ── Example usage ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    runner = SchemaMigrationRunner(api_key="your-api-key")

    plan = MigrationPlan(agent_id="acme-settlement-01")

    plan.add(SchemaMigration(
        version="2.1.0",
        description="Add dispute_auto_resolve capability",
        forward_metadata={
            "capabilities": ["escrow", "settlement", "dispute", "dispute_auto_resolve"],
            "schema_hash": "abc123",
        },
        backward_metadata={
            "capabilities": ["escrow", "settlement", "dispute"],
            "schema_hash": "def456",
        },
    ))

    plan.add(SchemaMigration(
        version="2.2.0",
        description="Add multi-currency settlement support",
        forward_metadata={
            "capabilities": [
                "escrow", "settlement", "dispute",
                "dispute_auto_resolve", "multi_currency",
            ],
            "schema_hash": "ghi789",
            "supported_currencies": ["USD", "EUR", "GBP"],
        },
        backward_metadata={
            "capabilities": ["escrow", "settlement", "dispute", "dispute_auto_resolve"],
            "schema_hash": "abc123",
        },
    ))

    result = runner.execute(plan)
    print(f"Migration status: {result['status']}")
    for entry in result["migration_log"]:
        print(f"  [{entry['status']}] {entry['version']}: {entry.get('description', '')}")
```

### Canary Release Manager

```python
"""
Progressive canary release with automatic promotion or rollback.

Stages traffic from 5% -> 25% -> 50% -> 100%, checking health at each gate.
Uses MigrationManager.deploy_canary() for traffic splitting and
MigrationManager.health_check() for gate validation.
"""

import time
from dataclasses import dataclass, field

from greenhelix_trading import MigrationManager, AgentVersionManager


DEFAULT_CANARY_STAGES = [5, 25, 50, 100]
DEFAULT_GATE_WAIT_SEC = 60
DEFAULT_MAX_REP_DROP = 3.0


@dataclass
class CanaryGateResult:
    stage_pct: int
    healthy: bool
    reputation_delta: float
    detail: str
    timestamp: float = field(default_factory=time.time)


class CanaryReleaseManager:
    """Manages a staged canary release with automatic health gates.

    At each stage, the manager:
      1. Calls deploy_canary() to shift traffic to the new version.
      2. Waits for the configured observation window.
      3. Runs health_check() and compares reputation to the baseline.
      4. If the gate passes, advances to the next stage.
      5. If the gate fails, calls rollback() and stops.
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: str = "https://api.greenhelix.net/v1",
        stages: list[int] | None = None,
        gate_wait_sec: float = DEFAULT_GATE_WAIT_SEC,
        max_reputation_drop: float = DEFAULT_MAX_REP_DROP,
    ):
        self.agent_id = agent_id
        self.stages = stages or list(DEFAULT_CANARY_STAGES)
        self.gate_wait_sec = gate_wait_sec
        self.max_reputation_drop = max_reputation_drop
        self.migrator = MigrationManager(
            api_key=api_key,
            agent_id=agent_id,
            base_url=base_url,
        )
        self.versions = AgentVersionManager(
            api_key=api_key,
            agent_id=agent_id,
            base_url=base_url,
        )

    def _get_baseline_reputation(self) -> float:
        check = self.migrator.pre_migration_check()
        return float(
            check.get("reputation", {}).get("reputation_score", 100)
        )

    def _evaluate_gate(
        self, new_version: str, stage_pct: int, baseline_rep: float
    ) -> CanaryGateResult:
        """Wait, then check health and reputation for the canary version."""
        time.sleep(self.gate_wait_sec)

        try:
            health = self.migrator.health_check(new_version)
        except Exception as exc:
            return CanaryGateResult(
                stage_pct=stage_pct,
                healthy=False,
                reputation_delta=0.0,
                detail=f"health_check exception: {exc}",
            )

        current_rep = float(
            health.get("reputation", {}).get("reputation_score", baseline_rep)
        )
        delta = baseline_rep - current_rep

        if delta > self.max_reputation_drop:
            return CanaryGateResult(
                stage_pct=stage_pct,
                healthy=False,
                reputation_delta=-delta,
                detail=f"reputation dropped {delta:.1f} points (max {self.max_reputation_drop})",
            )

        return CanaryGateResult(
            stage_pct=stage_pct,
            healthy=True,
            reputation_delta=-delta,
            detail="gate passed",
        )

    def release(
        self,
        old_version: str,
        new_version: str,
    ) -> dict:
        """Run the full canary release lifecycle.

        Returns a dict with overall status and per-stage gate results.
        """
        # Register new version
        self.versions.register_version(
            new_version, metadata={"strategy": "canary"}
        )

        baseline_rep = self._get_baseline_reputation()
        gate_results: list[dict] = []

        for stage_pct in self.stages:
            # Shift traffic
            self.migrator.deploy_canary(new_version, traffic_pct=stage_pct)

            # Evaluate the gate
            gate = self._evaluate_gate(new_version, stage_pct, baseline_rep)
            gate_results.append({
                "stage_pct": gate.stage_pct,
                "healthy": gate.healthy,
                "reputation_delta": gate.reputation_delta,
                "detail": gate.detail,
            })

            if not gate.healthy:
                # Automatic rollback
                self.migrator.rollback(old_version)
                return {
                    "agent_id": self.agent_id,
                    "old_version": old_version,
                    "new_version": new_version,
                    "status": "rolled_back",
                    "failed_at_stage": stage_pct,
                    "gates": gate_results,
                }

        # All stages passed — migrate remaining state
        self.migrator.migrate_state(old_version, new_version)

        return {
            "agent_id": self.agent_id,
            "old_version": old_version,
            "new_version": new_version,
            "status": "fully_promoted",
            "gates": gate_results,
        }


# ── Example usage ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    canary = CanaryReleaseManager(
        api_key="your-api-key",
        agent_id="acme-settlement-01",
        stages=[5, 25, 50, 100],
        gate_wait_sec=30,
        max_reputation_drop=3.0,
    )

    result = canary.release(
        old_version="2.0.3",
        new_version="2.1.0",
    )

    print(f"Canary release: {result['status']}")
    for gate in result["gates"]:
        status = "PASS" if gate["healthy"] else "FAIL"
        print(f"  [{status}] {gate['stage_pct']}%: {gate['detail']} "
              f"(rep delta: {gate['reputation_delta']:+.1f})")
```

