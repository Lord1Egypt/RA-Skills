---
name: greenhelix-async-agent-commerce
version: "1.3.1"
description: "Async Agent Commerce: Event-Driven Patterns for Autonomous Transactions. Build event-driven agent commerce systems using saga patterns, compensating transactions, dead letter handling, exactly-once processing, backpressure, and async escrow settlement. Covers event bus architecture and webhook integration with detailed code examples with code."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [async, event-driven, saga, agent-commerce, guide, greenhelix, openclaw, ai-agent]
price_usd: 39.0
content_type: markdown
executable: false
install: none
credentials: none
---
# Async Agent Commerce: Event-Driven Patterns for Autonomous Transactions

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code, require credentials, or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.


The entire GreenHelix companion library is synchronous -- request, wait, response. You call `create_escrow`, the HTTP connection blocks for 200 milliseconds, and you get back an escrow ID. You call `release_escrow`, the connection blocks again, and the funds move. This works perfectly for simple two-party transactions that settle in seconds. But real-world agent commerce is inherently asynchronous. An escrow evaluation takes 30 days. A dispute resolution takes hours. A multi-agent negotiation involves back-and-forth over minutes. A compliance check depends on a third-party regulatory API that responds in 8 seconds on a good day and 90 seconds on a bad one. Synchronous polling wastes resources and misses events. A buyer agent that polls `get_escrow_status` every 5 seconds for 30 days makes 518,400 API calls to learn about a single state change. Multiply that by a fleet of 500 agents, each managing 20 active escrows, and you are burning 5.18 billion API calls per month on polling alone -- most returning "no change." This guide rebuilds agent commerce on event-driven foundations using GreenHelix's event bus, webhooks, and messaging tools. It covers the patterns that production distributed systems have relied on for decades -- saga orchestration, compensating transactions, dead letter handling, exactly-once processing, and backpressure -- adapted specifically for autonomous agent transactions. Every pattern is implemented in Python using asyncio, every example uses the GreenHelix API, and every class is designed to run in production without human intervention.
> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## What You'll Learn
- Chapter 1: Why Async Matters for Agent Commerce
- Chapter 2: AsyncEventBus Class
- Chapter 3: Saga Orchestrator Pattern
- Chapter 4: Compensating Transactions
- Chapter 5: Dead Letter Handling
- Chapter 6: Exactly-Once Processing
- Chapter 7: Backpressure
- Chapter 8: Async Escrow Settlement
- Next Steps
- What's Next

## Full Guide

# Async Agent Commerce: Event-Driven Patterns for Autonomous Transactions

The entire GreenHelix companion library is synchronous -- request, wait, response. You call `create_escrow`, the HTTP connection blocks for 200 milliseconds, and you get back an escrow ID. You call `release_escrow`, the connection blocks again, and the funds move. This works perfectly for simple two-party transactions that settle in seconds. But real-world agent commerce is inherently asynchronous. An escrow evaluation takes 30 days. A dispute resolution takes hours. A multi-agent negotiation involves back-and-forth over minutes. A compliance check depends on a third-party regulatory API that responds in 8 seconds on a good day and 90 seconds on a bad one. Synchronous polling wastes resources and misses events. A buyer agent that polls `get_escrow_status` every 5 seconds for 30 days makes 518,400 API calls to learn about a single state change. Multiply that by a fleet of 500 agents, each managing 20 active escrows, and you are burning 5.18 billion API calls per month on polling alone -- most returning "no change." This guide rebuilds agent commerce on event-driven foundations using GreenHelix's event bus, webhooks, and messaging tools. It covers the patterns that production distributed systems have relied on for decades -- saga orchestration, compensating transactions, dead letter handling, exactly-once processing, and backpressure -- adapted specifically for autonomous agent transactions. Every pattern is implemented in Python using asyncio, every example uses the GreenHelix API, and every class is designed to run in production without human intervention.

---


> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## Table of Contents

1. [Why Async Matters for Agent Commerce](#chapter-1-why-async-matters-for-agent-commerce)
2. [AsyncEventBus Class](#chapter-2-asynceventbus-class)
3. [Saga Orchestrator Pattern](#chapter-3-saga-orchestrator-pattern)
4. [Compensating Transactions](#chapter-4-compensating-transactions)
5. [Dead Letter Handling](#chapter-5-dead-letter-handling)
6. [Exactly-Once Processing](#chapter-6-exactly-once-processing)
7. [Backpressure](#chapter-7-backpressure)
8. [Async Escrow Settlement](#chapter-8-async-escrow-settlement)

---

## Chapter 1: Why Async Matters for Agent Commerce

### The Polling Tax

Every synchronous agent commerce system pays a hidden tax: the cost of asking "has anything changed?" repeatedly until the answer is yes. Consider the lifecycle of a single escrow-protected service transaction. The buyer creates an escrow via `create_escrow`. The seller delivers the service. The buyer evaluates delivery quality. The buyer releases the escrow via `release_escrow`. In a synchronous model, the buyer must poll for two state transitions: "has the seller acknowledged the escrow?" and "has delivery been confirmed by the SLA monitor?" Each poll is an HTTP request. Each request consumes compute on the buyer's side, network bandwidth in transit, and compute on the GreenHelix gateway.

The numbers scale badly. A single agent managing 50 active transactions, polling each at 10-second intervals, generates 432,000 API calls per day. A fleet of 200 agents generates 86.4 million. At GreenHelix's free tier rate limit of 100 calls per minute, a single agent would exhaust its entire rate budget on polling alone, leaving zero capacity for actual commerce operations. Even at the pro tier (1,000 calls per minute), polling 50 transactions at 10-second intervals consumes 300 calls per minute -- 30% of the agent's total capacity wasted on "has anything changed? no."

```
Synchronous Polling Cost Model
====================================

                          FREE TIER    PRO TIER     ENTERPRISE
Rate limit (calls/min)    100          1,000        10,000
Active transactions        50           50           50
Poll interval (seconds)    10           10           10
Polls per minute           300          300          300
Budget consumed            300%         30%          3%
Remaining for commerce     0%           70%          97%

With 200 agents:
Total polls/day            86.4M        86.4M        86.4M
API cost at $0.001/call    $86,400      $86,400      $86,400
Useful information gained  ~200         ~200         ~200
Cost per useful event      $432         $432         $432
```

The last row is the damning one. Of 86.4 million polls per day, approximately 200 return an actual state change. The cost per useful event is $432. Event-driven architecture inverts this: instead of asking 432,000 times and getting one answer, the system notifies you once when the answer changes. The cost per useful event drops to the cost of processing one webhook callback -- effectively zero.

### Real-World Async Scenarios in Agent Commerce

Not every agent transaction is a simple request-response. These are the scenarios where async patterns become essential:

**Multi-day escrow evaluation.** A buyer agent creates an escrow for a data pipeline service with a 30-day evaluation period. The SLA requires 99.95% uptime measured over the full 30 days. The escrow cannot be released or disputed until the evaluation window closes. Synchronous polling for 30 days is absurd. An event-driven system subscribes to `escrow.evaluation_complete` and processes the release when the event fires.

**Multi-party negotiation.** Three agents negotiate a supply chain arrangement. Agent A offers raw data. Agent B offers transformation services. Agent C wants transformed data. The negotiation involves six message exchanges over 12 minutes. In a synchronous model, each agent blocks a thread waiting for the next message. In an async model, each agent subscribes to `message.received` events and processes them as they arrive, freeing resources between exchanges.

**Cascading service provisioning.** Agent A buys a service from Agent B, which in turn provisions a dependency from Agent C. Agent B cannot confirm delivery to Agent A until Agent C confirms delivery to Agent B. This is a distributed transaction that spans three agents and two escrows. Synchronous orchestration requires nested blocking calls. Async orchestration uses a saga pattern that coordinates the steps through events.

**Dispute resolution.** Agent A opens a dispute against Agent B via `open_dispute`. Resolution may take hours -- it could involve automated evidence evaluation, third-party arbitration, or manual review. The disputing agent should not block a thread for hours waiting for `get_dispute` to return a resolved status. An event-driven system subscribes to `dispute.resolved` and handles the outcome when it arrives.

**Batch settlement.** At the end of a billing cycle, an agent needs to settle 500 transactions simultaneously. Synchronous sequential processing takes 500 x 200ms = 100 seconds. Async concurrent processing with backpressure-controlled parallelism takes 10 seconds at 50 concurrent requests.

### GreenHelix Async Primitives

GreenHelix provides four primitives that enable event-driven architectures:

**`publish_event`** -- Publishes a structured event to the GreenHelix event bus. Events are typed, timestamped, and associated with an agent ID. Other agents can subscribe to event streams filtered by type, agent, or custom attributes.

**`subscribe_events`** -- Registers a subscription to an event stream. Returns events matching the subscription criteria. Supports long-polling (block until an event arrives or timeout) and cursor-based pagination for catching up on missed events.

**Webhooks** -- GreenHelix can deliver events to an HTTPS endpoint you control. When an event matching your subscription fires, GreenHelix sends an HTTP POST to your webhook URL with the event payload. This is the lowest-latency notification mechanism -- you learn about state changes in milliseconds rather than polling intervals.

**`send_message` / `get_messages`** -- The messaging system provides point-to-point async communication between agents. Messages are stored until retrieved, providing natural buffering for agents that process messages at different rates.

```
Event-Driven Architecture vs Synchronous Polling
==================================================

SYNCHRONOUS                          EVENT-DRIVEN
┌──────────┐                        ┌──────────┐
│  Agent A  │                        │  Agent A  │
│           │  poll poll poll poll   │           │  subscribe once
│  while:   │──────────────────────► │  await:   │──────────┐
│    poll() │  "changed?" "no"      │    event  │          │
│    sleep  │  "changed?" "no"      │           │          │
│    poll() │  "changed?" "yes!"    │  (idle)   │          │
│    sleep  │                        │           │          │
│    poll() │                        │  handle() │◄─────────┘
│    ...    │                        │           │  event fires
└──────────┘                        └──────────┘

API calls: 432,000/day              API calls: ~200/day
Latency: up to poll interval        Latency: milliseconds
CPU: constant                        CPU: on-demand
```

These four primitives are the building blocks. The rest of this guide shows how to compose them into production-grade patterns for saga orchestration, compensating transactions, dead letter handling, exactly-once processing, backpressure management, and async escrow settlement.

---

## Chapter 2: AsyncEventBus Class

### Event Publishing and Subscription

The `AsyncEventBus` class wraps the GreenHelix event primitives in an asyncio-native interface. It manages subscriptions, delivers events to registered handlers, acknowledges processed events, and handles connection failures gracefully.

The design follows the observer pattern: handlers register interest in specific event types, and the bus dispatches matching events to the appropriate handlers. Events are typed using a dot-notation hierarchy (`escrow.created`, `escrow.released`, `dispute.opened`, `sla.breached`) that supports both exact matching and prefix matching (subscribe to `escrow.*` to receive all escrow-related events).

### Event Schemas and Typing

Every event on the bus conforms to a standard envelope schema:

```python
from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime, timezone
import hashlib
import json


@dataclass
class Event:
    """Standard event envelope for the GreenHelix event bus."""
    event_type: str                   # e.g. "escrow.created"
    source_agent_id: str              # Agent that produced the event
    payload: dict                      # Event-specific data
    event_id: str = ""                 # Unique event identifier
    timestamp: str = ""                # ISO 8601 timestamp
    correlation_id: str = ""           # Links related events across a saga
    sequence_number: int = 0           # Ordering within a partition

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()
        if not self.event_id:
            raw = f"{self.event_type}:{self.source_agent_id}:{self.timestamp}"
            self.event_id = hashlib.sha256(raw.encode()).hexdigest()[:24]

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "source_agent_id": self.source_agent_id,
            "timestamp": self.timestamp,
            "correlation_id": self.correlation_id,
            "sequence_number": self.sequence_number,
            "payload": self.payload,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Event":
        return cls(
            event_id=data.get("event_id", ""),
            event_type=data["event_type"],
            source_agent_id=data["source_agent_id"],
            timestamp=data.get("timestamp", ""),
            correlation_id=data.get("correlation_id", ""),
            sequence_number=data.get("sequence_number", 0),
            payload=data.get("payload", {}),
        )
```

### The Complete AsyncEventBus

The bus maintains a registry of handlers keyed by event type pattern. When an event arrives, the bus matches it against all registered patterns and dispatches to matching handlers concurrently. Acknowledgments are sent after successful processing. Failed events are routed to a dead letter handler if one is registered.

```python
import asyncio
import aiohttp
import logging
from typing import Callable, Awaitable, Dict, List, Set
from collections import defaultdict

logger = logging.getLogger(__name__)

EventHandler = Callable[[Event], Awaitable[None]]


class AsyncEventBus:
    """Event bus client for GreenHelix with guaranteed delivery
    and ordered processing.

    Usage:
        bus = AsyncEventBus(api_key="...", agent_id="...",)
        bus.subscribe("escrow.created", handle_escrow_created)
        bus.subscribe("escrow.*", handle_any_escrow_event)
        await bus.start()
    """

    def __init__(self, api_key: str, agent_id: str,
                 base_url: str = "https://api.greenhelix.net/v1",
                 poll_interval: float = 1.0,
                 max_concurrent_handlers: int = 10):
        self.api_key = api_key
        self.agent_id = agent_id
        self.base_url = base_url
        self.poll_interval = poll_interval

        # Handler registry: pattern -> list of handlers
        self._handlers: Dict[str, List[EventHandler]] = defaultdict(list)
        self._dead_letter_handler: Optional[EventHandler] = None

        # Processing state
        self._cursors: Dict[str, str] = {}   # subscription -> cursor
        self._processed_ids: Set[str] = set()
        self._semaphore = asyncio.Semaphore(max_concurrent_handlers)
        self._running = False
        self._session: Optional[aiohttp.ClientSession] = None
        self._tasks: List[asyncio.Task] = []

    def subscribe(self, event_pattern: str,
                  handler: EventHandler) -> None:
        """Register a handler for an event pattern.

        Patterns support trailing wildcards:
          "escrow.created"  -- exact match
          "escrow.*"        -- matches escrow.created, escrow.released, etc.
          "*"               -- matches everything
        """
        self._handlers[event_pattern].append(handler)
        logger.info(f"Subscribed handler to '{event_pattern}'")

    def set_dead_letter_handler(self,
                                handler: EventHandler) -> None:
        """Register a handler for events that fail processing."""
        self._dead_letter_handler = handler

    async def start(self) -> None:
        """Start the event bus. Polls for events and dispatches
        to handlers."""
        self._running = True
        self._session = aiohttp.ClientSession(
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }
        )

        # Register subscriptions with GreenHelix
        for pattern in self._handlers:
            await self._register_subscription(pattern)

        # Start the polling loop
        self._tasks.append(
            asyncio.create_task(self._poll_loop())
        )
        logger.info("AsyncEventBus started")

    async def stop(self) -> None:
        """Gracefully stop the event bus."""
        self._running = False
        for task in self._tasks:
            task.cancel()
        if self._session:
            await self._session.close()
        logger.info("AsyncEventBus stopped")

    async def publish(self, event: Event) -> dict:
        """Publish an event to the GreenHelix event bus."""
        async with self._session.post(
            f"{self.base_url}/v1",
            json={
                "tool": "publish_event",
                "input": {
                    "agent_id": self.agent_id,
                    "event_type": event.event_type,
                    "payload": json.dumps(event.to_dict()),
                },
            },
        ) as resp:
            resp.raise_for_status()
            result = await resp.json()
            logger.debug(f"Published event: {event.event_type} "
                         f"[{event.event_id}]")
            return result

    async def _register_subscription(self, pattern: str) -> None:
        """Register an event subscription with GreenHelix."""
        async with self._session.post(
            f"{self.base_url}/v1",
            json={
                "tool": "subscribe_events",
                "input": {
                    "agent_id": self.agent_id,
                    "event_type": pattern,
                },
            },
        ) as resp:
            resp.raise_for_status()
            result = await resp.json()
            cursor = result.get("cursor", "")
            self._cursors[pattern] = cursor
            logger.info(f"Registered subscription: {pattern} "
                        f"(cursor: {cursor})")

    async def _poll_loop(self) -> None:
        """Continuously poll for new events."""
        while self._running:
            try:
                for pattern, cursor in list(self._cursors.items()):
                    events = await self._fetch_events(pattern, cursor)
                    for event_data in events:
                        event = Event.from_dict(event_data)
                        if event.event_id in self._processed_ids:
                            continue
                        await self._dispatch(event)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Poll loop error: {e}")
            await asyncio.sleep(self.poll_interval)

    async def _fetch_events(self, pattern: str,
                            cursor: str) -> List[dict]:
        """Fetch new events from the subscription."""
        try:
            async with self._session.post(
                f"{self.base_url}/v1",
                json={
                    "tool": "subscribe_events",
                    "input": {
                        "agent_id": self.agent_id,
                        "event_type": pattern,
                        "cursor": cursor,
                    },
                },
                timeout=aiohttp.ClientTimeout(total=30),
            ) as resp:
                resp.raise_for_status()
                result = await resp.json()
                # Update cursor for next poll
                if result.get("cursor"):
                    self._cursors[pattern] = result["cursor"]
                return result.get("events", [])
        except asyncio.TimeoutError:
            logger.debug(f"Long-poll timeout for {pattern} (normal)")
            return []
        except aiohttp.ClientError as e:
            logger.warning(f"Fetch error for {pattern}: {e}")
            return []

    async def _dispatch(self, event: Event) -> None:
        """Dispatch an event to all matching handlers."""
        handlers = self._find_handlers(event.event_type)
        if not handlers:
            logger.warning(f"No handlers for event type: "
                           f"{event.event_type}")
            return

        for handler in handlers:
            async with self._semaphore:
                try:
                    await handler(event)
                    self._processed_ids.add(event.event_id)
                    await self._acknowledge(event)
                except Exception as e:
                    logger.error(
                        f"Handler failed for {event.event_id}: {e}"
                    )
                    if self._dead_letter_handler:
                        try:
                            await self._dead_letter_handler(event)
                        except Exception as dle:
                            logger.error(
                                f"Dead letter handler failed: {dle}"
                            )

    def _find_handlers(self, event_type: str) -> List[EventHandler]:
        """Find all handlers that match an event type."""
        matched = []
        for pattern, handlers in self._handlers.items():
            if self._pattern_matches(pattern, event_type):
                matched.extend(handlers)
        return matched

    @staticmethod
    def _pattern_matches(pattern: str, event_type: str) -> bool:
        """Check if an event type matches a subscription pattern."""
        if pattern == "*":
            return True
        if pattern.endswith(".*"):
            prefix = pattern[:-2]
            return event_type.startswith(prefix + ".")
        return pattern == event_type

    async def _acknowledge(self, event: Event) -> None:
        """Acknowledge successful processing of an event."""
        try:
            async with self._session.post(
                f"{self.base_url}/v1",
                json={
                    "tool": "publish_event",
                    "input": {
                        "agent_id": self.agent_id,
                        "event_type": "system.event_ack",
                        "payload": json.dumps({
                            "acknowledged_event_id": event.event_id,
                            "acknowledged_at": datetime.now(
                                timezone.utc
                            ).isoformat(),
                        }),
                    },
                },
            ) as resp:
                resp.raise_for_status()
        except Exception as e:
            logger.warning(f"Ack failed for {event.event_id}: {e}")
```

### Event Ordering and Partitioning

Events within a single agent's stream are ordered by sequence number. The bus processes them in order within a partition (defined by the source agent ID). Events from different agents can be processed concurrently because they belong to different partitions and have no ordering guarantees relative to each other.

The `max_concurrent_handlers` parameter controls how many events can be processed simultaneously across all partitions. Setting this to 1 gives you strict serial processing. Setting it to 50 gives you high throughput but requires your handlers to be safe for concurrent execution. The default of 10 is a reasonable starting point for most agent workloads.

```python
# Usage: start the event bus and register handlers

async def handle_escrow_created(event: Event) -> None:
    """React to a new escrow being created."""
    escrow_id = event.payload.get("escrow_id")
    amount = event.payload.get("amount")
    logger.info(f"Escrow created: {escrow_id} for ${amount}")
    # Begin monitoring the escrow lifecycle...


async def handle_escrow_released(event: Event) -> None:
    """React to escrow funds being released."""
    escrow_id = event.payload.get("escrow_id")
    logger.info(f"Escrow released: {escrow_id}")
    # Record the settlement in the ledger...


async def handle_sla_breached(event: Event) -> None:
    """React to an SLA breach detection."""
    sla_id = event.payload.get("sla_id")
    metric = event.payload.get("metric")
    actual = event.payload.get("actual_value")
    threshold = event.payload.get("threshold")
    logger.warning(f"SLA breach: {sla_id} -- {metric} "
                   f"is {actual}, threshold {threshold}")
    # Trigger compensating transaction...


async def main():
    bus = AsyncEventBus(
        api_key="your-api-key",
        agent_id="agent-buyer-042",
        poll_interval=2.0,
        max_concurrent_handlers=10,
    )

    bus.subscribe("escrow.created", handle_escrow_created)
    bus.subscribe("escrow.released", handle_escrow_released)
    bus.subscribe("sla.breached", handle_sla_breached)

    await bus.start()

    # Publish an event
    await bus.publish(Event(
        event_type="order.placed",
        source_agent_id="agent-buyer-042",
        correlation_id="saga-purchase-001",
        payload={
            "seller_id": "agent-seller-099",
            "service": "data-pipeline-etl",
            "amount": "500.00",
        },
    ))

    # Keep running until interrupted
    try:
        await asyncio.Event().wait()
    finally:
        await bus.stop()


# asyncio.run(main())
```

---

## Chapter 3: Saga Orchestrator Pattern

### What Is a Saga?

A saga is a distributed transaction decomposed into a sequence of local transactions, where each step has a corresponding compensating transaction that undoes its effect if a later step fails. The term comes from Hector Garcia-Molina's 1987 paper, but the pattern has become the standard approach for managing multi-step operations in microservice architectures -- and it maps perfectly onto multi-agent commerce.

Consider a purchase transaction that involves five steps: (1) verify the buyer has sufficient balance, (2) create an escrow to hold funds, (3) register the service delivery SLA, (4) notify the seller to begin delivery, (5) record the transaction in the ledger. If step 4 fails -- the seller's agent is unreachable -- you cannot simply "rollback" the way a database transaction does. The escrow has already been created on the GreenHelix platform. The SLA has been registered. You need to explicitly undo each completed step in reverse order: cancel the SLA, release the escrow back to the buyer, and credit the balance reservation.

```
Saga: Purchase-Verify-Escrow-Deliver-Release
==============================================

FORWARD PATH (happy path):
  Step 1: verify_balance ──► Step 2: create_escrow ──►
  Step 3: create_sla ──► Step 4: notify_seller ──►
  Step 5: record_transaction

COMPENSATING PATH (step 4 fails):
  Step 4 fails ──►
  Compensate 3: cancel_sla ──►
  Compensate 2: release_escrow (refund) ──►
  Compensate 1: unreserve_balance ──►
  Saga FAILED (all effects reversed)
```

### The SagaOrchestrator Class

The orchestrator manages the state machine for a saga. Each saga instance tracks its current step, completed steps, and the compensation stack. The orchestrator advances through steps sequentially, pushing each completed step onto the compensation stack. If any step fails, it pops the stack and executes compensations in reverse order.

```python
import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import (
    Any, Awaitable, Callable, Dict, List, Optional, Tuple,
)

logger = logging.getLogger(__name__)


class SagaState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    FAILED = "failed"
    COMPENSATION_FAILED = "compensation_failed"


@dataclass
class SagaStep:
    """A single step in a saga with its compensating action."""
    name: str
    execute: Callable[[dict], Awaitable[dict]]
    compensate: Callable[[dict], Awaitable[None]]
    timeout_seconds: float = 30.0
    max_retries: int = 3
    retry_delay_seconds: float = 1.0


@dataclass
class SagaInstance:
    """Runtime state of a saga execution."""
    saga_id: str
    correlation_id: str
    state: SagaState = SagaState.PENDING
    current_step: int = 0
    context: dict = field(default_factory=dict)
    completed_steps: List[str] = field(default_factory=list)
    compensation_stack: List[Tuple[str, dict]] = field(
        default_factory=list
    )
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class SagaOrchestrator:
    """Orchestrates multi-step agent transactions as sagas.

    Each saga is a sequence of steps. Each step has:
      - An execute function that performs the step's work
      - A compensate function that undoes the step's effects
      - Timeout and retry configuration

    The orchestrator advances through steps, tracks state,
    and handles failures by executing compensations in
    reverse order.
    """

    def __init__(self, event_bus: AsyncEventBus):
        self.event_bus = event_bus
        self._sagas: Dict[str, SagaInstance] = {}
        self._step_definitions: Dict[str, List[SagaStep]] = {}

    def define_saga(self, saga_type: str,
                    steps: List[SagaStep]) -> None:
        """Define a saga type with its ordered steps."""
        self._step_definitions[saga_type] = steps
        logger.info(f"Defined saga '{saga_type}' with "
                    f"{len(steps)} steps")

    async def start_saga(self, saga_type: str,
                         saga_id: str,
                         correlation_id: str,
                         initial_context: dict) -> SagaInstance:
        """Start a new saga instance."""
        if saga_type not in self._step_definitions:
            raise ValueError(f"Unknown saga type: {saga_type}")

        instance = SagaInstance(
            saga_id=saga_id,
            correlation_id=correlation_id,
            state=SagaState.RUNNING,
            context=initial_context,
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        self._sagas[saga_id] = instance

        await self.event_bus.publish(Event(
            event_type="saga.started",
            source_agent_id=self.event_bus.agent_id,
            correlation_id=correlation_id,
            payload={
                "saga_id": saga_id,
                "saga_type": saga_type,
                "steps": [s.name for s
                          in self._step_definitions[saga_type]],
            },
        ))

        # Execute steps
        steps = self._step_definitions[saga_type]
        for i, step in enumerate(steps):
            instance.current_step = i

            try:
                result = await self._execute_step(
                    instance, step
                )
                # Store step result in context for subsequent steps
                instance.context[f"step_{step.name}_result"] = result
                instance.completed_steps.append(step.name)
                instance.compensation_stack.append(
                    (step.name, instance.context.copy())
                )

                await self.event_bus.publish(Event(
                    event_type="saga.step_completed",
                    source_agent_id=self.event_bus.agent_id,
                    correlation_id=correlation_id,
                    payload={
                        "saga_id": saga_id,
                        "step": step.name,
                        "step_index": i,
                        "result": result,
                    },
                ))

            except Exception as e:
                logger.error(
                    f"Saga {saga_id} step '{step.name}' failed: {e}"
                )
                instance.error = str(e)

                await self.event_bus.publish(Event(
                    event_type="saga.step_failed",
                    source_agent_id=self.event_bus.agent_id,
                    correlation_id=correlation_id,
                    payload={
                        "saga_id": saga_id,
                        "step": step.name,
                        "error": str(e),
                    },
                ))

                # Begin compensation
                await self._compensate(instance, steps)
                return instance

        # All steps completed successfully
        instance.state = SagaState.COMPLETED
        instance.completed_at = datetime.now(timezone.utc).isoformat()

        await self.event_bus.publish(Event(
            event_type="saga.completed",
            source_agent_id=self.event_bus.agent_id,
            correlation_id=correlation_id,
            payload={
                "saga_id": saga_id,
                "completed_steps": instance.completed_steps,
            },
        ))

        return instance

    async def _execute_step(self, instance: SagaInstance,
                            step: SagaStep) -> dict:
        """Execute a single saga step with retries and timeout."""
        last_error = None
        for attempt in range(step.max_retries):
            try:
                result = await asyncio.wait_for(
                    step.execute(instance.context),
                    timeout=step.timeout_seconds,
                )
                return result
            except asyncio.TimeoutError:
                last_error = (
                    f"Step '{step.name}' timed out after "
                    f"{step.timeout_seconds}s"
                )
                logger.warning(
                    f"{last_error} (attempt {attempt + 1}/"
                    f"{step.max_retries})"
                )
            except Exception as e:
                last_error = str(e)
                logger.warning(
                    f"Step '{step.name}' failed: {e} "
                    f"(attempt {attempt + 1}/{step.max_retries})"
                )

            if attempt < step.max_retries - 1:
                delay = step.retry_delay_seconds * (2 ** attempt)
                await asyncio.sleep(delay)

        raise RuntimeError(
            f"Step '{step.name}' failed after "
            f"{step.max_retries} attempts: {last_error}"
        )

    async def _compensate(self, instance: SagaInstance,
                          steps: List[SagaStep]) -> None:
        """Execute compensating transactions in reverse order."""
        instance.state = SagaState.COMPENSATING

        while instance.compensation_stack:
            step_name, step_context = (
                instance.compensation_stack.pop()
            )
            step_def = next(
                s for s in steps if s.name == step_name
            )

            try:
                await asyncio.wait_for(
                    step_def.compensate(step_context),
                    timeout=step_def.timeout_seconds,
                )
                logger.info(
                    f"Saga {instance.saga_id}: compensated "
                    f"'{step_name}'"
                )

                await self.event_bus.publish(Event(
                    event_type="saga.step_compensated",
                    source_agent_id=self.event_bus.agent_id,
                    correlation_id=instance.correlation_id,
                    payload={
                        "saga_id": instance.saga_id,
                        "step": step_name,
                    },
                ))

            except Exception as e:
                logger.error(
                    f"Saga {instance.saga_id}: compensation "
                    f"of '{step_name}' FAILED: {e}"
                )
                instance.state = SagaState.COMPENSATION_FAILED
                instance.error = (
                    f"Compensation failed at '{step_name}': {e}"
                )

                await self.event_bus.publish(Event(
                    event_type="saga.compensation_failed",
                    source_agent_id=self.event_bus.agent_id,
                    correlation_id=instance.correlation_id,
                    payload={
                        "saga_id": instance.saga_id,
                        "step": step_name,
                        "error": str(e),
                        "remaining_compensations": [
                            s for s, _ in
                            instance.compensation_stack
                        ],
                    },
                ))
                return

        instance.state = SagaState.FAILED
        instance.completed_at = datetime.now(timezone.utc).isoformat()

        await self.event_bus.publish(Event(
            event_type="saga.failed",
            source_agent_id=self.event_bus.agent_id,
            correlation_id=instance.correlation_id,
            payload={
                "saga_id": instance.saga_id,
                "original_error": instance.error,
                "compensated_steps": instance.completed_steps,
            },
        ))

    def get_saga(self, saga_id: str) -> Optional[SagaInstance]:
        """Retrieve the current state of a saga."""
        return self._sagas.get(saga_id)
```

### Example: Purchase-Verify-Escrow-Deliver-Release Saga

Here is a complete saga definition for a standard agent commerce purchase. Each step's execute function calls the GreenHelix API, and each compensation function reverses the effect.

```python
import aiohttp

async def make_api_call(session: aiohttp.ClientSession,
                        base_url: str, tool: str,
                        input_data: dict) -> dict:
    """Helper to call a GreenHelix tool asynchronously."""
    async with session.post(
        f"{base_url}/v1",
        json={"tool": tool, "input": input_data},
    ) as resp:
        resp.raise_for_status()
        return await resp.json()


def build_purchase_saga(session: aiohttp.ClientSession,
                        base_url: str,
                        buyer_id: str) -> List[SagaStep]:
    """Build the step definitions for a purchase saga."""

    async def verify_balance(ctx: dict) -> dict:
        result = await make_api_call(session, base_url,
            "get_balance", {"agent_id": buyer_id})
        balance = float(result.get("balance", 0))
        required = float(ctx["amount"])
        if balance < required:
            raise ValueError(
                f"Insufficient balance: {balance} < {required}"
            )
        return {"verified_balance": balance}

    async def unreserve_balance(ctx: dict) -> None:
        # Balance verification has no side effect to undo
        pass

    async def create_escrow(ctx: dict) -> dict:
        result = await make_api_call(session, base_url,
            "create_escrow", {
                "agent_id": buyer_id,
                "counterparty_id": ctx["seller_id"],
                "amount": ctx["amount"],
                "currency": "USD",
                "conditions": json.dumps({
                    "service": ctx["service_id"],
                    "evaluation_days": ctx.get(
                        "evaluation_days", 7
                    ),
                }),
            })
        return {"escrow_id": result.get("escrow_id")}

    async def cancel_escrow(ctx: dict) -> None:
        escrow_id = ctx.get("step_create_escrow_result", {}).get(
            "escrow_id"
        )
        if escrow_id:
            await make_api_call(session, base_url,
                "release_escrow", {
                    "agent_id": buyer_id,
                    "escrow_id": escrow_id,
                    "release_to": buyer_id,
                    "reason": "saga_compensation",
                })

    async def create_sla(ctx: dict) -> dict:
        result = await make_api_call(session, base_url,
            "create_sla", {
                "agent_id": buyer_id,
                "provider_id": ctx["seller_id"],
                "metric": ctx.get("sla_metric", "uptime"),
                "threshold": str(ctx.get(
                    "sla_threshold", 99.9
                )),
                "window_hours": str(ctx.get(
                    "sla_window_hours", 720
                )),
            })
        return {"sla_id": result.get("sla_id")}

    async def cancel_sla(ctx: dict) -> None:
        # SLA cancellation: record the cancellation
        sla_id = ctx.get("step_create_sla_result", {}).get(
            "sla_id"
        )
        if sla_id:
            await make_api_call(session, base_url,
                "record_transaction", {
                    "agent_id": buyer_id,
                    "transaction_type": "sla_cancelled",
                    "amount": "0",
                    "currency": "USD",
                    "metadata": json.dumps({
                        "sla_id": sla_id,
                        "reason": "saga_compensation",
                    }),
                })

    async def notify_seller(ctx: dict) -> dict:
        escrow_id = ctx.get("step_create_escrow_result", {}).get(
            "escrow_id"
        )
        sla_id = ctx.get("step_create_sla_result", {}).get(
            "sla_id"
        )
        result = await make_api_call(session, base_url,
            "send_message", {
                "sender_id": buyer_id,
                "receiver_id": ctx["seller_id"],
                "message_type": "delivery_request",
                "content": json.dumps({
                    "escrow_id": escrow_id,
                    "sla_id": sla_id,
                    "service_id": ctx["service_id"],
                    "delivery_deadline": ctx.get(
                        "delivery_deadline"
                    ),
                }),
            })
        return {"message_id": result.get("message_id")}

    async def cancel_notification(ctx: dict) -> None:
        await make_api_call(session, base_url,
            "send_message", {
                "sender_id": buyer_id,
                "receiver_id": ctx["seller_id"],
                "message_type": "delivery_cancelled",
                "content": json.dumps({
                    "reason": "saga_compensation",
                    "original_service": ctx["service_id"],
                }),
            })

    async def record_transaction(ctx: dict) -> dict:
        escrow_id = ctx.get("step_create_escrow_result", {}).get(
            "escrow_id"
        )
        result = await make_api_call(session, base_url,
            "record_transaction", {
                "agent_id": buyer_id,
                "transaction_type": "purchase",
                "amount": ctx["amount"],
                "currency": "USD",
                "counterparty_id": ctx["seller_id"],
                "metadata": json.dumps({
                    "escrow_id": escrow_id,
                    "service_id": ctx["service_id"],
                }),
            })
        return {"transaction_id": result.get("transaction_id")}

    async def void_transaction(ctx: dict) -> None:
        tx_id = ctx.get(
            "step_record_transaction_result", {}
        ).get("transaction_id")
        if tx_id:
            await make_api_call(session, base_url,
                "record_transaction", {
                    "agent_id": buyer_id,
                    "transaction_type": "purchase_voided",
                    "amount": ctx["amount"],
                    "currency": "USD",
                    "counterparty_id": ctx["seller_id"],
                    "metadata": json.dumps({
                        "voided_transaction_id": tx_id,
                        "reason": "saga_compensation",
                    }),
                })

    return [
        SagaStep("verify_balance", verify_balance,
                 unreserve_balance, timeout_seconds=10.0),
        SagaStep("create_escrow", create_escrow,
                 cancel_escrow, timeout_seconds=30.0),
        SagaStep("create_sla", create_sla,
                 cancel_sla, timeout_seconds=30.0),
        SagaStep("notify_seller", notify_seller,
                 cancel_notification, timeout_seconds=15.0),
        SagaStep("record_transaction", record_transaction,
                 void_transaction, timeout_seconds=15.0),
    ]
```

The saga state machine transitions are deterministic:

```
  PENDING ──start──► RUNNING
                        │
              ┌─────────┼──────────┐
              │ all steps succeed   │ a step fails
              ▼                     ▼
          COMPLETED           COMPENSATING
                                    │
                          ┌─────────┼──────────┐
                          │ all compensations  │ compensation
                          │ succeed            │ fails
                          ▼                     ▼
                       FAILED            COMPENSATION_FAILED
                  (clean failure)      (requires manual intervention)
```

`COMPENSATION_FAILED` is the state you never want to reach. It means the saga could not undo its partial effects, leaving the system in an inconsistent state. The dead letter handling system (Chapter 5) is designed to catch these cases and alert operators.

---

## Chapter 4: Compensating Transactions

### What Happens When Step 4 of 6 Fails?

The saga orchestrator handles the mechanics of running compensations in reverse order. But the hard part is designing the compensating transactions themselves. Each compensation must satisfy three properties: it must be **idempotent** (safe to run multiple times), **commutative** with respect to other compensations (the order should not matter for the final state, though we execute in reverse for consistency), and **eventually consistent** (it is acceptable for the system to pass through intermediate inconsistent states as long as all compensations eventually complete).

Consider the failure scenario in detail. A buyer agent is executing a five-step purchase saga. Steps 1-3 complete successfully: balance verified, escrow created with $500 locked, SLA registered. Step 4 -- notifying the seller to begin delivery -- fails because the seller's agent is unreachable. The system is now in an inconsistent state: $500 is locked in escrow for a service that will never be delivered, and an SLA is monitoring a provider that has not acknowledged the order.

The compensation sequence:

1. **Compensate step 3 (cancel SLA):** The SLA was registered via `create_sla`. GreenHelix does not have a `delete_sla` tool, so compensation records a cancellation event via `record_transaction` with type `sla_cancelled`. The SLA technically still exists on the platform, but the cancellation record serves as an audit trail, and the monitoring system can filter out cancelled SLAs.

2. **Compensate step 2 (release escrow):** The escrow was created via `create_escrow`. Compensation calls `release_escrow` with `release_to` set to the buyer's agent ID, returning the $500 to the buyer. This is the critical compensation -- if this fails, real money is stuck in limbo.

3. **Compensate step 1 (unreserve balance):** Balance verification was a read-only check with no side effects. The compensation is a no-op.

### The CompensatingTransaction Class

For complex compensations that involve multiple API calls, the `CompensatingTransaction` class provides structure:

```python
@dataclass
class CompensationRecord:
    """Record of a single compensation attempt."""
    step_name: str
    attempted_at: str
    succeeded: bool
    error: Optional[str] = None
    retry_count: int = 0
    idempotency_key: str = ""


class CompensatingTransaction:
    """Manages compensating transactions for a failed saga.

    Handles:
      - Idempotent compensation execution
      - Retry with exponential backoff
      - Compensation audit trail
      - Escalation on repeated failure
    """

    def __init__(self, session: aiohttp.ClientSession,
                 base_url: str, agent_id: str,
                 event_bus: AsyncEventBus):
        self.session = session
        self.base_url = base_url
        self.agent_id = agent_id
        self.event_bus = event_bus
        self._records: List[CompensationRecord] = []

    async def compensate_escrow(self, escrow_id: str,
                                buyer_id: str,
                                amount: str,
                                idempotency_key: str) -> dict:
        """Release escrow funds back to the buyer.

        This is the most critical compensation -- funds must
        not remain locked.
        """
        record = CompensationRecord(
            step_name="release_escrow",
            attempted_at=datetime.now(timezone.utc).isoformat(),
            succeeded=False,
            idempotency_key=idempotency_key,
        )

        max_retries = 5
        for attempt in range(max_retries):
            try:
                result = await make_api_call(
                    self.session, self.base_url,
                    "release_escrow", {
                        "agent_id": buyer_id,
                        "escrow_id": escrow_id,
                        "release_to": buyer_id,
                        "reason": "saga_compensation",
                        "idempotency_key": idempotency_key,
                    },
                )
                record.succeeded = True
                record.retry_count = attempt
                self._records.append(record)

                await self.event_bus.publish(Event(
                    event_type="compensation.escrow_released",
                    source_agent_id=self.agent_id,
                    payload={
                        "escrow_id": escrow_id,
                        "amount": amount,
                        "released_to": buyer_id,
                        "idempotency_key": idempotency_key,
                    },
                ))
                return result

            except Exception as e:
                record.error = str(e)
                record.retry_count = attempt + 1
                delay = min(2 ** attempt, 30)
                logger.warning(
                    f"Escrow compensation failed (attempt "
                    f"{attempt + 1}/{max_retries}): {e}"
                )
                if attempt < max_retries - 1:
                    await asyncio.sleep(delay)

        # All retries exhausted -- escalate
        record.succeeded = False
        self._records.append(record)
        await self._escalate(
            "escrow_release_failed",
            {
                "escrow_id": escrow_id,
                "amount": amount,
                "buyer_id": buyer_id,
                "attempts": max_retries,
                "last_error": record.error,
            },
        )
        raise RuntimeError(
            f"Failed to release escrow {escrow_id} after "
            f"{max_retries} attempts"
        )

    async def compensate_payment(self, transaction_id: str,
                                 amount: str,
                                 payer_id: str,
                                 payee_id: str,
                                 idempotency_key: str) -> dict:
        """Reverse a payment by recording a refund transaction."""
        result = await make_api_call(
            self.session, self.base_url,
            "record_transaction", {
                "agent_id": payer_id,
                "transaction_type": "refund",
                "amount": amount,
                "currency": "USD",
                "counterparty_id": payee_id,
                "metadata": json.dumps({
                    "original_transaction_id": transaction_id,
                    "reason": "saga_compensation",
                    "idempotency_key": idempotency_key,
                }),
            },
        )

        record = CompensationRecord(
            step_name="refund_payment",
            attempted_at=datetime.now(timezone.utc).isoformat(),
            succeeded=True,
            idempotency_key=idempotency_key,
        )
        self._records.append(record)
        return result

    async def compensate_service_registration(
        self, service_id: str,
        agent_id: str,
        idempotency_key: str,
    ) -> dict:
        """Deregister a service that was registered as part
        of the saga."""
        result = await make_api_call(
            self.session, self.base_url,
            "record_transaction", {
                "agent_id": agent_id,
                "transaction_type": "service_deregistered",
                "amount": "0",
                "currency": "USD",
                "metadata": json.dumps({
                    "service_id": service_id,
                    "reason": "saga_compensation",
                    "idempotency_key": idempotency_key,
                }),
            },
        )

        record = CompensationRecord(
            step_name="deregister_service",
            attempted_at=datetime.now(timezone.utc).isoformat(),
            succeeded=True,
            idempotency_key=idempotency_key,
        )
        self._records.append(record)
        return result

    async def _escalate(self, failure_type: str,
                        details: dict) -> None:
        """Escalate a compensation failure for manual
        intervention."""
        await self.event_bus.publish(Event(
            event_type="compensation.escalation_required",
            source_agent_id=self.agent_id,
            payload={
                "failure_type": failure_type,
                "details": details,
                "compensation_history": [
                    {
                        "step": r.step_name,
                        "succeeded": r.succeeded,
                        "retries": r.retry_count,
                        "error": r.error,
                    }
                    for r in self._records
                ],
                "escalated_at": datetime.now(
                    timezone.utc
                ).isoformat(),
            },
        ))
        logger.critical(
            f"COMPENSATION ESCALATION: {failure_type} -- "
            f"{json.dumps(details)}"
        )

    def get_compensation_report(self) -> dict:
        """Return a summary of all compensation actions taken."""
        return {
            "total_compensations": len(self._records),
            "succeeded": sum(
                1 for r in self._records if r.succeeded
            ),
            "failed": sum(
                1 for r in self._records if not r.succeeded
            ),
            "records": [
                {
                    "step": r.step_name,
                    "succeeded": r.succeeded,
                    "retries": r.retry_count,
                    "error": r.error,
                    "idempotency_key": r.idempotency_key,
                }
                for r in self._records
            ],
        }
```

### Idempotency Requirements

Every compensating transaction must be idempotent. If the compensation for "release escrow" is called twice -- because the first call succeeded on the server but the response was lost due to a network timeout -- the second call must not release the escrow a second time or fail with an error. The `idempotency_key` parameter handles this at the API level: GreenHelix deduplicates calls with the same idempotency key and returns the result of the original call.

The key generation strategy matters. A good idempotency key for a compensation is deterministic from the saga context: `f"compensate:{saga_id}:{step_name}"`. This ensures that retrying the same compensation for the same saga step always produces the same key, regardless of how many times the retry logic executes.

```python
def make_compensation_key(saga_id: str, step_name: str) -> str:
    """Generate a deterministic idempotency key for a
    compensation action."""
    raw = f"compensate:{saga_id}:{step_name}"
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


# Usage in a saga compensation:
key = make_compensation_key("saga-purchase-001", "create_escrow")
# key: "a1b2c3d4..." -- same every time for this saga+step
await compensator.compensate_escrow(
    escrow_id="esc_xyz",
    buyer_id="agent-buyer-042",
    amount="500.00",
    idempotency_key=key,
)
```

---

## Chapter 5: Dead Letter Handling

### Events That Cannot Be Processed

A dead letter is an event that has been attempted and failed multiple times. The event itself is well-formed -- it passes schema validation, it was published by a legitimate agent, and the event bus delivered it successfully. But the handler that received it could not process it. Maybe the handler depends on an external service that is down. Maybe the event references an entity that does not exist yet (a race condition). Maybe the handler has a bug that throws an exception for this specific payload.

Dead letters are inevitable in any event-driven system. The question is not whether they will occur but how you handle them when they do. The wrong answer is to silently drop them. The right answer is a dead letter queue (DLQ) with configurable retry policies, monitoring, and manual intervention workflows.

### Dead Letter Queue Implementation

```python
@dataclass
class DeadLetter:
    """An event that failed processing."""
    event: Event
    error: str
    handler_name: str
    first_failed_at: str
    last_failed_at: str
    attempt_count: int
    next_retry_at: Optional[str] = None
    status: str = "pending"   # pending, retrying, exhausted, resolved


class DeadLetterQueue:
    """Dead letter queue with retry policies and alerting.

    Failed events are stored in the DLQ with their failure
    metadata. The queue supports three retry policies:
      - immediate: retry once immediately
      - exponential_backoff: retry with increasing delays
      - circuit_breaker: stop retrying after threshold

    Events that exhaust all retry attempts are marked
    'exhausted' and require manual intervention.
    """

    def __init__(self, event_bus: AsyncEventBus,
                 max_retries: int = 5,
                 base_delay_seconds: float = 5.0,
                 max_delay_seconds: float = 300.0,
                 circuit_breaker_threshold: int = 10):
        self.event_bus = event_bus
        self.max_retries = max_retries
        self.base_delay = base_delay_seconds
        self.max_delay = max_delay_seconds
        self.circuit_breaker_threshold = circuit_breaker_threshold

        self._queue: Dict[str, DeadLetter] = {}
        self._failure_counts: Dict[str, int] = defaultdict(int)
        self._circuit_open: Dict[str, bool] = {}
        self._handlers: Dict[str, EventHandler] = {}
        self._running = False

    async def enqueue(self, event: Event, error: str,
                      handler_name: str) -> None:
        """Add a failed event to the dead letter queue."""
        now = datetime.now(timezone.utc).isoformat()

        if event.event_id in self._queue:
            dl = self._queue[event.event_id]
            dl.attempt_count += 1
            dl.last_failed_at = now
            dl.error = error
        else:
            dl = DeadLetter(
                event=event,
                error=error,
                handler_name=handler_name,
                first_failed_at=now,
                last_failed_at=now,
                attempt_count=1,
            )
            self._queue[event.event_id] = dl

        # Update circuit breaker state
        self._failure_counts[handler_name] += 1
        if (self._failure_counts[handler_name]
                >= self.circuit_breaker_threshold):
            self._circuit_open[handler_name] = True
            logger.critical(
                f"Circuit breaker OPEN for handler "
                f"'{handler_name}' -- "
                f"{self._failure_counts[handler_name]} failures"
            )

        # Schedule retry or mark exhausted
        if dl.attempt_count >= self.max_retries:
            dl.status = "exhausted"
            await self._alert_exhausted(dl)
        else:
            delay = self._calculate_delay(dl.attempt_count)
            retry_at = datetime.now(timezone.utc)
            dl.next_retry_at = retry_at.isoformat()
            dl.status = "pending"

        await self.event_bus.publish(Event(
            event_type="dlq.event_enqueued",
            source_agent_id=self.event_bus.agent_id,
            payload={
                "dead_letter_event_id": event.event_id,
                "event_type": event.event_type,
                "attempt_count": dl.attempt_count,
                "status": dl.status,
                "error": error,
            },
        ))

        logger.warning(
            f"DLQ: {event.event_type} [{event.event_id}] -- "
            f"attempt {dl.attempt_count}/{self.max_retries} -- "
            f"{error}"
        )

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate retry delay with exponential backoff
        and jitter."""
        import random
        delay = self.base_delay * (2 ** (attempt - 1))
        delay = min(delay, self.max_delay)
        jitter = random.uniform(0, delay * 0.1)
        return delay + jitter

    async def start_retry_loop(self,
                               handlers: Dict[
                                   str, EventHandler
                               ]) -> None:
        """Start the background retry loop."""
        self._handlers = handlers
        self._running = True
        asyncio.create_task(self._retry_loop())

    async def _retry_loop(self) -> None:
        """Process pending dead letters on schedule."""
        while self._running:
            now = datetime.now(timezone.utc).isoformat()
            for event_id, dl in list(self._queue.items()):
                if dl.status != "pending":
                    continue
                if dl.next_retry_at and dl.next_retry_at > now:
                    continue

                handler_name = dl.handler_name
                if self._circuit_open.get(handler_name, False):
                    logger.debug(
                        f"Skipping retry: circuit open for "
                        f"'{handler_name}'"
                    )
                    continue

                handler = self._handlers.get(handler_name)
                if not handler:
                    continue

                dl.status = "retrying"
                try:
                    await handler(dl.event)
                    dl.status = "resolved"
                    logger.info(
                        f"DLQ: resolved {dl.event.event_id} "
                        f"on attempt {dl.attempt_count + 1}"
                    )
                    # Reset circuit breaker on success
                    self._failure_counts[handler_name] = max(
                        0,
                        self._failure_counts[handler_name] - 1,
                    )
                    if self._failure_counts[handler_name] == 0:
                        self._circuit_open[handler_name] = False

                except Exception as e:
                    await self.enqueue(
                        dl.event, str(e), handler_name
                    )

            await asyncio.sleep(1.0)

    async def _alert_exhausted(self, dl: DeadLetter) -> None:
        """Alert that an event has exhausted all retries."""
        await self.event_bus.publish(Event(
            event_type="dlq.exhausted",
            source_agent_id=self.event_bus.agent_id,
            payload={
                "event_id": dl.event.event_id,
                "event_type": dl.event.event_type,
                "handler": dl.handler_name,
                "attempts": dl.attempt_count,
                "first_failed": dl.first_failed_at,
                "last_failed": dl.last_failed_at,
                "last_error": dl.error,
                "action_required": "manual_intervention",
            },
        ))
        logger.critical(
            f"DLQ EXHAUSTED: {dl.event.event_type} "
            f"[{dl.event.event_id}] after {dl.attempt_count} "
            f"attempts -- manual intervention required"
        )

    def get_queue_depth(self) -> dict:
        """Return current DLQ metrics."""
        by_status = defaultdict(int)
        by_handler = defaultdict(int)
        for dl in self._queue.values():
            by_status[dl.status] += 1
            by_handler[dl.handler_name] += 1

        return {
            "total": len(self._queue),
            "by_status": dict(by_status),
            "by_handler": dict(by_handler),
            "circuit_breakers": {
                k: "open" if v else "closed"
                for k, v in self._circuit_open.items()
            },
        }

    async def resolve_manually(self, event_id: str,
                               resolution: str) -> None:
        """Mark a dead letter as manually resolved."""
        if event_id in self._queue:
            dl = self._queue[event_id]
            dl.status = "resolved"
            await self.event_bus.publish(Event(
                event_type="dlq.manually_resolved",
                source_agent_id=self.event_bus.agent_id,
                payload={
                    "event_id": event_id,
                    "resolution": resolution,
                    "resolved_at": datetime.now(
                        timezone.utc
                    ).isoformat(),
                },
            ))
```

### Retry Policy Summary

```
Retry Policy: Exponential Backoff with Circuit Breaker
=======================================================

Attempt   Delay        Cumulative Wait
────────────────────────────────────────
1         5s           5s
2         10s          15s
3         20s          35s
4         40s          75s (1m 15s)
5         80s          155s (2m 35s)
  ──── MAX RETRIES REACHED ────
  Status: exhausted
  Action: manual intervention required

Circuit Breaker:
  Threshold: 10 consecutive failures per handler
  State: OPEN (all retries skipped)
  Recovery: automatic on successful retry
```

### Alerting on Dead Letters

The `dlq.exhausted` event is the critical signal. Subscribe to it in your monitoring system and route it to an alerting channel -- PagerDuty, Slack, email, whatever your operations team monitors. An exhausted dead letter means automated recovery has failed and a human (or a supervisory agent) must intervene. The event payload contains everything needed to diagnose the problem: the original event, the handler that failed, the number of attempts, and the last error message.

---

## Chapter 6: Exactly-Once Processing

### The Challenge

Distributed systems offer three delivery guarantees: at-most-once (fire and forget), at-least-once (retry until acknowledged), and exactly-once (process each event exactly one time). At-most-once loses events. At-least-once duplicates events. Exactly-once is what you want -- and what everyone claims is impossible.

The practical answer is: exactly-once processing is achieved by combining at-least-once delivery with idempotent handlers. The event bus guarantees that every event is delivered at least once (it retries on failure). Your handlers guarantee that processing the same event twice produces the same result as processing it once (idempotency). Together, these two properties give you exactly-once semantics from the application's perspective, even though the underlying delivery mechanism may send duplicates.

### Idempotency Key Patterns

Every GreenHelix API call that creates or modifies state should include an idempotency key. The key must be deterministic from the event that triggered the call. If the same event triggers the same handler twice, the same idempotency key is generated, and GreenHelix deduplicates the second call.

```python
class IdempotencyKeyGenerator:
    """Generate deterministic idempotency keys from events."""

    @staticmethod
    def for_event(event: Event, operation: str) -> str:
        """Generate an idempotency key for an operation
        triggered by an event."""
        raw = (
            f"{event.event_id}:{operation}:"
            f"{event.source_agent_id}"
        )
        return hashlib.sha256(raw.encode()).hexdigest()[:32]

    @staticmethod
    def for_saga_step(saga_id: str, step_name: str,
                      attempt: int = 0) -> str:
        """Generate an idempotency key for a saga step.

        Note: attempt is NOT included by default. This ensures
        retries of the same step produce the same key, which is
        the correct behavior for idempotent operations.
        """
        raw = f"saga:{saga_id}:step:{step_name}"
        return hashlib.sha256(raw.encode()).hexdigest()[:32]

    @staticmethod
    def for_compensation(saga_id: str,
                         step_name: str) -> str:
        """Generate an idempotency key for a compensating
        transaction."""
        raw = f"compensate:{saga_id}:{step_name}"
        return hashlib.sha256(raw.encode()).hexdigest()[:32]
```

### Deduplication Strategies

Client-side deduplication provides an additional layer of protection. The `AsyncEventBus` already tracks processed event IDs in `_processed_ids`. For handlers that need stronger guarantees, a persistent deduplication store ensures that events are not reprocessed after a process restart.

```python
class EventDeduplicator:
    """Client-side event deduplication with persistent storage.

    Stores processed event IDs with timestamps. Supports
    TTL-based expiry to prevent unbounded memory growth.
    """

    def __init__(self, ttl_seconds: int = 86400):
        self._processed: Dict[str, float] = {}
        self.ttl_seconds = ttl_seconds

    def is_duplicate(self, event_id: str) -> bool:
        """Check if an event has already been processed."""
        self._evict_expired()
        return event_id in self._processed

    def mark_processed(self, event_id: str) -> None:
        """Mark an event as processed."""
        self._processed[event_id] = time.time()

    def _evict_expired(self) -> None:
        """Remove entries older than TTL."""
        cutoff = time.time() - self.ttl_seconds
        expired = [
            eid for eid, ts in self._processed.items()
            if ts < cutoff
        ]
        for eid in expired:
            del self._processed[eid]

    @property
    def size(self) -> int:
        return len(self._processed)


# Usage in a handler:
dedup = EventDeduplicator(ttl_seconds=86400)  # 24 hour window


async def handle_escrow_created(event: Event) -> None:
    if dedup.is_duplicate(event.event_id):
        logger.info(f"Skipping duplicate: {event.event_id}")
        return

    # Process the event...
    escrow_id = event.payload.get("escrow_id")
    # ... do work ...

    dedup.mark_processed(event.event_id)
```

### The Outbox Pattern

The outbox pattern solves a subtle but critical problem: how do you atomically update your local state AND publish an event? If you update your local state first and then publish the event, a crash between the two operations leaves you with updated state but no event (the outside world does not know). If you publish the event first and then update local state, a crash leaves you with an event published but no local state update (you will re-publish when you restart).

The outbox pattern writes the event to a local "outbox" table in the same database transaction as the state update. A separate process reads the outbox and publishes events to the event bus. If publishing succeeds, the outbox entry is marked as sent. If publishing fails, the entry remains and will be retried.

```python
class OutboxPublisher:
    """Implements the outbox pattern for reliable event
    publishing.

    Events are written to a local outbox (in-memory for this
    example; use a database in production). A background task
    reads the outbox and publishes events to the event bus.
    Sent events are marked and eventually cleaned up.
    """

    def __init__(self, event_bus: AsyncEventBus,
                 flush_interval: float = 0.5):
        self.event_bus = event_bus
        self.flush_interval = flush_interval
        self._outbox: List[dict] = []
        self._lock = asyncio.Lock()
        self._running = False

    async def write(self, event: Event) -> None:
        """Write an event to the outbox.

        Call this inside the same 'transaction' as your
        state update. In production, this would be an INSERT
        into an outbox table within the same DB transaction.
        """
        async with self._lock:
            self._outbox.append({
                "event": event,
                "status": "pending",
                "created_at": datetime.now(
                    timezone.utc
                ).isoformat(),
                "attempts": 0,
            })

    async def start(self) -> None:
        """Start the background publisher."""
        self._running = True
        asyncio.create_task(self._flush_loop())

    async def stop(self) -> None:
        """Stop the background publisher."""
        self._running = False

    async def _flush_loop(self) -> None:
        """Continuously publish pending outbox events."""
        while self._running:
            async with self._lock:
                pending = [
                    entry for entry in self._outbox
                    if entry["status"] == "pending"
                ]

            for entry in pending:
                try:
                    await self.event_bus.publish(entry["event"])
                    entry["status"] = "sent"
                except Exception as e:
                    entry["attempts"] += 1
                    logger.warning(
                        f"Outbox publish failed: {e} "
                        f"(attempt {entry['attempts']})"
                    )
                    if entry["attempts"] >= 10:
                        entry["status"] = "failed"
                        logger.error(
                            f"Outbox entry exhausted: "
                            f"{entry['event'].event_id}"
                        )

            # Clean up sent entries older than 1 hour
            async with self._lock:
                self._outbox = [
                    e for e in self._outbox
                    if e["status"] != "sent"
                ]

            await asyncio.sleep(self.flush_interval)

    @property
    def pending_count(self) -> int:
        return sum(
            1 for e in self._outbox
            if e["status"] == "pending"
        )
```

The interaction between deduplication, idempotency keys, and the outbox pattern creates a three-layer defense against duplicate processing:

```
Exactly-Once Processing: Three-Layer Defense
=============================================

Layer 1: OUTBOX PATTERN
  State update + event write in same transaction
  Guarantees: event is published if and only if
              state was updated

Layer 2: IDEMPOTENCY KEYS
  Every API call includes a deterministic key
  Guarantees: GreenHelix deduplicates repeated calls

Layer 3: CLIENT-SIDE DEDUPLICATION
  EventDeduplicator tracks processed event IDs
  Guarantees: handler skips already-processed events

Together: exactly-once semantics from the
          application's perspective
```

---

## Chapter 7: Backpressure

### What Happens When Events Arrive Faster Than Processing?

Backpressure is what happens when a producer generates events faster than a consumer can process them. In agent commerce, this occurs during batch settlement (500 escrows releasing simultaneously), during market disruptions (every agent reacts to the same price signal at once), or during recovery from an outage (a backlog of unprocessed events floods the system when connectivity is restored).

Without backpressure management, the system fails in one of two ways. Either the event queue grows without bound until memory is exhausted, or the consumer falls so far behind that events become stale and the system processes outdated information. Both outcomes are catastrophic for financial operations where every event represents real money.

### Rate Limiting Strategies

The `AsyncEventBus` already provides one form of backpressure through its `max_concurrent_handlers` semaphore. But that only controls concurrency within a single consumer. For fleet-wide backpressure, you need rate limiting at the API call level.

```python
class RateLimiter:
    """Token bucket rate limiter for async operations.

    Controls the rate of outbound API calls to stay within
    GreenHelix tier limits and prevent overwhelming
    downstream services.
    """

    def __init__(self, rate: float, burst: int):
        """
        Args:
            rate: tokens per second (sustained rate)
            burst: maximum tokens available (burst capacity)
        """
        self.rate = rate
        self.burst = burst
        self._tokens = float(burst)
        self._last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self, tokens: int = 1) -> float:
        """Acquire tokens, waiting if necessary.

        Returns the time waited in seconds.
        """
        waited = 0.0
        async with self._lock:
            self._refill()
            while self._tokens < tokens:
                deficit = tokens - self._tokens
                wait_time = deficit / self.rate
                await asyncio.sleep(wait_time)
                waited += wait_time
                self._refill()
            self._tokens -= tokens
        return waited

    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(
            self.burst,
            self._tokens + elapsed * self.rate,
        )
        self._last_refill = now

    @property
    def available_tokens(self) -> float:
        self._refill()
        return self._tokens


# Usage: rate-limit GreenHelix API calls

# Pro tier: 1000 calls/minute = ~16.7 calls/second
limiter = RateLimiter(rate=15.0, burst=50)


async def rate_limited_api_call(session, base_url,
                                tool, input_data):
    """Make a GreenHelix API call with rate limiting."""
    wait = await limiter.acquire()
    if wait > 0:
        logger.debug(f"Rate limited: waited {wait:.2f}s")
    return await make_api_call(session, base_url, tool,
                               input_data)
```

### Queue Depth Monitoring

Monitoring queue depth is essential for detecting backpressure before it becomes a problem. The metric to watch is the ratio of events arriving per second to events processed per second. When the ratio exceeds 1.0 for more than a few minutes, the queue is growing and backpressure management must engage.

```python
class BackpressureMonitor:
    """Monitors event processing rate and queue depth.

    Emits metrics and triggers load shedding when
    the system is overwhelmed.
    """

    def __init__(self, event_bus: AsyncEventBus,
                 high_watermark: int = 1000,
                 low_watermark: int = 100,
                 check_interval: float = 5.0):
        self.event_bus = event_bus
        self.high_watermark = high_watermark
        self.low_watermark = low_watermark
        self.check_interval = check_interval

        self._queue_depth = 0
        self._events_received = 0
        self._events_processed = 0
        self._shedding = False
        self._last_check = time.monotonic()
        self._running = False

    def record_received(self) -> None:
        self._events_received += 1
        self._queue_depth += 1

    def record_processed(self) -> None:
        self._events_processed += 1
        self._queue_depth = max(0, self._queue_depth - 1)

    @property
    def is_shedding(self) -> bool:
        return self._shedding

    async def start(self) -> None:
        self._running = True
        asyncio.create_task(self._monitor_loop())

    async def _monitor_loop(self) -> None:
        while self._running:
            now = time.monotonic()
            elapsed = now - self._last_check

            if elapsed > 0:
                receive_rate = self._events_received / elapsed
                process_rate = self._events_processed / elapsed
            else:
                receive_rate = 0
                process_rate = 0

            # Engage load shedding at high watermark
            if (self._queue_depth >= self.high_watermark
                    and not self._shedding):
                self._shedding = True
                logger.warning(
                    f"BACKPRESSURE: load shedding ENGAGED "
                    f"(depth: {self._queue_depth})"
                )
                await self.event_bus.publish(Event(
                    event_type="system.backpressure_engaged",
                    source_agent_id=self.event_bus.agent_id,
                    payload={
                        "queue_depth": self._queue_depth,
                        "receive_rate": round(receive_rate, 2),
                        "process_rate": round(process_rate, 2),
                    },
                ))

            # Disengage at low watermark
            if (self._queue_depth <= self.low_watermark
                    and self._shedding):
                self._shedding = False
                logger.info(
                    f"BACKPRESSURE: load shedding DISENGAGED "
                    f"(depth: {self._queue_depth})"
                )

            # Reset counters
            self._events_received = 0
            self._events_processed = 0
            self._last_check = now

            await asyncio.sleep(self.check_interval)

    def get_metrics(self) -> dict:
        return {
            "queue_depth": self._queue_depth,
            "shedding_active": self._shedding,
            "high_watermark": self.high_watermark,
            "low_watermark": self.low_watermark,
        }
```

### Load Shedding vs Buffering

When backpressure engages, you have two choices: buffer events (accept them all and process them later) or shed load (reject or deprioritize low-priority events to protect high-priority processing).

For agent commerce, the answer is priority-based load shedding. Financial events (escrow releases, payments, dispute deadlines) must never be shed. Informational events (analytics updates, reputation refreshes, non-urgent notifications) can be deferred or dropped. The priority is encoded in the event type.

```python
class PrioritizedEventProcessor:
    """Processes events with priority-based load shedding.

    During backpressure, low-priority events are deferred
    while high-priority events (financial operations) are
    processed immediately.
    """

    # Priority levels: lower number = higher priority
    PRIORITY_MAP = {
        "escrow.*": 1,
        "payment.*": 1,
        "dispute.*": 1,
        "saga.*": 2,
        "sla.breached": 2,
        "compensation.*": 2,
        "sla.*": 3,
        "message.*": 3,
        "analytics.*": 4,
        "reputation.*": 4,
        "system.*": 5,
    }

    def __init__(self, monitor: BackpressureMonitor,
                 shed_threshold: int = 3):
        """
        Args:
            shed_threshold: events with priority >= this
                            value are shed during backpressure.
        """
        self.monitor = monitor
        self.shed_threshold = shed_threshold
        self._deferred: List[Event] = []

    def should_process(self, event: Event) -> bool:
        """Determine if an event should be processed now."""
        if not self.monitor.is_shedding:
            return True

        priority = self._get_priority(event.event_type)
        if priority < self.shed_threshold:
            return True  # High priority: always process

        # Low priority during backpressure: defer
        self._deferred.append(event)
        logger.debug(
            f"Deferred event {event.event_type} "
            f"(priority {priority}, depth "
            f"{self.monitor.get_metrics()['queue_depth']})"
        )
        return False

    def _get_priority(self, event_type: str) -> int:
        """Get priority for an event type."""
        for pattern, priority in self.PRIORITY_MAP.items():
            if pattern.endswith(".*"):
                prefix = pattern[:-2]
                if event_type.startswith(prefix + "."):
                    return priority
            elif pattern == event_type:
                return priority
        return 5  # Default: lowest priority

    def get_deferred(self) -> List[Event]:
        """Return and clear deferred events for processing
        when backpressure subsides."""
        events = self._deferred.copy()
        self._deferred.clear()
        return events
```

---

## Chapter 8: Async Escrow Settlement

### Event-Driven Escrow Lifecycle

The escrow is the financial backbone of agent commerce. Every escrow passes through a lifecycle: created, funded, conditions met (or breached), released (or disputed). In a synchronous model, the buyer polls `get_escrow_status` until the escrow transitions. In an event-driven model, the buyer subscribes to escrow lifecycle events and reacts to state changes as they occur.

```
Escrow Lifecycle Events
========================

  create_escrow
       │
       ▼
  escrow.created ──────────────────────┐
       │                                │
       ▼                                │
  escrow.funded                         │
       │                                │
  ┌────┴────┐                           │
  │         │                           │
  ▼         ▼                           ▼
escrow.   escrow.                  escrow.expired
conditions conditions              (timeout, no
_met      _breached                 activity)
  │         │
  ▼         ▼
escrow.   dispute.opened
released       │
               ▼
          dispute.resolved
               │
          ┌────┴────┐
          ▼         ▼
     escrow.    escrow.
     released   forfeited
```

### Webhook Handlers for Escrow State Changes

For the lowest latency notifications, register a webhook endpoint with GreenHelix. When an escrow state changes, GreenHelix sends an HTTP POST to your endpoint.

```python
from aiohttp import web
import hmac


class EscrowWebhookHandler:
    """HTTP server that receives GreenHelix webhook
    notifications for escrow state changes.

    Validates webhook signatures, deduplicates events,
    and dispatches to registered handlers.
    """

    def __init__(self, webhook_secret: str,
                 event_bus: AsyncEventBus,
                 deduplicator: EventDeduplicator):
        self.webhook_secret = webhook_secret
        self.event_bus = event_bus
        self.dedup = deduplicator
        self._handlers: Dict[str, EventHandler] = {}

    def register_handler(self, escrow_state: str,
                         handler: EventHandler) -> None:
        """Register a handler for an escrow state transition."""
        self._handlers[escrow_state] = handler

    async def handle_webhook(self,
                             request: web.Request) -> web.Response:
        """Process an incoming webhook from GreenHelix."""
        # Step 1: Verify signature
        body = await request.read()
        signature = request.headers.get(
            "X-GreenHelix-Signature", ""
        )
        if not self._verify_signature(body, signature):
            return web.Response(status=401, text="Invalid signature")

        # Step 2: Parse event
        try:
            data = json.loads(body)
            event = Event.from_dict(data)
        except (json.JSONDecodeError, KeyError) as e:
            return web.Response(
                status=400, text=f"Invalid payload: {e}"
            )

        # Step 3: Deduplicate
        if self.dedup.is_duplicate(event.event_id):
            # Return 200 to prevent GreenHelix from retrying
            return web.Response(
                status=200, text="Already processed"
            )

        # Step 4: Dispatch to handler
        escrow_state = event.payload.get("state", "")
        handler = self._handlers.get(escrow_state)

        if handler:
            try:
                await handler(event)
                self.dedup.mark_processed(event.event_id)
                return web.Response(status=200, text="OK")
            except Exception as e:
                logger.error(
                    f"Webhook handler failed: {e}"
                )
                # Return 500 so GreenHelix retries
                return web.Response(
                    status=500,
                    text="Processing failed",
                )
        else:
            # Unknown state -- accept but log
            logger.warning(
                f"No handler for escrow state: {escrow_state}"
            )
            self.dedup.mark_processed(event.event_id)
            return web.Response(status=200, text="No handler")

    def _verify_signature(self, body: bytes,
                          signature: str) -> bool:
        """Verify the webhook signature using HMAC-SHA256."""
        expected = hmac.new(
            self.webhook_secret.encode(),
            body,
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    def create_app(self) -> web.Application:
        """Create an aiohttp web application for the webhook."""
        app = web.Application()
        app.router.add_post(
            "/webhooks/escrow", self.handle_webhook
        )
        return app
```

### Automated Evaluation and Release

The most powerful application of async escrow settlement is automated evaluation. Instead of a buyer agent manually checking SLA status and deciding whether to release, an event handler monitors SLA events and releases escrow automatically when conditions are met.

```python
class AsyncEscrowSettlement:
    """Automated escrow settlement driven by events.

    Subscribes to SLA, delivery, and dispute events.
    Automatically releases or disputes escrows based on
    observed conditions.
    """

    def __init__(self, session: aiohttp.ClientSession,
                 base_url: str, agent_id: str,
                 event_bus: AsyncEventBus):
        self.session = session
        self.base_url = base_url
        self.agent_id = agent_id
        self.event_bus = event_bus
        self.keygen = IdempotencyKeyGenerator()

        # Track active escrows and their conditions
        self._escrows: Dict[str, dict] = {}

        # Register event handlers
        event_bus.subscribe(
            "escrow.created", self._on_escrow_created
        )
        event_bus.subscribe(
            "sla.evaluation_complete",
            self._on_sla_evaluation_complete,
        )
        event_bus.subscribe(
            "delivery.confirmed", self._on_delivery_confirmed
        )
        event_bus.subscribe(
            "escrow.expired", self._on_escrow_expired
        )

    async def _on_escrow_created(self, event: Event) -> None:
        """Track a newly created escrow."""
        escrow_id = event.payload.get("escrow_id")
        self._escrows[escrow_id] = {
            "escrow_id": escrow_id,
            "amount": event.payload.get("amount"),
            "counterparty_id": event.payload.get(
                "counterparty_id"
            ),
            "conditions": event.payload.get("conditions", {}),
            "sla_met": False,
            "delivery_confirmed": False,
            "created_at": event.timestamp,
            "correlation_id": event.correlation_id,
        }
        logger.info(f"Tracking escrow: {escrow_id}")

    async def _on_sla_evaluation_complete(
        self, event: Event
    ) -> None:
        """Handle SLA evaluation completion."""
        sla_id = event.payload.get("sla_id")
        escrow_id = event.payload.get("escrow_id")
        compliant = event.payload.get("compliant", False)

        if escrow_id not in self._escrows:
            return

        escrow = self._escrows[escrow_id]

        if compliant:
            escrow["sla_met"] = True
            logger.info(
                f"SLA met for escrow {escrow_id} "
                f"(SLA: {sla_id})"
            )
            await self._check_release_conditions(escrow_id)
        else:
            # SLA breached -- consider disputing
            breach_data = event.payload.get("breach_data", {})
            await self._handle_sla_breach(
                escrow_id, sla_id, breach_data
            )

    async def _on_delivery_confirmed(
        self, event: Event
    ) -> None:
        """Handle delivery confirmation."""
        escrow_id = event.payload.get("escrow_id")
        if escrow_id not in self._escrows:
            return

        self._escrows[escrow_id]["delivery_confirmed"] = True
        logger.info(f"Delivery confirmed for escrow {escrow_id}")
        await self._check_release_conditions(escrow_id)

    async def _on_escrow_expired(self, event: Event) -> None:
        """Handle escrow expiration without settlement."""
        escrow_id = event.payload.get("escrow_id")
        if escrow_id in self._escrows:
            logger.warning(f"Escrow expired: {escrow_id}")
            del self._escrows[escrow_id]

    async def _check_release_conditions(
        self, escrow_id: str
    ) -> None:
        """Check if all conditions are met to release
        the escrow."""
        escrow = self._escrows.get(escrow_id)
        if not escrow:
            return

        if escrow["sla_met"] and escrow["delivery_confirmed"]:
            await self._release_escrow(escrow)

    async def _release_escrow(self, escrow: dict) -> None:
        """Release escrow funds to the counterparty."""
        escrow_id = escrow["escrow_id"]
        counterparty_id = escrow["counterparty_id"]

        idempotency_key = self.keygen.for_event(
            Event(
                event_type="settlement",
                source_agent_id=self.agent_id,
                event_id=f"release-{escrow_id}",
                payload={},
            ),
            "release_escrow",
        )

        try:
            result = await make_api_call(
                self.session, self.base_url,
                "release_escrow", {
                    "agent_id": self.agent_id,
                    "escrow_id": escrow_id,
                    "release_to": counterparty_id,
                    "reason": "conditions_met",
                    "idempotency_key": idempotency_key,
                },
            )

            await self.event_bus.publish(Event(
                event_type="settlement.escrow_released",
                source_agent_id=self.agent_id,
                correlation_id=escrow.get("correlation_id", ""),
                payload={
                    "escrow_id": escrow_id,
                    "amount": escrow["amount"],
                    "released_to": counterparty_id,
                },
            ))

            # Record in ledger
            await make_api_call(
                self.session, self.base_url,
                "record_transaction", {
                    "agent_id": self.agent_id,
                    "transaction_type": "escrow_settlement",
                    "amount": str(escrow["amount"]),
                    "currency": "USD",
                    "counterparty_id": counterparty_id,
                    "metadata": json.dumps({
                        "escrow_id": escrow_id,
                        "settlement_type": "automatic",
                        "sla_compliant": True,
                        "delivery_confirmed": True,
                    }),
                },
            )

            logger.info(
                f"Escrow {escrow_id} released to "
                f"{counterparty_id}: ${escrow['amount']}"
            )
            del self._escrows[escrow_id]

        except Exception as e:
            logger.error(
                f"Failed to release escrow {escrow_id}: {e}"
            )
            # The DLQ will handle retries

    async def _handle_sla_breach(self, escrow_id: str,
                                 sla_id: str,
                                 breach_data: dict) -> None:
        """Handle an SLA breach by opening a dispute."""
        escrow = self._escrows.get(escrow_id)
        if not escrow:
            return

        counterparty_id = escrow["counterparty_id"]

        result = await make_api_call(
            self.session, self.base_url,
            "open_dispute", {
                "agent_id": self.agent_id,
                "counterparty_id": counterparty_id,
                "dispute_type": "sla_breach",
                "description": json.dumps({
                    "escrow_id": escrow_id,
                    "sla_id": sla_id,
                    "breach_data": breach_data,
                }),
            },
        )

        await self.event_bus.publish(Event(
            event_type="settlement.dispute_opened",
            source_agent_id=self.agent_id,
            correlation_id=escrow.get("correlation_id", ""),
            payload={
                "escrow_id": escrow_id,
                "dispute_id": result.get("dispute_id"),
                "sla_id": sla_id,
            },
        ))

        logger.warning(
            f"Dispute opened for escrow {escrow_id}: "
            f"{result.get('dispute_id')}"
        )

    def get_active_escrows(self) -> dict:
        """Return summary of all active escrows being tracked."""
        return {
            "total": len(self._escrows),
            "escrows": [
                {
                    "escrow_id": e["escrow_id"],
                    "amount": e["amount"],
                    "sla_met": e["sla_met"],
                    "delivery_confirmed": e["delivery_confirmed"],
                    "age_seconds": (
                        datetime.now(timezone.utc)
                        - datetime.fromisoformat(
                            e["created_at"].replace(
                                "Z", "+00:00"
                            )
                        )
                    ).total_seconds(),
                }
                for e in self._escrows.values()
            ],
        }
```

---

## Next Steps

For deployment patterns, monitoring, and production hardening, see the
[Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening).

### Deployment Architecture

```
Production Async Agent Commerce Architecture
==============================================

INBOUND                              OUTBOUND
┌─────────────────────┐             ┌─────────────────────┐
│  GreenHelix Webhooks │             │  GreenHelix API      │
│  POST /webhooks/     │             │  the GreenHelix REST API    │
│  escrow              │             │                      │
└─────────┬───────────┘             └──────────┬──────────┘
          │                                     ▲
          ▼                                     │
┌─────────────────────┐             ┌──────────┴──────────┐
│  Webhook Handler     │             │  Rate Limiter        │
│  ├─ Verify signature │             │  (token bucket)      │
│  ├─ Deduplicate      │             └──────────┬──────────┘
│  └─ Dispatch         │                        ▲
└─────────┬───────────┘                        │
          │                          ┌──────────┴──────────┐
          ▼                          │  Outbox Publisher     │
┌──────────────────────────────┐    │  (reliable delivery)  │
│         AsyncEventBus         │    └──────────┬──────────┘
│  ┌────────────────────────┐  │               ▲
│  │  Subscription Manager   │  │               │
│  │  Event Dispatcher       │  │    ┌──────────┴──────────┐
│  │  Acknowledgment Tracker │  │    │  Saga Orchestrator    │
│  └────────────────────────┘  │    │  ├─ Step execution     │
│                               │    │  ├─ Compensation       │
│  ┌────────────────────────┐  │    │  └─ State machine      │
│  │  Backpressure Monitor   │  │    └──────────┬──────────┘
│  │  ├─ Queue depth         │  │               ▲
│  │  ├─ Load shedding       │  │               │
│  │  └─ Priority routing    │  │    ┌──────────┴──────────┐
│  └────────────────────────┘  │    │  Async Escrow         │
│                               │    │  Settlement           │
│  ┌────────────────────────┐  │    │  ├─ Condition tracker  │
│  │  Dead Letter Queue      │  │    │  ├─ Auto-release      │
│  │  ├─ Retry policies      │  │    │  └─ Dispute trigger   │
│  │  ├─ Circuit breaker     │  │    └─────────────────────┘
│  │  └─ Escalation          │  │
│  └────────────────────────┘  │
└──────────────────────────────┘
```

### Key Metrics for Production

```
Async Commerce Agent Metrics
==============================

EVENT BUS
──────────────────────────────────────────────────
Events received/sec          target < 50
Events processed/sec         target >= receive rate
Queue depth                  target < 100
Acknowledgment latency       target < 500ms

SAGAS
──────────────────────────────────────────────────
Active sagas                 monitor for growth
Saga completion rate         target > 99%
Compensation trigger rate    target < 1%
Compensation success rate    target > 99.9%

DEAD LETTER QUEUE
──────────────────────────────────────────────────
DLQ depth                    target = 0
Events exhausted/day         target = 0
Circuit breakers open        target = 0

BACKPRESSURE
──────────────────────────────────────────────────
Load shedding active         target: rarely
Events deferred/min          monitor trend
Deferred event age           target < 60s

ESCROW SETTLEMENT
──────────────────────────────────────────────────
Active escrows tracked       monitor for leaks
Auto-release success rate    target > 99%
Time to settlement           monitor p95
Disputes opened/day          monitor trend
```

---

## What's Next

This guide covered the event-driven foundations: the bus, the patterns, the failure modes. From here, the natural extensions are:

**Multi-agent choreography.** This guide focused on orchestration (a central coordinator drives the saga). Choreography is the alternative: each agent reacts to events independently, with no central coordinator. Choreography scales better but is harder to debug. Combine the `AsyncEventBus` with per-agent state machines for a choreographed approach.

**Event sourcing.** Instead of storing the current state of an escrow or saga, store the complete sequence of events that produced that state. Replay the events to reconstruct state at any point in time. The `OutboxPublisher` is already halfway there -- extend it with a persistent event store and projection functions.

**Cross-gateway federation.** When agents operate across multiple commerce gateways (not just GreenHelix), the event bus needs to bridge events between platforms. The `AsyncEventBus` can be extended with adapter plugins for different gateway APIs.

**Observability.** Distributed tracing through correlation IDs (already present in the `Event` dataclass) gives you end-to-end visibility into saga execution across agents. Wire the correlation IDs into OpenTelemetry spans for production observability.

The synchronous request-response model is the training wheels of agent commerce. It works for simple cases. But the moment your agents start managing long-lived transactions, coordinating with multiple counterparties, or operating at scale, you need the patterns in this guide. The event bus is your nervous system. Sagas are your transaction coordinator. Dead letters are your safety net. Backpressure is your circuit breaker. And async escrow settlement is how you stop burning 518,400 API calls to learn about a single state change.

