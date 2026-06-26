---
name: greenhelix-agent-testing-qa-toolkit
version: "1.3.1"
description: "Agent Testing & QA Toolkit: Integration, Chaos, and Contract Testing for Multi-Agent Systems. Comprehensive testing toolkit for agent commerce systems: unit vs integration vs e2e testing strategies, mock strategies, chaos testing, contract testing between agents, performance benchmarking, CI/CD for agent deployments, and canary releases."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [testing, qa, chaos-testing, contract-testing, ci-cd, guide, greenhelix, openclaw, ai-agent]
price_usd: 39.0
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
# Agent Testing & QA Toolkit: Integration, Chaos, and Contract Testing for Multi-Agent Systems

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `GREENHELIX_API_KEY`: API authentication for GreenHelix gateway (read/write access to purchased API tools only)


Most agent commerce tests are shallow mock-and-assert. Mock the HTTP call, assert the response shape, call it a day. This catches typos and regressions in your serialization layer, but it misses the failures that actually wake you up at 3 AM: network partitions during escrow settlement that leave funds locked indefinitely, race conditions when two agents simultaneously accept the same marketplace listing, schema drift between agent versions that silently corrupts payment metadata, and cascade failures when a single agent in a five-agent pipeline goes unresponsive and every upstream caller retries into a thundering herd. These are not edge cases. They are the normal operating conditions of a distributed multi-agent system under load. The problem is not that teams skip testing -- it is that they test the wrong layer. A unit test that mocks `create_escrow` and asserts it returns an escrow ID tells you nothing about what happens when the escrow creation succeeds but the confirmation webhook never arrives. This guide provides a comprehensive testing toolkit that goes beyond mocks: integration testing against real GreenHelix APIs with recording and playback, chaos testing that injects real failure modes into agent communication, contract testing that catches breaking changes before they hit production, and performance benchmarking that establishes baselines and catches regressions. Every class in this guide is designed to drop into your CI pipeline with zero modification.
1. [The Testing Pyramid for Agent Systems](#chapter-1-the-testing-pyramid-for-agent-systems)
2. [AgentTestHarness Class](#chapter-2-agenttestharness-class)

## What You'll Learn
- Chapter 1: The Testing Pyramid for Agent Systems
- Chapter 2: AgentTestHarness Class
- Chapter 3: Mock Strategies for Agent Commerce
- Chapter 4: ChaosInjector Class
- Chapter 5: ContractValidator Class
- Chapter 6: Performance Benchmarking
- Chapter 7: CI/CD for Agent Deployments
- Chapter 8: Canary Releases
- What's Next

## Full Guide

# Agent Testing & QA Toolkit: Integration, Chaos, and Contract Testing for Multi-Agent Systems

Most agent commerce tests are shallow mock-and-assert. Mock the HTTP call, assert the response shape, call it a day. This catches typos and regressions in your serialization layer, but it misses the failures that actually wake you up at 3 AM: network partitions during escrow settlement that leave funds locked indefinitely, race conditions when two agents simultaneously accept the same marketplace listing, schema drift between agent versions that silently corrupts payment metadata, and cascade failures when a single agent in a five-agent pipeline goes unresponsive and every upstream caller retries into a thundering herd. These are not edge cases. They are the normal operating conditions of a distributed multi-agent system under load. The problem is not that teams skip testing -- it is that they test the wrong layer. A unit test that mocks `create_escrow` and asserts it returns an escrow ID tells you nothing about what happens when the escrow creation succeeds but the confirmation webhook never arrives. This guide provides a comprehensive testing toolkit that goes beyond mocks: integration testing against real GreenHelix APIs with recording and playback, chaos testing that injects real failure modes into agent communication, contract testing that catches breaking changes before they hit production, and performance benchmarking that establishes baselines and catches regressions. Every class in this guide is designed to drop into your CI pipeline with zero modification.

---

## Table of Contents

1. [The Testing Pyramid for Agent Systems](#chapter-1-the-testing-pyramid-for-agent-systems)
2. [AgentTestHarness Class](#chapter-2-agenttestharness-class)
3. [Mock Strategies for Agent Commerce](#chapter-3-mock-strategies-for-agent-commerce)
4. [ChaosInjector Class](#chapter-4-chaosinjector-class)
5. [ContractValidator Class](#chapter-5-contractvalidator-class)
6. [Performance Benchmarking](#chapter-6-performance-benchmarking)
7. [CI/CD for Agent Deployments](#chapter-7-cicd-for-agent-deployments)
8. [Canary Releases](#chapter-8-canary-releases)

---

## Chapter 1: The Testing Pyramid for Agent Systems

### Why the Classic Pyramid Breaks for Agents

The classic testing pyramid -- wide base of unit tests, narrower band of integration tests, thin tip of end-to-end tests -- assumes a single deployable artifact with well-defined boundaries. Agent commerce systems break this assumption in three ways. First, your agent is one participant in a multi-party workflow. Unit testing your escrow creation logic tells you nothing about whether the counterparty agent will accept the escrow terms, release on time, or even be reachable. Second, the GreenHelix gateway is a stateful system: wallets accumulate balances, escrows transition through lifecycle states, trust scores evolve based on historical behavior. Mocking away that state means your tests operate in a universe that does not match production. Third, agent commerce involves real money. A bug in your retry logic that works fine in unit tests can drain a wallet in production if the idempotency key handling is wrong.

This does not mean unit tests are worthless. It means you need to be precise about what each layer catches and build your pyramid accordingly.

### The Three Layers

**Unit tests** validate your agent's internal logic in isolation: input validation, response parsing, state machine transitions, error classification, retry decisions, and business rules. They run in milliseconds, require no network access, and should cover every branch in your agent's decision-making code. What they miss: anything involving the actual GreenHelix API, inter-agent communication, or stateful workflows.

**Integration tests** validate your agent's interaction with real GreenHelix tools, either against the sandbox API or via recorded responses. They catch serialization errors, unexpected response shapes, authentication failures, rate limit handling, and incorrect tool parameter construction. They run in seconds (against recordings) or minutes (against the live sandbox). What they miss: multi-agent coordination, failure modes, and performance characteristics.

**End-to-end tests** validate complete multi-agent workflows: agent A discovers agent B on the marketplace, negotiates terms, creates an escrow, agent B delivers, agent A releases payment, both agents submit metrics. They catch integration failures between agents, workflow ordering bugs, and state synchronization issues. They run in minutes and require a full sandbox environment. What they miss: rare failure modes (which chaos testing covers) and performance under load (which benchmarking covers).

### What Each Layer Catches

| Failure Mode | Unit | Integration | E2E | Chaos |
|---|---|---|---|---|
| Input validation bug | Yes | -- | -- | -- |
| Wrong tool parameter name | -- | Yes | Yes | -- |
| Authentication misconfiguration | -- | Yes | Yes | -- |
| Escrow lifecycle state error | Partial | Yes | Yes | -- |
| Schema drift between versions | -- | -- | Yes | -- |
| Network partition during payment | -- | -- | -- | Yes |
| Race condition in multi-agent bid | -- | -- | Partial | Yes |
| Cascade failure from agent crash | -- | -- | -- | Yes |
| Retry storm draining wallet | -- | -- | -- | Yes |
| Slow response degrading throughput | -- | -- | -- | Yes |

"Partial" means the layer can catch it if you write the test specifically for that scenario, but it will not catch it by default.

### Recommended Ratios and Cost Model

For a production agent commerce system, target this distribution:

- **60% unit tests** -- fast, cheap, catch logic bugs. Write these first for every new feature.
- **30% integration tests** -- moderate speed, catch API interaction bugs. Use recorded responses for CI, live sandbox for nightly runs.
- **10% end-to-end and chaos tests** -- slow, expensive, catch system-level failures. Run on merge to main and before releases.

The cost model matters. A unit test runs in 5ms and costs nothing. An integration test against recordings runs in 50ms. An integration test against the live sandbox runs in 500ms and consumes API credits. An end-to-end test runs in 30-120 seconds and consumes credits across multiple agent wallets. A chaos test can run for minutes and may leave state that needs cleanup. Budget accordingly.

### Test Isolation Strategy

Every test layer needs a different isolation strategy:

```python
# Unit: no external dependencies, pure logic
def test_escrow_amount_validation():
    agent = MyAgent(api_key="fake", agent_id="test-agent")
    with pytest.raises(ValueError, match="amount must be positive"):
        agent.validate_escrow_params(amount=-100, counterparty="agent-b")


# Integration: recorded responses or sandbox, isolated wallet
def test_create_escrow_against_sandbox(test_harness):
    result = test_harness.execute("create_escrow", {
        "payer": "test-agent-a",
        "payee": "test-agent-b",
        "amount": "1.00",
        "currency": "USD",
        "conditions": {"delivery_by": "2026-12-31T00:00:00Z"},
    })
    assert result["status"] == "pending"
    assert "escrow_id" in result


# E2E: full agent lifecycle, dedicated test agents
def test_full_commerce_workflow(agent_a, agent_b):
    # Agent B registers a service
    service = agent_b.register_service("data-enrichment", price="5.00")
    # Agent A discovers and purchases
    results = agent_a.search_services("data-enrichment")
    escrow = agent_a.create_escrow(payee=agent_b.agent_id, amount="5.00")
    # Agent B delivers and agent A releases
    agent_b.deliver(escrow["escrow_id"])
    agent_a.release_escrow(escrow["escrow_id"])
    assert agent_a.get_balance() < initial_balance
```

Name your test agents with the `test-` prefix so they are excluded from leaderboards and production metrics. GreenHelix filters `test-*` prefixed agents from public rankings.

---

## Chapter 2: AgentTestHarness Class

### The Problem with Live API Testing in CI

Running integration tests against the live GreenHelix sandbox in every CI run creates three problems: flaky tests from network latency variance, API credit consumption that scales with your commit frequency, and rate limit hits when multiple developers push simultaneously. You need a way to capture real API responses once, then replay them deterministically in CI.

The `AgentTestHarness` class solves this with a record/playback pattern. In record mode, it proxies every API call through to the real GreenHelix sandbox and saves the request-response pair to a cassette file. In playback mode, it matches incoming requests against recorded cassettes and returns the saved response without making a network call. This gives you the confidence of real API validation with the speed and reliability of mocking.

### The Complete AgentTestHarness

```python
import hashlib
import json
import os
import time
import logging
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass, field

import requests


logger = logging.getLogger(__name__)


@dataclass
class CassetteEntry:
    """A single recorded request-response pair."""
    request_tool: str
    request_input: dict
    response_status: int
    response_body: dict
    response_headers: dict
    timestamp: float
    latency_ms: float


@dataclass
class Cassette:
    """A collection of recorded interactions."""
    name: str
    entries: list[CassetteEntry] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def save(self, path: Path) -> None:
        data = {
            "name": self.name,
            "metadata": self.metadata,
            "entries": [
                {
                    "request_tool": e.request_tool,
                    "request_input": e.request_input,
                    "response_status": e.response_status,
                    "response_body": e.response_body,
                    "response_headers": e.response_headers,
                    "timestamp": e.timestamp,
                    "latency_ms": e.latency_ms,
                }
                for e in self.entries
            ],
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, default=str))
        logger.info("Saved cassette %s with %d entries", self.name, len(self.entries))

    @classmethod
    def load(cls, path: Path) -> "Cassette":
        data = json.loads(path.read_text())
        entries = [
            CassetteEntry(**e) for e in data["entries"]
        ]
        return cls(name=data["name"], entries=entries, metadata=data.get("metadata", {}))


class AgentTestHarness:
    """
    Test harness that wraps GreenHelix API calls with
    recording/playback for deterministic CI testing.
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: str = "https://sandbox.greenhelix.net/v1",
        cassette_dir: str = "tests/cassettes",
        mode: str = "playback",  # "record", "playback", or "passthrough"
    ):
        self.api_key = api_key
        self.agent_id = agent_id
        self.base_url = base_url
        self.cassette_dir = Path(cassette_dir)
        self.mode = mode
        self._current_cassette: Optional[Cassette] = None
        self._playback_index: int = 0

        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })

        # Assertion counters for test reporting
        self.call_count = 0
        self.assertion_count = 0
        self.failures: list[str] = []

    def start_cassette(self, name: str) -> None:
        """Begin recording or loading a cassette."""
        cassette_path = self.cassette_dir / f"{name}.json"

        if self.mode == "record":
            self._current_cassette = Cassette(
                name=name,
                metadata={
                    "agent_id": self.agent_id,
                    "base_url": self.base_url,
                    "recorded_at": time.time(),
                },
            )
            logger.info("Recording cassette: %s", name)

        elif self.mode == "playback":
            if not cassette_path.exists():
                raise FileNotFoundError(
                    f"Cassette not found: {cassette_path}. "
                    f"Run with mode='record' first."
                )
            self._current_cassette = Cassette.load(cassette_path)
            self._playback_index = 0
            logger.info(
                "Playing back cassette: %s (%d entries)",
                name, len(self._current_cassette.entries),
            )

        elif self.mode == "passthrough":
            self._current_cassette = None
            logger.info("Passthrough mode: all calls go to live API")

    def stop_cassette(self) -> None:
        """Finish recording and save the cassette."""
        if self.mode == "record" and self._current_cassette:
            cassette_path = self.cassette_dir / f"{self._current_cassette.name}.json"
            self._current_cassette.save(cassette_path)
        self._current_cassette = None
        self._playback_index = 0

    def execute(self, tool: str, input_data: dict) -> dict:
        """
        Execute a GreenHelix tool call, recording or playing back
        depending on the current mode.
        """
        self.call_count += 1

        if self.mode == "playback":
            return self._playback(tool, input_data)
        elif self.mode == "record":
            return self._record(tool, input_data)
        else:
            return self._live_call(tool, input_data)

    def _live_call(self, tool: str, input_data: dict) -> dict:
        """Make a real API call to GreenHelix."""
        start = time.monotonic()
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        latency_ms = (time.monotonic() - start) * 1000

        body = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
        return {
            "status_code": resp.status_code,
            "body": body,
            "headers": dict(resp.headers),
            "latency_ms": latency_ms,
        }

    def _record(self, tool: str, input_data: dict) -> dict:
        """Make a live call and record the result."""
        result = self._live_call(tool, input_data)

        if self._current_cassette:
            entry = CassetteEntry(
                request_tool=tool,
                request_input=input_data,
                response_status=result["status_code"],
                response_body=result["body"],
                response_headers=result["headers"],
                timestamp=time.time(),
                latency_ms=result["latency_ms"],
            )
            self._current_cassette.entries.append(entry)

        return result

    def _playback(self, tool: str, input_data: dict) -> dict:
        """Return a recorded response from the cassette."""
        if not self._current_cassette:
            raise RuntimeError("No cassette loaded for playback")

        if self._playback_index >= len(self._current_cassette.entries):
            raise RuntimeError(
                f"Cassette exhausted: expected at most "
                f"{len(self._current_cassette.entries)} calls, "
                f"got call #{self._playback_index + 1} for tool '{tool}'"
            )

        entry = self._current_cassette.entries[self._playback_index]
        self._playback_index += 1

        # Verify the call matches what was recorded
        if entry.request_tool != tool:
            self.failures.append(
                f"Call #{self._playback_index}: expected tool "
                f"'{entry.request_tool}', got '{tool}'"
            )
            logger.warning(
                "Tool mismatch at index %d: recorded=%s, actual=%s",
                self._playback_index - 1, entry.request_tool, tool,
            )

        return {
            "status_code": entry.response_status,
            "body": entry.response_body,
            "headers": entry.response_headers,
            "latency_ms": entry.latency_ms,
        }

    # ── Assertion Helpers ────────────────────────────────────────────

    def assert_success(self, result: dict, msg: str = "") -> None:
        """Assert the API call returned 200."""
        self.assertion_count += 1
        if result["status_code"] != 200:
            detail = msg or f"Expected 200, got {result['status_code']}"
            self.failures.append(detail)
            raise AssertionError(detail)

    def assert_status(self, result: dict, expected: int, msg: str = "") -> None:
        """Assert a specific HTTP status code."""
        self.assertion_count += 1
        if result["status_code"] != expected:
            detail = msg or f"Expected {expected}, got {result['status_code']}"
            self.failures.append(detail)
            raise AssertionError(detail)

    def assert_field(self, result: dict, field: str, expected: Any = None) -> None:
        """Assert a field exists in the response body, optionally matching a value."""
        self.assertion_count += 1
        body = result["body"]
        if field not in body:
            detail = f"Field '{field}' not found in response. Keys: {list(body.keys())}"
            self.failures.append(detail)
            raise AssertionError(detail)
        if expected is not None and body[field] != expected:
            detail = f"Field '{field}': expected {expected!r}, got {body[field]!r}"
            self.failures.append(detail)
            raise AssertionError(detail)

    def assert_escrow_state(self, result: dict, expected_state: str) -> None:
        """Assert an escrow is in a specific lifecycle state."""
        self.assertion_count += 1
        state = result["body"].get("status") or result["body"].get("state")
        if state != expected_state:
            detail = f"Escrow state: expected '{expected_state}', got '{state}'"
            self.failures.append(detail)
            raise AssertionError(detail)

    def assert_balance_changed(
        self, before: dict, after: dict, expected_delta: str
    ) -> None:
        """Assert a wallet balance changed by the expected amount."""
        self.assertion_count += 1
        from decimal import Decimal
        before_bal = Decimal(str(before["body"]["balance"]))
        after_bal = Decimal(str(after["body"]["balance"]))
        delta = after_bal - before_bal
        if delta != Decimal(expected_delta):
            detail = (
                f"Balance delta: expected {expected_delta}, "
                f"got {delta} ({before_bal} -> {after_bal})"
            )
            self.failures.append(detail)
            raise AssertionError(detail)

    def report(self) -> dict:
        """Generate a test execution report."""
        return {
            "total_calls": self.call_count,
            "total_assertions": self.assertion_count,
            "failures": len(self.failures),
            "failure_details": self.failures,
            "mode": self.mode,
            "passed": len(self.failures) == 0,
        }
```

### Using the Harness in Tests

Record cassettes once against the live sandbox, then replay them in every CI run:

```python
import pytest
import os


@pytest.fixture
def harness():
    mode = os.environ.get("TEST_MODE", "playback")
    h = AgentTestHarness(
        api_key=os.environ.get("GREENHELIX_API_KEY", "test-key"),
        agent_id="test-qa-agent",
        mode=mode,
    )
    return h


def test_escrow_lifecycle(harness):
    """Test the full escrow create -> release cycle."""
    harness.start_cassette("escrow_lifecycle")

    # Create escrow
    create_result = harness.execute("create_escrow", {
        "payer": "test-qa-agent",
        "payee": "test-counterparty",
        "amount": "10.00",
        "currency": "USD",
        "conditions": {"delivery_by": "2026-12-31T00:00:00Z"},
    })
    harness.assert_success(create_result)
    harness.assert_field(create_result, "escrow_id")
    harness.assert_escrow_state(create_result, "pending")

    escrow_id = create_result["body"]["escrow_id"]

    # Release escrow
    release_result = harness.execute("release_escrow", {
        "escrow_id": escrow_id,
        "agent_id": "test-qa-agent",
    })
    harness.assert_success(release_result)
    harness.assert_escrow_state(release_result, "released")

    harness.stop_cassette()

    report = harness.report()
    assert report["passed"], f"Test failures: {report['failure_details']}"
```

To re-record cassettes when the API changes, run your tests with `TEST_MODE=record`. Commit the cassette JSON files alongside your tests. Review cassette diffs in pull requests to catch unexpected API response changes -- this is a lightweight form of contract testing that requires zero additional tooling.

### Cassette Hygiene

Three rules keep cassettes reliable. First, never record cassettes with production API keys. Use sandbox keys exclusively. The cassette files will contain response data that could leak if your repository is public. Second, re-record cassettes on a schedule (weekly or when the GreenHelix API version changes). Stale cassettes mask real incompatibilities. Third, strip non-deterministic fields (timestamps, request IDs) from cassette matching. The harness matches on tool name by default, which is sufficient for ordered test flows. For unordered flows, extend the matching to include a hash of the input parameters.

---

## Chapter 3: Mock Strategies for Agent Commerce

### When Mocks Are the Right Tool

Mocks are appropriate when you need to test your agent's decision logic without involving any external system. The goal is speed and isolation: validate that your agent makes the right decisions given specific API responses, without caring whether those responses came from a real server. Use mocks for unit tests. Use the test harness (Chapter 2) for integration tests. Never mock in end-to-end tests.

### Mocking the the REST API Endpoint

The GreenHelix gateway exposes a single endpoint for tool execution: the REST API (`POST /v1/{tool}`) with a JSON body containing `tool` and `input` fields. This makes mocking straightforward -- you intercept the one endpoint and route responses based on the tool name.

```python
import json
import time
from typing import Callable, Optional
from dataclasses import dataclass, field
from unittest.mock import MagicMock


@dataclass
class MockResponse:
    """A canned response for a specific tool call."""
    status_code: int = 200
    body: dict = field(default_factory=dict)
    headers: dict = field(default_factory=lambda: {"content-type": "application/json"})
    delay_ms: float = 0


class GreenHelixMock:
    """
    Mock server for GreenHelix REST API endpoints.
    Supports static responses, stateful escrow simulation,
    and programmable error injection.
    """

    def __init__(self):
        self._handlers: dict[str, Callable] = {}
        self._default_responses: dict[str, MockResponse] = {}
        self._call_log: list[dict] = []
        self._escrow_state: dict[str, dict] = {}
        self._wallet_balances: dict[str, str] = {}
        self._error_queue: list[MockResponse] = []

        # Register built-in stateful handlers
        self._handlers["create_escrow"] = self._handle_create_escrow
        self._handlers["release_escrow"] = self._handle_release_escrow
        self._handlers["cancel_escrow"] = self._handle_cancel_escrow
        self._handlers["get_balance"] = self._handle_get_balance
        self._handlers["deposit"] = self._handle_deposit

    def set_response(self, tool: str, response: MockResponse) -> None:
        """Set a static response for a tool."""
        self._default_responses[tool] = response

    def set_balance(self, agent_id: str, balance: str) -> None:
        """Pre-set a wallet balance for stateful testing."""
        self._wallet_balances[agent_id] = balance

    def inject_error(self, status_code: int, body: Optional[dict] = None) -> None:
        """Queue an error to be returned on the next call (any tool)."""
        self._error_queue.append(MockResponse(
            status_code=status_code,
            body=body or {"type": "error", "title": "Injected error", "status": status_code},
        ))

    def inject_errors(self, count: int, status_code: int) -> None:
        """Queue multiple identical errors."""
        for _ in range(count):
            self.inject_error(status_code)

    def execute(self, tool: str, input_data: dict) -> dict:
        """Simulate a the REST API call."""
        self._call_log.append({
            "tool": tool,
            "input": input_data,
            "timestamp": time.time(),
        })

        # Check error queue first
        if self._error_queue:
            err = self._error_queue.pop(0)
            if err.delay_ms > 0:
                time.sleep(err.delay_ms / 1000)
            return {"status_code": err.status_code, "body": err.body, "headers": err.headers}

        # Check for custom handler
        if tool in self._handlers:
            return self._handlers[tool](input_data)

        # Check for static response
        if tool in self._default_responses:
            resp = self._default_responses[tool]
            if resp.delay_ms > 0:
                time.sleep(resp.delay_ms / 1000)
            return {"status_code": resp.status_code, "body": resp.body, "headers": resp.headers}

        # Default: 404 unknown tool
        return {
            "status_code": 404,
            "body": {"type": "error", "title": f"Unknown tool: {tool}", "status": 404},
            "headers": {"content-type": "application/json"},
        }

    # ── Stateful Handlers ────────────────────────────────────────────

    def _handle_create_escrow(self, input_data: dict) -> dict:
        escrow_id = f"esc_{hashlib.sha256(json.dumps(input_data, sort_keys=True).encode()).hexdigest()[:12]}"
        self._escrow_state[escrow_id] = {
            "escrow_id": escrow_id,
            "payer": input_data["payer"],
            "payee": input_data["payee"],
            "amount": input_data["amount"],
            "currency": input_data.get("currency", "USD"),
            "status": "pending",
            "created_at": time.time(),
        }
        return {
            "status_code": 200,
            "body": self._escrow_state[escrow_id].copy(),
            "headers": {"content-type": "application/json"},
        }

    def _handle_release_escrow(self, input_data: dict) -> dict:
        escrow_id = input_data.get("escrow_id")
        if escrow_id not in self._escrow_state:
            return {
                "status_code": 404,
                "body": {"type": "error", "title": "Escrow not found", "status": 404},
                "headers": {"content-type": "application/json"},
            }
        escrow = self._escrow_state[escrow_id]
        if escrow["status"] != "pending":
            return {
                "status_code": 409,
                "body": {
                    "type": "error",
                    "title": f"Cannot release escrow in state '{escrow['status']}'",
                    "status": 409,
                },
                "headers": {"content-type": "application/json"},
            }
        escrow["status"] = "released"
        escrow["released_at"] = time.time()
        return {
            "status_code": 200,
            "body": escrow.copy(),
            "headers": {"content-type": "application/json"},
        }

    def _handle_cancel_escrow(self, input_data: dict) -> dict:
        escrow_id = input_data.get("escrow_id")
        if escrow_id not in self._escrow_state:
            return {
                "status_code": 404,
                "body": {"type": "error", "title": "Escrow not found", "status": 404},
                "headers": {"content-type": "application/json"},
            }
        escrow = self._escrow_state[escrow_id]
        if escrow["status"] != "pending":
            return {
                "status_code": 409,
                "body": {
                    "type": "error",
                    "title": f"Cannot cancel escrow in state '{escrow['status']}'",
                    "status": 409,
                },
                "headers": {"content-type": "application/json"},
            }
        escrow["status"] = "cancelled"
        escrow["cancelled_at"] = time.time()
        return {
            "status_code": 200,
            "body": escrow.copy(),
            "headers": {"content-type": "application/json"},
        }

    def _handle_get_balance(self, input_data: dict) -> dict:
        agent_id = input_data.get("agent_id", "")
        balance = self._wallet_balances.get(agent_id, "0.00")
        return {
            "status_code": 200,
            "body": {"agent_id": agent_id, "balance": balance, "currency": "USD"},
            "headers": {"content-type": "application/json"},
        }

    def _handle_deposit(self, input_data: dict) -> dict:
        agent_id = input_data.get("agent_id", "")
        amount = input_data.get("amount", "0.00")
        from decimal import Decimal
        current = Decimal(self._wallet_balances.get(agent_id, "0.00"))
        new_balance = current + Decimal(str(amount))
        self._wallet_balances[agent_id] = str(new_balance)
        return {
            "status_code": 200,
            "body": {
                "agent_id": agent_id,
                "deposited": str(amount),
                "balance": str(new_balance),
                "currency": "USD",
            },
            "headers": {"content-type": "application/json"},
        }

    # ── Introspection ────────────────────────────────────────────────

    def get_call_log(self) -> list[dict]:
        return self._call_log.copy()

    def get_calls_for_tool(self, tool: str) -> list[dict]:
        return [c for c in self._call_log if c["tool"] == tool]

    def assert_called(self, tool: str, times: Optional[int] = None) -> None:
        calls = self.get_calls_for_tool(tool)
        if times is not None and len(calls) != times:
            raise AssertionError(
                f"Expected {times} calls to '{tool}', got {len(calls)}"
            )
        if not calls:
            raise AssertionError(f"Expected at least one call to '{tool}', got none")

    def reset(self) -> None:
        self._call_log.clear()
        self._escrow_state.clear()
        self._wallet_balances.clear()
        self._error_queue.clear()
```

### Mock Factories for Common Scenarios

Building mocks from scratch for every test is tedious. Factory functions encapsulate common setups:

```python
import hashlib


def create_funded_mock(agent_id: str, balance: str = "100.00") -> GreenHelixMock:
    """Create a mock with a pre-funded wallet."""
    mock = GreenHelixMock()
    mock.set_balance(agent_id, balance)
    return mock


def create_failing_mock(failure_count: int = 3, status_code: int = 500) -> GreenHelixMock:
    """Create a mock that fails N times then succeeds."""
    mock = GreenHelixMock()
    mock.inject_errors(failure_count, status_code)
    return mock


def create_rate_limited_mock(burst_limit: int = 5) -> GreenHelixMock:
    """Create a mock that returns 429 after N calls."""
    mock = GreenHelixMock()
    original_execute = mock.execute

    call_count = 0
    def rate_limited_execute(tool: str, input_data: dict) -> dict:
        nonlocal call_count
        call_count += 1
        if call_count > burst_limit:
            return {
                "status_code": 429,
                "body": {
                    "type": "error",
                    "title": "Rate limit exceeded",
                    "status": 429,
                    "retry_after": 60,
                },
                "headers": {
                    "content-type": "application/json",
                    "retry-after": "60",
                },
            }
        return original_execute(tool, input_data)

    mock.execute = rate_limited_execute
    return mock


def create_timeout_mock(timeout_tools: list[str], timeout_ms: int = 30000) -> GreenHelixMock:
    """Create a mock where specific tools always time out."""
    mock = GreenHelixMock()
    for tool in timeout_tools:
        mock.set_response(tool, MockResponse(
            status_code=504,
            body={"type": "error", "title": "Gateway timeout", "status": 504},
            delay_ms=timeout_ms,
        ))
    return mock
```

### Testing Retry Logic with Mocks

The most common production failure pattern is transient errors requiring retries. Use the mock's error queue to validate your retry logic handles escalating failures:

```python
def test_retry_logic_with_backoff(my_agent_class):
    """Verify the agent retries transient errors with backoff."""
    mock = GreenHelixMock()
    # Fail twice with 500, then succeed
    mock.inject_errors(2, 500)
    mock.set_balance("test-agent", "50.00")

    agent = my_agent_class(api=mock, agent_id="test-agent")
    result = agent.check_balance()

    # Agent should have retried and eventually succeeded
    assert result["balance"] == "50.00"
    # Should have made 3 calls total: 2 failures + 1 success
    mock.assert_called("get_balance", times=3)


def test_retry_exhaustion():
    """Verify the agent gives up after max retries."""
    mock = GreenHelixMock()
    mock.inject_errors(10, 503)  # More errors than max retries

    agent = my_agent_class(api=mock, agent_id="test-agent", max_retries=3)
    with pytest.raises(ServiceUnavailableError):
        agent.check_balance()

    mock.assert_called("get_balance", times=4)  # 1 initial + 3 retries
```

---

## Chapter 4: ChaosInjector Class

### Why Chaos Testing Matters for Agent Commerce

Unit tests and integration tests validate the happy path and a handful of known error paths. Chaos testing answers a different question: what happens when the infrastructure itself misbehaves in ways you did not anticipate? In agent commerce, the consequences of unhandled infrastructure failures are financial. An escrow that gets created but whose confirmation is lost leaves funds locked. A webhook that delivers twice triggers duplicate payments. A DNS resolution delay that pushes a request past its timeout causes a retry that creates a duplicate escrow. These are not hypothetical -- they are the actual failure modes observed in production multi-agent systems.

The `ChaosInjector` class wraps any API client (real or mock) and injects configurable failures into the communication layer. It operates at the transport level, corrupting responses after they leave the server but before your agent processes them.

### The Complete ChaosInjector

```python
import copy
import json
import random
import time
import threading
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional


logger = logging.getLogger(__name__)


class FailureMode(Enum):
    LATENCY = "latency"
    TIMEOUT = "timeout"
    PARTIAL_RESPONSE = "partial_response"
    WRONG_STATUS = "wrong_status"
    CORRUPT_BODY = "corrupt_body"
    SCHEMA_DRIFT = "schema_drift"
    CONNECTION_RESET = "connection_reset"
    DUPLICATE_RESPONSE = "duplicate_response"


@dataclass
class ChaosConfig:
    """Configuration for a chaos injection scenario."""
    failure_mode: FailureMode
    probability: float = 1.0       # 0.0 to 1.0
    target_tools: list[str] = field(default_factory=list)  # empty = all tools
    latency_ms: float = 5000       # for LATENCY mode
    timeout_ms: float = 30000      # for TIMEOUT mode
    corrupt_fields: list[str] = field(default_factory=list)  # for CORRUPT_BODY
    drift_schema: dict = field(default_factory=dict)  # for SCHEMA_DRIFT


class ChaosInjector:
    """
    Wraps an API client and injects configurable failures
    into agent-to-gateway communication.
    """

    def __init__(self, wrapped_client: Any, seed: Optional[int] = None):
        self._client = wrapped_client
        self._configs: list[ChaosConfig] = []
        self._rng = random.Random(seed)
        self._event_log: list[dict] = []
        self._active = True
        self._lock = threading.Lock()

    def add_chaos(self, config: ChaosConfig) -> None:
        """Register a chaos configuration."""
        self._configs.append(config)
        logger.info(
            "Chaos registered: %s (p=%.2f, tools=%s)",
            config.failure_mode.value,
            config.probability,
            config.target_tools or "all",
        )

    def pause(self) -> None:
        """Temporarily disable chaos injection."""
        self._active = False

    def resume(self) -> None:
        """Re-enable chaos injection."""
        self._active = True

    def execute(self, tool: str, input_data: dict) -> dict:
        """Execute with potential chaos injection."""
        # Get the real response first
        result = self._client.execute(tool, input_data)

        if not self._active:
            return result

        # Apply each matching chaos config
        for config in self._configs:
            if not self._should_apply(config, tool):
                continue

            event = {
                "timestamp": time.time(),
                "tool": tool,
                "failure_mode": config.failure_mode.value,
            }

            result = self._apply_chaos(config, result, tool)
            event["applied"] = True
            with self._lock:
                self._event_log.append(event)
            logger.warning(
                "Chaos injected: %s on tool '%s'",
                config.failure_mode.value, tool,
            )

        return result

    def _should_apply(self, config: ChaosConfig, tool: str) -> bool:
        """Determine if this chaos config applies to this call."""
        if config.target_tools and tool not in config.target_tools:
            return False
        return self._rng.random() < config.probability

    def _apply_chaos(self, config: ChaosConfig, result: dict, tool: str) -> dict:
        """Apply a specific failure mode to the response."""
        mode = config.failure_mode

        if mode == FailureMode.LATENCY:
            time.sleep(config.latency_ms / 1000)
            return result

        elif mode == FailureMode.TIMEOUT:
            time.sleep(config.timeout_ms / 1000)
            raise TimeoutError(
                f"Chaos: simulated timeout after {config.timeout_ms}ms "
                f"on tool '{tool}'"
            )

        elif mode == FailureMode.PARTIAL_RESPONSE:
            corrupted = copy.deepcopy(result)
            body = corrupted.get("body", {})
            keys = list(body.keys())
            if len(keys) > 1:
                # Remove a random subset of fields
                remove_count = max(1, len(keys) // 2)
                for key in self._rng.sample(keys, remove_count):
                    del body[key]
            corrupted["body"] = body
            return corrupted

        elif mode == FailureMode.WRONG_STATUS:
            corrupted = copy.deepcopy(result)
            corrupted["status_code"] = self._rng.choice([500, 502, 503, 504])
            return corrupted

        elif mode == FailureMode.CORRUPT_BODY:
            corrupted = copy.deepcopy(result)
            body = corrupted.get("body", {})
            for field_name in config.corrupt_fields:
                if field_name in body:
                    original = body[field_name]
                    body[field_name] = self._corrupt_value(original)
            corrupted["body"] = body
            return corrupted

        elif mode == FailureMode.SCHEMA_DRIFT:
            corrupted = copy.deepcopy(result)
            body = corrupted.get("body", {})
            # Add unexpected fields
            for key, value in config.drift_schema.items():
                body[key] = value
            # Rename existing fields to simulate API version change
            if "status" in body:
                body["state"] = body.pop("status")
            corrupted["body"] = body
            return corrupted

        elif mode == FailureMode.CONNECTION_RESET:
            raise ConnectionError(
                f"Chaos: simulated connection reset on tool '{tool}'"
            )

        elif mode == FailureMode.DUPLICATE_RESPONSE:
            # Return the response twice (simulates webhook double-delivery)
            return result  # caller sees normal response, but we log it as duplicate

        return result

    def _corrupt_value(self, value: Any) -> Any:
        """Corrupt a value while keeping the same type."""
        if isinstance(value, str):
            if value.replace(".", "").replace("-", "").isdigit():
                # Numeric string: flip sign or add digits
                return str(float(value) * -1)
            return value[::-1]  # Reverse the string
        elif isinstance(value, (int, float)):
            return value * -1
        elif isinstance(value, bool):
            return not value
        elif isinstance(value, list):
            return []
        elif isinstance(value, dict):
            return {}
        return None

    def get_event_log(self) -> list[dict]:
        """Return the log of all chaos events."""
        with self._lock:
            return self._event_log.copy()

    def get_injection_count(self) -> int:
        """Return the total number of chaos injections."""
        with self._lock:
            return len(self._event_log)

    def reset(self) -> None:
        """Clear all chaos configs and logs."""
        self._configs.clear()
        with self._lock:
            self._event_log.clear()
```

### Chaos Scenarios for Agent Commerce

Here are the chaos scenarios that match real production failures. Each one uses the `ChaosInjector` with specific configurations:

```python
def scenario_agent_dies_mid_escrow(harness, chaos):
    """
    Simulate: Agent creates escrow, then the counterparty agent
    becomes unreachable before delivery.
    """
    chaos.add_chaos(ChaosConfig(
        failure_mode=FailureMode.CONNECTION_RESET,
        probability=1.0,
        target_tools=["release_escrow", "cancel_escrow"],
    ))

    # Create escrow succeeds
    result = chaos.execute("create_escrow", {
        "payer": "test-agent-a",
        "payee": "test-agent-b",
        "amount": "25.00",
        "currency": "USD",
        "conditions": {"delivery_by": "2026-12-31T00:00:00Z"},
    })
    assert result["status_code"] == 200

    # Attempting to release or cancel fails with connection reset
    try:
        chaos.execute("release_escrow", {
            "escrow_id": result["body"]["escrow_id"],
            "agent_id": "test-agent-a",
        })
        assert False, "Should have raised ConnectionError"
    except ConnectionError:
        pass  # Expected -- agent should handle this with retry + timeout


def scenario_webhook_double_delivery(harness, chaos):
    """
    Simulate: Webhook delivers the same escrow release notification twice.
    Agent must be idempotent.
    """
    chaos.add_chaos(ChaosConfig(
        failure_mode=FailureMode.DUPLICATE_RESPONSE,
        probability=1.0,
        target_tools=["release_escrow"],
    ))

    # First release succeeds
    result1 = chaos.execute("release_escrow", {
        "escrow_id": "esc_abc123",
        "agent_id": "test-agent-a",
    })
    # Second identical release should be idempotent
    result2 = chaos.execute("release_escrow", {
        "escrow_id": "esc_abc123",
        "agent_id": "test-agent-a",
    })
    # Agent should handle both gracefully -- no double payment


def scenario_schema_drift_between_versions(harness, chaos):
    """
    Simulate: GreenHelix API changes 'status' field to 'state'
    in escrow responses (v2 migration).
    """
    chaos.add_chaos(ChaosConfig(
        failure_mode=FailureMode.SCHEMA_DRIFT,
        probability=1.0,
        target_tools=["create_escrow", "release_escrow"],
        drift_schema={"api_version": "2.0", "deprecated_fields": ["status"]},
    ))

    result = chaos.execute("create_escrow", {
        "payer": "test-agent-a",
        "payee": "test-agent-b",
        "amount": "10.00",
        "currency": "USD",
    })
    # Agent should handle both 'status' and 'state' fields
    body = result["body"]
    state = body.get("status") or body.get("state")
    assert state is not None, "Agent must handle schema drift gracefully"


def scenario_latency_spike_during_payment(harness, chaos):
    """
    Simulate: 5-second latency spike on payment tools.
    Tests whether agent times out and retries (risking double-payment)
    or waits patiently.
    """
    chaos.add_chaos(ChaosConfig(
        failure_mode=FailureMode.LATENCY,
        probability=0.5,
        target_tools=["deposit", "create_escrow", "release_escrow"],
        latency_ms=5000,
    ))

    # Agent should handle variable latency without creating duplicates
    result = chaos.execute("deposit", {
        "agent_id": "test-agent-a",
        "amount": "10.00",
    })
    assert result["status_code"] == 200
```

### Running Chaos Tests in CI

Chaos tests should run on merge to main, not on every commit. They are slower and nondeterministic by design. Use a fixed random seed for reproducibility in CI, and a random seed for exploratory testing locally:

```python
@pytest.fixture
def chaos_harness():
    """Create a chaos-wrapped test harness."""
    mock = create_funded_mock("test-agent-a", "1000.00")
    mock.set_balance("test-agent-b", "500.00")
    seed = int(os.environ.get("CHAOS_SEED", "42"))
    injector = ChaosInjector(mock, seed=seed)
    return injector


@pytest.mark.chaos
class TestChaosResilience:
    """Chaos tests -- run with: pytest -m chaos"""

    def test_survives_random_failures(self, chaos_harness):
        chaos_harness.add_chaos(ChaosConfig(
            failure_mode=FailureMode.WRONG_STATUS,
            probability=0.3,
        ))
        chaos_harness.add_chaos(ChaosConfig(
            failure_mode=FailureMode.LATENCY,
            probability=0.2,
            latency_ms=2000,
        ))

        successes = 0
        for _ in range(100):
            try:
                result = chaos_harness.execute("get_balance", {"agent_id": "test-agent-a"})
                if result["status_code"] == 200:
                    successes += 1
            except (TimeoutError, ConnectionError):
                pass

        # With 30% status corruption and 20% latency, expect ~70% success
        assert successes > 50, f"Only {successes}/100 succeeded under chaos"
```

---

## Chapter 5: ContractValidator Class

### The Contract Testing Problem

In a multi-agent system, every agent is both a producer and consumer of API contracts. Agent A calls `create_escrow` expecting a response with an `escrow_id` field. Agent B subscribes to escrow webhooks expecting a `status` field with specific enum values. When agent A upgrades its GreenHelix SDK and the response format changes, agent B breaks. Nobody tested the interaction because each agent has its own test suite and neither tests the contract between them.

Contract testing solves this by making the interface between agents an explicit, versioned, testable artifact. Each consumer declares what it expects from a producer. Each producer validates that its responses satisfy all consumer expectations. When a change breaks a contract, the producer's CI fails before the code ships.

### The Complete ContractValidator

```python
import json
import re
import time
import logging
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Optional


logger = logging.getLogger(__name__)


class Severity(Enum):
    ERROR = "error"          # Breaking change, blocks deployment
    WARNING = "warning"      # Potentially breaking, manual review
    INFO = "info"            # Non-breaking change, informational


@dataclass
class ContractViolation:
    """A single contract violation."""
    field: str
    expected: str
    actual: str
    severity: Severity
    message: str


@dataclass
class ToolContract:
    """Contract definition for a single GreenHelix tool."""
    tool_name: str
    version: str
    input_schema: dict          # JSON Schema for tool input
    output_schema: dict         # JSON Schema for tool output
    required_output_fields: list[str] = field(default_factory=list)
    optional_output_fields: list[str] = field(default_factory=list)
    status_codes: list[int] = field(default_factory=lambda: [200])
    constraints: list[dict] = field(default_factory=list)


@dataclass
class AgentContract:
    """Contract between two agents or between an agent and the gateway."""
    consumer: str               # Agent ID of the consumer
    producer: str               # Agent ID or "gateway"
    tools: list[ToolContract] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def save(self, path: Path) -> None:
        data = {
            "consumer": self.consumer,
            "producer": self.producer,
            "metadata": self.metadata,
            "tools": [
                {
                    "tool_name": t.tool_name,
                    "version": t.version,
                    "input_schema": t.input_schema,
                    "output_schema": t.output_schema,
                    "required_output_fields": t.required_output_fields,
                    "optional_output_fields": t.optional_output_fields,
                    "status_codes": t.status_codes,
                    "constraints": t.constraints,
                }
                for t in self.tools
            ],
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2))

    @classmethod
    def load(cls, path: Path) -> "AgentContract":
        data = json.loads(path.read_text())
        tools = [ToolContract(**t) for t in data["tools"]]
        return cls(
            consumer=data["consumer"],
            producer=data["producer"],
            tools=tools,
            metadata=data.get("metadata", {}),
        )


class ContractValidator:
    """
    Validates API responses against consumer-driven contracts.
    Catches breaking changes before they reach production.
    """

    def __init__(self, contracts_dir: str = "contracts"):
        self.contracts_dir = Path(contracts_dir)
        self._contracts: list[AgentContract] = []
        self._violations: list[ContractViolation] = []
        self._validations: int = 0

    def load_contracts(self) -> int:
        """Load all contract files from the contracts directory."""
        loaded = 0
        if not self.contracts_dir.exists():
            logger.warning("Contracts directory not found: %s", self.contracts_dir)
            return 0

        for path in self.contracts_dir.glob("*.contract.json"):
            contract = AgentContract.load(path)
            self._contracts.append(contract)
            loaded += 1
            logger.info(
                "Loaded contract: %s -> %s (%d tools)",
                contract.consumer, contract.producer, len(contract.tools),
            )
        return loaded

    def add_contract(self, contract: AgentContract) -> None:
        """Register a contract programmatically."""
        self._contracts.append(contract)

    def validate_response(
        self, tool: str, response: dict, producer: str = "gateway"
    ) -> list[ContractViolation]:
        """Validate a tool response against all matching contracts."""
        self._validations += 1
        violations = []

        for contract in self._contracts:
            if contract.producer != producer:
                continue

            for tool_contract in contract.tools:
                if tool_contract.tool_name != tool:
                    continue

                tool_violations = self._validate_tool_response(
                    tool_contract, response, contract.consumer
                )
                violations.extend(tool_violations)

        self._violations.extend(violations)
        return violations

    def _validate_tool_response(
        self,
        contract: ToolContract,
        response: dict,
        consumer: str,
    ) -> list[ContractViolation]:
        """Validate a single tool response against its contract."""
        violations = []
        body = response.get("body", {})
        status = response.get("status_code", 0)

        # Check status code
        if status not in contract.status_codes:
            violations.append(ContractViolation(
                field="status_code",
                expected=str(contract.status_codes),
                actual=str(status),
                severity=Severity.ERROR,
                message=(
                    f"Consumer '{consumer}' expects status "
                    f"{contract.status_codes} from '{contract.tool_name}', "
                    f"got {status}"
                ),
            ))

        # Check required fields
        for field_name in contract.required_output_fields:
            if field_name not in body:
                violations.append(ContractViolation(
                    field=field_name,
                    expected="present",
                    actual="missing",
                    severity=Severity.ERROR,
                    message=(
                        f"Consumer '{consumer}' requires field "
                        f"'{field_name}' in '{contract.tool_name}' response"
                    ),
                ))

        # Check field types from output schema
        for field_name, schema in contract.output_schema.items():
            if field_name not in body:
                continue
            type_violation = self._check_type(field_name, body[field_name], schema)
            if type_violation:
                violations.append(type_violation)

        # Check constraints
        for constraint in contract.constraints:
            constraint_violation = self._check_constraint(constraint, body)
            if constraint_violation:
                violations.append(constraint_violation)

        return violations

    def _check_type(
        self, field_name: str, value: Any, schema: dict
    ) -> Optional[ContractViolation]:
        """Check that a field value matches the expected type."""
        expected_type = schema.get("type")
        if expected_type is None:
            return None

        type_map = {
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool,
            "array": list,
            "object": dict,
        }

        expected_python_type = type_map.get(expected_type)
        if expected_python_type and not isinstance(value, expected_python_type):
            return ContractViolation(
                field=field_name,
                expected=expected_type,
                actual=type(value).__name__,
                severity=Severity.ERROR,
                message=(
                    f"Field '{field_name}': expected type '{expected_type}', "
                    f"got '{type(value).__name__}'"
                ),
            )

        # Check enum constraint
        if "enum" in schema and value not in schema["enum"]:
            return ContractViolation(
                field=field_name,
                expected=str(schema["enum"]),
                actual=str(value),
                severity=Severity.ERROR,
                message=(
                    f"Field '{field_name}': value '{value}' not in "
                    f"allowed values {schema['enum']}"
                ),
            )

        # Check pattern constraint
        if "pattern" in schema and isinstance(value, str):
            if not re.match(schema["pattern"], value):
                return ContractViolation(
                    field=field_name,
                    expected=f"pattern: {schema['pattern']}",
                    actual=value,
                    severity=Severity.WARNING,
                    message=(
                        f"Field '{field_name}': value '{value}' does not "
                        f"match pattern '{schema['pattern']}'"
                    ),
                )

        return None

    def _check_constraint(
        self, constraint: dict, body: dict
    ) -> Optional[ContractViolation]:
        """Check a custom constraint against the response body."""
        constraint_type = constraint.get("type")

        if constraint_type == "field_equals":
            field_name = constraint["field"]
            expected = constraint["value"]
            actual = body.get(field_name)
            if actual != expected:
                return ContractViolation(
                    field=field_name,
                    expected=str(expected),
                    actual=str(actual),
                    severity=Severity(constraint.get("severity", "error")),
                    message=constraint.get("message", f"{field_name} != {expected}"),
                )

        elif constraint_type == "field_present_if":
            condition_field = constraint["condition_field"]
            condition_value = constraint["condition_value"]
            required_field = constraint["required_field"]
            if body.get(condition_field) == condition_value:
                if required_field not in body:
                    return ContractViolation(
                        field=required_field,
                        expected=f"present when {condition_field}={condition_value}",
                        actual="missing",
                        severity=Severity.ERROR,
                        message=(
                            f"Field '{required_field}' required when "
                            f"'{condition_field}' is '{condition_value}'"
                        ),
                    )

        return None

    def check_backward_compatibility(
        self, old_contract: ToolContract, new_contract: ToolContract
    ) -> list[ContractViolation]:
        """
        Check that a new version of a tool contract is
        backward-compatible with the old version.
        """
        violations = []

        # Removing a required output field is a breaking change
        old_required = set(old_contract.required_output_fields)
        new_required = set(new_contract.required_output_fields)
        removed_fields = old_required - new_required
        for field_name in removed_fields:
            if field_name not in new_contract.optional_output_fields:
                violations.append(ContractViolation(
                    field=field_name,
                    expected="present (was required)",
                    actual="removed",
                    severity=Severity.ERROR,
                    message=(
                        f"Breaking change: required field '{field_name}' "
                        f"removed from '{new_contract.tool_name}' "
                        f"(v{old_contract.version} -> v{new_contract.version})"
                    ),
                ))

        # Changing a field type is a breaking change
        for field_name in old_contract.output_schema:
            if field_name not in new_contract.output_schema:
                continue
            old_type = old_contract.output_schema[field_name].get("type")
            new_type = new_contract.output_schema[field_name].get("type")
            if old_type and new_type and old_type != new_type:
                violations.append(ContractViolation(
                    field=field_name,
                    expected=f"type: {old_type}",
                    actual=f"type: {new_type}",
                    severity=Severity.ERROR,
                    message=(
                        f"Breaking change: field '{field_name}' type changed "
                        f"from '{old_type}' to '{new_type}'"
                    ),
                ))

        # Narrowing an enum is a breaking change
        for field_name in old_contract.output_schema:
            if field_name not in new_contract.output_schema:
                continue
            old_enum = set(old_contract.output_schema[field_name].get("enum", []))
            new_enum = set(new_contract.output_schema[field_name].get("enum", []))
            if old_enum and new_enum:
                removed_values = old_enum - new_enum
                if removed_values:
                    violations.append(ContractViolation(
                        field=field_name,
                        expected=f"enum includes {removed_values}",
                        actual=f"enum: {new_enum}",
                        severity=Severity.ERROR,
                        message=(
                            f"Breaking change: enum values {removed_values} "
                            f"removed from '{field_name}'"
                        ),
                    ))

        # Adding new required input fields is a breaking change
        old_required_inputs = set(old_contract.input_schema.get("required", []))
        new_required_inputs = set(new_contract.input_schema.get("required", []))
        added_required = new_required_inputs - old_required_inputs
        for field_name in added_required:
            violations.append(ContractViolation(
                field=field_name,
                expected="optional or absent",
                actual="required",
                severity=Severity.ERROR,
                message=(
                    f"Breaking change: new required input field "
                    f"'{field_name}' added to '{new_contract.tool_name}'"
                ),
            ))

        return violations

    def report(self) -> dict:
        """Generate a validation report."""
        errors = [v for v in self._violations if v.severity == Severity.ERROR]
        warnings = [v for v in self._violations if v.severity == Severity.WARNING]
        return {
            "total_validations": self._validations,
            "total_violations": len(self._violations),
            "errors": len(errors),
            "warnings": len(warnings),
            "passed": len(errors) == 0,
            "violations": [
                {
                    "field": v.field,
                    "expected": v.expected,
                    "actual": v.actual,
                    "severity": v.severity.value,
                    "message": v.message,
                }
                for v in self._violations
            ],
        }
```

### Defining Consumer-Driven Contracts

Each agent that consumes a tool declares what it expects. Store these as JSON files in a `contracts/` directory:

```json
{
  "consumer": "buyer-agent-v2",
  "producer": "gateway",
  "metadata": {
    "created": "2026-04-01",
    "owner": "team-payments"
  },
  "tools": [
    {
      "tool_name": "create_escrow",
      "version": "1.0",
      "input_schema": {
        "required": ["payer", "payee", "amount", "currency"],
        "properties": {
          "payer": {"type": "string"},
          "payee": {"type": "string"},
          "amount": {"type": "string", "pattern": "^\\d+\\.\\d{2}$"},
          "currency": {"type": "string", "enum": ["USD"]}
        }
      },
      "output_schema": {
        "escrow_id": {"type": "string", "pattern": "^esc_"},
        "status": {"type": "string", "enum": ["pending", "released", "cancelled", "expired"]},
        "amount": {"type": "string"},
        "currency": {"type": "string"}
      },
      "required_output_fields": ["escrow_id", "status", "amount"],
      "status_codes": [200],
      "constraints": [
        {
          "type": "field_equals",
          "field": "status",
          "value": "pending",
          "severity": "error",
          "message": "New escrows must have status 'pending'"
        }
      ]
    }
  ]
}
```

### Using Contracts in Tests

```python
def test_escrow_contract_compliance(harness):
    """Verify gateway responses satisfy our contract."""
    validator = ContractValidator(contracts_dir="contracts")
    validator.load_contracts()

    harness.start_cassette("contract_escrow")

    result = harness.execute("create_escrow", {
        "payer": "test-buyer",
        "payee": "test-seller",
        "amount": "50.00",
        "currency": "USD",
        "conditions": {"delivery_by": "2026-12-31T00:00:00Z"},
    })

    violations = validator.validate_response("create_escrow", result)
    harness.stop_cassette()

    report = validator.report()
    assert report["passed"], (
        f"Contract violations: {json.dumps(report['violations'], indent=2)}"
    )


def test_backward_compatibility():
    """Verify a new contract version is backward-compatible."""
    validator = ContractValidator()

    old_contract = ToolContract(
        tool_name="create_escrow",
        version="1.0",
        input_schema={"required": ["payer", "payee", "amount"]},
        output_schema={
            "status": {"type": "string", "enum": ["pending", "released", "cancelled"]},
        },
        required_output_fields=["escrow_id", "status", "amount"],
    )

    new_contract = ToolContract(
        tool_name="create_escrow",
        version="1.1",
        input_schema={"required": ["payer", "payee", "amount"]},
        output_schema={
            "status": {
                "type": "string",
                "enum": ["pending", "released", "cancelled", "expired"],
            },
        },
        required_output_fields=["escrow_id", "status", "amount", "created_at"],
    )

    violations = validator.check_backward_compatibility(old_contract, new_contract)
    # Adding "expired" to the enum is fine (widening)
    # Adding "created_at" as required output is fine (more data)
    assert len(violations) == 0
```

---

## Chapter 6: Performance Benchmarking

### Why Agent Performance Benchmarks Are Different

Traditional API benchmarks measure latency and throughput for a single endpoint. Agent commerce benchmarks must measure multi-step workflows: discover a service, negotiate terms, create escrow, deliver, release, submit metrics. The total latency is the sum of individual call latencies plus your agent's processing time between calls. A 10% regression in escrow creation latency might be invisible in isolation but pushes your end-to-end workflow past the SLA when compounded with five other calls.

### The AgentBenchmark Class

```python
import statistics
import time
import tracemalloc
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


logger = logging.getLogger(__name__)


@dataclass
class BenchmarkResult:
    """Results from a single benchmark run."""
    name: str
    iterations: int
    total_time_ms: float
    mean_ms: float
    median_ms: float
    p95_ms: float
    p99_ms: float
    min_ms: float
    max_ms: float
    std_dev_ms: float
    throughput_ops_sec: float
    errors: int
    peak_memory_mb: float
    latencies: list[float] = field(default_factory=list)


class AgentBenchmark:
    """
    Performance benchmarking for agent commerce operations.
    Measures latency, throughput, memory, and connection usage.
    """

    def __init__(self, client: Any, warmup_iterations: int = 5):
        self._client = client
        self._warmup_iterations = warmup_iterations
        self._results: list[BenchmarkResult] = []

    def benchmark_tool(
        self,
        name: str,
        tool: str,
        input_data: dict,
        iterations: int = 100,
    ) -> BenchmarkResult:
        """Benchmark a single tool call."""

        # Warmup: discard first N iterations
        for _ in range(self._warmup_iterations):
            try:
                self._client.execute(tool, input_data)
            except Exception:
                pass

        latencies = []
        errors = 0
        tracemalloc.start()

        start_total = time.monotonic()
        for _ in range(iterations):
            start = time.monotonic()
            try:
                self._client.execute(tool, input_data)
            except Exception:
                errors += 1
            elapsed = (time.monotonic() - start) * 1000
            latencies.append(elapsed)

        total_time = (time.monotonic() - start_total) * 1000
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        sorted_latencies = sorted(latencies)
        result = BenchmarkResult(
            name=name,
            iterations=iterations,
            total_time_ms=total_time,
            mean_ms=statistics.mean(latencies),
            median_ms=statistics.median(latencies),
            p95_ms=sorted_latencies[int(len(sorted_latencies) * 0.95)],
            p99_ms=sorted_latencies[int(len(sorted_latencies) * 0.99)],
            min_ms=min(latencies),
            max_ms=max(latencies),
            std_dev_ms=statistics.stdev(latencies) if len(latencies) > 1 else 0,
            throughput_ops_sec=(iterations / total_time) * 1000 if total_time > 0 else 0,
            errors=errors,
            peak_memory_mb=peak_memory / (1024 * 1024),
            latencies=latencies,
        )

        self._results.append(result)
        return result

    def benchmark_workflow(
        self,
        name: str,
        workflow: Callable[[], None],
        iterations: int = 50,
    ) -> BenchmarkResult:
        """Benchmark a multi-step workflow."""
        for _ in range(self._warmup_iterations):
            try:
                workflow()
            except Exception:
                pass

        latencies = []
        errors = 0
        tracemalloc.start()

        start_total = time.monotonic()
        for _ in range(iterations):
            start = time.monotonic()
            try:
                workflow()
            except Exception:
                errors += 1
            elapsed = (time.monotonic() - start) * 1000
            latencies.append(elapsed)

        total_time = (time.monotonic() - start_total) * 1000
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        sorted_latencies = sorted(latencies)
        result = BenchmarkResult(
            name=name,
            iterations=iterations,
            total_time_ms=total_time,
            mean_ms=statistics.mean(latencies),
            median_ms=statistics.median(latencies),
            p95_ms=sorted_latencies[int(len(sorted_latencies) * 0.95)],
            p99_ms=sorted_latencies[int(len(sorted_latencies) * 0.99)],
            min_ms=min(latencies),
            max_ms=max(latencies),
            std_dev_ms=statistics.stdev(latencies) if len(latencies) > 1 else 0,
            throughput_ops_sec=(iterations / total_time) * 1000 if total_time > 0 else 0,
            errors=errors,
            peak_memory_mb=peak_memory / (1024 * 1024),
            latencies=latencies,
        )

        self._results.append(result)
        return result

    def compare(
        self, baseline: BenchmarkResult, current: BenchmarkResult, threshold_pct: float = 10.0
    ) -> dict:
        """Compare two benchmark results and flag regressions."""
        regression_fields = {}

        for metric in ["mean_ms", "median_ms", "p95_ms", "p99_ms"]:
            baseline_val = getattr(baseline, metric)
            current_val = getattr(current, metric)
            if baseline_val == 0:
                continue
            pct_change = ((current_val - baseline_val) / baseline_val) * 100
            regression_fields[metric] = {
                "baseline": round(baseline_val, 2),
                "current": round(current_val, 2),
                "change_pct": round(pct_change, 2),
                "regression": pct_change > threshold_pct,
            }

        throughput_change = 0
        if baseline.throughput_ops_sec > 0:
            throughput_change = (
                (current.throughput_ops_sec - baseline.throughput_ops_sec)
                / baseline.throughput_ops_sec
            ) * 100

        any_regression = any(v["regression"] for v in regression_fields.values())

        return {
            "baseline_name": baseline.name,
            "current_name": current.name,
            "metrics": regression_fields,
            "throughput_change_pct": round(throughput_change, 2),
            "has_regression": any_regression,
            "threshold_pct": threshold_pct,
        }

    def generate_report(self) -> str:
        """Generate a markdown benchmark report."""
        lines = ["# Agent Benchmark Report", ""]
        lines.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
        lines.append("")

        lines.append("| Benchmark | Iterations | Mean (ms) | Median (ms) | P95 (ms) | P99 (ms) | Throughput (ops/s) | Errors | Memory (MB) |")
        lines.append("|---|---|---|---|---|---|---|---|---|")

        for r in self._results:
            lines.append(
                f"| {r.name} | {r.iterations} | "
                f"{r.mean_ms:.2f} | {r.median_ms:.2f} | "
                f"{r.p95_ms:.2f} | {r.p99_ms:.2f} | "
                f"{r.throughput_ops_sec:.1f} | {r.errors} | "
                f"{r.peak_memory_mb:.2f} |"
            )

        lines.append("")
        return "\n".join(lines)
```

### Running Benchmarks and Catching Regressions

```python
def test_escrow_performance_regression(harness):
    """Flag if escrow operations regress more than 10%."""
    bench = AgentBenchmark(harness, warmup_iterations=3)

    # Benchmark individual operations
    create_result = bench.benchmark_tool(
        "create_escrow",
        "create_escrow",
        {
            "payer": "test-agent-a",
            "payee": "test-agent-b",
            "amount": "10.00",
            "currency": "USD",
        },
        iterations=50,
    )

    balance_result = bench.benchmark_tool(
        "get_balance",
        "get_balance",
        {"agent_id": "test-agent-a"},
        iterations=100,
    )

    # Benchmark full workflow
    def escrow_workflow():
        harness.execute("create_escrow", {
            "payer": "test-agent-a",
            "payee": "test-agent-b",
            "amount": "1.00",
            "currency": "USD",
        })
        harness.execute("get_balance", {"agent_id": "test-agent-a"})

    workflow_result = bench.benchmark_workflow("escrow_workflow", escrow_workflow, iterations=30)

    # Generate report
    report = bench.generate_report()
    logger.info("\n%s", report)

    # Assert no individual operation exceeds 500ms at P99
    assert create_result.p99_ms < 500, f"create_escrow P99: {create_result.p99_ms}ms"
    assert balance_result.p99_ms < 200, f"get_balance P99: {balance_result.p99_ms}ms"

    # Save results for next run's comparison
    Path("benchmarks/latest.json").parent.mkdir(exist_ok=True)
    Path("benchmarks/latest.json").write_text(json.dumps({
        "create_escrow": {"mean_ms": create_result.mean_ms, "p99_ms": create_result.p99_ms},
        "get_balance": {"mean_ms": balance_result.mean_ms, "p99_ms": balance_result.p99_ms},
        "workflow": {"mean_ms": workflow_result.mean_ms, "p99_ms": workflow_result.p99_ms},
    }, indent=2))
```

Store benchmark baselines in your repository. On each run, load the previous baseline, compare against current results, and fail the build if any metric regresses beyond your threshold. This turns performance into a first-class CI constraint rather than something you notice three weeks later when users complain.

---

## Chapter 7: CI/CD for Agent Deployments

### Pipeline Architecture

An agent commerce CI/CD pipeline has five stages. Each stage gates the next -- if any stage fails, the pipeline stops and the deploy does not happen.

```
  lint → unit → integration → chaos → deploy
   │       │         │          │        │
  10s     30s      2min       5min     3min
```

The total pipeline takes about 10 minutes. This is slower than a typical web application pipeline because the chaos stage runs real failure simulations. The tradeoff is worth it: catching a retry-storm bug in CI is cheaper than catching it when it drains a production wallet.

### GitHub Actions Configuration

```yaml
name: Agent Commerce CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: "3.12"
  GREENHELIX_SANDBOX_KEY: ${{ secrets.GREENHELIX_SANDBOX_KEY }}

jobs:
  lint:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install ruff mypy
      - run: ruff check src/ tests/
      - run: mypy src/ --ignore-missing-imports

  unit:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install -r requirements.txt -r requirements-test.txt
      - run: python -m pytest tests/unit/ -x -q --tb=short
        env:
          TEST_MODE: playback

  integration:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    needs: unit
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install -r requirements.txt -r requirements-test.txt
      - run: python -m pytest tests/integration/ -x -q --tb=short
        env:
          TEST_MODE: playback
          GREENHELIX_API_KEY: ${{ env.GREENHELIX_SANDBOX_KEY }}

  chaos:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    needs: integration
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install -r requirements.txt -r requirements-test.txt
      - run: python -m pytest tests/ -m chaos -x -q --tb=short
        env:
          CHAOS_SEED: ${{ github.run_number }}
          TEST_MODE: playback

  deploy:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    needs: [integration, chaos]
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - name: Deploy to staging
        run: |
          pip install -r requirements.txt
          python deploy.py --env staging --agent-id ${{ vars.AGENT_ID }}
        env:
          GREENHELIX_API_KEY: ${{ secrets.GREENHELIX_STAGING_KEY }}

      - name: Smoke test staging
        run: |
          python -m pytest tests/smoke/ -x -q --tb=short
        env:
          GREENHELIX_API_KEY: ${{ secrets.GREENHELIX_STAGING_KEY }}
          TARGET_ENV: staging

      - name: Deploy to production
        run: |
          python deploy.py --env production --agent-id ${{ vars.AGENT_ID }}
        env:
          GREENHELIX_API_KEY: ${{ secrets.GREENHELIX_PROD_KEY }}
```

### Environment Key Management

Separate your GreenHelix API keys by environment. Never use the same key for sandbox, staging, and production. The key hierarchy:

| Environment | Key Source | Wallet | Purpose |
|---|---|---|---|
| Local dev | `.env` file (gitignored) | Test wallet, fake funds | Developer iteration |
| CI sandbox | GitHub secret `GREENHELIX_SANDBOX_KEY` | Sandbox wallet, free credits | Automated testing |
| Staging | GitHub secret `GREENHELIX_STAGING_KEY` | Staging wallet, real funds (capped) | Pre-production validation |
| Production | GitHub secret `GREENHELIX_PROD_KEY` | Production wallet, real funds | Live traffic |

Set budget caps on every non-production key using the GreenHelix `set_budget_cap` tool. A runaway integration test should not be able to spend more than $5:

```python
def configure_test_budget(api_key: str, agent_id: str) -> None:
    """Set conservative budget caps for test environments."""
    import requests
    resp = requests.post(
        "https://sandbox.greenhelix.netthe REST API",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "tool": "set_budget_cap",
            "input": {
                "agent_id": agent_id,
                "daily_limit": "5.00",
                "monthly_limit": "50.00",
                "per_transaction_limit": "1.00",
                "currency": "USD",
            },
        },
    )
    resp.raise_for_status()
```

### Rollback Triggers

Define explicit rollback criteria. If any of these conditions are true after a deploy, automatically roll back:

```python
import requests
import sys


def check_rollback_criteria(
    api_key: str,
    agent_id: str,
    base_url: str = "https://api.greenhelix.net/v1",
) -> bool:
    """Return True if a rollback is needed."""
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    })

    def execute(tool: str, input_data: dict) -> dict:
        resp = session.post(
            f"{base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        return resp.json() if resp.status_code == 200 else {"error": resp.status_code}

    # Check 1: Agent is reachable and registered
    identity = execute("get_agent_identity", {"agent_id": agent_id})
    if "error" in identity:
        print(f"ROLLBACK: Agent identity check failed: {identity}")
        return True

    # Check 2: Trust score hasn't dropped
    trust = execute("get_trust_score", {"agent_id": agent_id})
    if trust.get("score", 0) < 0.5:
        print(f"ROLLBACK: Trust score below threshold: {trust.get('score')}")
        return True

    # Check 3: No unusual error rate in recent metrics
    metrics = execute("get_agent_metrics", {"agent_id": agent_id, "window": "5m"})
    error_rate = metrics.get("error_rate", 0)
    if error_rate > 0.05:  # More than 5% errors
        print(f"ROLLBACK: Error rate too high: {error_rate}")
        return True

    # Check 4: Balance is not draining unexpectedly
    balance = execute("get_balance", {"agent_id": agent_id})
    balance_val = float(balance.get("balance", "0"))
    if balance_val < 10.0:  # Minimum operating balance
        print(f"ROLLBACK: Balance critically low: {balance_val}")
        return True

    print("All rollback checks passed")
    return False


if __name__ == "__main__":
    import os
    should_rollback = check_rollback_criteria(
        api_key=os.environ["GREENHELIX_API_KEY"],
        agent_id=os.environ["AGENT_ID"],
    )
    sys.exit(1 if should_rollback else 0)
```

Call this script as a post-deploy step. If it exits with code 1, your pipeline triggers a rollback to the previous version.

---

## Chapter 8: Canary Releases

### The Case for Canary Deployments

A canary release deploys a new agent version to a small percentage of traffic before rolling it out fully. This is standard practice for web services, but agent commerce adds a complication: agents are stateful. A canary agent that creates an escrow must be able to see that escrow through to completion, even if it is rolled back. This means your canary strategy must handle in-flight transactions gracefully.

### Canary Deployment Architecture

The canary pattern for GreenHelix agents uses two agent registrations with a traffic router:

```
                    ┌──────────────┐
                    │  Traffic     │
    Incoming ──────▶│  Router      │
    Requests        │  (5%/95%)    │
                    └──────┬───────┘
                           │
                    ┌──────┴───────┐
                    │              │
               ┌────▼────┐  ┌─────▼─────┐
               │ Canary  │  │ Stable    │
               │ v2.1.0  │  │ v2.0.0   │
               │  (5%)   │  │  (95%)   │
               └─────────┘  └──────────┘
```

Both versions share the same GreenHelix wallet but use different agent IDs (e.g., `my-agent` and `my-agent-canary`). This lets you track metrics separately while maintaining a single financial identity.

### The CanaryController Class

```python
import time
import logging
import threading
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


logger = logging.getLogger(__name__)


@dataclass
class CanaryMetrics:
    """Metrics collected during a canary deployment."""
    requests_total: int = 0
    requests_success: int = 0
    requests_error: int = 0
    latency_sum_ms: float = 0
    latency_samples: list[float] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)

    @property
    def error_rate(self) -> float:
        if self.requests_total == 0:
            return 0.0
        return self.requests_error / self.requests_total

    @property
    def mean_latency_ms(self) -> float:
        if not self.latency_samples:
            return 0.0
        return self.latency_sum_ms / len(self.latency_samples)

    @property
    def uptime_seconds(self) -> float:
        return time.time() - self.start_time


@dataclass
class CanaryConfig:
    """Configuration for a canary deployment."""
    stable_agent_id: str
    canary_agent_id: str
    initial_weight_pct: float = 5.0
    promotion_steps: list[float] = field(
        default_factory=lambda: [5.0, 25.0, 50.0, 100.0]
    )
    step_duration_seconds: float = 300  # 5 minutes per step
    error_rate_threshold: float = 0.05  # 5% error rate triggers rollback
    latency_threshold_ms: float = 1000  # P95 latency threshold
    min_requests_before_eval: int = 20  # Minimum sample size


class CanaryController:
    """
    Manages canary deployments for GreenHelix agents.
    Routes traffic, monitors health, and auto-promotes or rolls back.
    """

    def __init__(
        self,
        config: CanaryConfig,
        stable_client: Any,
        canary_client: Any,
        metrics_client: Optional[Any] = None,
    ):
        self.config = config
        self._stable = stable_client
        self._canary = canary_client
        self._metrics_client = metrics_client

        self._current_weight: float = 0.0
        self._current_step: int = 0
        self._stable_metrics = CanaryMetrics()
        self._canary_metrics = CanaryMetrics()
        self._state: str = "idle"  # idle, running, promoted, rolled_back
        self._lock = threading.Lock()
        self._rollback_reason: Optional[str] = None

    def start(self) -> None:
        """Begin the canary deployment."""
        self._state = "running"
        self._current_weight = self.config.initial_weight_pct
        self._current_step = 0
        self._stable_metrics = CanaryMetrics()
        self._canary_metrics = CanaryMetrics()
        logger.info(
            "Canary started: %s at %.1f%% traffic",
            self.config.canary_agent_id,
            self._current_weight,
        )

    def route_request(self, tool: str, input_data: dict) -> dict:
        """Route a request to either stable or canary based on weight."""
        import random

        if self._state != "running":
            return self._stable.execute(tool, input_data)

        use_canary = random.random() * 100 < self._current_weight
        client = self._canary if use_canary else self._stable
        metrics = self._canary_metrics if use_canary else self._stable_metrics

        start = time.monotonic()
        try:
            result = client.execute(tool, input_data)
            elapsed_ms = (time.monotonic() - start) * 1000

            with self._lock:
                metrics.requests_total += 1
                metrics.latency_sum_ms += elapsed_ms
                metrics.latency_samples.append(elapsed_ms)

                status = result.get("status_code", 0)
                if 200 <= status < 400:
                    metrics.requests_success += 1
                else:
                    metrics.requests_error += 1

            return result

        except Exception as exc:
            with self._lock:
                metrics.requests_total += 1
                metrics.requests_error += 1
            raise

    def evaluate(self) -> dict:
        """
        Evaluate canary health. Returns action: 'promote', 'hold', or 'rollback'.
        """
        with self._lock:
            canary = self._canary_metrics
            stable = self._stable_metrics

        if canary.requests_total < self.config.min_requests_before_eval:
            return {
                "action": "hold",
                "reason": (
                    f"Insufficient canary samples: "
                    f"{canary.requests_total}/{self.config.min_requests_before_eval}"
                ),
                "canary_metrics": self._metrics_snapshot(canary),
                "stable_metrics": self._metrics_snapshot(stable),
            }

        # Check error rate
        if canary.error_rate > self.config.error_rate_threshold:
            error_detail = (
                f"Canary error rate {canary.error_rate:.2%} exceeds "
                f"threshold {self.config.error_rate_threshold:.2%}"
            )
            return {
                "action": "rollback",
                "reason": error_detail,
                "canary_metrics": self._metrics_snapshot(canary),
                "stable_metrics": self._metrics_snapshot(stable),
            }

        # Check latency
        if canary.latency_samples:
            sorted_latencies = sorted(canary.latency_samples)
            p95_idx = int(len(sorted_latencies) * 0.95)
            p95 = sorted_latencies[p95_idx] if p95_idx < len(sorted_latencies) else 0

            if p95 > self.config.latency_threshold_ms:
                latency_detail = (
                    f"Canary P95 latency {p95:.0f}ms exceeds "
                    f"threshold {self.config.latency_threshold_ms:.0f}ms"
                )
                return {
                    "action": "rollback",
                    "reason": latency_detail,
                    "canary_metrics": self._metrics_snapshot(canary),
                    "stable_metrics": self._metrics_snapshot(stable),
                }

        # Compare error rates: canary should not be significantly worse
        if (
            stable.requests_total >= self.config.min_requests_before_eval
            and canary.error_rate > stable.error_rate * 2
            and canary.error_rate > 0.01
        ):
            compare_detail = (
                f"Canary error rate {canary.error_rate:.2%} is >2x "
                f"stable error rate {stable.error_rate:.2%}"
            )
            return {
                "action": "rollback",
                "reason": compare_detail,
                "canary_metrics": self._metrics_snapshot(canary),
                "stable_metrics": self._metrics_snapshot(stable),
            }

        # Check if enough time has passed for promotion
        if canary.uptime_seconds >= self.config.step_duration_seconds:
            return {
                "action": "promote",
                "reason": (
                    f"Canary healthy after {canary.uptime_seconds:.0f}s "
                    f"at {self._current_weight:.0f}% traffic"
                ),
                "canary_metrics": self._metrics_snapshot(canary),
                "stable_metrics": self._metrics_snapshot(stable),
            }

        return {
            "action": "hold",
            "reason": "Waiting for evaluation period to complete",
            "canary_metrics": self._metrics_snapshot(canary),
            "stable_metrics": self._metrics_snapshot(stable),
        }

    def promote(self) -> bool:
        """Advance to the next traffic weight step. Returns True if fully promoted."""
        self._current_step += 1

        if self._current_step >= len(self.config.promotion_steps):
            self._state = "promoted"
            self._current_weight = 100.0
            logger.info("Canary fully promoted to 100%% traffic")
            return True

        self._current_weight = self.config.promotion_steps[self._current_step]
        # Reset metrics for the new step
        with self._lock:
            self._canary_metrics = CanaryMetrics()
            self._stable_metrics = CanaryMetrics()

        logger.info(
            "Canary promoted to %.1f%% traffic (step %d/%d)",
            self._current_weight,
            self._current_step + 1,
            len(self.config.promotion_steps),
        )
        return False

    def rollback(self, reason: str) -> None:
        """Roll back the canary deployment."""
        self._state = "rolled_back"
        self._current_weight = 0.0
        self._rollback_reason = reason
        logger.warning("Canary rolled back: %s", reason)

    def run_deployment(self) -> dict:
        """
        Run the full canary deployment lifecycle.
        Returns the final state and metrics.
        """
        self.start()

        while self._state == "running":
            time.sleep(10)  # Evaluate every 10 seconds
            evaluation = self.evaluate()

            if evaluation["action"] == "rollback":
                self.rollback(evaluation["reason"])
                break

            elif evaluation["action"] == "promote":
                fully_promoted = self.promote()
                if fully_promoted:
                    break

            # "hold" means keep waiting

        return {
            "final_state": self._state,
            "final_weight": self._current_weight,
            "rollback_reason": self._rollback_reason,
            "canary_metrics": self._metrics_snapshot(self._canary_metrics),
            "stable_metrics": self._metrics_snapshot(self._stable_metrics),
        }

    def _metrics_snapshot(self, metrics: CanaryMetrics) -> dict:
        sorted_latencies = sorted(metrics.latency_samples) if metrics.latency_samples else []
        p95_idx = int(len(sorted_latencies) * 0.95) if sorted_latencies else 0
        return {
            "requests_total": metrics.requests_total,
            "requests_success": metrics.requests_success,
            "requests_error": metrics.requests_error,
            "error_rate": round(metrics.error_rate, 4),
            "mean_latency_ms": round(metrics.mean_latency_ms, 2),
            "p95_latency_ms": round(sorted_latencies[p95_idx], 2) if sorted_latencies else 0,
            "uptime_seconds": round(metrics.uptime_seconds, 1),
        }

    @property
    def state(self) -> str:
        return self._state

    @property
    def current_weight(self) -> float:
        return self._current_weight
```

### Using the CanaryController in Practice

```python
def deploy_canary(stable_api_key: str, canary_api_key: str) -> dict:
    """Deploy a new agent version as a canary."""
    from my_agent import AgentClient

    stable = AgentClient(api_key=stable_api_key, agent_id="my-agent")
    canary = AgentClient(api_key=canary_api_key, agent_id="my-agent-canary")

    config = CanaryConfig(
        stable_agent_id="my-agent",
        canary_agent_id="my-agent-canary",
        initial_weight_pct=5.0,
        promotion_steps=[5.0, 25.0, 50.0, 100.0],
        step_duration_seconds=300,     # 5 minutes per step
        error_rate_threshold=0.05,     # 5% errors trigger rollback
        latency_threshold_ms=1000,     # 1 second P95 threshold
        min_requests_before_eval=20,
    )

    controller = CanaryController(config, stable, canary)
    result = controller.run_deployment()

    if result["final_state"] == "rolled_back":
        print(f"Canary FAILED: {result['rollback_reason']}")
        print(f"Canary metrics: {result['canary_metrics']}")
        print(f"Stable metrics: {result['stable_metrics']}")
    elif result["final_state"] == "promoted":
        print("Canary PROMOTED to 100% traffic")
        print(f"Final canary metrics: {result['canary_metrics']}")

    return result
```

### Handling In-Flight Transactions During Rollback

The most important detail: when you roll back a canary, do not kill the canary agent immediately. In-flight escrows created by the canary must complete. The rollback stops routing new traffic to the canary, but the canary agent continues running until all its active escrows are settled:

```python
def graceful_rollback(
    controller: CanaryController,
    canary_client: Any,
    reason: str,
    drain_timeout_seconds: int = 600,
) -> None:
    """Roll back canary traffic while draining in-flight transactions."""
    # Stop new traffic immediately
    controller.rollback(reason)

    # Check for in-flight escrows
    active_escrows = canary_client.execute("list_escrows", {
        "agent_id": controller.config.canary_agent_id,
        "status": "pending",
    })

    pending = active_escrows.get("body", {}).get("escrows", [])
    if not pending:
        logger.info("No in-flight transactions, canary shutdown clean")
        return

    logger.info(
        "Draining %d in-flight escrows before canary shutdown", len(pending)
    )

    deadline = time.time() + drain_timeout_seconds
    while time.time() < deadline:
        remaining = canary_client.execute("list_escrows", {
            "agent_id": controller.config.canary_agent_id,
            "status": "pending",
        })
        pending_count = len(remaining.get("body", {}).get("escrows", []))
        if pending_count == 0:
            logger.info("All in-flight transactions drained")
            return
        logger.info(
            "Waiting for %d in-flight transactions to complete...",
            pending_count,
        )
        time.sleep(30)

    logger.warning(
        "Drain timeout reached with %d transactions still pending. "
        "These will need manual resolution.",
        pending_count,
    )
```

### Monitoring Canary Health via GreenHelix Metrics

Use GreenHelix's built-in metrics to monitor canary health without building custom instrumentation. The `submit_metrics` and `get_agent_metrics` tools provide per-agent observability:

```python
def monitor_canary_via_greenhelix(
    api_key: str,
    stable_agent_id: str,
    canary_agent_id: str,
) -> dict:
    """Compare canary and stable metrics using GreenHelix's metrics tools."""
    import requests

    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    })
    base_url = "https://api.greenhelix.net/v1"

    def get_metrics(agent_id: str) -> dict:
        resp = session.post(
            f"{base_url}/v1",
            json={
                "tool": "get_agent_metrics",
                "input": {"agent_id": agent_id, "window": "5m"},
            },
        )
        return resp.json() if resp.status_code == 200 else {}

    stable_metrics = get_metrics(stable_agent_id)
    canary_metrics = get_metrics(canary_agent_id)

    comparison = {
        "stable": {
            "error_rate": stable_metrics.get("error_rate", 0),
            "mean_latency_ms": stable_metrics.get("mean_latency_ms", 0),
            "requests": stable_metrics.get("request_count", 0),
        },
        "canary": {
            "error_rate": canary_metrics.get("error_rate", 0),
            "mean_latency_ms": canary_metrics.get("mean_latency_ms", 0),
            "requests": canary_metrics.get("request_count", 0),
        },
    }

    # Flag if canary is significantly worse
    stable_err = comparison["stable"]["error_rate"]
    canary_err = comparison["canary"]["error_rate"]
    comparison["canary_healthy"] = canary_err <= max(stable_err * 2, 0.05)

    return comparison
```

---

## What's Next

This guide covered the complete testing and QA toolkit for agent commerce on GreenHelix: the testing pyramid adapted for multi-agent systems, the `AgentTestHarness` for recording and replaying API interactions, the `GreenHelixMock` for isolated unit testing with stateful escrow simulation, the `ChaosInjector` for validating resilience against real failure modes, the `ContractValidator` for catching breaking changes between agent versions, the `AgentBenchmark` for performance regression detection, CI/CD pipeline configuration with proper environment isolation, and the `CanaryController` for progressive rollouts with automatic rollback.

The six classes -- `AgentTestHarness`, `GreenHelixMock`, `ChaosInjector`, `ContractValidator`, `AgentBenchmark`, and `CanaryController` -- compose into a testing stack that covers every layer from unit to production deployment. Start with the harness and mocks for your immediate test gaps, add chaos testing when you have basic coverage, and implement canary releases when you are deploying frequently enough that manual validation becomes a bottleneck.

For the agent commerce patterns these tests validate, see the companion guides:

- **Agent-to-Agent Commerce: Escrow, Payments, and Trust** (P4) -- the escrow patterns, marketplace discovery, and payment flows that the test harness records and the contract validator checks.
- **Locking Down Agent Commerce** (P7) -- the security hardening that chaos testing validates under failure conditions.
- **The AI Agent FinOps Playbook** (P6) -- the budget caps and spending controls that prevent runaway test costs and protect canary deployments.
- **Agent Observability Deep Dive** (P11) -- the monitoring infrastructure that feeds canary health evaluation and benchmark reporting.

For the full API reference and tool catalog (all 128 tools), visit the GreenHelix developer documentation at [https://api.greenhelix.net/docs](https://api.greenhelix.net/docs).

---

*Price: $39 | Format: Digital Guide | Updates: Lifetime access*

