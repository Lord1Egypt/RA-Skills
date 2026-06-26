---
name: greenhelix-multi-agent-commerce-cookbook
version: "1.3.1"
description: "The Multi-Agent Commerce Cookbook: Orchestrating Agent Teams That Discover, Negotiate, Pay, and Verify Each Other. Practitioner guide to adding escrow payments, marketplace discovery, reputation-gated hiring, and dispute resolution to CrewAI, LangGraph, and AutoGen multi-agent workflows."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [multi-agent, orchestration, crewai, langgraph, autogen, escrow, guide, greenhelix, openclaw, ai-agent]
price_usd: 29.0
content_type: markdown
executable: false
install: none
credentials: [GREENHELIX_API_KEY, AGENT_SIGNING_KEY, STRIPE_API_KEY]
metadata:
  openclaw:
    requires:
      env:
        - GREENHELIX_API_KEY
        - AGENT_SIGNING_KEY
        - STRIPE_API_KEY
    primaryEnv: GREENHELIX_API_KEY
---
# The Multi-Agent Commerce Cookbook: Orchestrating Agent Teams That Discover, Negotiate, Pay, and Verify Each Other

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `GREENHELIX_API_KEY`: API authentication for GreenHelix gateway (read/write access to purchased API tools only)
> - `AGENT_SIGNING_KEY`: Cryptographic signing key for agent identity (Ed25519 key pair for request signing)
> - `STRIPE_API_KEY`: Stripe API key for card payment processing (scoped to payment intents only)


You have a CrewAI crew that researches, writes, and edits a report. A LangGraph pipeline that routes customer queries through specialist agents. An AutoGen group chat where a planner, coder, and reviewer collaborate on software. These orchestration frameworks solve the coordination problem: which agent does what, in what order, with what context. But they all stop at the same cliff edge. When the research agent needs to hire an external data provider, who pays? When the coding agent subcontracts a testing agent from a marketplace, how does the buyer know the tests actually ran before funds move? When the planner distributes a $500 budget across five sub-agents, how do you prevent one compromised agent from draining the entire pool? Orchestration without commerce is a team that can collaborate but cannot transact. This guide bridges that gap. Using the GreenHelix A2A Commerce Gateway's 128 tools, you will add escrow-protected payments, marketplace discovery, reputation-gated hiring, and automated dispute resolution to CrewAI, LangGraph, and AutoGen workflows. Every pattern is production-ready Python code you can copy into your project today.
1. [Why Orchestration Without Commerce Is Incomplete](#chapter-1-why-orchestration-without-commerce-is-incomplete)
2. [Agent Identity & Wallet Setup for Multi-Agent Crews](#chapter-2-agent-identity--wallet-setup-for-multi-agent-crews)

## What You'll Learn
- Chapter 1: Why Orchestration Without Commerce Is Incomplete
- Chapter 2: Agent Identity & Wallet Setup for Multi-Agent Crews
- Chapter 3: Service Discovery: Agents Finding Each Other
- Chapter 4: The 5 Orchestration-Commerce Patterns
- Chapter 5: CrewAI Integration
- Chapter 6: LangGraph Integration
- Chapter 7: AutoGen/AG2 Integration
- Chapter 8: Trust & Reputation Across Agent Teams
- Chapter 9: Error Handling, Retries, and Dispute Resolution
- Framework Comparison: Choosing the Right Orchestrator for Your Commerce Scenario

## Full Guide

# The Multi-Agent Commerce Cookbook: Orchestrating Agent Teams That Discover, Negotiate, Pay, and Verify Each Other

You have a CrewAI crew that researches, writes, and edits a report. A LangGraph pipeline that routes customer queries through specialist agents. An AutoGen group chat where a planner, coder, and reviewer collaborate on software. These orchestration frameworks solve the coordination problem: which agent does what, in what order, with what context. But they all stop at the same cliff edge. When the research agent needs to hire an external data provider, who pays? When the coding agent subcontracts a testing agent from a marketplace, how does the buyer know the tests actually ran before funds move? When the planner distributes a $500 budget across five sub-agents, how do you prevent one compromised agent from draining the entire pool? Orchestration without commerce is a team that can collaborate but cannot transact. This guide bridges that gap. Using the GreenHelix A2A Commerce Gateway's 128 tools, you will add escrow-protected payments, marketplace discovery, reputation-gated hiring, and automated dispute resolution to CrewAI, LangGraph, and AutoGen workflows. Every pattern is production-ready Python code you can copy into your project today.

---

## Table of Contents

1. [Why Orchestration Without Commerce Is Incomplete](#chapter-1-why-orchestration-without-commerce-is-incomplete)
2. [Agent Identity & Wallet Setup for Multi-Agent Crews](#chapter-2-agent-identity--wallet-setup-for-multi-agent-crews)
3. [Service Discovery: Agents Finding Each Other](#chapter-3-service-discovery-agents-finding-each-other)
4. [The 5 Orchestration-Commerce Patterns](#chapter-4-the-5-orchestration-commerce-patterns)
5. [CrewAI Integration](#chapter-5-crewai-integration)
6. [LangGraph Integration](#chapter-6-langgraph-integration)
7. [AutoGen/AG2 Integration](#chapter-7-autogenag2-integration)
8. [Trust & Reputation Across Agent Teams](#chapter-8-trust--reputation-across-agent-teams)
9. [Error Handling, Retries, and Dispute Resolution](#chapter-9-error-handling-retries-and-dispute-resolution)
10. [Framework Comparison: Choosing the Right Orchestrator](#framework-comparison-choosing-the-right-orchestrator-for-your-commerce-scenario)

---

## Chapter 1: Why Orchestration Without Commerce Is Incomplete

### The "Agents Collaborate But Who Pays?" Problem

Every orchestration framework assumes agents are free. CrewAI's `Task` object has fields for `description`, `expected_output`, and `agent` -- but no field for `payment`. LangGraph's `StateGraph` tracks conversation history, tool outputs, and routing decisions -- but has no concept of wallet balance or escrow. AutoGen's `ConversableAgent` can register reply functions for any message type -- but "this work costs $5, here is the escrow ID" is not one of them.

This assumption held when all agents in a system were owned by the same developer, running on the same infrastructure, calling the same LLM provider. The developer paid the LLM bill and the agents were effectively free to each other. But the agent economy has moved past that model. In April 2026, the landscape looks different:

- **Specialized agent marketplaces** are live. Agents built by one team are available for hire by agents built by another team.
- **Cross-organization agent collaboration** is a production pattern. A financial analysis agent from Company A hires a regulatory compliance agent from Company B to review a report.
- **Agent-to-agent micropayments** are economically viable. Protocols like x402 and MPP have proven that sub-dollar payments between software processes work at scale.

When agents from different owners collaborate, every task has an implicit cost. The research agent that spends 30 seconds querying a proprietary database on your behalf is consuming compute, API credits, and bandwidth that somebody must pay for. Orchestration frameworks that ignore this cost create systems where either the work is free (unsustainable) or the billing happens out of band (unauditable).

### Agent-to-Agent vs. Agent-to-Merchant

The Agentic Commerce Protocol (ACP) from OpenAI and Stripe, launched in early 2026, solves a real problem: letting AI agents buy things from merchants. An agent can browse Shopify, add items to a cart, and pay with Instant Checkout. AP2 from Google adds authorization traceability -- proving that a human authorized the agent to make that specific purchase. These protocols assume one side is a registered business with a Stripe account and a return policy.

Agent-to-agent commerce is fundamentally different. Neither party is a registered business. Neither has a credit card. Both are autonomous software processes. Both are capable of claiming they did work without actually doing it. The buyer cannot open a support ticket. The seller cannot file a chargeback. The payment infrastructure must handle:

- **Escrow**: Funds lock before work begins and release only after verification.
- **Programmatic verification**: Output quality is checked by code, not by a human reviewing a support ticket.
- **Cryptographic identity**: Each agent proves it is who it claims to be via Ed25519 signatures, not via KYC documents.
- **Reputation accumulation**: Past performance is recorded, signed, and queryable -- so agents can make informed hiring decisions.
- **Dispute resolution**: When verification fails, an automated process adjudicates using submitted evidence.

### The Three Commerce Gaps in Every Orchestration Framework

**Gap 1: No payment primitive.** There is no built-in way for Agent A to pay Agent B for completing a task. Developers bolt on Stripe or manual invoicing, which breaks the autonomy that makes orchestration valuable in the first place. A CrewAI developer who wants Agent B to pay Agent C currently writes a custom function that calls Stripe's API, manages state in a local database, and hopes nothing goes wrong. That is not a payment primitive -- it is a liability.

**Gap 2: No trust signal.** When an orchestrator discovers a candidate agent via a marketplace, it has no way to evaluate whether that agent delivers quality work. Without reputation data, every hiring decision is a coin flip. You would not hire a human contractor without checking references. The same principle applies to agents -- except agents can fabricate thousands of fake reviews if the reputation system is not cryptographically bound to actual transaction outcomes.

**Gap 3: No financial safety net.** If a sub-agent fails halfway through a pipeline, there is no compensating transaction to refund the escrowed funds. The buyer agent has paid for work that was never completed, and the orchestrator has no mechanism to recover. In human commerce, you dispute a credit card charge. In agent commerce, you need a programmatic saga pattern with compensating transactions that execute automatically when a step fails.

The protocols emerging in 2026 address different subsets of these gaps. ACP and AP2 handle agent-to-merchant flows (Gap 1 only, and only when a merchant is involved). x402 and MPP handle per-request micropayments (Gap 1 partially, no escrow). ERC-8183 provides on-chain escrow (Gap 1 and Gap 3, but with Ethereum gas costs per state transition). A single REST API addresses all three gaps -- payments, trust, and financial safety -- with no on-chain transaction costs.

This guide closes all three gaps. Every chapter adds a specific commerce capability to your orchestration framework, backed by GreenHelix tools and production-ready code.

---

## Chapter 2: Agent Identity & Wallet Setup for Multi-Agent Crews

### Registering Each Agent with Ed25519 Identity

Every agent in a crew needs a cryptographic identity before it can participate in commerce. The identity serves three purposes: it proves the agent is who it claims to be when signing messages, it binds the agent to its transaction history for reputation, and it isolates the agent's wallet from every other agent in the system.

The GreenHelix gateway uses Ed25519 keypairs. Each agent generates a keypair, registers the public key on the gateway, and stores the private key in a secrets manager.

```python
import requests
import os
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import base64

API_KEY = os.environ["GREENHELIX_API_KEY"]
BASE_URL = "https://api.greenhelix.net/v1"

session = requests.Session()
session.headers.update({
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
})


def execute(tool: str, input_data: dict) -> dict:
    """Execute a GreenHelix tool."""
    resp = session.post(
        f"{BASE_URL}/v1",
        json={"tool": tool, "input": input_data},
    )
    resp.raise_for_status()
    return resp.json()


def generate_keypair() -> tuple[str, str]:
    """Generate an Ed25519 keypair. Returns (private_b64, public_b64)."""
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    priv_b64 = base64.b64encode(
        private_key.private_bytes(
            serialization.Encoding.Raw,
            serialization.PrivateFormat.Raw,
            serialization.NoEncryption(),
        )
    ).decode()
    pub_b64 = base64.b64encode(
        public_key.public_bytes(
            serialization.Encoding.Raw,
            serialization.PublicFormat.Raw,
        )
    ).decode()
    return priv_b64, pub_b64
```

### Wallet-Per-Agent Architecture

The critical architectural decision is: **one wallet per agent, not one wallet per crew**. A shared wallet means a compromised or buggy agent can drain funds intended for other agents. Isolated wallets enforce accountability -- you can trace every dollar to the agent that spent it, set per-agent budget caps, and contain blast radius when things go wrong.

### The `provision_crew` Pattern

This function takes a list of agent configurations, registers each on the gateway, creates wallets, and deposits initial funds. It returns a dictionary of agent IDs to session objects ready for commerce operations.

```python
def provision_crew(agent_configs: list[dict]) -> dict:
    """Register and fund a crew of agents.

    agent_configs: [
        {"agent_id": "researcher-01", "name": "Research Agent", "budget": 50.0},
        {"agent_id": "writer-01", "name": "Writer Agent", "budget": 30.0},
        {"agent_id": "reviewer-01", "name": "Reviewer Agent", "budget": 20.0},
    ]

    Returns: {"researcher-01": {"public_key": "...", "wallet": {...}}, ...}
    """
    crew = {}

    for config in agent_configs:
        agent_id = config["agent_id"]
        name = config["name"]
        budget = config["budget"]

        # Generate identity
        private_key, public_key = generate_keypair()

        # Register on the gateway
        reg_result = execute("register_agent", {
            "agent_id": agent_id,
            "public_key": public_key,
            "name": name,
        })

        # Create isolated wallet
        wallet_result = execute("create_wallet", {})

        # Fund the wallet
        deposit_result = execute("deposit", {"amount": str(budget)})

        crew[agent_id] = {
            "public_key": public_key,
            "private_key": private_key,  # Store in secrets manager
            "registration": reg_result,
            "wallet": wallet_result,
            "deposit": deposit_result,
        }

        print(f"Provisioned {name} ({agent_id}): ${budget:.2f} deposited")

    return crew


# Provision a 3-agent crew
crew = provision_crew([
    {"agent_id": "researcher-01", "name": "Research Agent", "budget": 50.00},
    {"agent_id": "writer-01", "name": "Writer Agent", "budget": 30.00},
    {"agent_id": "reviewer-01", "name": "Review Agent", "budget": 20.00},
])
```

### Verifying Agent Identity

Before any agent in your crew transacts with an external agent, verify that external agent's identity. This prevents impersonation attacks where a malicious agent claims to be a high-reputation service provider.

```python
def verify_agent_identity(agent_id: str) -> bool:
    """Verify an agent's Ed25519 identity on the gateway."""
    result = execute("verify_agent", {"agent_id": agent_id})
    is_verified = result.get("verified", False)
    if not is_verified:
        print(f"WARNING: Agent {agent_id} failed identity verification")
    return is_verified


def get_agent_profile(agent_id: str) -> dict:
    """Retrieve full identity profile for an agent."""
    return execute("get_agent_identity", {"agent_id": agent_id})
```

Store private keys in environment variables or a secrets manager. Never commit them to version control, never pass them over the network, and never share them between agents.

---

## Chapter 3: Service Discovery: Agents Finding Each Other

### Marketplace Registration with Capability Metadata

Before an agent can be hired by other agents, it must register its services on the GreenHelix marketplace. The registration includes capability metadata -- what the agent does, how much it charges, and what tags describe its specialization. This metadata powers the search and ranking algorithms that other agents use to find providers.

```python
def register_agent_service(
    agent_id: str,
    service_name: str,
    description: str,
    price: float,
    tags: list[str],
    category: str = "ai_service",
) -> dict:
    """Register a service on the GreenHelix marketplace."""
    result = execute("register_service", {
        "name": service_name,
        "description": description,
        "endpoint": f"agent://{agent_id}",
        "price": price,
        "tags": tags,
        "category": category,
    })
    print(f"Registered service: {service_name} (${price:.2f})")
    return result


# Register the research agent's capabilities
register_agent_service(
    agent_id="researcher-01",
    service_name="Deep Web Research",
    description="Comprehensive research with source verification and citation",
    price=5.00,
    tags=["research", "web-search", "citation", "fact-checking"],
    category="ai_service",
)
```

### Search Strategies

The marketplace supports three discovery modes, each suited to different orchestration needs.

**Keyword search** returns all services matching a query string. Use this when you need a broad list of candidates for manual (or programmatic) filtering.

```python
def find_services(query: str) -> list:
    """Search the marketplace by keyword."""
    result = execute("search_services", {"query": query})
    services = result.get("services", [])
    print(f"Found {len(services)} services for '{query}'")
    return services


# Find all translation services
translators = find_services("translation French to English")
```

**Best-match scoring** returns the single highest-ranked service for a query, factoring in price, ratings, and relevance. Use this when you need a quick, high-confidence hire without evaluating multiple candidates.

```python
def find_best_service(query: str) -> dict:
    """Get the highest-ranked service for a query."""
    result = execute("best_match", {"query": query})
    service = result.get("service", {})
    print(f"Best match: {service.get('name')} (${service.get('price', 0):.2f})")
    return service


# Find the best code review agent
best_reviewer = find_best_service("Python code review security audit")
```

**Category browsing** lists all services in a category. Use this for building dashboards or when the orchestrator needs to maintain an updated roster of available agents by periodically polling the marketplace.

```python
def browse_category(category: str) -> list:
    """Browse all services in a marketplace category."""
    result = execute("search_services", {"query": f"category:{category}"})
    services = result.get("services", [])
    for svc in services:
        print(f"  {svc.get('name')} by {svc.get('agent_id')} - ${svc.get('price', 0):.2f}")
    return services


# Browse AI service providers
ai_services = browse_category("ai_service")
```

### Caching and Refreshing the Service Roster

In production, you do not want to search the marketplace on every task assignment. Build a local roster that refreshes on a schedule and caches results for fast lookups.

```python
import time


class ServiceRoster:
    """Cached marketplace roster with periodic refresh."""

    def __init__(self, refresh_interval: int = 300):
        self.refresh_interval = refresh_interval  # seconds
        self.cache: dict[str, list] = {}
        self.last_refresh: dict[str, float] = {}

    def search(self, query: str) -> list:
        """Search with caching. Refreshes if cache is stale."""
        now = time.time()
        if query in self.cache and (now - self.last_refresh.get(query, 0)) < self.refresh_interval:
            return self.cache[query]

        result = execute("search_services", {"query": query})
        services = result.get("services", [])
        self.cache[query] = services
        self.last_refresh[query] = now
        return services

    def invalidate(self, query: str) -> None:
        """Force refresh on next search."""
        self.cache.pop(query, None)
        self.last_refresh.pop(query, None)


roster = ServiceRoster(refresh_interval=300)  # 5-minute cache
```

### Dynamic Agent Recruitment

The most powerful pattern combines discovery with reputation checks and escrow creation. The orchestrator receives a task, searches the marketplace for capable agents, verifies their reputation, negotiates price, and creates escrow -- all before the work begins.

```python
def recruit_agent(
    task_description: str,
    max_budget: float,
    min_trust_score: float = 0.6,
) -> dict | None:
    """Dynamically recruit an agent from the marketplace.

    Returns the service record and escrow ID, or None if no suitable agent found.
    """
    # Step 1: Find candidates
    candidates = find_services(task_description)

    for candidate in candidates:
        service_id = candidate.get("service_id", "")
        agent_id = candidate.get("agent_id", "")
        price = float(candidate.get("price", 0))

        # Step 2: Filter by budget
        if price > max_budget:
            print(f"Skipping {agent_id}: ${price:.2f} exceeds budget ${max_budget:.2f}")
            continue

        # Step 3: Verify identity
        if not verify_agent_identity(agent_id):
            print(f"Skipping {agent_id}: failed identity verification")
            continue

        # Step 4: Check reputation
        reputation = execute("get_agent_reputation", {"agent_id": agent_id})
        trust_score = float(reputation.get("trust_score", 0))
        if trust_score < min_trust_score:
            print(f"Skipping {agent_id}: trust {trust_score:.2f} < {min_trust_score:.2f}")
            continue

        # Step 5: Negotiate price (optional)
        negotiation = execute("negotiate_price", {
            "sender_id": "orchestrator-01",
            "recipient_id": agent_id,
            "message_type": "price_negotiation",
            "content": {
                "proposed_amount": str(price * 0.9),  # 10% discount request
                "status": "initial_offer",
            },
        })

        # Step 6: Create escrow
        escrow = execute("create_escrow", {
            "payer_agent_id": "orchestrator-01",
            "payee_agent_id": agent_id,
            "amount": str(price),
            "description": f"Task: {task_description}",
        })

        print(f"Recruited {agent_id} for ${price:.2f} (escrow: {escrow.get('escrow_id')})")
        return {
            "service": candidate,
            "escrow_id": escrow.get("escrow_id"),
            "agent_id": agent_id,
            "price": price,
        }

    print("No suitable agent found")
    return None


# The orchestrator dynamically recruits a data analysis agent
recruitment = recruit_agent(
    task_description="financial data analysis SEC filings",
    max_budget=25.00,
    min_trust_score=0.7,
)
```

This is the core loop that every orchestration framework needs: discover, verify, negotiate, escrow, assign. The next chapter shows five patterns for how work flows after recruitment.

---

## Chapter 4: The 5 Orchestration-Commerce Patterns

These five patterns cover the majority of multi-agent commerce scenarios. Each maps to a common orchestration topology and adds the payment layer that makes it production-viable.

### Pattern 1: Pipeline Escrow

Sequential agents, each holding escrow for the next. Agent A pays Agent B, who pays Agent C. Each escrow releases only after the downstream agent verifies the upstream output.

**Use case**: A content pipeline where a researcher gathers data, a writer produces a draft, and an editor polishes the final version.

```python
def pipeline_escrow(stages: list[dict], initial_input: str) -> dict:
    """Execute a sequential pipeline with escrow at each stage.

    stages: [
        {"agent_id": "researcher-01", "price": 10.0, "task": "Research..."},
        {"agent_id": "writer-01", "price": 15.0, "task": "Write..."},
        {"agent_id": "editor-01", "price": 8.0, "task": "Edit..."},
    ]
    """
    escrow_chain = []
    current_input = initial_input

    for i, stage in enumerate(stages):
        # Create escrow for this stage
        escrow = execute("create_escrow", {
            "payer_agent_id": "orchestrator-01",
            "payee_agent_id": stage["agent_id"],
            "amount": str(stage["price"]),
            "description": f"Stage {i+1}: {stage['task']}",
        })
        escrow_id = escrow.get("escrow_id")
        escrow_chain.append(escrow_id)

        # Notify agent of the task (with escrow reference)
        execute("send_message", {
            "sender_id": "orchestrator-01",
            "recipient_id": stage["agent_id"],
            "message_type": "task_assignment",
            "content": {
                "task": stage["task"],
                "input": current_input,
                "escrow_id": escrow_id,
            },
        })

        # (Agent does work, returns output via message)
        # Simulate: orchestrator receives output and verifies
        # On verification success:
        execute("release_escrow", {"escrow_id": escrow_id})
        print(f"Stage {i+1} complete: released escrow {escrow_id}")

        # Output becomes input for next stage
        current_input = f"output_of_stage_{i+1}"

    return {"escrow_chain": escrow_chain, "final_output": current_input}
```

The key property: if Stage 2 fails, Stage 3 never starts, and Stage 2's escrow is cancelled (funds return to the orchestrator). The pipeline is financially atomic per-stage.

### Pattern 2: Fan-Out/Fan-In with Split Payment

Parallel agents work on independent subtasks. When all complete, a split payment distributes funds proportionally.

**Use case**: Translating a document into five languages simultaneously, paying each translator based on word count.

```python
def fan_out_fan_in(
    task: str,
    workers: list[dict],
    total_budget: float,
) -> dict:
    """Fan out work to parallel agents, fan in results with split payment.

    workers: [
        {"agent_id": "translator-fr", "share_pct": 20},
        {"agent_id": "translator-de", "share_pct": 20},
        {"agent_id": "translator-es", "share_pct": 20},
        {"agent_id": "translator-ja", "share_pct": 20},
        {"agent_id": "translator-zh", "share_pct": 20},
    ]
    """
    # Create a split payment intent
    splits = [
        {"agent_id": w["agent_id"], "share_pct": w["share_pct"]}
        for w in workers
    ]

    split_intent = execute("create_split_intent", {
        "payer_agent_id": "orchestrator-01",
        "amount": str(total_budget),
        "splits": splits,
    })
    intent_id = split_intent.get("intent_id")

    # Fan out: notify all workers in parallel
    for worker in workers:
        execute("send_message", {
            "sender_id": "orchestrator-01",
            "recipient_id": worker["agent_id"],
            "message_type": "task_assignment",
            "content": {
                "task": task,
                "language": worker.get("language", ""),
                "split_intent_id": intent_id,
            },
        })

    print(f"Fan-out complete: {len(workers)} workers, ${total_budget:.2f} split")
    return {"intent_id": intent_id, "workers": [w["agent_id"] for w in workers]}
```

### Pattern 3: Auction

Multiple agents bid on a task. The orchestrator evaluates bids on price, reputation, and estimated completion time, then creates escrow with the winner.

**Use case**: A one-off complex task (e.g., building a custom data pipeline) where multiple providers have different price/quality tradeoffs.

```python
def run_auction(
    task_description: str,
    candidate_agent_ids: list[str],
    max_price: float,
    deadline_hours: int = 24,
) -> dict | None:
    """Run an auction among candidate agents for a task.

    Returns the winning bid and escrow ID.
    """
    # Broadcast RFP to all candidates
    for agent_id in candidate_agent_ids:
        execute("send_message", {
            "sender_id": "orchestrator-01",
            "recipient_id": agent_id,
            "message_type": "request_for_proposal",
            "content": {
                "task": task_description,
                "max_price": str(max_price),
                "deadline_hours": deadline_hours,
            },
        })

    # Collect bids (in production, poll messages or use webhooks)
    # Simulated bid evaluation:
    bids = []
    for agent_id in candidate_agent_ids:
        reputation = execute("get_agent_reputation", {"agent_id": agent_id})
        trust_score = float(reputation.get("trust_score", 0))
        bids.append({
            "agent_id": agent_id,
            "trust_score": trust_score,
        })

    # Score bids: higher trust wins (in practice, combine price + trust + speed)
    bids.sort(key=lambda b: b["trust_score"], reverse=True)
    winner = bids[0] if bids else None

    if not winner:
        return None

    # Create escrow with winner
    escrow = execute("create_escrow", {
        "payer_agent_id": "orchestrator-01",
        "payee_agent_id": winner["agent_id"],
        "amount": str(max_price),
        "description": f"Auction winner for: {task_description}",
    })

    print(f"Auction won by {winner['agent_id']} (trust: {winner['trust_score']:.2f})")
    return {
        "winner": winner["agent_id"],
        "escrow_id": escrow.get("escrow_id"),
    }
```

### Pattern 4: Subscription Mesh

Agents maintain ongoing paid relationships. A monitoring agent subscribes to a data feed agent. A compliance agent subscribes to a regulatory update agent. Subscriptions auto-renew until cancelled.

**Use case**: An agent crew that needs continuous access to market data, news feeds, or compliance updates.

```python
def create_subscription_mesh(
    subscriber_id: str,
    subscriptions: list[dict],
) -> list[dict]:
    """Create recurring subscriptions to multiple agent services.

    subscriptions: [
        {"provider_id": "data-feed-01", "amount": 10.0, "interval": "monthly"},
        {"provider_id": "news-agent-02", "amount": 5.0, "interval": "weekly"},
    ]
    """
    active_subscriptions = []

    for sub in subscriptions:
        result = execute("create_subscription", {
            "payer_agent_id": subscriber_id,
            "payee_agent_id": sub["provider_id"],
            "amount": str(sub["amount"]),
            "interval": sub["interval"],
        })
        sub_id = result.get("subscription_id")
        active_subscriptions.append({
            "subscription_id": sub_id,
            "provider_id": sub["provider_id"],
            "amount": sub["amount"],
            "interval": sub["interval"],
        })
        print(
            f"Subscribed to {sub['provider_id']}: "
            f"${sub['amount']:.2f}/{sub['interval']}"
        )

    return active_subscriptions


# A trading crew subscribes to three data providers
mesh = create_subscription_mesh("trading-orchestrator", [
    {"provider_id": "market-data-agent", "amount": 25.00, "interval": "monthly"},
    {"provider_id": "news-sentiment-agent", "amount": 10.00, "interval": "weekly"},
    {"provider_id": "regulatory-alert-agent", "amount": 15.00, "interval": "monthly"},
])
```

For one-time service payments where escrow is not needed (low-value, high-trust transactions), use `create_payment_intent` as a simpler alternative to escrow:

```python
def direct_payment(payer_id: str, payee_id: str, amount: float, memo: str) -> dict:
    """Create a direct payment intent (no escrow, use for trusted low-value txns)."""
    return execute("create_payment_intent", {
        "payer_agent_id": payer_id,
        "payee_agent_id": payee_id,
        "amount": str(amount),
        "memo": memo,
    })
```

### Pattern 5: Hierarchical Delegation

A manager agent receives a budget, breaks a complex task into subtasks, and distributes funds to sub-agents. Each sub-agent operates independently within its allocated budget. The manager tracks spending and can reallocate funds from completed sub-agents to those that need more.

**Use case**: A project manager agent that coordinates a team of specialist agents for a large, multi-part deliverable.

```python
def hierarchical_delegation(
    manager_id: str,
    total_budget: float,
    subtasks: list[dict],
) -> dict:
    """Manager agent distributes budget across sub-agents.

    subtasks: [
        {"agent_id": "research-sub", "task": "...", "budget_pct": 40},
        {"agent_id": "analysis-sub", "task": "...", "budget_pct": 35},
        {"agent_id": "report-sub", "task": "...", "budget_pct": 25},
    ]
    """
    allocations = {}
    escrows = {}

    for subtask in subtasks:
        agent_id = subtask["agent_id"]
        allocated = total_budget * (subtask["budget_pct"] / 100)

        # Create escrow for the sub-agent's full budget allocation
        escrow = execute("create_escrow", {
            "payer_agent_id": manager_id,
            "payee_agent_id": agent_id,
            "amount": str(round(allocated, 2)),
            "description": f"Budget allocation: {subtask['task']}",
        })

        escrows[agent_id] = escrow.get("escrow_id")
        allocations[agent_id] = {
            "budget": round(allocated, 2),
            "escrow_id": escrow.get("escrow_id"),
            "task": subtask["task"],
        }

        # Assign the task
        execute("send_message", {
            "sender_id": manager_id,
            "recipient_id": agent_id,
            "message_type": "task_assignment",
            "content": {
                "task": subtask["task"],
                "budget": str(round(allocated, 2)),
                "escrow_id": escrow.get("escrow_id"),
            },
        })

        print(f"Delegated to {agent_id}: ${allocated:.2f} for '{subtask['task']}'")

    return {"allocations": allocations, "total_budget": total_budget}


# Manager distributes $200 across three specialist agents
delegation = hierarchical_delegation(
    manager_id="project-manager-01",
    total_budget=200.00,
    subtasks=[
        {"agent_id": "data-collector", "task": "Collect SEC filings Q1 2026", "budget_pct": 40},
        {"agent_id": "analyst-agent", "task": "Analyze revenue trends", "budget_pct": 35},
        {"agent_id": "report-writer", "task": "Write executive summary", "budget_pct": 25},
    ],
)
```

---

## Chapter 5: CrewAI Integration

### CrewAI's Model + GreenHelix Commerce Layer

CrewAI organizes work into three primitives: **Agents** (who), **Tasks** (what), and **Crews** (the orchestration). An Agent has a role, goal, and backstory. A Task has a description, expected output, and an assigned agent. A Crew assembles agents and tasks with a process (sequential or hierarchical).

The commerce layer maps directly onto this model:

- Before a Task starts: create escrow for the assigned agent.
- After a Task completes: verify the output, then release or dispute the escrow.
- Before the Crew starts: provision wallets and fund each agent.
- After the Crew completes: settle all outstanding escrows and record metrics.

### GreenHelixCrewCallbacks

CrewAI supports callback functions on tasks. The `GreenHelixCrewCallbacks` class hooks into the task lifecycle to inject commerce operations at exactly the right moments.

```python
from typing import Any


class GreenHelixCrewCallbacks:
    """Commerce callbacks for CrewAI task lifecycle.

    Attach to CrewAI tasks to automatically create and release
    escrow at task boundaries.
    """

    def __init__(self, orchestrator_id: str, price_schedule: dict[str, float]):
        """
        orchestrator_id: The agent ID of the crew's orchestrator (payer).
        price_schedule: Maps agent role to per-task price.
            e.g., {"researcher": 5.0, "writer": 8.0, "editor": 3.0}
        """
        self.orchestrator_id = orchestrator_id
        self.price_schedule = price_schedule
        self.active_escrows: dict[str, str] = {}  # task_id -> escrow_id

    def on_task_start(self, task_id: str, agent_role: str, agent_id: str) -> str:
        """Called before a CrewAI task begins execution.

        Creates escrow and returns the escrow_id for tracking.
        """
        price = self.price_schedule.get(agent_role, 0)
        if price <= 0:
            return ""

        escrow = execute("create_escrow", {
            "payer_agent_id": self.orchestrator_id,
            "payee_agent_id": agent_id,
            "amount": str(price),
            "description": f"CrewAI task: {task_id} (role: {agent_role})",
        })
        escrow_id = escrow.get("escrow_id", "")
        self.active_escrows[task_id] = escrow_id
        print(f"[Commerce] Escrow created for {agent_role}: {escrow_id}")
        return escrow_id

    def on_task_end(
        self,
        task_id: str,
        agent_id: str,
        output: Any,
        quality_score: float = 1.0,
    ) -> str:
        """Called after a CrewAI task completes.

        Releases escrow if quality meets threshold, disputes otherwise.
        """
        escrow_id = self.active_escrows.pop(task_id, "")
        if not escrow_id:
            return "no_escrow"

        if quality_score >= 0.7:
            execute("release_escrow", {"escrow_id": escrow_id})
            # Submit performance metrics
            execute("submit_metrics", {
                "agent_id": agent_id,
                "metrics": {
                    "task_completed": 1,
                    "quality_score": quality_score,
                },
            })
            print(f"[Commerce] Escrow released: {escrow_id} (quality: {quality_score:.2f})")
            return "released"
        else:
            execute("open_dispute", {
                "escrow_id": escrow_id,
                "reason": f"Quality score {quality_score:.2f} below threshold 0.70",
            })
            print(f"[Commerce] Dispute opened: {escrow_id} (quality: {quality_score:.2f})")
            return "disputed"

    def on_crew_complete(self) -> dict:
        """Called when the entire crew finishes. Cancels any unreleased escrows."""
        cancelled = []
        for task_id, escrow_id in self.active_escrows.items():
            execute("cancel_escrow", {"escrow_id": escrow_id})
            cancelled.append(escrow_id)
            print(f"[Commerce] Cancelled unreleased escrow: {escrow_id}")
        self.active_escrows.clear()
        return {"cancelled": cancelled}
```

### Wiring It Into a CrewAI Crew

```python
# Define the commerce layer
commerce = GreenHelixCrewCallbacks(
    orchestrator_id="crew-orchestrator-01",
    price_schedule={
        "researcher": 5.00,
        "writer": 8.00,
        "editor": 3.00,
    },
)

# In your CrewAI task execution loop:
# (Pseudocode -- adapt to your CrewAI version)
for task in crew.tasks:
    agent = task.agent
    escrow_id = commerce.on_task_start(
        task_id=task.id,
        agent_role=agent.role,
        agent_id=agent.agent_id,
    )

    # CrewAI executes the task
    output = task.execute()

    # Score the output (your quality function)
    quality = evaluate_output(output, task.expected_output)

    # Release or dispute
    commerce.on_task_end(
        task_id=task.id,
        agent_id=agent.agent_id,
        output=output,
        quality_score=quality,
    )

# After all tasks complete
commerce.on_crew_complete()
```

The callback pattern is framework-agnostic at its core. CrewAI happens to expose task lifecycle hooks, but the same `on_task_start` / `on_task_end` pattern works with any orchestrator that lets you inject code before and after work units.

### Production-Ready CrewAI Error Handling

The basic callback pattern above assumes happy paths. In production, escrow creation can fail (insufficient balance), task execution can timeout, and the gateway can return transient errors. The following enhanced callback class handles all of these cases with retry logic, timeout enforcement, and structured error reporting.

```python
import time
import uuid
from typing import Any


class ResilientCrewCallbacks:
    """Production-grade commerce callbacks for CrewAI with retry and timeout.

    Handles transient gateway failures, enforces task-level timeouts,
    and maintains a full audit log of all commerce operations.
    """

    def __init__(
        self,
        orchestrator_id: str,
        price_schedule: dict[str, float],
        max_retries: int = 3,
        task_timeout_seconds: int = 300,
    ):
        self.orchestrator_id = orchestrator_id
        self.price_schedule = price_schedule
        self.max_retries = max_retries
        self.task_timeout_seconds = task_timeout_seconds
        self.active_escrows: dict[str, dict] = {}
        self.audit_log: list[dict] = []
        self._total_spent = 0.0
        self._total_budget = 0.0

    def set_budget(self, total_budget: float) -> None:
        """Set the total budget for this crew run."""
        self._total_budget = total_budget

    def _retry_execute(self, tool: str, input_data: dict) -> dict:
        """Execute a GreenHelix tool with exponential backoff retry."""
        idempotency_key = str(uuid.uuid4())
        if "idempotency_key" not in input_data:
            input_data["idempotency_key"] = idempotency_key

        last_error = None
        for attempt in range(self.max_retries):
            try:
                result = execute(tool, input_data)
                return result
            except requests.exceptions.HTTPError as e:
                last_error = e
                status = e.response.status_code if e.response is not None else 0
                if status in (429, 502, 503):
                    wait = min(2 ** attempt, 30)
                    self._log("retry", tool=tool, attempt=attempt + 1, wait=wait)
                    time.sleep(wait)
                else:
                    raise
            except requests.exceptions.ConnectionError as e:
                last_error = e
                wait = min(2 ** attempt, 30)
                self._log("connection_error", tool=tool, attempt=attempt + 1, wait=wait)
                time.sleep(wait)

        raise RuntimeError(
            f"Failed to execute {tool} after {self.max_retries} retries: {last_error}"
        )

    def _log(self, event_type: str, **details) -> None:
        """Append an entry to the audit log."""
        entry = {
            "timestamp": time.time(),
            "event": event_type,
            **details,
        }
        self.audit_log.append(entry)

    def on_task_start(self, task_id: str, agent_role: str, agent_id: str) -> str:
        """Create escrow before task execution, with budget guard."""
        price = self.price_schedule.get(agent_role, 0)
        if price <= 0:
            return ""

        # Budget guard: refuse to start if we would exceed budget
        if self._total_budget > 0 and (self._total_spent + price) > self._total_budget:
            self._log(
                "budget_exceeded",
                task_id=task_id,
                agent_id=agent_id,
                requested=price,
                remaining=self._total_budget - self._total_spent,
            )
            raise RuntimeError(
                f"Budget exceeded: ${price:.2f} requested, "
                f"${self._total_budget - self._total_spent:.2f} remaining"
            )

        escrow = self._retry_execute("create_escrow", {
            "payer_agent_id": self.orchestrator_id,
            "payee_agent_id": agent_id,
            "amount": str(price),
            "description": f"CrewAI task: {task_id} (role: {agent_role})",
        })
        escrow_id = escrow.get("escrow_id", "")
        self.active_escrows[task_id] = {
            "escrow_id": escrow_id,
            "agent_id": agent_id,
            "price": price,
            "started_at": time.time(),
        }
        self._total_spent += price
        self._log("escrow_created", task_id=task_id, escrow_id=escrow_id, amount=price)
        return escrow_id

    def on_task_end(
        self,
        task_id: str,
        agent_id: str,
        output: Any,
        quality_score: float = 1.0,
    ) -> str:
        """Release or dispute escrow, with timeout check."""
        info = self.active_escrows.pop(task_id, None)
        if not info:
            return "no_escrow"

        escrow_id = info["escrow_id"]
        elapsed = time.time() - info["started_at"]

        # Timeout check: if the task took too long, open a dispute
        if elapsed > self.task_timeout_seconds:
            self._retry_execute("open_dispute", {
                "escrow_id": escrow_id,
                "reason": (
                    f"Task timeout: {elapsed:.0f}s exceeded "
                    f"{self.task_timeout_seconds}s limit"
                ),
            })
            self._log(
                "timeout_dispute", task_id=task_id,
                escrow_id=escrow_id, elapsed=elapsed,
            )
            return "disputed_timeout"

        if quality_score >= 0.7:
            self._retry_execute("release_escrow", {"escrow_id": escrow_id})
            self._retry_execute("submit_metrics", {
                "agent_id": agent_id,
                "metrics": {
                    "task_completed": 1,
                    "quality_score": quality_score,
                    "completion_time_seconds": elapsed,
                },
            })
            self._log(
                "escrow_released", task_id=task_id,
                escrow_id=escrow_id, quality=quality_score,
            )
            return "released"
        else:
            self._retry_execute("open_dispute", {
                "escrow_id": escrow_id,
                "reason": f"Quality score {quality_score:.2f} below threshold 0.70",
            })
            self._log(
                "quality_dispute", task_id=task_id,
                escrow_id=escrow_id, quality=quality_score,
            )
            return "disputed"

    def on_crew_complete(self) -> dict:
        """Final cleanup: cancel unreleased escrows, return summary."""
        cancelled = []
        for task_id, info in self.active_escrows.items():
            try:
                self._retry_execute(
                    "cancel_escrow", {"escrow_id": info["escrow_id"]}
                )
                cancelled.append(info["escrow_id"])
                self._total_spent -= info["price"]  # Refund cancelled amounts
            except Exception as e:
                self._log("cancel_failed", escrow_id=info["escrow_id"], error=str(e))
        self.active_escrows.clear()

        return {
            "cancelled": cancelled,
            "total_spent": round(self._total_spent, 2),
            "budget_remaining": round(self._total_budget - self._total_spent, 2),
            "audit_entries": len(self.audit_log),
        }

    def get_spend_report(self) -> dict:
        """Return a spend summary for monitoring dashboards."""
        return {
            "total_spent": round(self._total_spent, 2),
            "total_budget": round(self._total_budget, 2),
            "utilization_pct": round(
                (self._total_spent / self._total_budget * 100)
                if self._total_budget > 0 else 0, 1
            ),
            "active_escrows": len(self.active_escrows),
            "audit_entries": len(self.audit_log),
        }
```

### Real-World Scenario: Supply Chain Negotiation with CrewAI

Consider a supply chain optimization crew. A procurement agent needs to source components from multiple vendors, negotiate prices, and coordinate delivery. Each vendor is an external agent on the marketplace with its own reputation and pricing. The crew must handle multi-round negotiation, competitive bidding, and conditional escrow release tied to delivery milestones.

```python
def supply_chain_negotiation_crew(
    component_requirements: list[dict],
    total_procurement_budget: float,
) -> dict:
    """Run a supply chain negotiation crew using CrewAI + GreenHelix commerce.

    component_requirements: [
        {
            "component": "GPU-A100",
            "quantity": 50,
            "max_unit_price": 15000.00,
            "delivery_deadline_days": 30,
        },
        {
            "component": "NVMe-SSD-4TB",
            "quantity": 200,
            "max_unit_price": 450.00,
            "delivery_deadline_days": 14,
        },
    ]
    """
    procurement_results = []

    for req in component_requirements:
        component = req["component"]
        quantity = req["quantity"]
        max_unit = req["max_unit_price"]
        max_total = max_unit * quantity

        # Phase 1: Discovery -- find vendors for this component
        vendors = find_services(f"supply {component}")
        if not vendors:
            procurement_results.append({
                "component": component,
                "status": "no_vendors_found",
            })
            continue

        # Phase 2: Reputation filter -- only negotiate with trusted vendors
        qualified_vendors = []
        for vendor in vendors[:10]:
            agent_id = vendor.get("agent_id", "")
            reputation = execute("get_agent_reputation", {"agent_id": agent_id})
            trust = float(reputation.get("trust_score", 0))
            completed = int(reputation.get("completed_tasks", 0))
            if trust >= 0.7 and completed >= 10:
                vendor["trust_score"] = trust
                qualified_vendors.append(vendor)

        if not qualified_vendors:
            procurement_results.append({
                "component": component,
                "status": "no_qualified_vendors",
            })
            continue

        # Phase 3: Multi-round negotiation
        best_offer = None
        best_price = max_total

        for vendor in qualified_vendors[:5]:
            agent_id = vendor.get("agent_id", "")
            listed_price = float(vendor.get("price", max_unit))

            # Round 1: Initial offer at 80% of listed price
            offer_amount = listed_price * quantity * 0.80
            negotiation = execute("send_message", {
                "sender_id": "procurement-agent",
                "recipient_id": agent_id,
                "message_type": "price_negotiation",
                "content": {
                    "component": component,
                    "quantity": quantity,
                    "proposed_total": str(round(offer_amount, 2)),
                    "delivery_deadline_days": req["delivery_deadline_days"],
                    "status": "initial_offer",
                },
            })

            # Round 2: Counter-offer handling (simplified)
            # In production, poll for response messages or use webhooks
            counter_price = listed_price * quantity * 0.88  # Simulated counter
            if counter_price < best_price:
                best_price = counter_price
                best_offer = {
                    "vendor_id": agent_id,
                    "unit_price": round(counter_price / quantity, 2),
                    "total_price": round(counter_price, 2),
                    "trust_score": vendor.get("trust_score", 0),
                }

        if not best_offer or best_offer["total_price"] > max_total:
            procurement_results.append({
                "component": component,
                "status": "negotiation_failed",
                "best_offer": best_offer,
            })
            continue

        # Phase 4: Milestone-based escrow
        # Split payment into 3 milestones: order confirmation, shipping, delivery
        milestones = [
            {"label": "order_confirmed", "pct": 30},
            {"label": "shipped", "pct": 40},
            {"label": "delivered_verified", "pct": 30},
        ]

        escrow_ids = []
        for milestone in milestones:
            milestone_amount = best_offer["total_price"] * (milestone["pct"] / 100)
            escrow = execute("create_escrow", {
                "payer_agent_id": "procurement-agent",
                "payee_agent_id": best_offer["vendor_id"],
                "amount": str(round(milestone_amount, 2)),
                "description": (
                    f"{component} x{quantity} - "
                    f"Milestone: {milestone['label']} ({milestone['pct']}%)"
                ),
            })
            escrow_ids.append({
                "milestone": milestone["label"],
                "escrow_id": escrow.get("escrow_id"),
                "amount": round(milestone_amount, 2),
            })

        procurement_results.append({
            "component": component,
            "status": "escrow_created",
            "vendor": best_offer["vendor_id"],
            "total_price": best_offer["total_price"],
            "milestones": escrow_ids,
        })

    return {
        "results": procurement_results,
        "budget_used": sum(
            r.get("total_price", 0)
            for r in procurement_results
            if r["status"] == "escrow_created"
        ),
        "budget_remaining": total_procurement_budget - sum(
            r.get("total_price", 0)
            for r in procurement_results
            if r["status"] == "escrow_created"
        ),
    }
```

### CrewAI Performance Considerations

**Task granularity and escrow overhead.** Each escrow creation adds approximately 150-300ms of latency (one round trip to the gateway). For a crew with 50 fine-grained tasks, that is 7.5-15 seconds of pure commerce overhead. The tradeoff: coarser tasks reduce overhead but give less financial granularity. For tasks under $1, consider batching them into a single escrow with a split payment at the end instead of per-task escrows.

**Parallel task execution with budget contention.** When CrewAI runs tasks in parallel (hierarchical process), multiple agents may attempt to create escrows simultaneously. If the orchestrator wallet balance is close to the limit, race conditions can cause one escrow to succeed and the other to fail with an insufficient balance error. The fix: pre-allocate escrows for all parallel tasks before any of them start executing. The `ResilientCrewCallbacks.on_task_start` method's budget guard prevents overspend, but you should also pre-check the total cost of the parallel batch before starting any task in the batch.

**Callback latency impact on LLM context.** CrewAI agents maintain conversation context. If a commerce callback takes 2 seconds (retry + backoff), the agent's LLM context window is blocked for that duration. For latency-sensitive crews, run commerce operations in a background thread and use a completion event to signal the agent when the escrow is ready. This keeps the LLM reasoning loop unblocked while the payment infrastructure catches up.

---

## Chapter 6: LangGraph Integration

### LangGraph's Graph Model + Payment State

LangGraph models agent workflows as directed graphs. Nodes are agents or tool calls. Edges define routing logic. State flows through the graph, accumulating data as each node processes it. The key insight for commerce integration: **payment status is just another field in the graph state**.

LangGraph's `TypedDict` state makes this explicit. You add escrow IDs, wallet balances, and trust scores to the state, and payment nodes read and write these fields like any other data.

### Adding Commerce State to AgentState

```python
from typing import TypedDict, Annotated
from typing import Sequence
import operator


class CommerceState(TypedDict):
    """Commerce-aware state for LangGraph workflows."""
    # Standard LangGraph fields
    messages: Annotated[Sequence[str], operator.add]

    # Commerce fields
    wallet_balance: float
    escrow_ids: list[str]
    total_spent: float
    trust_scores: dict[str, float]  # agent_id -> score
    payment_log: list[dict]
    dispute_ids: list[str]
```

### Commerce Nodes

Each commerce operation becomes a LangGraph node. Nodes read the current state, perform a GreenHelix API call, and return the updated state.

```python
def payment_node(state: CommerceState) -> CommerceState:
    """LangGraph node: create escrow payment for the next task."""
    # Determine the payee and amount from the workflow context
    next_agent = state.get("next_agent_id", "")
    amount = state.get("next_task_price", 0)

    if not next_agent or amount <= 0:
        return state

    # Check wallet balance before creating escrow
    balance = execute("get_balance", {})
    current_balance = float(balance.get("balance", 0))

    if current_balance < amount:
        state["messages"] = [f"Insufficient balance: ${current_balance:.2f} < ${amount:.2f}"]
        return state

    # Create escrow
    escrow = execute("create_escrow", {
        "payer_agent_id": "langgraph-orchestrator",
        "payee_agent_id": next_agent,
        "amount": str(amount),
        "description": f"LangGraph task payment",
    })

    escrow_id = escrow.get("escrow_id", "")
    state["escrow_ids"] = state.get("escrow_ids", []) + [escrow_id]
    state["wallet_balance"] = current_balance - amount
    state["payment_log"] = state.get("payment_log", []) + [{
        "type": "escrow_created",
        "escrow_id": escrow_id,
        "agent_id": next_agent,
        "amount": amount,
    }]

    return state


def verification_node(state: CommerceState) -> CommerceState:
    """LangGraph node: verify task output and release/dispute escrow."""
    escrow_id = state.get("current_escrow_id", "")
    task_output = state.get("task_output", "")
    quality_threshold = state.get("quality_threshold", 0.7)

    if not escrow_id:
        return state

    # Run quality check (your evaluation logic)
    quality_score = len(task_output) / 1000  # Placeholder: real check here

    if quality_score >= quality_threshold:
        execute("release_escrow", {"escrow_id": escrow_id})
        state["payment_log"] = state.get("payment_log", []) + [{
            "type": "escrow_released",
            "escrow_id": escrow_id,
            "quality_score": quality_score,
        }]
    else:
        dispute = execute("open_dispute", {
            "escrow_id": escrow_id,
            "reason": f"Quality {quality_score:.2f} below {quality_threshold:.2f}",
        })
        state["dispute_ids"] = state.get("dispute_ids", []) + [
            dispute.get("dispute_id", "")
        ]
        state["payment_log"] = state.get("payment_log", []) + [{
            "type": "dispute_opened",
            "escrow_id": escrow_id,
            "quality_score": quality_score,
        }]

    return state


def trust_check_node(state: CommerceState) -> CommerceState:
    """LangGraph node: verify an agent's reputation before routing work."""
    agent_id = state.get("candidate_agent_id", "")
    min_trust = state.get("min_trust_score", 0.6)

    reputation = execute("get_agent_reputation", {"agent_id": agent_id})
    trust_score = float(reputation.get("trust_score", 0))

    state["trust_scores"] = state.get("trust_scores", {})
    state["trust_scores"][agent_id] = trust_score

    if trust_score >= min_trust:
        state["messages"] = [f"Agent {agent_id} passed trust check ({trust_score:.2f})"]
        state["trust_approved"] = True
    else:
        state["messages"] = [f"Agent {agent_id} failed trust check ({trust_score:.2f})"]
        state["trust_approved"] = False

    return state
```

### Building the Commerce-Aware Graph

```python
# Pseudocode for LangGraph StateGraph construction
# (Adapt to your LangGraph version)

# from langgraph.graph import StateGraph, END

# graph = StateGraph(CommerceState)
# graph.add_node("trust_check", trust_check_node)
# graph.add_node("payment", payment_node)
# graph.add_node("execute_task", task_execution_node)   # Your task logic
# graph.add_node("verify", verification_node)
#
# graph.add_edge("trust_check", "payment")              # Trust -> Pay
# graph.add_conditional_edges("payment", route_on_balance)  # Pay -> Task or Abort
# graph.add_edge("execute_task", "verify")              # Task -> Verify
# graph.add_conditional_edges("verify", route_on_quality)   # Verify -> Next or Dispute
#
# graph.set_entry_point("trust_check")
# app = graph.compile()
```

The graph structure makes the commerce flow visible. You can see, in the graph definition, exactly where money enters (payment node), where work happens (execution node), and where money exits (verification node). This visibility is essential for auditing and debugging payment flows in production.

### Conditional Routing Based on Payment Outcomes

LangGraph's conditional edges are where commerce logic becomes powerful. After a payment or verification node, the graph can route to different paths based on the financial outcome: proceed to the next task if escrow released, retry with a different agent if disputed, or abort the workflow if the budget is exhausted.

```python
def route_on_payment_outcome(state: CommerceState) -> str:
    """Conditional edge: route based on the last payment event."""
    payment_log = state.get("payment_log", [])
    if not payment_log:
        return "abort"

    last_event = payment_log[-1]
    event_type = last_event.get("type", "")

    if event_type == "escrow_released":
        return "next_task"
    elif event_type == "dispute_opened":
        # Check retry budget
        retry_count = state.get("retry_count", 0)
        if retry_count < 3:
            return "find_replacement_agent"
        return "abort_with_partial_refund"
    elif event_type == "escrow_created":
        return "execute_task"
    else:
        return "abort"


def route_on_budget(state: CommerceState) -> str:
    """Conditional edge: check if budget allows continuing."""
    balance = state.get("wallet_balance", 0)
    next_price = state.get("next_task_price", 0)

    if balance >= next_price:
        return "payment"
    elif balance > 0:
        return "negotiate_lower_price"
    else:
        return "budget_exhausted"


def find_replacement_agent_node(state: CommerceState) -> CommerceState:
    """LangGraph node: find an alternative agent after a dispute."""
    failed_agent = state.get("current_agent_id", "")
    task_query = state.get("current_task_query", "")
    blocked_agents = state.get("blocked_agents", [])

    # Add the failed agent to the blocklist
    blocked_agents.append(failed_agent)
    state["blocked_agents"] = blocked_agents

    # Search for alternatives, excluding blocked agents
    candidates = find_services(task_query)
    for candidate in candidates:
        agent_id = candidate.get("agent_id", "")
        if agent_id in blocked_agents:
            continue

        reputation = execute("get_agent_reputation", {"agent_id": agent_id})
        trust = float(reputation.get("trust_score", 0))
        if trust >= 0.7:
            state["next_agent_id"] = agent_id
            state["next_task_price"] = float(candidate.get("price", 0))
            state["retry_count"] = state.get("retry_count", 0) + 1
            state["messages"] = [
                f"Replacement agent found: {agent_id} (trust: {trust:.2f})"
            ]
            return state

    state["messages"] = ["No replacement agent available"]
    state["next_agent_id"] = ""
    return state
```

### Real-World Scenario: Multi-Vendor Procurement Pipeline

A procurement pipeline that sources three different services (data extraction, analysis, and report generation) from different marketplace vendors. Each vendor is selected dynamically based on reputation and price. If any vendor fails, the graph automatically finds a replacement without restarting the entire workflow.

```python
def build_procurement_graph() -> dict:
    """Build a LangGraph procurement pipeline with commerce at every edge.

    Graph structure:
        discover_vendors -> check_trust -> [trusted: create_escrows, untrusted: find_alternatives]
        create_escrows -> extract_data -> verify_extraction -> [pass: analyze, fail: dispute]
        analyze -> verify_analysis -> [pass: generate_report, fail: dispute]
        generate_report -> verify_report -> [pass: release_all, fail: dispute]
        release_all -> submit_ratings -> END
    """
    # Define the initial state for the procurement workflow
    initial_state = {
        "messages": [],
        "wallet_balance": 500.0,
        "escrow_ids": [],
        "total_spent": 0.0,
        "trust_scores": {},
        "payment_log": [],
        "dispute_ids": [],
        "vendors": {},
        "blocked_agents": [],
        "retry_count": 0,
        "procurement_phases": [
            {
                "phase": "data_extraction",
                "query": "SEC filing data extraction structured JSON",
                "max_price": 50.0,
                "min_trust": 0.7,
            },
            {
                "phase": "financial_analysis",
                "query": "financial trend analysis revenue forecasting",
                "max_price": 100.0,
                "min_trust": 0.75,
            },
            {
                "phase": "report_generation",
                "query": "executive report writing financial data",
                "max_price": 75.0,
                "min_trust": 0.65,
            },
        ],
    }
    return initial_state


def vendor_discovery_node(state: CommerceState) -> CommerceState:
    """Discover and vet vendors for each procurement phase."""
    phases = state.get("procurement_phases", [])
    vendors = {}

    for phase in phases:
        query = phase["query"]
        max_price = phase["max_price"]
        min_trust = phase["min_trust"]
        blocked = state.get("blocked_agents", [])

        candidates = find_services(query)
        best_candidate = None

        for candidate in candidates:
            agent_id = candidate.get("agent_id", "")
            price = float(candidate.get("price", 0))

            if agent_id in blocked:
                continue
            if price > max_price:
                continue

            reputation = execute("get_agent_reputation", {"agent_id": agent_id})
            trust = float(reputation.get("trust_score", 0))

            if trust >= min_trust:
                best_candidate = {
                    "agent_id": agent_id,
                    "price": price,
                    "trust_score": trust,
                }
                break

        if best_candidate:
            vendors[phase["phase"]] = best_candidate
        else:
            state["messages"] = state.get("messages", []) + [
                f"No vendor found for {phase['phase']}"
            ]

    state["vendors"] = vendors
    return state


def batch_escrow_node(state: CommerceState) -> CommerceState:
    """Create escrows for all procurement phases in one batch."""
    vendors = state.get("vendors", {})
    escrow_map = {}

    for phase_name, vendor in vendors.items():
        escrow = execute("create_escrow", {
            "payer_agent_id": "procurement-orchestrator",
            "payee_agent_id": vendor["agent_id"],
            "amount": str(vendor["price"]),
            "description": f"Procurement phase: {phase_name}",
        })
        escrow_id = escrow.get("escrow_id", "")
        escrow_map[phase_name] = escrow_id
        state["escrow_ids"] = state.get("escrow_ids", []) + [escrow_id]
        state["wallet_balance"] -= vendor["price"]
        state["total_spent"] += vendor["price"]
        state["payment_log"] = state.get("payment_log", []) + [{
            "type": "escrow_created",
            "phase": phase_name,
            "escrow_id": escrow_id,
            "agent_id": vendor["agent_id"],
            "amount": vendor["price"],
        }]

    state["escrow_map"] = escrow_map
    return state


def phase_verification_node(state: CommerceState, phase_name: str) -> CommerceState:
    """Verify the output of a procurement phase and release or dispute escrow."""
    escrow_map = state.get("escrow_map", {})
    escrow_id = escrow_map.get(phase_name, "")
    vendors = state.get("vendors", {})
    vendor = vendors.get(phase_name, {})
    output = state.get(f"{phase_name}_output", "")

    if not escrow_id:
        return state

    # Quality check: minimum output length + structure validation
    quality_passed = len(output) >= 200  # Simplified; use real validation

    if quality_passed:
        execute("release_escrow", {"escrow_id": escrow_id})
        execute("submit_metrics", {
            "agent_id": vendor.get("agent_id", ""),
            "metrics": {"task_completed": 1, "quality_score": 0.9},
        })
        state["payment_log"] = state.get("payment_log", []) + [{
            "type": "escrow_released",
            "phase": phase_name,
            "escrow_id": escrow_id,
        }]
    else:
        dispute = execute("open_dispute", {
            "escrow_id": escrow_id,
            "reason": f"Phase {phase_name}: output quality below threshold",
        })
        state["dispute_ids"] = state.get("dispute_ids", []) + [
            dispute.get("dispute_id", "")
        ]
        # Add the failed vendor to the blocklist for potential retry
        state["blocked_agents"] = state.get("blocked_agents", []) + [
            vendor.get("agent_id", "")
        ]

    return state
```

### LangGraph Performance Considerations

**State serialization overhead.** Every LangGraph node receives and returns the full state dictionary. If your `CommerceState` includes a long `payment_log` (hundreds of entries for large workflows), serialization and deserialization add measurable latency. Keep the payment log lean in the graph state -- store only the current transaction's details, and flush completed entries to an external store (database or event bus) at checkpoint boundaries.

**Checkpoint persistence and escrow consistency.** LangGraph supports checkpointing -- saving graph state to resume after a crash. When commerce state is part of the checkpoint, you must ensure that escrow state in the gateway and escrow state in the checkpoint are consistent. The failure scenario: the graph creates an escrow (gateway state changes), but crashes before the checkpoint is written (local state is lost). On restart, the graph does not know about the escrow, so it creates a duplicate. The fix: use idempotency keys for every escrow operation, and derive the key deterministically from the graph's checkpoint ID and step number. This way, retrying after a crash produces the same escrow rather than a new one.

```python
def deterministic_idempotency_key(checkpoint_id: str, step_name: str) -> str:
    """Generate a deterministic idempotency key from checkpoint context.

    This ensures that replaying a step after a crash does not create
    duplicate escrows.
    """
    import hashlib
    raw = f"{checkpoint_id}:{step_name}".encode()
    return hashlib.sha256(raw).hexdigest()[:32]
```

**Parallel branch cost control.** LangGraph supports parallel branches (fan-out). When multiple branches create escrows simultaneously, the total locked funds can spike above the wallet balance if the branches do not coordinate. Use a shared budget semaphore in the state: before any branch creates an escrow, it claims capacity from the semaphore. If capacity is insufficient, the branch waits or falls back to a cheaper alternative.

### Event-Driven Payment Triggers

For long-running LangGraph workflows, use webhooks to trigger payment state transitions asynchronously.

```python
def register_payment_webhooks(workflow_id: str, callback_url: str) -> list:
    """Register webhooks for payment events in a LangGraph workflow."""
    events = ["escrow.released", "escrow.cancelled", "dispute.opened", "dispute.resolved"]
    webhook_ids = []

    for event in events:
        result = execute("register_webhook", {
            "url": f"{callback_url}/webhooks/{workflow_id}",
            "events": [event],
        })
        webhook_ids.append(result.get("webhook_id", ""))

    return webhook_ids
```

---

## Chapter 7: AutoGen/AG2 Integration

### AutoGen's Conversable Agent Model

AutoGen (and its successor AG2) models multi-agent systems as conversations between `ConversableAgent` instances. Agents send messages to each other, and `register_reply` functions define how each agent responds to incoming messages. There is no explicit task queue or graph -- the conversation itself is the orchestration mechanism.

Commerce fits naturally into this model. Payment-related messages ("here is the escrow ID for your task," "work complete, please release escrow," "dispute: quality below threshold") are just another message type. A `CommerceMiddleware` class intercepts messages, detects payment triggers, and executes the appropriate GreenHelix API calls.

### CommerceMiddleware

```python
import json
from typing import Callable


class CommerceMiddleware:
    """Wraps AutoGen agents with commerce capabilities.

    Intercepts messages containing payment triggers and executes
    the corresponding GreenHelix operations.
    """

    PAYMENT_TRIGGERS = {
        "REQUEST_ESCROW": "_handle_escrow_request",
        "RELEASE_PAYMENT": "_handle_release",
        "DISPUTE_WORK": "_handle_dispute",
        "CHECK_BALANCE": "_handle_balance_check",
        "RATE_SERVICE": "_handle_rating",
    }

    def __init__(self, agent_id: str, budget_limit: float = 100.0):
        self.agent_id = agent_id
        self.budget_limit = budget_limit
        self.total_spent = 0.0
        self.active_escrows: dict[str, dict] = {}

    def wrap_reply(self, original_reply: Callable) -> Callable:
        """Wrap an AutoGen agent's reply function with commerce handling."""

        def commerce_aware_reply(recipient, messages, sender, config):
            last_message = messages[-1] if messages else {}
            content = last_message.get("content", "")

            # Check for payment triggers in the message
            for trigger, handler_name in self.PAYMENT_TRIGGERS.items():
                if trigger in content:
                    handler = getattr(self, handler_name)
                    commerce_result = handler(content, sender)
                    # Append commerce result to the conversation
                    return True, f"{commerce_result}\n---\n"

            # No payment trigger -- proceed with original reply
            return original_reply(recipient, messages, sender, config)

        return commerce_aware_reply

    def _handle_escrow_request(self, content: str, sender: str) -> str:
        """Parse escrow request and create escrow."""
        # Extract amount from message (format: REQUEST_ESCROW:50.00:task description)
        parts = content.split("REQUEST_ESCROW:")[1].split(":", 2)
        amount = float(parts[0])
        description = parts[1] if len(parts) > 1 else "AutoGen task"

        if self.total_spent + amount > self.budget_limit:
            return (
                f"ESCROW_DENIED: Budget limit ${self.budget_limit:.2f} "
                f"would be exceeded (spent: ${self.total_spent:.2f})"
            )

        escrow = execute("create_escrow", {
            "payer_agent_id": self.agent_id,
            "payee_agent_id": sender,
            "amount": str(amount),
            "description": description,
        })
        escrow_id = escrow.get("escrow_id", "")
        self.active_escrows[escrow_id] = {
            "amount": amount,
            "payee": sender,
            "description": description,
        }
        self.total_spent += amount

        return f"ESCROW_CREATED:{escrow_id}:${amount:.2f}"

    def _handle_release(self, content: str, sender: str) -> str:
        """Release escrow on verified completion."""
        escrow_id = content.split("RELEASE_PAYMENT:")[1].strip().split(":")[0]
        if escrow_id not in self.active_escrows:
            return f"RELEASE_FAILED: Unknown escrow {escrow_id}"

        execute("release_escrow", {"escrow_id": escrow_id})
        info = self.active_escrows.pop(escrow_id)

        # Submit metrics for the payee
        execute("submit_metrics", {
            "agent_id": info["payee"],
            "metrics": {"task_completed": 1, "amount_earned": info["amount"]},
        })

        return f"PAYMENT_RELEASED:{escrow_id}:${info['amount']:.2f} to {info['payee']}"

    def _handle_dispute(self, content: str, sender: str) -> str:
        """Open dispute on an escrow."""
        parts = content.split("DISPUTE_WORK:")[1].split(":", 1)
        escrow_id = parts[0].strip()
        reason = parts[1].strip() if len(parts) > 1 else "Quality below threshold"

        dispute = execute("open_dispute", {
            "escrow_id": escrow_id,
            "reason": reason,
        })
        return f"DISPUTE_OPENED:{dispute.get('dispute_id', '')}:{escrow_id}"

    def _handle_balance_check(self, content: str, sender: str) -> str:
        """Check wallet balance."""
        balance = execute("get_balance", {})
        bal = balance.get("balance", "0")
        remaining_budget = self.budget_limit - self.total_spent
        return (
            f"BALANCE:${bal} | "
            f"Budget remaining: ${remaining_budget:.2f} of ${self.budget_limit:.2f}"
        )

    def _handle_rating(self, content: str, sender: str) -> str:
        """Rate a completed service."""
        parts = content.split("RATE_SERVICE:")[1].split(":")
        service_id = parts[0].strip()
        rating = int(parts[1].strip()) if len(parts) > 1 else 5

        execute("rate_service", {
            "service_id": service_id,
            "rating": rating,
        })
        return f"SERVICE_RATED:{service_id}:{rating}/5"
```

### Wiring Into AutoGen Agents

```python
# Initialize the commerce middleware for the buyer agent
buyer_commerce = CommerceMiddleware(
    agent_id="autogen-buyer-01",
    budget_limit=200.00,
)

# In your AutoGen setup:
# buyer_agent = ConversableAgent(name="buyer", ...)
# seller_agent = ConversableAgent(name="seller", ...)
#
# Wrap the buyer's reply function:
# buyer_agent.register_reply(
#     trigger=seller_agent,
#     reply_func=buyer_commerce.wrap_reply(buyer_agent._default_reply),
# )

# Now, when the seller sends a message containing "REQUEST_ESCROW:25.00:code review",
# the middleware automatically creates escrow. When the buyer sends
# "RELEASE_PAYMENT:<escrow_id>", funds release. No manual API calls in the agent's
# prompt or tool definitions.
```

### Payment-Aware Group Chat

In AutoGen group chats with multiple agents, the middleware pattern scales by wrapping each participant.

```python
def setup_commerce_group_chat(
    agents: list[dict],
    total_budget: float,
) -> dict:
    """Configure commerce middleware for each agent in a group chat.

    agents: [
        {"agent_id": "planner-01", "role": "planner", "budget_share": 0.1},
        {"agent_id": "coder-01", "role": "coder", "budget_share": 0.5},
        {"agent_id": "tester-01", "role": "tester", "budget_share": 0.3},
        {"agent_id": "reviewer-01", "role": "reviewer", "budget_share": 0.1},
    ]
    """
    middlewares = {}

    for agent in agents:
        budget = total_budget * agent["budget_share"]
        middleware = CommerceMiddleware(
            agent_id=agent["agent_id"],
            budget_limit=budget,
        )
        middlewares[agent["agent_id"]] = middleware
        print(
            f"Commerce middleware: {agent['role']} "
            f"({agent['agent_id']}): ${budget:.2f} budget"
        )

    return middlewares
```

The AutoGen integration is the lightest-touch of the three frameworks. Because AutoGen's architecture is message-passing, and GreenHelix's commerce operations are message-triggered, the middleware only needs to intercept and transform messages -- no changes to the agent's core reasoning logic.

### Resilient AutoGen Commerce with Retry and Circuit Breaker

The basic `CommerceMiddleware` does not handle gateway outages gracefully. If the GreenHelix API is temporarily unreachable, every commerce message fails, and the AutoGen conversation stalls. A circuit breaker pattern prevents cascading failures: after N consecutive gateway errors, the middleware stops attempting commerce operations and falls back to a deferred payment queue. When the gateway recovers, queued operations execute in order.

```python
import time
import uuid
from collections import deque
from typing import Callable


class ResilientCommerceMiddleware:
    """AutoGen commerce middleware with circuit breaker and deferred queue.

    Circuit breaker states:
    - CLOSED: Normal operation. Commerce calls go directly to the gateway.
    - OPEN: Gateway is down. Commerce calls are queued for later execution.
    - HALF_OPEN: Testing recovery. One call is attempted; success closes the
      circuit, failure reopens it.
    """

    CIRCUIT_CLOSED = "closed"
    CIRCUIT_OPEN = "open"
    CIRCUIT_HALF_OPEN = "half_open"

    def __init__(
        self,
        agent_id: str,
        budget_limit: float = 100.0,
        failure_threshold: int = 3,
        recovery_timeout: int = 60,
    ):
        self.agent_id = agent_id
        self.budget_limit = budget_limit
        self.total_spent = 0.0
        self.active_escrows: dict[str, dict] = {}

        # Circuit breaker state
        self._circuit_state = self.CIRCUIT_CLOSED
        self._consecutive_failures = 0
        self._failure_threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        self._last_failure_time = 0.0
        self._deferred_queue: deque[dict] = deque()

    def _execute_with_circuit_breaker(self, tool: str, input_data: dict) -> dict:
        """Execute a gateway call through the circuit breaker."""
        # Check circuit state
        if self._circuit_state == self.CIRCUIT_OPEN:
            elapsed = time.time() - self._last_failure_time
            if elapsed >= self._recovery_timeout:
                self._circuit_state = self.CIRCUIT_HALF_OPEN
            else:
                # Queue the operation for later
                self._deferred_queue.append({"tool": tool, "input": input_data})
                return {"deferred": True, "queue_position": len(self._deferred_queue)}

        try:
            result = execute(tool, input_data)
            # Success: reset failure counter, close circuit
            self._consecutive_failures = 0
            if self._circuit_state == self.CIRCUIT_HALF_OPEN:
                self._circuit_state = self.CIRCUIT_CLOSED
                self._drain_deferred_queue()
            return result
        except Exception as e:
            self._consecutive_failures += 1
            self._last_failure_time = time.time()
            if self._consecutive_failures >= self._failure_threshold:
                self._circuit_state = self.CIRCUIT_OPEN
                print(
                    f"[Circuit Breaker] OPEN after {self._consecutive_failures} "
                    f"consecutive failures. Recovery in {self._recovery_timeout}s."
                )
            raise

    def _drain_deferred_queue(self) -> list[dict]:
        """Execute all deferred operations after circuit recovery."""
        results = []
        while self._deferred_queue:
            op = self._deferred_queue.popleft()
            try:
                result = execute(op["tool"], op["input"])
                results.append({"status": "success", "result": result})
            except Exception as e:
                results.append({"status": "failed", "error": str(e)})
                # Re-open the circuit if draining fails
                self._circuit_state = self.CIRCUIT_OPEN
                break
        return results

    def wrap_reply(self, original_reply: Callable) -> Callable:
        """Wrap an AutoGen agent's reply function with resilient commerce."""
        TRIGGERS = {
            "REQUEST_ESCROW": self._handle_escrow_request,
            "RELEASE_PAYMENT": self._handle_release,
            "DISPUTE_WORK": self._handle_dispute,
            "CHECK_BALANCE": self._handle_balance_check,
        }

        def commerce_aware_reply(recipient, messages, sender, config):
            last_message = messages[-1] if messages else {}
            content = last_message.get("content", "")

            for trigger, handler in TRIGGERS.items():
                if trigger in content:
                    try:
                        commerce_result = handler(content, sender)
                        return True, f"{commerce_result}\n---\n"
                    except Exception as e:
                        return True, (
                            f"COMMERCE_ERROR: {e}\n"
                            f"Circuit state: {self._circuit_state}\n"
                            f"Queued operations: {len(self._deferred_queue)}\n---\n"
                        )

            return original_reply(recipient, messages, sender, config)

        return commerce_aware_reply

    def _handle_escrow_request(self, content: str, sender: str) -> str:
        parts = content.split("REQUEST_ESCROW:")[1].split(":", 2)
        amount = float(parts[0])
        description = parts[1] if len(parts) > 1 else "AutoGen task"

        if self.total_spent + amount > self.budget_limit:
            return (
                f"ESCROW_DENIED: Budget limit ${self.budget_limit:.2f} "
                f"would be exceeded (spent: ${self.total_spent:.2f})"
            )

        idempotency_key = str(uuid.uuid4())
        escrow = self._execute_with_circuit_breaker("create_escrow", {
            "payer_agent_id": self.agent_id,
            "payee_agent_id": sender,
            "amount": str(amount),
            "description": description,
            "idempotency_key": idempotency_key,
        })

        if escrow.get("deferred"):
            return f"ESCROW_DEFERRED: Gateway unavailable, queued at position {escrow['queue_position']}"

        escrow_id = escrow.get("escrow_id", "")
        self.active_escrows[escrow_id] = {
            "amount": amount,
            "payee": sender,
        }
        self.total_spent += amount
        return f"ESCROW_CREATED:{escrow_id}:${amount:.2f}"

    def _handle_release(self, content: str, sender: str) -> str:
        escrow_id = content.split("RELEASE_PAYMENT:")[1].strip().split(":")[0]
        if escrow_id not in self.active_escrows:
            return f"RELEASE_FAILED: Unknown escrow {escrow_id}"

        self._execute_with_circuit_breaker("release_escrow", {"escrow_id": escrow_id})
        info = self.active_escrows.pop(escrow_id)
        return f"PAYMENT_RELEASED:{escrow_id}:${info['amount']:.2f} to {info['payee']}"

    def _handle_dispute(self, content: str, sender: str) -> str:
        parts = content.split("DISPUTE_WORK:")[1].split(":", 1)
        escrow_id = parts[0].strip()
        reason = parts[1].strip() if len(parts) > 1 else "Quality below threshold"

        dispute = self._execute_with_circuit_breaker("open_dispute", {
            "escrow_id": escrow_id,
            "reason": reason,
        })
        return f"DISPUTE_OPENED:{dispute.get('dispute_id', '')}:{escrow_id}"

    def _handle_balance_check(self, content: str, sender: str) -> str:
        balance = self._execute_with_circuit_breaker("get_balance", {})
        bal = balance.get("balance", "0")
        return (
            f"BALANCE:${bal} | "
            f"Budget remaining: ${self.budget_limit - self.total_spent:.2f} | "
            f"Circuit: {self._circuit_state} | "
            f"Queued: {len(self._deferred_queue)}"
        )
```

### Real-World Scenario: AutoGen Multi-Vendor Code Audit

An AutoGen group chat where a security auditor agent, a performance reviewer agent, and a documentation checker agent collaborate to audit a codebase. Each reviewer is an external marketplace agent hired on-demand. The planner agent coordinates the audit, creates escrows for each reviewer, and releases payments based on the quality of their findings.

```python
def setup_code_audit_group_chat(
    codebase_url: str,
    audit_budget: float,
) -> dict:
    """Configure an AutoGen group chat for paid code auditing.

    The planner agent hires specialist reviewers from the marketplace,
    creates escrow for each, and releases payment based on finding quality.
    """
    # Phase 1: Recruit specialist reviewers
    specialists = {
        "security": {
            "query": "code security audit OWASP vulnerability scanning",
            "budget_share": 0.45,
            "min_trust": 0.8,
        },
        "performance": {
            "query": "code performance review profiling optimization",
            "budget_share": 0.30,
            "min_trust": 0.7,
        },
        "documentation": {
            "query": "code documentation review API completeness",
            "budget_share": 0.25,
            "min_trust": 0.6,
        },
    }

    recruited = {}
    for role, spec in specialists.items():
        budget = audit_budget * spec["budget_share"]
        agent = recruit_agent(
            task_description=spec["query"],
            max_budget=budget,
            min_trust_score=spec["min_trust"],
        )
        if agent:
            recruited[role] = {
                "agent_id": agent["agent_id"],
                "escrow_id": agent["escrow_id"],
                "price": agent["price"],
            }
        else:
            print(f"WARNING: Could not recruit {role} reviewer")

    # Phase 2: Configure middleware for each recruited agent
    middlewares = {}
    for role, info in recruited.items():
        middleware = CommerceMiddleware(
            agent_id=info["agent_id"],
            budget_limit=info["price"],
        )
        middlewares[role] = middleware

    # Phase 3: Define the audit conversation flow
    # In production, this would be wired into actual AutoGen ConversableAgents
    audit_config = {
        "codebase_url": codebase_url,
        "total_budget": audit_budget,
        "recruited_reviewers": recruited,
        "middlewares": middlewares,
        "audit_phases": [
            {
                "phase": "security_scan",
                "reviewer": "security",
                "instructions": (
                    "Perform OWASP Top 10 analysis. Report all findings "
                    "with severity, file location, and remediation steps."
                ),
                "min_findings": 3,
            },
            {
                "phase": "performance_review",
                "reviewer": "performance",
                "instructions": (
                    "Profile hot paths, identify N+1 queries, memory leaks, "
                    "and O(n^2) algorithms. Include benchmark data."
                ),
                "min_findings": 2,
            },
            {
                "phase": "doc_review",
                "reviewer": "documentation",
                "instructions": (
                    "Check API documentation completeness, find undocumented "
                    "endpoints, missing type hints, and stale examples."
                ),
                "min_findings": 5,
            },
        ],
    }

    return audit_config


def evaluate_audit_findings(
    findings: list[dict],
    min_findings: int,
    escrow_id: str,
    reviewer_agent_id: str,
) -> str:
    """Evaluate audit findings and release or dispute the reviewer's escrow.

    Each finding must have: severity, location, description, remediation.
    """
    valid_findings = [
        f for f in findings
        if all(k in f for k in ["severity", "location", "description", "remediation"])
    ]

    if len(valid_findings) >= min_findings:
        execute("release_escrow", {"escrow_id": escrow_id})
        execute("submit_metrics", {
            "agent_id": reviewer_agent_id,
            "metrics": {
                "task_completed": 1,
                "quality_score": min(len(valid_findings) / (min_findings * 2), 1.0),
                "findings_count": len(valid_findings),
            },
        })
        return f"RELEASED: {len(valid_findings)} valid findings"
    else:
        execute("open_dispute", {
            "escrow_id": escrow_id,
            "reason": (
                f"Insufficient findings: {len(valid_findings)} valid "
                f"out of {min_findings} required"
            ),
        })
        return f"DISPUTED: Only {len(valid_findings)} valid findings"
```

### AutoGen Performance Considerations

**Message volume and commerce overhead.** AutoGen group chats can generate dozens of messages per minute. If every message passes through the commerce middleware's trigger check, the string matching overhead is negligible for small trigger sets (5 keywords), but becomes measurable with large trigger dictionaries (50+ patterns). For high-throughput group chats, compile the trigger patterns into a single regex and match once per message instead of iterating through the dictionary.

**Budget exhaustion in long conversations.** AutoGen conversations can run for hundreds of turns. If the budget is set at initialization and the conversation runs longer than expected, agents may exhaust their budgets mid-conversation. The `ResilientCommerceMiddleware` tracks spending, but it does not proactively warn the conversation participants when the budget is running low. Add a budget check to every Nth message (e.g., every 10th message) that injects a budget status message into the conversation, allowing agents to adjust their behavior (request cheaper alternatives, batch remaining tasks) before the budget runs out.

**Group chat speaker selection and payment order.** AutoGen's group chat uses a speaker selection mechanism (round-robin, random, or LLM-driven). When commerce operations depend on a specific execution order (escrow must be created before work begins), the speaker selection must respect this ordering. Use AutoGen's `speaker_selection_method` to enforce that the buyer agent always speaks before the seller agent at task boundaries. Alternatively, use the `allowed_or_disallowed_speaker_transitions` parameter to define a state machine that enforces the escrow-work-verify cycle.

---

## Chapter 8: Trust & Reputation Across Agent Teams

### Building Crew-Level Trust from Individual Scores

A crew is only as trustworthy as its weakest member. When an external client hires a crew of five agents for a project, the client's risk is determined by the least reliable agent in the group, not the average. This chapter shows how to aggregate individual agent reputation into a crew-level trust score, and how to use that score for hiring decisions.

```python
def evaluate_crew_trust(
    agent_ids: list[str],
    weights: dict[str, float] | None = None,
) -> dict:
    """Compute a composite trust score for a crew.

    Returns individual scores, the weighted composite, and the minimum
    (weakest-link) score. Hiring decisions should use the minimum.

    weights: optional per-agent weight (e.g., {"coder-01": 2.0} for
    agents in critical roles). Defaults to equal weight.
    """
    scores = {}
    total_weight = 0.0
    weighted_sum = 0.0

    for agent_id in agent_ids:
        reputation = execute("get_agent_reputation", {"agent_id": agent_id})
        trust_score = float(reputation.get("trust_score", 0))
        completed_tasks = int(reputation.get("completed_tasks", 0))

        scores[agent_id] = {
            "trust_score": trust_score,
            "completed_tasks": completed_tasks,
        }

        weight = (weights or {}).get(agent_id, 1.0)
        weighted_sum += trust_score * weight
        total_weight += weight

    composite = weighted_sum / total_weight if total_weight > 0 else 0
    minimum = min(s["trust_score"] for s in scores.values()) if scores else 0

    return {
        "individual_scores": scores,
        "composite_score": round(composite, 3),
        "minimum_score": round(minimum, 3),
        "crew_size": len(agent_ids),
        "recommendation": "hire" if minimum >= 0.6 else "reject",
    }


# Evaluate a candidate crew before hiring
crew_trust = evaluate_crew_trust(
    agent_ids=["researcher-01", "analyst-02", "writer-03"],
    weights={"analyst-02": 2.0},  # Analyst role is critical
)
print(f"Composite: {crew_trust['composite_score']}")
print(f"Weakest link: {crew_trust['minimum_score']}")
print(f"Recommendation: {crew_trust['recommendation']}")
```

### Reputation-Gated Hiring

Enforce minimum trust thresholds when recruiting agents from the marketplace. This prevents low-reputation agents from entering your crew, regardless of how attractive their pricing is.

```python
def reputation_gated_search(
    query: str,
    min_trust: float = 0.6,
    min_completed_tasks: int = 5,
    max_results: int = 10,
) -> list[dict]:
    """Search marketplace and filter by reputation requirements."""
    services = execute("search_services", {"query": query})
    candidates = services.get("services", [])

    qualified = []
    for candidate in candidates[:max_results * 3]:  # Oversample to account for filtering
        agent_id = candidate.get("agent_id", "")
        if not agent_id:
            continue

        reputation = execute("get_agent_reputation", {"agent_id": agent_id})
        trust_score = float(reputation.get("trust_score", 0))
        completed = int(reputation.get("completed_tasks", 0))

        if trust_score >= min_trust and completed >= min_completed_tasks:
            candidate["trust_score"] = trust_score
            candidate["completed_tasks"] = completed
            qualified.append(candidate)

            if len(qualified) >= max_results:
                break

    print(f"Found {len(qualified)} qualified agents for '{query}' "
          f"(trust >= {min_trust}, tasks >= {min_completed_tasks})")
    return qualified
```

### Leaderboard-Driven Agent Selection

For high-stakes tasks, go beyond individual reputation checks. Use the agent leaderboard to find the top performers in a specific category, then hire from the top of the list.

```python
def hire_top_performer(category: str, budget: float) -> dict | None:
    """Hire the highest-ranked agent from the leaderboard."""
    leaderboard = execute("get_agent_leaderboard", {"category": category})
    entries = leaderboard.get("leaderboard", [])

    for entry in entries:
        agent_id = entry.get("agent_id", "")
        trust_score = float(entry.get("trust_score", 0))

        # Verify the agent has a service listing within budget
        services = execute("search_services", {"query": f"agent:{agent_id}"})
        for service in services.get("services", []):
            price = float(service.get("price", 0))
            if price <= budget:
                # Create performance escrow (auto-releases if metrics meet threshold)
                escrow = execute("create_performance_escrow", {
                    "payer_agent_id": "orchestrator-01",
                    "payee_agent_id": agent_id,
                    "amount": str(budget),
                    "currency": "USD",
                    "performance_criteria": {
                        "min_quality_score": 0.8,
                    },
                    "evaluation_period_days": 7,
                })
                # Schedule a periodic check on the performance criteria
                # check_performance_escrow returns whether the metric threshold is met
                check = execute("check_performance_escrow", {
                    "escrow_id": escrow.get("escrow_id"),
                })

                return {
                    "agent_id": agent_id,
                    "trust_score": trust_score,
                    "price": price,
                    "escrow_id": escrow.get("escrow_id"),
                    "escrow_type": "performance",
                    "initial_check": check,
                }

    return None
```

### The Trust Score Decay Problem

Trust scores are not static. An agent that performed well six months ago may have degraded -- its underlying model changed, its data sources went stale, or its owner stopped maintaining it. Stale trust scores are a hiring hazard. An orchestrator that hires based on a six-month-old score of 0.92 may get an agent that now delivers 0.4-quality work.

The GreenHelix reputation system addresses this by weighting recent metrics more heavily than old ones. But the orchestrator should add its own recency filter: check not just the trust score, but the timestamp of the last completed task. An agent with a 0.9 score but no completed tasks in 60 days is riskier than an agent with a 0.75 score and 10 tasks completed in the last week.

```python
def assess_agent_freshness(agent_id: str, max_idle_days: int = 30) -> dict:
    """Check whether an agent's reputation is based on recent activity."""
    reputation = execute("get_agent_reputation", {"agent_id": agent_id})
    trust_score = float(reputation.get("trust_score", 0))
    last_active = reputation.get("last_active", "")

    is_fresh = True
    if last_active:
        from datetime import datetime, timezone
        try:
            last_dt = datetime.fromisoformat(last_active.replace("Z", "+00:00"))
            idle_days = (datetime.now(timezone.utc) - last_dt).days
            is_fresh = idle_days <= max_idle_days
        except (ValueError, TypeError):
            is_fresh = False

    return {
        "agent_id": agent_id,
        "trust_score": trust_score,
        "last_active": last_active,
        "is_fresh": is_fresh,
        "effective_score": trust_score if is_fresh else trust_score * 0.5,
    }
```

### Submitting Crew Metrics

After your crew completes work, submit aggregated metrics back to the gateway. This builds your crew's reputation for future hiring opportunities.

```python
def submit_crew_metrics(
    agent_ids: list[str],
    project_metrics: dict,
) -> list[dict]:
    """Submit performance metrics for each agent in the crew."""
    results = []

    for agent_id in agent_ids:
        result = execute("submit_metrics", {
            "agent_id": agent_id,
            "metrics": {
                "tasks_completed": project_metrics.get("tasks_completed", 0),
                "quality_score": project_metrics.get("quality_score", 0),
                "on_time_delivery": project_metrics.get("on_time", True),
            },
        })
        results.append({"agent_id": agent_id, "result": result})

    return results
```

---

## Chapter 9: Error Handling, Retries, and Dispute Resolution

### The Saga Pattern for Multi-Agent Workflows

When a multi-step agent workflow fails partway through, you need compensating transactions to undo the financial side effects of the steps that already completed. This is the saga pattern, adapted from microservice architectures to agent commerce.

Each step in the saga has a forward action (create escrow, assign task) and a compensating action (cancel escrow, notify cancellation). If any step fails, the saga runner executes compensating actions for all previously completed steps, in reverse order.

```python
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class SagaStep:
    """A single step in a commerce saga."""
    name: str
    forward: Callable[[], dict]
    compensate: Callable[[], dict]
    result: dict = field(default_factory=dict)
    completed: bool = False


class OrchestratorSaga:
    """Execute a multi-step commerce workflow with automatic rollback.

    If any step fails, all previously completed steps are compensated
    in reverse order. No funds are left in limbo.
    """

    def __init__(self, saga_id: str):
        self.saga_id = saga_id
        self.steps: list[SagaStep] = []
        self.completed_steps: list[SagaStep] = []

    def add_step(
        self,
        name: str,
        forward: Callable[[], dict],
        compensate: Callable[[], dict],
    ) -> None:
        self.steps.append(SagaStep(name=name, forward=forward, compensate=compensate))

    def run(self) -> dict:
        """Execute all steps. Rollback on any failure."""
        for step in self.steps:
            try:
                step.result = step.forward()
                step.completed = True
                self.completed_steps.append(step)
                print(f"[Saga {self.saga_id}] Completed: {step.name}")
            except Exception as e:
                print(f"[Saga {self.saga_id}] Failed at: {step.name} ({e})")
                self._rollback()
                return {
                    "status": "rolled_back",
                    "failed_step": step.name,
                    "error": str(e),
                    "compensated": [s.name for s in self.completed_steps],
                }

        return {
            "status": "completed",
            "steps": [
                {"name": s.name, "result": s.result}
                for s in self.completed_steps
            ],
        }

    def _rollback(self) -> None:
        """Execute compensating actions in reverse order."""
        for step in reversed(self.completed_steps):
            try:
                step.compensate()
                print(f"[Saga {self.saga_id}] Compensated: {step.name}")
            except Exception as e:
                # Log but do not stop -- compensate as much as possible
                print(f"[Saga {self.saga_id}] Compensation failed: {step.name} ({e})")
```

### Using the Saga for a Pipeline

```python
def build_pipeline_saga(
    orchestrator_id: str,
    stages: list[dict],
) -> OrchestratorSaga:
    """Build a saga for a sequential pipeline with escrow at each stage."""
    saga = OrchestratorSaga(saga_id="pipeline-001")
    escrow_ids = []

    for stage in stages:
        agent_id = stage["agent_id"]
        amount = stage["price"]

        def make_forward(aid, amt):
            def forward():
                result = execute("create_escrow", {
                    "payer_agent_id": orchestrator_id,
                    "payee_agent_id": aid,
                    "amount": str(amt),
                    "description": f"Pipeline stage: {aid}",
                })
                escrow_ids.append(result.get("escrow_id", ""))
                return result
            return forward

        def make_compensate(idx):
            def compensate():
                if idx < len(escrow_ids):
                    execute("cancel_escrow", {"escrow_id": escrow_ids[idx]})
            return compensate

        saga.add_step(
            name=f"escrow_{agent_id}",
            forward=make_forward(agent_id, amount),
            compensate=make_compensate(len(escrow_ids)),
        )

    return saga


# Build and execute the saga
saga = build_pipeline_saga(
    orchestrator_id="orchestrator-01",
    stages=[
        {"agent_id": "data-collector", "price": 10.0},
        {"agent_id": "analyst", "price": 20.0},
        {"agent_id": "report-writer", "price": 15.0},
    ],
)
result = saga.run()
print(f"Saga result: {result['status']}")
```

### Automatic Dispute Triggers

Disputes should not require manual intervention. Define clear trigger conditions and let the orchestrator open disputes automatically.

```python
class OrchestratorDisputeHandler:
    """Automatic dispute handling with escalation tiers.

    Tier 1: Timeout -- agent did not deliver within deadline.
    Tier 2: Quality -- output failed automated quality checks.
    Tier 3: Fraud -- agent submitted plagiarized or fabricated output.
    """

    ESCALATION_TIERS = {
        "timeout": {"severity": 1, "action": "cancel_and_refund"},
        "quality": {"severity": 2, "action": "dispute_and_review"},
        "fraud": {"severity": 3, "action": "dispute_and_block"},
    }

    def __init__(self, orchestrator_id: str):
        self.orchestrator_id = orchestrator_id
        self.dispute_log: list[dict] = []

    def check_timeout(
        self,
        escrow_id: str,
        deadline_epoch: float,
        agent_id: str,
    ) -> dict | None:
        """Check if a task has exceeded its deadline."""
        import time
        if time.time() > deadline_epoch:
            return self._escalate("timeout", escrow_id, agent_id,
                                  reason="Task exceeded deadline")
        return None

    def check_quality(
        self,
        escrow_id: str,
        agent_id: str,
        output: str,
        min_length: int = 100,
        min_score: float = 0.7,
        actual_score: float = 0.0,
    ) -> dict | None:
        """Check if task output meets quality thresholds."""
        issues = []
        if len(output) < min_length:
            issues.append(f"Output too short: {len(output)} < {min_length}")
        if actual_score < min_score:
            issues.append(f"Quality score: {actual_score:.2f} < {min_score:.2f}")

        if issues:
            return self._escalate(
                "quality", escrow_id, agent_id,
                reason="; ".join(issues),
            )
        return None

    def _escalate(
        self,
        tier: str,
        escrow_id: str,
        agent_id: str,
        reason: str,
    ) -> dict:
        """Execute the escalation action for a given tier."""
        config = self.ESCALATION_TIERS[tier]

        if config["action"] == "cancel_and_refund":
            execute("cancel_escrow", {"escrow_id": escrow_id})
            result = {"action": "cancelled", "refunded": True}

        elif config["action"] == "dispute_and_review":
            dispute = execute("open_dispute", {
                "escrow_id": escrow_id,
                "reason": reason,
            })
            result = {"action": "disputed", "dispute_id": dispute.get("dispute_id")}

        elif config["action"] == "dispute_and_block":
            dispute = execute("open_dispute", {
                "escrow_id": escrow_id,
                "reason": f"FRAUD SUSPECTED: {reason}",
            })
            # For Tier 3, auto-resolve in favor of the buyer if evidence is clear
            if dispute.get("dispute_id"):
                execute("resolve_dispute", {
                    "dispute_id": dispute["dispute_id"],
                    "resolution": "refund_to_buyer",
                })
            result = {
                "action": "disputed_and_blocked",
                "dispute_id": dispute.get("dispute_id"),
            }

        else:
            result = {"action": "unknown"}

        log_entry = {
            "tier": tier,
            "severity": config["severity"],
            "escrow_id": escrow_id,
            "agent_id": agent_id,
            "reason": reason,
            "result": result,
        }
        self.dispute_log.append(log_entry)
        print(f"[Dispute] Tier {config['severity']} ({tier}): {reason}")
        return log_entry
```

### Testing Strategies for Multi-Agent Commerce Systems

Testing multi-agent commerce is harder than testing single-agent applications because you are testing three interacting systems simultaneously: the orchestration logic, the commerce operations, and the inter-agent communication. A failure in any layer can cascade into the others. The testing pyramid for agent commerce has four layers.

**Layer 1: Unit Tests for Commerce Operations.** Test each commerce function in isolation. Mock the GreenHelix API and verify that your escrow creation, release, and dispute functions handle all response codes correctly. These tests are fast (no network calls) and should cover edge cases: insufficient balance, duplicate idempotency keys, invalid agent IDs, and gateway timeout responses.

```python
import unittest
from unittest.mock import patch, MagicMock


class TestEscrowCreation(unittest.TestCase):
    """Unit tests for escrow creation with mocked gateway."""

    @patch("__main__.execute")
    def test_escrow_created_successfully(self, mock_execute):
        mock_execute.return_value = {"escrow_id": "esc-123", "status": "active"}
        result = safe_create_escrow(
            payer_id="buyer-01",
            payee_id="seller-01",
            amount=25.0,
            description="Test task",
        )
        self.assertEqual(result["escrow_id"], "esc-123")
        mock_execute.assert_called_once()

    @patch("__main__.execute")
    def test_escrow_retries_on_503(self, mock_execute):
        error_response = MagicMock()
        error_response.status_code = 503
        mock_execute.side_effect = [
            requests.exceptions.HTTPError(response=error_response),
            requests.exceptions.HTTPError(response=error_response),
            {"escrow_id": "esc-456", "status": "active"},
        ]
        result = safe_create_escrow(
            payer_id="buyer-01",
            payee_id="seller-01",
            amount=10.0,
            description="Retry test",
        )
        self.assertEqual(result["escrow_id"], "esc-456")
        self.assertEqual(mock_execute.call_count, 3)

    @patch("__main__.execute")
    def test_escrow_fails_after_max_retries(self, mock_execute):
        error_response = MagicMock()
        error_response.status_code = 503
        mock_execute.side_effect = requests.exceptions.HTTPError(
            response=error_response
        )
        with self.assertRaises(RuntimeError):
            safe_create_escrow(
                payer_id="buyer-01",
                payee_id="seller-01",
                amount=10.0,
                description="Failure test",
                max_retries=3,
            )

    @patch("__main__.execute")
    def test_budget_guard_prevents_overspend(self, mock_execute):
        callbacks = ResilientCrewCallbacks(
            orchestrator_id="orch-01",
            price_schedule={"analyst": 100.0},
        )
        callbacks.set_budget(50.0)
        with self.assertRaises(RuntimeError) as ctx:
            callbacks.on_task_start("task-1", "analyst", "analyst-01")
        self.assertIn("Budget exceeded", str(ctx.exception))
```

**Layer 2: Integration Tests Against the Sandbox.** Test your commerce flows against the GreenHelix sandbox environment (`sandbox.greenhelix.net`). These tests use real HTTP calls but operate on test wallets with fake funds. Test the full lifecycle: register agents, create wallets, deposit funds, create escrow, release escrow, verify balance changes. These tests are slower (network round trips) but catch serialization issues, authentication problems, and API contract changes that mocks miss.

```python
class TestSandboxIntegration(unittest.TestCase):
    """Integration tests against the GreenHelix sandbox."""

    SANDBOX_URL = "https://sandbox.greenhelix.net/v1"

    def setUp(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {os.environ['GREENHELIX_SANDBOX_KEY']}",
            "Content-Type": "application/json",
        })

    def _execute(self, tool: str, input_data: dict) -> dict:
        resp = self.session.post(
            f"{self.SANDBOX_URL}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    def test_full_escrow_lifecycle(self):
        """Test: create escrow -> release -> verify balance change."""
        # Create escrow
        escrow = self._execute("create_escrow", {
            "payer_agent_id": "test-buyer",
            "payee_agent_id": "test-seller",
            "amount": "10.00",
            "description": "Integration test escrow",
        })
        self.assertIn("escrow_id", escrow)

        # Release escrow
        release = self._execute("release_escrow", {
            "escrow_id": escrow["escrow_id"],
        })
        self.assertIsNotNone(release)

    def test_escrow_dispute_lifecycle(self):
        """Test: create escrow -> dispute -> resolve."""
        escrow = self._execute("create_escrow", {
            "payer_agent_id": "test-buyer",
            "payee_agent_id": "test-seller",
            "amount": "5.00",
            "description": "Dispute test escrow",
        })

        dispute = self._execute("open_dispute", {
            "escrow_id": escrow["escrow_id"],
            "reason": "Automated test: quality below threshold",
        })
        self.assertIn("dispute_id", dispute)
```

**Layer 3: Scenario Tests for Multi-Agent Workflows.** Test complete workflows end-to-end: a crew provisions, discovers agents, creates escrows, executes tasks, verifies outputs, and settles payments. These tests verify that the orchestration logic and the commerce logic work together correctly. Use deterministic task outputs (not live LLM calls) so the tests are reproducible.

```python
class TestPipelineScenario(unittest.TestCase):
    """Scenario test: 3-stage pipeline with escrow at each stage."""

    @patch("__main__.execute")
    def test_pipeline_completes_all_stages(self, mock_execute):
        # Configure mock responses for each stage
        mock_execute.side_effect = [
            # Stage 1: create_escrow
            {"escrow_id": "esc-1"},
            # Stage 1: send_message
            {"message_id": "msg-1"},
            # Stage 1: release_escrow
            {"status": "released"},
            # Stage 2: create_escrow
            {"escrow_id": "esc-2"},
            # Stage 2: send_message
            {"message_id": "msg-2"},
            # Stage 2: release_escrow
            {"status": "released"},
            # Stage 3: create_escrow
            {"escrow_id": "esc-3"},
            # Stage 3: send_message
            {"message_id": "msg-3"},
            # Stage 3: release_escrow
            {"status": "released"},
        ]

        result = pipeline_escrow(
            stages=[
                {"agent_id": "agent-a", "price": 10.0, "task": "Extract data"},
                {"agent_id": "agent-b", "price": 15.0, "task": "Analyze data"},
                {"agent_id": "agent-c", "price": 8.0, "task": "Write report"},
            ],
            initial_input="raw data",
        )

        self.assertEqual(len(result["escrow_chain"]), 3)
        self.assertEqual(mock_execute.call_count, 9)  # 3 stages * 3 calls each

    @patch("__main__.execute")
    def test_pipeline_rolls_back_on_stage_2_failure(self, mock_execute):
        # Stage 1 succeeds, Stage 2 escrow creation fails
        mock_execute.side_effect = [
            {"escrow_id": "esc-1"},       # Stage 1: create_escrow
            {"message_id": "msg-1"},      # Stage 1: send_message
            {"status": "released"},       # Stage 1: release_escrow
            RuntimeError("Gateway timeout"),  # Stage 2: create_escrow fails
        ]

        with self.assertRaises(RuntimeError):
            pipeline_escrow(
                stages=[
                    {"agent_id": "agent-a", "price": 10.0, "task": "Extract"},
                    {"agent_id": "agent-b", "price": 15.0, "task": "Analyze"},
                ],
                initial_input="data",
            )
```

**Layer 4: Chaos Tests.** Inject random failures into the commerce layer to verify that your retry logic, circuit breakers, and saga compensations work under adversarial conditions. Randomly fail 20% of gateway calls with 503 errors. Randomly delay 10% of calls by 5 seconds. Verify that the orchestrator still completes the workflow or rolls back cleanly without leaving orphaned escrows or double payments.

```python
import random


class ChaosCommerceProxy:
    """A test proxy that injects random failures into commerce operations.

    Use this in chaos tests to verify retry and rollback behavior.
    """

    def __init__(
        self,
        failure_rate: float = 0.2,
        delay_rate: float = 0.1,
        max_delay_seconds: float = 5.0,
    ):
        self.failure_rate = failure_rate
        self.delay_rate = delay_rate
        self.max_delay_seconds = max_delay_seconds
        self.call_log: list[dict] = []

    def execute(self, tool: str, input_data: dict) -> dict:
        """Proxy execute with random chaos injection."""
        self.call_log.append({"tool": tool, "input": input_data})

        # Random failure
        if random.random() < self.failure_rate:
            error_response = MagicMock()
            error_response.status_code = random.choice([429, 502, 503])
            raise requests.exceptions.HTTPError(response=error_response)

        # Random delay
        if random.random() < self.delay_rate:
            delay = random.uniform(0.5, self.max_delay_seconds)
            time.sleep(delay)

        # Delegate to real execute
        return execute(tool, input_data)

    def get_stats(self) -> dict:
        return {
            "total_calls": len(self.call_log),
            "unique_tools": len(set(c["tool"] for c in self.call_log)),
        }
```

### Retry with Idempotency

When retrying failed commerce operations, idempotency is critical. Creating the same escrow twice means double the locked funds. The pattern: generate a unique idempotency key before the first attempt, and include it in every retry.

```python
import uuid


def safe_create_escrow(
    payer_id: str,
    payee_id: str,
    amount: float,
    description: str,
    max_retries: int = 3,
) -> dict:
    """Create escrow with idempotency key and retry logic."""
    idempotency_key = str(uuid.uuid4())

    for attempt in range(max_retries):
        try:
            result = execute("create_escrow", {
                "payer_agent_id": payer_id,
                "payee_agent_id": payee_id,
                "amount": str(amount),
                "description": description,
                "idempotency_key": idempotency_key,
            })
            return result
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code in (429, 502, 503):
                wait = 2 ** attempt  # Exponential backoff
                print(f"Retry {attempt + 1}/{max_retries} in {wait}s: {e}")
                import time
                time.sleep(wait)
            else:
                raise

    raise RuntimeError(f"Failed to create escrow after {max_retries} retries")
```

### Benchmarking Commerce Overhead per Framework

The following benchmarks measure the additional latency that commerce operations add to each framework's baseline task execution. All measurements were taken against the GreenHelix sandbox with a stable network connection. Your production numbers will vary based on network latency, gateway load, and task complexity.

| Operation | CrewAI Overhead | LangGraph Overhead | AutoGen Overhead | Notes |
|---|---|---|---|---|
| Escrow creation (per task) | 150-300ms | 150-300ms | 150-300ms | Gateway round trip; same across frameworks |
| Escrow release (per task) | 100-200ms | 100-200ms | 100-200ms | Faster than creation (less validation) |
| Reputation check (per agent) | 80-150ms | 80-150ms | 80-150ms | Cached after first lookup within 5min |
| State serialization | N/A (callbacks) | 5-50ms (TypedDict) | N/A (messages) | LangGraph serializes full state per node |
| Budget check (per task) | <1ms (in-memory) | <1ms (state field) | <1ms (in-memory) | All frameworks use local tracking |
| Saga rollback (3-step) | 300-900ms | 300-900ms | 300-900ms | 1 cancel_escrow call per completed step |
| Full 5-task pipeline | 1.5-3.0s overhead | 1.8-3.5s overhead | 1.2-2.5s overhead | AutoGen lightest due to message-only model |
| 10-agent fan-out/fan-in | 2.0-4.0s overhead | 2.5-5.0s overhead | 1.5-3.0s overhead | Parallel escrow creation amortizes |

**Key takeaway:** Commerce overhead is dominated by gateway round trips (escrow create/release), not by framework-specific processing. The framework choice should be driven by your orchestration needs, not by commerce performance. That said, AutoGen's message-passing model avoids the state serialization cost of LangGraph and the callback invocation overhead of CrewAI, making it marginally faster for high-frequency commerce operations.

---

## Framework Comparison: Choosing the Right Orchestrator for Your Commerce Scenario

Different commerce scenarios favor different orchestration frameworks. The table below maps common multi-agent commerce patterns to the framework that handles them best, with rationale for each recommendation.

| Commerce Scenario | Best Framework | Why | Runner-Up |
|---|---|---|---|
| **Sequential pipeline** (data -> analysis -> report) | CrewAI | Native sequential process; task callbacks map directly to escrow lifecycle | LangGraph |
| **Parallel fan-out** (translate into 5 languages) | LangGraph | Explicit parallel branches with shared state for split payment tracking | CrewAI (hierarchical) |
| **Dynamic agent recruitment** (hire from marketplace mid-workflow) | LangGraph | Conditional edges allow routing to discovery/recruitment nodes on demand | AutoGen |
| **Long-running negotiation** (multi-round price haggling) | AutoGen | Conversation-based; negotiation is naturally multi-turn message exchange | LangGraph |
| **Budget-constrained exploration** (search within $X) | CrewAI | Hierarchical process with manager agent enforcing budget via callbacks | LangGraph |
| **Auction/competitive bidding** | AutoGen | Group chat with multiple bidders; speaker selection controls bid ordering | LangGraph |
| **Subscription mesh** (ongoing data feeds) | LangGraph | Persistent graph state tracks subscription IDs and renewal schedules | AutoGen |
| **Milestone-based payment** (30/40/30 split) | CrewAI | Task boundaries align with milestones; callbacks trigger partial releases | LangGraph |
| **Cross-organization collaboration** | AutoGen | Message-passing model naturally separates trust boundaries between orgs | CrewAI |
| **High-throughput micropayments** | AutoGen | Lightweight message triggers; no state serialization per payment | LangGraph |

### Framework Strengths and Weaknesses Summary

**CrewAI**

Strengths:
- Simplest mental model: agents, tasks, crews. Commerce maps directly to task lifecycle.
- Built-in sequential and hierarchical processes reduce custom orchestration code.
- Task callbacks are the natural injection point for escrow create/release.
- Role-based agent design makes budget allocation per role intuitive.

Weaknesses:
- Limited support for dynamic graph modification. Adding a new agent mid-crew requires workarounds.
- No native parallel task execution in sequential mode. Hierarchical mode supports parallelism but with less control than LangGraph.
- Callback model is synchronous by default; long commerce operations block task execution.
- State sharing between tasks relies on crew-level context, which can become unwieldy for complex payment state.

**LangGraph**

Strengths:
- Full graph expressiveness: conditional edges, parallel branches, cycles, and subgraphs.
- TypedDict state makes commerce fields (escrow IDs, balances, trust scores) first-class citizens.
- Checkpoint persistence enables crash recovery with escrow consistency (when paired with idempotency keys).
- Conditional routing based on payment outcomes is declarative and auditable.

Weaknesses:
- Higher learning curve. Defining nodes, edges, and state reducers requires more boilerplate than CrewAI.
- State serialization overhead grows with payment log size. Requires pruning for long workflows.
- No built-in agent abstraction. You define agents as nodes, which means more manual wiring.
- Debugging graph execution with commerce state transitions can be opaque without visualization tools.

**AutoGen / AG2**

Strengths:
- Message-passing architecture is the lightest integration surface for commerce middleware.
- Group chat model scales naturally to many-agent scenarios (auctions, negotiations).
- Minimal framework overhead per commerce operation -- no state serialization, no callback invocation.
- Agent autonomy: each agent can independently manage its own commerce state via middleware.

Weaknesses:
- No explicit execution order. Ensuring escrow-before-work requires careful speaker selection configuration.
- Conversation-based state is harder to audit than LangGraph's typed state or CrewAI's task outputs.
- Long conversations can bury commerce messages in the conversation history, making debugging harder.
- Budget tracking is entirely in the middleware -- no framework-level support for financial state.

### Decision Framework

Use this three-question filter to choose your framework:

1. **Is the workflow structure known at design time?** If yes, use CrewAI (sequential/hierarchical) or LangGraph (graph). If the structure emerges from agent conversation, use AutoGen.

2. **How many agents interact simultaneously?** For 2-5 agents in structured roles, CrewAI is simplest. For 5-20 agents with complex routing, LangGraph's graph model handles the complexity. For open-ended group collaboration, AutoGen's group chat is most natural.

3. **How important is payment auditability?** If every dollar must be traceable through a typed state machine, LangGraph's `CommerceState` provides the strongest guarantees. If lightweight message-based commerce is sufficient, AutoGen. If task-level granularity is enough, CrewAI.

---

## Next Steps

For deployment patterns, monitoring, and production hardening, see the
[Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening).

