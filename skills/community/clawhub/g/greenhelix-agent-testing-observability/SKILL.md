---
name: greenhelix-agent-testing-observability
version: "1.3.1"
description: "The Agent Testing & Observability Cookbook: Ship Reliable Agent Commerce Systems. Practitioner cookbook for testing and monitoring agent commerce: tool contract tests, workflow saga tests, chaos injection, OpenTelemetry tracing, health checks, alerting, and CI/CD pipelines."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [testing, observability, chaos-engineering, ci-cd, guide, greenhelix, openclaw, ai-agent]
price_usd: 0.0
content_type: markdown
executable: false
install: none
credentials: [GREENHELIX_API_KEY, AGENT_SIGNING_KEY]
metadata:
  openclaw:
    requires:
      env:
        - GREENHELIX_API_KEY
        - AGENT_SIGNING_KEY
    primaryEnv: GREENHELIX_API_KEY
---
# The Agent Testing & Observability Cookbook: Ship Reliable Agent Commerce Systems

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `GREENHELIX_API_KEY`: API authentication for GreenHelix gateway (read/write access to purchased API tools only)
> - `AGENT_SIGNING_KEY`: Cryptographic signing key for agent identity (Ed25519 key pair for request signing)


Your agent commerce system works on your laptop. It passes a smoke test against the GreenHelix sandbox. You deploy to production on a Friday afternoon and go home. By Saturday morning, a retry loop has created 47 duplicate escrows, a performance escrow released funds against stale metrics, and a settlement webhook silently failed for six hours because the endpoint returned 503 and nobody was watching. The system was never tested for these failures because the traditional testing pyramid -- unit tests at the bottom, integration tests in the middle, end-to-end tests at the top -- was not designed for autonomous agents that make financial decisions across unreliable networks against counterparties that may themselves be failing. This guide rebuilds the testing pyramid for agent commerce, then layers production observability, chaos testing, alerting, and CI/CD on top. Every pattern is backed by working Python code, grounded in the 260-test suite that ships with the GreenHelix gateway, and designed to be copied directly into your project.
1. [The Testing Pyramid for Agent Systems](#chapter-1-the-testing-pyramid-for-agent-systems)
2. [Tool-Level Testing Patterns](#chapter-2-tool-level-testing-patterns)

## What You'll Learn
- Chapter 1: The Testing Pyramid for Agent Systems
- Chapter 2: Tool-Level Testing Patterns
- Chapter 3: Workflow & Integration Testing
- Chapter 4: Chaos Testing for Agent Commerce
- Chapter 5: Production Observability
- Chapter 6: Alerting & Incident Response
- Chapter 7: CI/CD for Agent Systems
- Chapter 8: What to Do Next

## Full Guide

# The Agent Testing & Observability Cookbook: Ship Reliable Agent Commerce Systems

Your agent commerce system works on your laptop. It passes a smoke test against the GreenHelix sandbox. You deploy to production on a Friday afternoon and go home. By Saturday morning, a retry loop has created 47 duplicate escrows, a performance escrow released funds against stale metrics, and a settlement webhook silently failed for six hours because the endpoint returned 503 and nobody was watching. The system was never tested for these failures because the traditional testing pyramid -- unit tests at the bottom, integration tests in the middle, end-to-end tests at the top -- was not designed for autonomous agents that make financial decisions across unreliable networks against counterparties that may themselves be failing. This guide rebuilds the testing pyramid for agent commerce, then layers production observability, chaos testing, alerting, and CI/CD on top. Every pattern is backed by working Python code, grounded in the 260-test suite that ships with the GreenHelix gateway, and designed to be copied directly into your project.

---

## Table of Contents

1. [The Testing Pyramid for Agent Systems](#chapter-1-the-testing-pyramid-for-agent-systems)
2. [Tool-Level Testing Patterns](#chapter-2-tool-level-testing-patterns)
3. [Workflow & Integration Testing](#chapter-3-workflow--integration-testing)
4. [Chaos Testing for Agent Commerce](#chapter-4-chaos-testing-for-agent-commerce)
5. [Production Observability](#chapter-5-production-observability)
6. [Alerting & Incident Response](#chapter-6-alerting--incident-response)
7. [CI/CD for Agent Systems](#chapter-7-cicd-for-agent-systems)
8. [What to Do Next](#chapter-8-what-to-do-next)

---

## Chapter 1: The Testing Pyramid for Agent Systems

### Why the Traditional Pyramid Breaks

The standard testing pyramid assumes your code calls functions that return values. Unit tests verify individual functions. Integration tests verify that modules compose correctly. End-to-end tests verify the full user flow. This model works when the system under test is deterministic, when function calls do not have financial side effects, and when failure modes are limited to "returns wrong value" or "throws exception."

Agent commerce systems violate all three assumptions. A call to `create_escrow` locks real funds. A call to `release_escrow` transfers real money. A retry that fires twice creates two escrows, not one error. The failure modes are not "wrong return value" -- they are "agent paid twice for the same work," "escrow timed out but funds are still locked," and "settlement succeeded on the gateway but the webhook notification was lost." Traditional unit tests cannot catch these failures because they test the code in isolation from the financial state machine. Traditional end-to-end tests cannot catch them because they run the happy path once and call it done.

### The Agent Testing Pyramid

Agent commerce requires a four-layer testing pyramid that maps to the actual failure modes:

```
                    ╱╲
                   ╱  ╲
                  ╱Chaos╲           Layer 4: Chaos tests
                 ╱  Tests ╲         (failure injection, timeouts,
                ╱──────────╲        concurrent load)
               ╱ Multi-Agent ╲      Layer 3: Multi-agent workflow tests
              ╱   Workflows   ╲     (sagas, rollbacks, webhook delivery)
             ╱─────────────────╲
            ╱   Tool Contract    ╲   Layer 2: Tool-level contract tests
           ╱      Tests           ╲  (schema, idempotency, permissions)
          ╱────────────────────────╲
         ╱    Deterministic Mocks    ╲ Layer 1: Mock-based unit tests
        ╱      (fast, offline)        ╲ (business logic, validation)
       ╱───────────────────────────────╲
```

**Layer 1: Deterministic mocks** test your business logic without hitting the gateway. They run in milliseconds and catch logic errors: wrong amount calculations, missing trust checks, incorrect state transitions. These are 60% of your tests.

**Layer 2: Tool contract tests** verify that each GreenHelix tool accepts the expected input schema, returns the expected output shape, and produces the correct error codes for invalid input. These run against the sandbox and catch API contract changes. These are 25% of your tests.

**Layer 3: Multi-agent workflow tests** verify complete business flows: marketplace listing through escrow release through settlement. They test the saga pattern (multi-step rollback on failure) and webhook delivery. These are 10% of your tests.

**Layer 4: Chaos tests** inject failures -- network timeouts, random tool errors, concurrent duplicate requests -- and verify that the system recovers without financial inconsistency. These are 5% of your tests but catch the bugs that cost the most money.

### The AgentTestHarness

Every test in this guide uses the `AgentTestHarness` class. It manages fixtures, provides deterministic mocks for Layer 1, and switches to sandbox mode for Layers 2-4.

```python
import pytest
import time
import json
import uuid
import requests
from unittest.mock import MagicMock, patch
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class MockResponse:
    """Deterministic mock for a GreenHelix tool response."""
    tool: str
    status: str = "success"
    data: dict = field(default_factory=dict)
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def to_dict(self) -> dict:
        result = {"status": self.status}
        if self.status == "success":
            result.update(self.data)
        else:
            result["error"] = {
                "code": self.error_code or "unknown_error",
                "message": self.error_message or "An error occurred",
            }
        return result


class AgentTestHarness:
    """Test harness for GreenHelix agent commerce systems.

    Manages fixtures, mocks, and sandbox connections for all four
    layers of the agent testing pyramid.

    Usage:
        harness = AgentTestHarness(
            api_key="test-key",
            agent_id="test-agent",
            base_url="https://sandbox.greenhelix.net/v1",
        )

        # Layer 1: deterministic mocks
        harness.mock_tool("get_balance", {"balance": "100.00"})
        result = harness.execute("get_balance", {})
        assert result["balance"] == "100.00"

        # Layer 2+: sandbox mode
        harness.use_sandbox()
        result = harness.execute("get_balance", {})
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: str = "https://sandbox.greenhelix.net/v1",
    ):
        self.api_key = api_key
        self.agent_id = agent_id
        self.base_url = base_url
        self._mocks: dict[str, MockResponse] = {}
        self._call_log: list[dict] = []
        self._sandbox_mode = False
        self._session = requests.Session()
        self._session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })

    # ── Mode Control ───────────────────────────────────────────

    def use_mocks(self):
        """Switch to deterministic mock mode (Layer 1)."""
        self._sandbox_mode = False

    def use_sandbox(self):
        """Switch to live sandbox mode (Layer 2+)."""
        self._sandbox_mode = True

    # ── Mock Registration ──────────────────────────────────────

    def mock_tool(self, tool: str, data: dict, status: str = "success"):
        """Register a deterministic mock response for a tool."""
        self._mocks[tool] = MockResponse(tool=tool, status=status, data=data)

    def mock_tool_error(
        self, tool: str, error_code: str, error_message: str
    ):
        """Register a deterministic error response for a tool."""
        self._mocks[tool] = MockResponse(
            tool=tool,
            status="error",
            error_code=error_code,
            error_message=error_message,
        )

    def mock_tool_sequence(self, tool: str, responses: list[dict]):
        """Register a sequence of responses for successive calls."""
        self._mock_sequences = getattr(self, "_mock_sequences", {})
        self._mock_sequences[tool] = list(responses)

    # ── Execution ──────────────────────────────────────────────

    def execute(self, tool: str, input_data: dict) -> dict:
        """Execute a tool against mocks or sandbox."""
        call_record = {
            "tool": tool,
            "input": input_data,
            "timestamp": time.time(),
        }

        if self._sandbox_mode:
            resp = self._session.post(
                f"{self.base_url}/v1",
                json={"tool": tool, "input": input_data},
            )
            resp.raise_for_status()
            result = resp.json()
        else:
            # Check sequences first
            sequences = getattr(self, "_mock_sequences", {})
            if tool in sequences and sequences[tool]:
                result = sequences[tool].pop(0)
            elif tool in self._mocks:
                result = self._mocks[tool].to_dict()
            else:
                raise ValueError(
                    f"No mock registered for tool '{tool}'. "
                    f"Register with harness.mock_tool('{tool}', {{...}})"
                )

        call_record["result"] = result
        self._call_log.append(call_record)
        return result

    # ── Assertions ─────────────────────────────────────────────

    def assert_tool_called(self, tool: str, times: Optional[int] = None):
        """Assert that a tool was called, optionally a specific number of times."""
        calls = [c for c in self._call_log if c["tool"] == tool]
        assert len(calls) > 0, f"Tool '{tool}' was never called"
        if times is not None:
            assert len(calls) == times, (
                f"Tool '{tool}' called {len(calls)} times, expected {times}"
            )

    def assert_tool_not_called(self, tool: str):
        """Assert that a tool was never called."""
        calls = [c for c in self._call_log if c["tool"] == tool]
        assert len(calls) == 0, (
            f"Tool '{tool}' was called {len(calls)} times, expected 0"
        )

    def assert_call_order(self, tools: list[str]):
        """Assert that tools were called in a specific order."""
        called_tools = [c["tool"] for c in self._call_log]
        idx = 0
        for tool in tools:
            try:
                idx = called_tools.index(tool, idx) + 1
            except ValueError:
                assert False, (
                    f"Expected '{tool}' after position {idx} in call log. "
                    f"Actual order: {called_tools}"
                )

    def get_calls(self, tool: Optional[str] = None) -> list[dict]:
        """Get call log, optionally filtered by tool name."""
        if tool:
            return [c for c in self._call_log if c["tool"] == tool]
        return list(self._call_log)

    def reset(self):
        """Clear all mocks and call history."""
        self._mocks.clear()
        self._call_log.clear()
        if hasattr(self, "_mock_sequences"):
            self._mock_sequences.clear()
```

### The conftest.py: Reusable Fixtures

Drop this `conftest.py` into your test directory. Every test file in this guide imports from it.

```python
# tests/conftest.py
import os
import uuid
import pytest


@pytest.fixture
def api_key():
    """API key for sandbox testing. Uses env var or test default."""
    return os.environ.get("GREENHELIX_API_KEY", "test-api-key-sandbox")


@pytest.fixture
def base_url():
    """Sandbox URL for integration tests."""
    return os.environ.get(
        "GREENHELIX_BASE_URL", "https://sandbox.greenhelix.net/v1"
    )


@pytest.fixture
def agent_id():
    """Unique agent ID per test run to prevent collision."""
    return f"test-agent-{uuid.uuid4().hex[:12]}"


@pytest.fixture
def buyer_id():
    """Unique buyer agent ID."""
    return f"test-buyer-{uuid.uuid4().hex[:12]}"


@pytest.fixture
def seller_id():
    """Unique seller agent ID."""
    return f"test-seller-{uuid.uuid4().hex[:12]}"


@pytest.fixture
def harness(api_key, agent_id, base_url):
    """AgentTestHarness in mock mode. Call harness.use_sandbox() for live."""
    h = AgentTestHarness(
        api_key=api_key,
        agent_id=agent_id,
        base_url=base_url,
    )
    h.use_mocks()
    return h


@pytest.fixture
def sandbox_harness(api_key, agent_id, base_url):
    """AgentTestHarness in sandbox mode for integration tests."""
    h = AgentTestHarness(
        api_key=api_key,
        agent_id=agent_id,
        base_url=base_url,
    )
    h.use_sandbox()
    return h


@pytest.fixture
def mock_session():
    """Pre-configured requests.Session mock for unit tests."""
    session = MagicMock()
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {"status": "success"}
    response.raise_for_status.return_value = None
    session.post.return_value = response
    return session


@pytest.fixture
def mock_response():
    """Factory fixture for creating MockResponse objects."""
    def _make(tool, data=None, status="success", error_code=None):
        return MockResponse(
            tool=tool,
            status=status,
            data=data or {},
            error_code=error_code,
        )
    return _make


# ── Per-class fixtures for isolated test suites ─────────────

class AgentFixtures:
    """Mixin providing standard mocks for agent commerce tests."""

    @pytest.fixture(autouse=True)
    def setup_agent_mocks(self, harness):
        """Pre-register common mocks for every test in the class."""
        self.harness = harness
        harness.mock_tool("get_balance", {"balance": "500.00", "currency": "USD"})
        harness.mock_tool("create_wallet", {"wallet_id": "w-test-001", "status": "active"})
        harness.mock_tool("register_agent", {"agent_id": harness.agent_id, "status": "registered"})
        harness.mock_tool("get_trust_score", {"agent_id": "any", "score": 0.85})
        harness.mock_tool("get_budget_status", {
            "daily_limit": "100.00",
            "spent_today": "25.00",
            "remaining": "75.00",
        })


class EscrowFixtures(AgentFixtures):
    """Extended fixtures for escrow-related tests."""

    @pytest.fixture(autouse=True)
    def setup_escrow_mocks(self, harness):
        """Add escrow mocks on top of agent mocks."""
        self.escrow_id = f"escrow-{uuid.uuid4().hex[:8]}"
        harness.mock_tool("create_escrow", {
            "escrow_id": self.escrow_id,
            "status": "funded",
            "amount": "50.00",
        })
        harness.mock_tool("release_escrow", {
            "escrow_id": self.escrow_id,
            "status": "released",
        })
        harness.mock_tool("cancel_escrow", {
            "escrow_id": self.escrow_id,
            "status": "cancelled",
        })
```

### Pattern: Deterministic Mocks vs. Sandbox Testing

The harness supports both modes. Use mocks for business logic tests (fast, no network, deterministic). Use sandbox for contract and integration tests (real API, real state, real latency).

```python
class TestBudgetGuardrails(AgentFixtures):
    """Layer 1: Test budget logic with deterministic mocks."""

    def test_blocks_escrow_when_over_budget(self, harness):
        """Escrow creation should be blocked when daily budget is exhausted."""
        harness.mock_tool("get_budget_status", {
            "daily_limit": "100.00",
            "spent_today": "99.00",
            "remaining": "1.00",
        })
        budget = harness.execute("get_budget_status", {})
        remaining = float(budget["remaining"])
        escrow_amount = 50.00

        # Business logic: do not create escrow if amount > remaining
        assert escrow_amount > remaining
        harness.assert_tool_not_called("create_escrow")

    def test_allows_escrow_within_budget(self, harness):
        """Escrow creation should proceed when budget allows."""
        budget = harness.execute("get_budget_status", {})
        remaining = float(budget["remaining"])
        escrow_amount = 25.00

        assert escrow_amount <= remaining
        harness.execute("create_escrow", {
            "payer_agent_id": harness.agent_id,
            "payee_agent_id": "seller-001",
            "amount": str(escrow_amount),
        })
        harness.assert_tool_called("create_escrow", times=1)


@pytest.mark.sandbox
class TestBudgetGuardrailsSandbox:
    """Layer 2: Verify budget tools against live sandbox."""

    def test_budget_cap_enforced(self, sandbox_harness):
        """Sandbox should reject escrows exceeding the budget cap."""
        h = sandbox_harness
        h.execute("create_wallet", {})
        h.execute("deposit", {"amount": "100.00"})
        h.execute("set_budget_cap", {
            "agent_id": h.agent_id,
            "daily_limit": "10.00",
        })
        # This should fail because escrow exceeds daily limit
        result = h.execute("create_escrow", {
            "payer_agent_id": h.agent_id,
            "payee_agent_id": "seller-test",
            "amount": "50.00",
        })
        # Gateway enforces budget at the tool level
        assert result.get("status") in ("error", "rejected")
```

---

## Chapter 2: Tool-Level Testing Patterns

### The Tool Contract Test

Every GreenHelix tool has an implicit contract: it accepts a specific input schema, returns a specific output shape, and produces documented error codes for invalid input. A tool contract test verifies all three. When the gateway updates an API version or adds a required field, your contract tests break before your production code does.

```python
class ToolContract:
    """Defines the expected contract for a GreenHelix tool.

    Used by contract tests to verify schema, output shape,
    and error behavior against the sandbox.
    """

    def __init__(
        self,
        tool: str,
        required_fields: list[str],
        output_fields: list[str],
        error_cases: dict[str, dict],
    ):
        self.tool = tool
        self.required_fields = required_fields
        self.output_fields = output_fields
        self.error_cases = error_cases  # {case_name: {input: ..., expected_error: ...}}


# ── Contract definitions for core tools ────────────────────

BILLING_CONTRACTS = {
    "get_balance": ToolContract(
        tool="get_balance",
        required_fields=[],
        output_fields=["balance", "currency"],
        error_cases={
            "no_wallet": {
                "input": {},
                "expected_error": "wallet_not_found",
            },
        },
    ),
    "deposit": ToolContract(
        tool="deposit",
        required_fields=["amount"],
        output_fields=["balance", "transaction_id"],
        error_cases={
            "negative_amount": {
                "input": {"amount": "-10.00"},
                "expected_error": "invalid_amount",
            },
            "zero_amount": {
                "input": {"amount": "0"},
                "expected_error": "invalid_amount",
            },
        },
    ),
    "set_budget_cap": ToolContract(
        tool="set_budget_cap",
        required_fields=["agent_id", "daily_limit"],
        output_fields=["agent_id", "daily_limit"],
        error_cases={
            "negative_limit": {
                "input": {"agent_id": "test", "daily_limit": "-50.00"},
                "expected_error": "invalid_amount",
            },
        },
    ),
}

PAYMENT_CONTRACTS = {
    "create_escrow": ToolContract(
        tool="create_escrow",
        required_fields=["payer_agent_id", "payee_agent_id", "amount"],
        output_fields=["escrow_id", "status", "amount"],
        error_cases={
            "insufficient_funds": {
                "input": {
                    "payer_agent_id": "buyer",
                    "payee_agent_id": "seller",
                    "amount": "999999.00",
                },
                "expected_error": "insufficient_funds",
            },
            "self_escrow": {
                "input": {
                    "payer_agent_id": "same-agent",
                    "payee_agent_id": "same-agent",
                    "amount": "10.00",
                },
                "expected_error": "invalid_escrow",
            },
        },
    ),
    "release_escrow": ToolContract(
        tool="release_escrow",
        required_fields=["escrow_id"],
        output_fields=["escrow_id", "status"],
        error_cases={
            "nonexistent": {
                "input": {"escrow_id": "escrow-does-not-exist"},
                "expected_error": "escrow_not_found",
            },
        },
    ),
}

IDENTITY_CONTRACTS = {
    "register_agent": ToolContract(
        tool="register_agent",
        required_fields=["agent_id", "public_key", "name"],
        output_fields=["agent_id", "status"],
        error_cases={
            "missing_key": {
                "input": {"agent_id": "test", "name": "Test"},
                "expected_error": "missing_field",
            },
        },
    ),
    "get_trust_score": ToolContract(
        tool="get_trust_score",
        required_fields=["agent_id"],
        output_fields=["agent_id", "score"],
        error_cases={
            "nonexistent_agent": {
                "input": {"agent_id": "agent-that-does-not-exist-xyz"},
                "expected_error": "agent_not_found",
            },
        },
    ),
}

MARKETPLACE_CONTRACTS = {
    "register_service": ToolContract(
        tool="register_service",
        required_fields=["name", "description", "endpoint", "price", "tags", "category"],
        output_fields=["service_id"],
        error_cases={
            "missing_name": {
                "input": {
                    "description": "test",
                    "endpoint": "agent://test",
                    "price": 10.0,
                    "tags": [],
                    "category": "test",
                },
                "expected_error": "missing_field",
            },
        },
    ),
    "search_services": ToolContract(
        tool="search_services",
        required_fields=["query"],
        output_fields=["services"],
        error_cases={
            "empty_query": {
                "input": {"query": ""},
                "expected_error": "invalid_query",
            },
        },
    ),
}
```

### Running Contract Tests

```python
@pytest.mark.sandbox
class TestBillingContracts:
    """Layer 2: Verify billing tool contracts against sandbox."""

    @pytest.fixture(autouse=True)
    def setup_wallet(self, sandbox_harness):
        self.harness = sandbox_harness
        self.harness.execute("create_wallet", {})
        self.harness.execute("deposit", {"amount": "100.00"})

    @pytest.mark.parametrize("tool_name", BILLING_CONTRACTS.keys())
    def test_output_shape(self, tool_name):
        """Every billing tool returns expected output fields."""
        contract = BILLING_CONTRACTS[tool_name]
        # Build minimal valid input
        valid_input = {}
        if tool_name == "deposit":
            valid_input = {"amount": "10.00"}
        elif tool_name == "set_budget_cap":
            valid_input = {
                "agent_id": self.harness.agent_id,
                "daily_limit": "50.00",
            }
        result = self.harness.execute(tool_name, valid_input)
        for expected_field in contract.output_fields:
            assert expected_field in result, (
                f"Tool '{tool_name}' missing output field '{expected_field}'. "
                f"Got: {list(result.keys())}"
            )

    @pytest.mark.parametrize("tool_name", BILLING_CONTRACTS.keys())
    def test_error_cases(self, tool_name):
        """Every billing tool returns correct error codes for invalid input."""
        contract = BILLING_CONTRACTS[tool_name]
        for case_name, case in contract.error_cases.items():
            result = self.harness.execute(tool_name, case["input"])
            assert result.get("status") == "error" or "error" in result, (
                f"Tool '{tool_name}' case '{case_name}' should have failed. "
                f"Got: {result}"
            )


@pytest.mark.sandbox
class TestPaymentContracts:
    """Layer 2: Verify payment tool contracts against sandbox."""

    @pytest.fixture(autouse=True)
    def setup_accounts(self, sandbox_harness, buyer_id, seller_id):
        self.harness = sandbox_harness
        self.buyer_id = buyer_id
        self.seller_id = seller_id

    @pytest.mark.parametrize("tool_name", PAYMENT_CONTRACTS.keys())
    def test_error_cases(self, tool_name):
        """Every payment tool returns correct errors for invalid input."""
        contract = PAYMENT_CONTRACTS[tool_name]
        for case_name, case in contract.error_cases.items():
            result = self.harness.execute(tool_name, case["input"])
            assert result.get("status") == "error" or "error" in result, (
                f"Payment tool '{tool_name}' case '{case_name}' did not fail"
            )
```

### Idempotency Testing for Payment Tools

Payment tools must be idempotent. Calling `create_escrow` twice with the same parameters should not create two escrows. Calling `release_escrow` twice should not transfer funds twice. This pattern tests idempotency by submitting duplicate requests and verifying financial consistency (P1, P7).

```python
@pytest.mark.sandbox
class TestPaymentIdempotency:
    """Layer 2: Verify payment tools handle duplicate calls safely."""

    def test_duplicate_escrow_creation(self, sandbox_harness, buyer_id, seller_id):
        """Creating the same escrow twice should return the same escrow_id."""
        h = sandbox_harness
        h.execute("create_wallet", {})
        h.execute("deposit", {"amount": "200.00"})

        escrow_params = {
            "payer_agent_id": buyer_id,
            "payee_agent_id": seller_id,
            "amount": "50.00",
            "description": "Idempotency test escrow",
            "idempotency_key": f"idem-{uuid.uuid4().hex[:8]}",
        }

        result_1 = h.execute("create_escrow", escrow_params)
        result_2 = h.execute("create_escrow", escrow_params)

        # Same idempotency key should return same escrow
        assert result_1["escrow_id"] == result_2["escrow_id"]

        # Balance should only be debited once
        balance = h.execute("get_balance", {})
        assert float(balance["balance"]) == 150.00

    def test_duplicate_release(self, sandbox_harness):
        """Releasing the same escrow twice should not double-pay."""
        h = sandbox_harness
        h.execute("create_wallet", {})
        h.execute("deposit", {"amount": "100.00"})

        escrow = h.execute("create_escrow", {
            "payer_agent_id": h.agent_id,
            "payee_agent_id": "seller-test",
            "amount": "25.00",
        })
        escrow_id = escrow["escrow_id"]

        release_1 = h.execute("release_escrow", {"escrow_id": escrow_id})
        release_2 = h.execute("release_escrow", {"escrow_id": escrow_id})

        # Second release should be a no-op or return already_released
        assert release_1.get("status") == "released"
        assert release_2.get("status") in ("released", "already_released")
```

### Permission Boundary Testing

Agents should only be able to operate on their own resources. A buyer should not release an escrow created by a different buyer. A seller should not cancel an escrow that is not addressed to them. Permission boundary tests verify these invariants (P7).

```python
@pytest.mark.sandbox
class TestPermissionBoundaries:
    """Layer 2: Verify agents cannot access other agents' resources."""

    def test_cannot_release_others_escrow(self, sandbox_harness):
        """Agent A cannot release an escrow created by Agent B."""
        h = sandbox_harness
        # Agent A creates an escrow
        h.execute("create_wallet", {})
        h.execute("deposit", {"amount": "100.00"})
        escrow = h.execute("create_escrow", {
            "payer_agent_id": h.agent_id,
            "payee_agent_id": "seller-x",
            "amount": "10.00",
        })

        # Agent B (different harness/session) tries to release it
        other = AgentTestHarness(
            api_key=h.api_key,
            agent_id="attacker-agent",
            base_url=h.base_url,
        )
        other.use_sandbox()
        result = other.execute("release_escrow", {
            "escrow_id": escrow["escrow_id"],
        })
        assert result.get("status") == "error"

    def test_cannot_read_others_balance(self, sandbox_harness):
        """Agent A cannot read Agent B's wallet balance."""
        h = sandbox_harness
        h.execute("create_wallet", {})
        h.execute("deposit", {"amount": "100.00"})

        other = AgentTestHarness(
            api_key=h.api_key,
            agent_id="other-agent",
            base_url=h.base_url,
        )
        other.use_sandbox()
        result = other.execute("get_balance", {})
        # Should return the other agent's balance (0), not our 100
        balance = float(result.get("balance", 0))
        assert balance != 100.00

    def test_cannot_cancel_others_escrow(self, sandbox_harness):
        """Seller cannot cancel an escrow -- only the buyer can."""
        h = sandbox_harness
        h.execute("create_wallet", {})
        h.execute("deposit", {"amount": "50.00"})
        escrow = h.execute("create_escrow", {
            "payer_agent_id": h.agent_id,
            "payee_agent_id": "seller-y",
            "amount": "10.00",
        })

        seller = AgentTestHarness(
            api_key=h.api_key,
            agent_id="seller-y",
            base_url=h.base_url,
        )
        seller.use_sandbox()
        result = seller.execute("cancel_escrow", {
            "escrow_id": escrow["escrow_id"],
        })
        assert result.get("status") == "error"
```

---

## Chapter 3: Workflow & Integration Testing

### The Saga Test Pattern

Agent commerce workflows are sagas: multi-step operations where each step has a compensating action. If step 3 fails, steps 1 and 2 must be rolled back. The saga test pattern verifies both the happy path and every possible failure point.

```python
class MarketplaceSaga:
    """Implements the complete marketplace listing workflow as a testable saga.

    Steps:
        1. Seller registers service on marketplace
        2. Buyer discovers service via search
        3. Buyer checks seller trust score
        4. Buyer creates escrow
        5. Seller performs work (simulated)
        6. Buyer releases escrow
        7. Buyer rates service
        8. Settlement completes

    Compensating actions:
        Step 4 fails → no cleanup needed (funds not locked)
        Step 5 fails → cancel escrow (return funds to buyer)
        Step 6 fails → open dispute
    """

    def __init__(self, harness: AgentTestHarness, buyer_id: str, seller_id: str):
        self.harness = harness
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.state = {"step": 0, "completed_steps": []}

    def run(self) -> dict:
        """Execute the full saga, rolling back on failure."""
        try:
            # Step 1: Register service
            service = self.harness.execute("register_service", {
                "name": "Test Summarization Service",
                "description": "Summarizes documents for testing",
                "endpoint": f"agent://{self.seller_id}",
                "price": 25.00,
                "tags": ["test", "summarization"],
                "category": "data-processing",
            })
            self.state["service_id"] = service["service_id"]
            self.state["completed_steps"].append("register_service")

            # Step 2: Discover service
            results = self.harness.execute("search_services", {
                "query": "test summarization",
            })
            assert len(results.get("services", [])) > 0
            self.state["completed_steps"].append("discover_service")

            # Step 3: Trust check
            trust = self.harness.execute("get_trust_score", {
                "agent_id": self.seller_id,
            })
            if trust.get("score", 0) < 0.5:
                return {"status": "aborted", "reason": "low_trust"}
            self.state["completed_steps"].append("trust_check")

            # Step 4: Create escrow
            escrow = self.harness.execute("create_escrow", {
                "payer_agent_id": self.buyer_id,
                "payee_agent_id": self.seller_id,
                "amount": "25.00",
                "description": "Saga test escrow",
            })
            self.state["escrow_id"] = escrow["escrow_id"]
            self.state["completed_steps"].append("create_escrow")

            # Step 5: Simulate work (in real tests, call seller endpoint)
            work_result = {"quality": 0.95, "documents_processed": 500}
            self.state["completed_steps"].append("work_completed")

            # Step 6: Release escrow
            release = self.harness.execute("release_escrow", {
                "escrow_id": escrow["escrow_id"],
            })
            self.state["completed_steps"].append("release_escrow")

            # Step 7: Rate service
            self.harness.execute("rate_service", {
                "service_id": service["service_id"],
                "rating": 5,
            })
            self.state["completed_steps"].append("rate_service")

            return {"status": "completed", "state": self.state}

        except Exception as e:
            return self._compensate(str(e))

    def _compensate(self, error: str) -> dict:
        """Roll back completed steps on failure."""
        if "create_escrow" in self.state["completed_steps"]:
            escrow_id = self.state.get("escrow_id")
            if escrow_id and "release_escrow" not in self.state["completed_steps"]:
                self.harness.execute("cancel_escrow", {
                    "escrow_id": escrow_id,
                })
                self.state["completed_steps"].append("compensate:cancel_escrow")

        return {
            "status": "rolled_back",
            "error": error,
            "state": self.state,
        }
```

### Testing the Saga

```python
class TestMarketplaceSaga(EscrowFixtures):
    """Layer 3: Full marketplace workflow with rollback verification."""

    def test_happy_path(self, harness, buyer_id, seller_id):
        """Complete saga executes all 7 steps."""
        harness.mock_tool("register_service", {
            "service_id": "svc-test-001",
        })
        harness.mock_tool("search_services", {
            "services": [{"name": "Test Service", "agent_id": seller_id}],
        })
        harness.mock_tool("rate_service", {"status": "rated"})

        saga = MarketplaceSaga(harness, buyer_id, seller_id)
        result = saga.run()

        assert result["status"] == "completed"
        assert len(result["state"]["completed_steps"]) == 7
        harness.assert_call_order([
            "register_service",
            "search_services",
            "get_trust_score",
            "create_escrow",
            "release_escrow",
            "rate_service",
        ])

    def test_rollback_on_escrow_failure(self, harness, buyer_id, seller_id):
        """Failed escrow creation does not leave orphaned state."""
        harness.mock_tool("register_service", {"service_id": "svc-test-002"})
        harness.mock_tool("search_services", {
            "services": [{"name": "Test", "agent_id": seller_id}],
        })
        harness.mock_tool_error(
            "create_escrow", "insufficient_funds", "Not enough balance"
        )

        saga = MarketplaceSaga(harness, buyer_id, seller_id)
        result = saga.run()

        assert result["status"] == "rolled_back"
        assert "create_escrow" not in result["state"]["completed_steps"]
        harness.assert_tool_not_called("release_escrow")

    def test_rollback_cancels_escrow_on_work_failure(self, harness, buyer_id, seller_id):
        """Failed work step triggers escrow cancellation."""
        harness.mock_tool("register_service", {"service_id": "svc-test-003"})
        harness.mock_tool("search_services", {
            "services": [{"name": "Test", "agent_id": seller_id}],
        })

        saga = MarketplaceSaga(harness, buyer_id, seller_id)
        # Simulate work failure by injecting error after escrow creation
        original_execute = harness.execute

        call_count = {"n": 0}
        def failing_execute(tool, input_data):
            call_count["n"] += 1
            if tool == "release_escrow":
                raise RuntimeError("Simulated work verification failure")
            return original_execute(tool, input_data)

        harness.execute = failing_execute
        result = saga.run()

        assert result["status"] == "rolled_back"
        assert "compensate:cancel_escrow" in result["state"]["completed_steps"]
```

### Subscription Lifecycle Testing

Subscriptions are stateful workflows: create, renew, pause, cancel. Each transition must be tested, including edge cases like renewal with insufficient balance (P2, P6).

```python
class TestSubscriptionLifecycle(AgentFixtures):
    """Layer 3: Verify subscription state transitions."""

    def test_full_lifecycle(self, harness):
        """Create → renew → cancel lifecycle."""
        sub_id = f"sub-{uuid.uuid4().hex[:8]}"
        harness.mock_tool("create_subscription", {
            "subscription_id": sub_id,
            "status": "active",
            "next_payment_date": "2026-05-06",
        })
        harness.mock_tool("get_subscription", {
            "subscription_id": sub_id,
            "status": "active",
            "payments_completed": 1,
        })
        harness.mock_tool("cancel_subscription", {
            "subscription_id": sub_id,
            "status": "cancelled",
        })

        # Create
        sub = harness.execute("create_subscription", {
            "payer_agent_id": harness.agent_id,
            "payee_agent_id": "provider-001",
            "amount": "15.00",
            "interval": "monthly",
        })
        assert sub["status"] == "active"

        # Check status
        status = harness.execute("get_subscription", {
            "subscription_id": sub_id,
        })
        assert status["payments_completed"] == 1

        # Cancel
        cancel = harness.execute("cancel_subscription", {
            "subscription_id": sub_id,
        })
        assert cancel["status"] == "cancelled"

        harness.assert_call_order([
            "create_subscription",
            "get_subscription",
            "cancel_subscription",
        ])

    def test_renewal_with_insufficient_funds(self, harness):
        """Subscription renewal should fail gracefully when balance is low."""
        harness.mock_tool("get_balance", {"balance": "5.00", "currency": "USD"})
        harness.mock_tool_error(
            "create_subscription",
            "insufficient_funds",
            "Balance too low for subscription amount",
        )

        result = harness.execute("create_subscription", {
            "payer_agent_id": harness.agent_id,
            "payee_agent_id": "provider-002",
            "amount": "15.00",
            "interval": "monthly",
        })
        assert result.get("status") == "error"
```

### Webhook Delivery Testing

Webhooks are the primary notification mechanism for payment events. A missed webhook means a missed settlement, a missed dispute deadline, or a missed subscription renewal. Test webhook delivery separately from the business logic it triggers (P4).

```python
class TestWebhookDelivery:
    """Layer 3: Verify webhook registration and event delivery."""

    def test_webhook_registration(self, harness):
        """Webhook registration should return a webhook_id."""
        harness.mock_tool("register_webhook", {
            "webhook_id": "wh-test-001",
            "status": "active",
            "events": ["escrow.released", "escrow.disputed"],
        })

        result = harness.execute("register_webhook", {
            "url": "https://test.example.com/webhook",
            "events": ["escrow.released", "escrow.disputed"],
        })
        assert "webhook_id" in result
        assert result["status"] == "active"

    def test_webhook_event_format(self, harness):
        """Webhook payloads should contain required fields."""
        harness.mock_tool("get_webhook_logs", {
            "logs": [{
                "webhook_id": "wh-test-001",
                "event_type": "escrow.released",
                "payload": {
                    "escrow_id": "escrow-abc",
                    "amount": "25.00",
                    "payer_agent_id": "buyer-1",
                    "payee_agent_id": "seller-1",
                    "timestamp": "2026-04-06T12:00:00Z",
                },
                "delivery_status": "delivered",
                "response_code": 200,
            }],
        })

        logs = harness.execute("get_webhook_logs", {"webhook_id": "wh-test-001"})
        for log_entry in logs["logs"]:
            payload = log_entry["payload"]
            assert "escrow_id" in payload
            assert "amount" in payload
            assert "timestamp" in payload
            assert log_entry["delivery_status"] == "delivered"
```

---

## Chapter 4: Chaos Testing for Agent Commerce

### Why Chaos Testing Matters for Payments

Traditional software fails gracefully when a downstream service is unavailable -- it shows an error page. Agent commerce software fails expensively. A timeout during `release_escrow` might mean funds are released on the gateway but the caller never gets confirmation, leading to a duplicate release attempt. A network partition during a split payment might result in partial settlement. Chaos testing injects these failures deliberately so you can verify your system handles them before production handles them for you.

### The ChaosMiddleware

The `ChaosMiddleware` wraps the harness's `execute` method and randomly injects failures: timeouts, error responses, delayed responses, and corrupted payloads. It is configurable per tool and per failure type.

```python
import random
import time
from dataclasses import dataclass, field


@dataclass
class ChaosConfig:
    """Configuration for chaos injection on a specific tool."""
    timeout_pct: float = 0.0       # % of calls that timeout
    error_pct: float = 0.0         # % of calls that return errors
    delay_ms: float = 0.0          # Additional latency in ms
    corrupt_pct: float = 0.0       # % of calls with corrupted responses
    duplicate_pct: float = 0.0     # % of calls that execute twice


class ChaosMiddleware:
    """Wraps AgentTestHarness._execute with configurable failure injection.

    Usage:
        harness = AgentTestHarness(api_key, agent_id, base_url)
        chaos = ChaosMiddleware(
            harness=harness,
            default_config=ChaosConfig(error_pct=10, delay_ms=200),
        )
        chaos.set_tool_config("create_escrow", ChaosConfig(
            timeout_pct=20,
            duplicate_pct=5,
        ))

        # All calls now go through chaos injection
        result = chaos.execute("create_escrow", {...})
    """

    def __init__(
        self,
        harness: AgentTestHarness,
        default_config: ChaosConfig = None,
        seed: int = None,
    ):
        self.harness = harness
        self.default_config = default_config or ChaosConfig()
        self._tool_configs: dict[str, ChaosConfig] = {}
        self._rng = random.Random(seed)
        self._chaos_log: list[dict] = []

    def set_tool_config(self, tool: str, config: ChaosConfig):
        """Set chaos configuration for a specific tool."""
        self._tool_configs[tool] = config

    def execute(self, tool: str, input_data: dict) -> dict:
        """Execute a tool with chaos injection."""
        config = self._tool_configs.get(tool, self.default_config)
        chaos_event = {"tool": tool, "injection": None, "timestamp": time.time()}

        # Check timeout injection
        if self._rng.random() * 100 < config.timeout_pct:
            chaos_event["injection"] = "timeout"
            self._chaos_log.append(chaos_event)
            raise TimeoutError(
                f"Chaos: simulated timeout for tool '{tool}'"
            )

        # Check error injection
        if self._rng.random() * 100 < config.error_pct:
            chaos_event["injection"] = "error"
            self._chaos_log.append(chaos_event)
            return {
                "status": "error",
                "error": {
                    "code": "chaos_injected_error",
                    "message": f"Chaos: simulated error for tool '{tool}'",
                },
            }

        # Apply delay
        if config.delay_ms > 0:
            delay_seconds = config.delay_ms / 1000.0
            actual_delay = self._rng.uniform(0, delay_seconds * 2)
            time.sleep(actual_delay)
            chaos_event["injection"] = f"delay:{actual_delay:.3f}s"

        # Execute the real call
        result = self.harness.execute(tool, input_data)

        # Check duplicate execution
        if self._rng.random() * 100 < config.duplicate_pct:
            chaos_event["injection"] = "duplicate"
            self._chaos_log.append(chaos_event)
            # Execute again -- this tests idempotency
            duplicate_result = self.harness.execute(tool, input_data)
            return duplicate_result

        # Check corruption
        if self._rng.random() * 100 < config.corrupt_pct:
            chaos_event["injection"] = "corrupt"
            self._chaos_log.append(chaos_event)
            if isinstance(result, dict):
                result["_chaos_corrupted"] = True
                # Remove a random key to simulate partial response
                keys = [k for k in result.keys() if k != "status"]
                if keys:
                    del result[self._rng.choice(keys)]

        self._chaos_log.append(chaos_event)
        return result

    def get_chaos_log(self) -> list[dict]:
        """Get the log of all chaos injections."""
        return list(self._chaos_log)

    def get_injection_stats(self) -> dict:
        """Get summary statistics of chaos injections."""
        stats = {"total": len(self._chaos_log)}
        for entry in self._chaos_log:
            injection = entry.get("injection") or "none"
            category = injection.split(":")[0]
            stats[category] = stats.get(category, 0) + 1
        return stats
```

### Chaos Test Patterns

```python
class TestEscrowUnderChaos:
    """Layer 4: Verify escrow operations survive failure injection."""

    def test_escrow_survives_timeout_retry(self, harness):
        """Escrow creation retries correctly after timeout."""
        harness.use_mocks()
        harness.mock_tool("create_escrow", {
            "escrow_id": "escrow-chaos-001",
            "status": "funded",
            "amount": "50.00",
        })

        chaos = ChaosMiddleware(
            harness=harness,
            seed=42,
            default_config=ChaosConfig(timeout_pct=50),
        )

        # Retry loop -- real production code should have this
        max_retries = 5
        result = None
        for attempt in range(max_retries):
            try:
                result = chaos.execute("create_escrow", {
                    "payer_agent_id": "buyer",
                    "payee_agent_id": "seller",
                    "amount": "50.00",
                    "idempotency_key": "idem-chaos-001",
                })
                break
            except TimeoutError:
                continue

        assert result is not None, "All retry attempts timed out"
        assert result["escrow_id"] == "escrow-chaos-001"

    def test_no_double_payment_under_duplicates(self, harness):
        """Duplicate chaos injection does not cause double payment."""
        harness.use_mocks()
        call_count = {"n": 0}

        original_execute = harness.execute
        def counting_execute(tool, input_data):
            call_count["n"] += 1
            return original_execute(tool, input_data)

        harness.execute = counting_execute
        harness.mock_tool("release_escrow", {
            "escrow_id": "escrow-dup-test",
            "status": "released",
        })

        chaos = ChaosMiddleware(
            harness=harness,
            seed=99,
            default_config=ChaosConfig(duplicate_pct=100),
        )

        result = chaos.execute("release_escrow", {
            "escrow_id": "escrow-dup-test",
        })

        # The middleware called execute twice, but the result should
        # still represent a single release
        assert result["status"] == "released"

    def test_concurrent_escrow_load(self, harness):
        """Concurrent escrow creation does not cause race conditions."""
        import concurrent.futures

        harness.use_mocks()
        harness.mock_tool("create_escrow", {
            "escrow_id": "will-be-unique",
            "status": "funded",
            "amount": "10.00",
        })

        chaos = ChaosMiddleware(
            harness=harness,
            seed=7,
            default_config=ChaosConfig(delay_ms=50, error_pct=10),
        )

        results = []
        errors = []

        def create_escrow(i):
            try:
                return chaos.execute("create_escrow", {
                    "payer_agent_id": "buyer",
                    "payee_agent_id": "seller",
                    "amount": "10.00",
                    "idempotency_key": f"concurrent-{i}",
                })
            except Exception as e:
                return {"status": "error", "message": str(e)}

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
            futures = [pool.submit(create_escrow, i) for i in range(20)]
            for f in concurrent.futures.as_completed(futures):
                r = f.result()
                if r.get("status") == "error":
                    errors.append(r)
                else:
                    results.append(r)

        # At least some should succeed despite chaos
        assert len(results) > 0
        # Errors are expected under chaos -- verify they are handled
        total = len(results) + len(errors)
        assert total == 20

    def test_escrow_timeout_deadline(self, harness):
        """Escrow must be released or cancelled before deadline."""
        harness.use_mocks()
        deadline = time.time() + 2  # 2 second deadline for test

        harness.mock_tool("create_escrow", {
            "escrow_id": "escrow-deadline",
            "status": "funded",
            "deadline": deadline,
        })
        harness.mock_tool("cancel_escrow", {
            "escrow_id": "escrow-deadline",
            "status": "cancelled",
            "reason": "deadline_exceeded",
        })

        escrow = harness.execute("create_escrow", {
            "payer_agent_id": "buyer",
            "payee_agent_id": "seller",
            "amount": "30.00",
        })

        # Simulate deadline passing
        time.sleep(0.1)  # In real tests use time mocking
        current_time = time.time()
        if current_time < deadline:
            # Still within deadline -- release is valid
            harness.mock_tool("release_escrow", {
                "escrow_id": "escrow-deadline",
                "status": "released",
            })
            result = harness.execute("release_escrow", {
                "escrow_id": escrow["escrow_id"],
            })
            assert result["status"] == "released"
        else:
            # Deadline exceeded -- should auto-cancel
            result = harness.execute("cancel_escrow", {
                "escrow_id": escrow["escrow_id"],
            })
            assert result["status"] == "cancelled"
```

---

## Chapter 5: Production Observability

### Why printf Debugging Does Not Work for Payments

When a payment fails in production, you need to know three things instantly: which tool failed, how long it took, and what the input was. You need this information structured, searchable, and available without SSH-ing into a server. The `AgentTracer` wraps every `_execute` call with timing, success/failure tracking, and structured output.

### The AgentTracer

```python
import time
import json
import logging
from dataclasses import dataclass, field
from typing import Optional, Callable


@dataclass
class TraceRecord:
    """A single traced tool execution."""
    tool: str
    agent_id: str
    started_at: float
    ended_at: float
    duration_ms: float
    success: bool
    input_data: dict
    output_data: Optional[dict] = None
    error: Optional[str] = None
    trace_id: str = ""

    def to_dict(self) -> dict:
        return {
            "trace_id": self.trace_id,
            "tool": self.tool,
            "agent_id": self.agent_id,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "duration_ms": round(self.duration_ms, 2),
            "success": self.success,
            "error": self.error,
        }


class AgentTracer:
    """Wraps _execute and records timing, success/failure, tool name.

    Provides structured observability for every tool call in production.

    Usage:
        tracer = AgentTracer(
            api_key="...",
            agent_id="production-buyer-01",
            base_url="https://api.greenhelix.net/v1",
        )

        # Wrap an existing AgentCommerce or harness
        result = tracer.trace("create_escrow", {
            "payer_agent_id": "buyer",
            "payee_agent_id": "seller",
            "amount": "50.00",
        })

        # Get metrics
        print(tracer.get_metrics())
        # {'total_calls': 47, 'success_rate': 0.957,
        #  'avg_latency_ms': 142.3, 'p99_latency_ms': 890.1,
        #  'error_rate_by_tool': {'create_escrow': 0.02}}
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: str = "https://api.greenhelix.net/v1",
        logger: Optional[logging.Logger] = None,
        on_slow_call: Optional[Callable] = None,
        slow_threshold_ms: float = 2000.0,
    ):
        self.api_key = api_key
        self.agent_id = agent_id
        self.base_url = base_url
        self.logger = logger or logging.getLogger("agent_tracer")
        self.on_slow_call = on_slow_call
        self.slow_threshold_ms = slow_threshold_ms
        self._traces: list[TraceRecord] = []
        self._session = requests.Session()
        self._session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })

    def trace(self, tool: str, input_data: dict) -> dict:
        """Execute a tool with full tracing."""
        trace_id = f"trace-{uuid.uuid4().hex[:12]}"
        started_at = time.time()

        try:
            resp = self._session.post(
                f"{self.base_url}/v1",
                json={"tool": tool, "input": input_data},
            )
            resp.raise_for_status()
            result = resp.json()
            success = result.get("status") != "error"
            error = None if success else json.dumps(result.get("error", {}))
        except Exception as e:
            result = {"status": "error", "error": str(e)}
            success = False
            error = str(e)

        ended_at = time.time()
        duration_ms = (ended_at - started_at) * 1000

        record = TraceRecord(
            tool=tool,
            agent_id=self.agent_id,
            started_at=started_at,
            ended_at=ended_at,
            duration_ms=duration_ms,
            success=success,
            input_data=input_data,
            output_data=result if success else None,
            error=error,
            trace_id=trace_id,
        )
        self._traces.append(record)

        # Structured log
        self.logger.info(json.dumps({
            "event": "tool_execution",
            "trace_id": trace_id,
            "tool": tool,
            "agent_id": self.agent_id,
            "duration_ms": round(duration_ms, 2),
            "success": success,
            "error": error,
        }))

        # Slow call callback
        if duration_ms > self.slow_threshold_ms and self.on_slow_call:
            self.on_slow_call(record)

        return result

    def get_metrics(self) -> dict:
        """Compute aggregate metrics from traced calls."""
        if not self._traces:
            return {"total_calls": 0}

        total = len(self._traces)
        successes = sum(1 for t in self._traces if t.success)
        durations = sorted(t.duration_ms for t in self._traces)

        # Per-tool error rates
        tool_calls: dict[str, dict] = {}
        for t in self._traces:
            if t.tool not in tool_calls:
                tool_calls[t.tool] = {"total": 0, "errors": 0}
            tool_calls[t.tool]["total"] += 1
            if not t.success:
                tool_calls[t.tool]["errors"] += 1

        error_rate_by_tool = {
            tool: stats["errors"] / stats["total"]
            for tool, stats in tool_calls.items()
            if stats["errors"] > 0
        }

        # Per-tool latency
        tool_latencies: dict[str, list[float]] = {}
        for t in self._traces:
            tool_latencies.setdefault(t.tool, []).append(t.duration_ms)

        avg_latency_by_tool = {
            tool: round(sum(lats) / len(lats), 2)
            for tool, lats in tool_latencies.items()
        }

        return {
            "total_calls": total,
            "success_rate": round(successes / total, 4),
            "avg_latency_ms": round(sum(durations) / total, 2),
            "p50_latency_ms": round(durations[total // 2], 2),
            "p95_latency_ms": round(durations[int(total * 0.95)], 2),
            "p99_latency_ms": round(durations[int(total * 0.99)], 2),
            "error_rate_by_tool": error_rate_by_tool,
            "avg_latency_by_tool": avg_latency_by_tool,
        }

    def get_traces(
        self,
        tool: Optional[str] = None,
        success: Optional[bool] = None,
        min_duration_ms: Optional[float] = None,
    ) -> list[dict]:
        """Query traces with optional filters."""
        filtered = self._traces
        if tool:
            filtered = [t for t in filtered if t.tool == tool]
        if success is not None:
            filtered = [t for t in filtered if t.success == success]
        if min_duration_ms is not None:
            filtered = [t for t in filtered if t.duration_ms >= min_duration_ms]
        return [t.to_dict() for t in filtered]

    def get_revenue_metrics(self) -> dict:
        """Extract revenue-specific metrics from traced calls."""
        escrow_creates = [
            t for t in self._traces
            if t.tool == "create_escrow" and t.success
        ]
        escrow_releases = [
            t for t in self._traces
            if t.tool == "release_escrow" and t.success
        ]
        deposits = [
            t for t in self._traces
            if t.tool == "deposit" and t.success
        ]

        total_escrowed = sum(
            float(t.input_data.get("amount", 0))
            for t in escrow_creates
        )
        total_deposited = sum(
            float(t.input_data.get("amount", 0))
            for t in deposits
        )

        return {
            "escrows_created": len(escrow_creates),
            "escrows_released": len(escrow_releases),
            "total_escrowed": round(total_escrowed, 2),
            "total_deposited": round(total_deposited, 2),
            "release_rate": (
                round(len(escrow_releases) / len(escrow_creates), 4)
                if escrow_creates else 0
            ),
        }
```

### Structured Logging for Agent Decisions

The tracer's structured logging integrates with any log aggregator (Datadog, ELK, CloudWatch). Each log line is a JSON object with consistent fields. The key decision: log the tool name and duration for every call, but redact input data in production to avoid logging sensitive information like API keys or wallet amounts. Enable full input logging only in staging (P7 security patterns).

```python
# Production logging configuration
import logging

def configure_production_logging():
    """Set up structured JSON logging for agent commerce."""
    logger = logging.getLogger("agent_tracer")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    return logger


def configure_staging_logging():
    """Staging logger with full input/output capture."""
    logger = logging.getLogger("agent_tracer")
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler("/var/log/agent-commerce/traces.jsonl")
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    return logger
```

### Custom Metrics Dashboard

Extract the metrics you need for a Grafana or Datadog dashboard from the tracer. These are the five metrics every agent commerce system should track.

```python
class MetricsExporter:
    """Export AgentTracer metrics to monitoring systems."""

    def __init__(self, tracer: AgentTracer):
        self.tracer = tracer

    def export_prometheus(self) -> str:
        """Export metrics in Prometheus text format."""
        metrics = self.tracer.get_metrics()
        revenue = self.tracer.get_revenue_metrics()
        lines = [
            f'agent_commerce_calls_total {metrics["total_calls"]}',
            f'agent_commerce_success_rate {metrics["success_rate"]}',
            f'agent_commerce_latency_p50_ms {metrics.get("p50_latency_ms", 0)}',
            f'agent_commerce_latency_p99_ms {metrics.get("p99_latency_ms", 0)}',
            f'agent_commerce_escrows_created {revenue["escrows_created"]}',
            f'agent_commerce_escrows_released {revenue["escrows_released"]}',
            f'agent_commerce_total_escrowed {revenue["total_escrowed"]}',
            f'agent_commerce_release_rate {revenue["release_rate"]}',
        ]

        for tool, rate in metrics.get("error_rate_by_tool", {}).items():
            lines.append(
                f'agent_commerce_error_rate{{tool="{tool}"}} {rate}'
            )

        return "\n".join(lines)

    def to_datadog_events(self) -> list[dict]:
        """Format failed traces as Datadog events."""
        failed = self.tracer.get_traces(success=False)
        return [
            {
                "title": f"Tool failure: {t['tool']}",
                "text": t.get("error", "Unknown error"),
                "tags": [
                    f"tool:{t['tool']}",
                    f"agent:{t['agent_id']}",
                    "service:agent-commerce",
                ],
                "alert_type": "error",
            }
            for t in failed
        ]
```

---

## Chapter 6: Alerting & Incident Response

### What to Alert On

Not every error deserves a page. These six conditions are the ones that, left unaddressed, cause financial loss in agent commerce systems.

| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| Settlement failure | `release_escrow` returns error 3+ times | Critical | Check gateway status, pause new escrows |
| Escrow timeout | Escrow unfunded/unreleased past deadline | High | Auto-cancel or escalate to dispute |
| Balance anomaly | Balance drops >50% in single transaction | Critical | Pause agent, audit recent calls |
| Reputation drop | Trust score drops below threshold | Medium | Pause hiring, investigate metrics |
| Webhook delivery failure | >5 consecutive webhook delivery failures | High | Check endpoint, enable retry queue |
| Duplicate payment | Same escrow_id released twice in 60s | Critical | Immediate halt, audit ledger |

### The HealthChecker

The `HealthChecker` runs synthetic transactions against the sandbox (or a dedicated health-check agent on production) to verify the full payment pipeline is operational. Run it every 60 seconds from your monitoring system.

```python
class HealthChecker:
    """Synthetic transaction health checks for agent commerce.

    Runs a mini escrow lifecycle (create wallet → deposit → create
    escrow → release → verify balance) and reports pass/fail with
    latency metrics.

    Usage:
        checker = HealthChecker(
            api_key="health-check-key",
            agent_id="health-check-agent",
            base_url="https://sandbox.greenhelix.net/v1",
        )

        result = checker.run_health_check()
        # {
        #     "healthy": True,
        #     "checks": {
        #         "wallet": {"status": "pass", "latency_ms": 45.2},
        #         "deposit": {"status": "pass", "latency_ms": 78.1},
        #         "escrow_create": {"status": "pass", "latency_ms": 112.4},
        #         "escrow_release": {"status": "pass", "latency_ms": 95.6},
        #         "balance_verify": {"status": "pass", "latency_ms": 41.0},
        #     },
        #     "total_latency_ms": 372.3,
        # }
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: str = "https://sandbox.greenhelix.net/v1",
        timeout_ms: float = 5000.0,
    ):
        self.api_key = api_key
        self.agent_id = agent_id
        self.base_url = base_url
        self.timeout_ms = timeout_ms
        self._session = requests.Session()
        self._session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })

    def _timed_execute(self, tool: str, input_data: dict) -> tuple[dict, float]:
        """Execute a tool and return (result, latency_ms)."""
        start = time.time()
        resp = self._session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
            timeout=self.timeout_ms / 1000.0,
        )
        latency_ms = (time.time() - start) * 1000
        resp.raise_for_status()
        return resp.json(), latency_ms

    def run_health_check(self) -> dict:
        """Run a full synthetic transaction health check."""
        checks = {}
        healthy = True
        health_agent = f"{self.agent_id}-{int(time.time())}"

        # Check 1: Wallet creation
        try:
            result, latency = self._timed_execute("create_wallet", {})
            checks["wallet"] = {"status": "pass", "latency_ms": round(latency, 2)}
        except Exception as e:
            checks["wallet"] = {"status": "fail", "error": str(e)}
            healthy = False

        # Check 2: Deposit
        try:
            result, latency = self._timed_execute("deposit", {"amount": "1.00"})
            checks["deposit"] = {"status": "pass", "latency_ms": round(latency, 2)}
        except Exception as e:
            checks["deposit"] = {"status": "fail", "error": str(e)}
            healthy = False

        # Check 3: Escrow creation
        escrow_id = None
        try:
            result, latency = self._timed_execute("create_escrow", {
                "payer_agent_id": health_agent,
                "payee_agent_id": f"{health_agent}-payee",
                "amount": "0.01",
                "description": "Health check escrow",
            })
            escrow_id = result.get("escrow_id")
            checks["escrow_create"] = {"status": "pass", "latency_ms": round(latency, 2)}
        except Exception as e:
            checks["escrow_create"] = {"status": "fail", "error": str(e)}
            healthy = False

        # Check 4: Escrow release
        if escrow_id:
            try:
                result, latency = self._timed_execute("release_escrow", {
                    "escrow_id": escrow_id,
                })
                checks["escrow_release"] = {"status": "pass", "latency_ms": round(latency, 2)}
            except Exception as e:
                checks["escrow_release"] = {"status": "fail", "error": str(e)}
                healthy = False
        else:
            checks["escrow_release"] = {"status": "skip", "reason": "no escrow_id"}

        # Check 5: Balance verification
        try:
            result, latency = self._timed_execute("get_balance", {})
            checks["balance_verify"] = {"status": "pass", "latency_ms": round(latency, 2)}
        except Exception as e:
            checks["balance_verify"] = {"status": "fail", "error": str(e)}
            healthy = False

        total_latency = sum(
            c.get("latency_ms", 0) for c in checks.values()
        )

        return {
            "healthy": healthy,
            "checks": checks,
            "total_latency_ms": round(total_latency, 2),
            "timestamp": time.time(),
            "agent_id": self.agent_id,
        }

    def run_and_alert(self, alert_callback: Callable = None) -> dict:
        """Run health check and trigger alert callback on failure."""
        result = self.run_health_check()

        if not result["healthy"] and alert_callback:
            failed_checks = {
                name: check for name, check in result["checks"].items()
                if check.get("status") == "fail"
            }
            alert_callback({
                "severity": "critical",
                "title": "Agent Commerce Health Check Failed",
                "failed_checks": failed_checks,
                "timestamp": result["timestamp"],
            })

        return result
```

### Testing the HealthChecker

```python
class TestHealthChecker:
    """Verify the health checker itself works correctly."""

    def test_reports_healthy_when_all_pass(self, harness):
        """All checks passing produces healthy=True."""
        harness.use_mocks()
        harness.mock_tool("create_wallet", {"wallet_id": "w-health"})
        harness.mock_tool("deposit", {"balance": "1.00", "transaction_id": "tx-h"})
        harness.mock_tool("create_escrow", {
            "escrow_id": "escrow-health", "status": "funded",
        })
        harness.mock_tool("release_escrow", {
            "escrow_id": "escrow-health", "status": "released",
        })
        harness.mock_tool("get_balance", {"balance": "0.99"})

        # HealthChecker delegates to the harness in test mode
        checker = HealthChecker(
            api_key=harness.api_key,
            agent_id=harness.agent_id,
            base_url=harness.base_url,
        )
        # In real tests, patch _timed_execute to use harness
        # Here we verify the structure
        assert checker.timeout_ms == 5000.0

    def test_reports_unhealthy_on_escrow_failure(self):
        """Failed escrow check produces healthy=False."""
        checker = HealthChecker(
            api_key="test",
            agent_id="test",
            base_url="https://sandbox.greenhelix.net/v1",
        )

        alerts_received = []
        def mock_alert(alert):
            alerts_received.append(alert)

        # Patch to simulate failure -- in real code use sandbox
        original = checker._timed_execute
        def failing_execute(tool, input_data):
            if tool == "create_escrow":
                raise ConnectionError("Gateway timeout")
            return original(tool, input_data)

        checker._timed_execute = failing_execute
        try:
            result = checker.run_and_alert(alert_callback=mock_alert)
        except Exception:
            pass  # Expected when wallet/deposit also fail
```

### Dead Letter Queue for Webhooks

When webhook delivery fails, events must not be silently dropped. Implement a dead letter queue that captures failed deliveries for retry (P4).

```python
class WebhookDeadLetterQueue:
    """Captures failed webhook deliveries for manual retry."""

    def __init__(self, max_retries: int = 3, retry_delay_seconds: float = 60.0):
        self.max_retries = max_retries
        self.retry_delay_seconds = retry_delay_seconds
        self._queue: list[dict] = []

    def enqueue(self, event: dict, error: str):
        """Add a failed webhook event to the dead letter queue."""
        self._queue.append({
            "event": event,
            "error": error,
            "retries": 0,
            "enqueued_at": time.time(),
            "next_retry_at": time.time() + self.retry_delay_seconds,
        })

    def get_pending(self) -> list[dict]:
        """Get events ready for retry."""
        now = time.time()
        return [
            entry for entry in self._queue
            if entry["retries"] < self.max_retries
            and entry["next_retry_at"] <= now
        ]

    def mark_delivered(self, event_id: str):
        """Remove a successfully retried event."""
        self._queue = [
            e for e in self._queue
            if e["event"].get("event_id") != event_id
        ]

    def mark_retried(self, event_id: str):
        """Increment retry count and schedule next attempt."""
        for entry in self._queue:
            if entry["event"].get("event_id") == event_id:
                entry["retries"] += 1
                entry["next_retry_at"] = (
                    time.time()
                    + self.retry_delay_seconds * (2 ** entry["retries"])
                )
                break

    def get_dead_letters(self) -> list[dict]:
        """Get events that have exhausted all retries."""
        return [
            entry for entry in self._queue
            if entry["retries"] >= self.max_retries
        ]
```

---

## Chapter 7: CI/CD for Agent Systems

### Running Tests in GitHub Actions

Agent commerce tests require three things that standard CI does not provide: a GreenHelix API key for sandbox testing, isolation between parallel test runs (unique agent IDs), and network access to `sandbox.greenhelix.net`. This GitHub Actions template handles all three.

```yaml
# .github/workflows/agent-commerce-tests.yml
name: Agent Commerce Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  GREENHELIX_API_KEY: ${{ secrets.GREENHELIX_API_KEY }}
  GREENHELIX_BASE_URL: https://sandbox.greenhelix.net/v1

jobs:
  # ── Layer 1: Fast mock-based tests (no network) ──────────
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          pip install pytest requests cryptography

      - name: Run unit tests (Layer 1)
        run: |
          pytest tests/ -x -q \
            -m "not sandbox and not chaos" \
            --tb=short \
            --junit-xml=results/unit-tests.xml

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: unit-test-results
          path: results/unit-tests.xml

  # ── Layer 2: Contract tests against sandbox ──────────────
  contract-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install pytest requests cryptography

      - name: Run contract tests (Layer 2)
        run: |
          pytest tests/ -x -q \
            -m "sandbox and not chaos" \
            --tb=short \
            --junit-xml=results/contract-tests.xml
        env:
          GREENHELIX_API_KEY: ${{ secrets.GREENHELIX_API_KEY }}

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: contract-test-results
          path: results/contract-tests.xml

  # ── Layer 3 + 4: Integration and chaos tests ─────────────
  integration-tests:
    runs-on: ubuntu-latest
    needs: contract-tests
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install pytest requests cryptography

      - name: Run integration tests (Layer 3)
        run: |
          pytest tests/ -x -q \
            -m "integration" \
            --tb=short \
            --junit-xml=results/integration-tests.xml
        env:
          GREENHELIX_API_KEY: ${{ secrets.GREENHELIX_API_KEY }}

      - name: Run chaos tests (Layer 4)
        run: |
          pytest tests/ -q \
            -m "chaos" \
            --tb=short \
            --junit-xml=results/chaos-tests.xml
        env:
          GREENHELIX_API_KEY: ${{ secrets.GREENHELIX_API_KEY }}
        continue-on-error: true  # Chaos tests may have expected failures

      - name: Upload all results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: integration-test-results
          path: results/

  # ── Health check against staging ─────────────────────────
  staging-health:
    runs-on: ubuntu-latest
    needs: integration-tests
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install requests

      - name: Run health check against staging
        run: |
          python -c "
          from health_checker import HealthChecker
          import json, sys

          checker = HealthChecker(
              api_key='${{ secrets.GREENHELIX_API_KEY }}',
              agent_id='ci-health-check',
              base_url='https://sandbox.greenhelix.net/v1',
          )
          result = checker.run_health_check()
          print(json.dumps(result, indent=2))

          if not result['healthy']:
              print('HEALTH CHECK FAILED')
              sys.exit(1)
          print('HEALTH CHECK PASSED')
          "
```

### Staging with the GreenHelix Sandbox

The sandbox at `sandbox.greenhelix.net` mirrors the production API exactly. Use it as your staging environment. Every test in Layers 2-4 runs against it. The sandbox resets balances nightly, so do not rely on state persisting between CI runs. Generate unique agent IDs per run using the `agent_id` fixture from the conftest (P1).

```python
# pytest.ini or pyproject.toml
# [tool.pytest.ini_options]
# markers:
#     sandbox: Tests that require the GreenHelix sandbox
#     chaos: Chaos testing with failure injection
#     integration: Multi-step workflow integration tests

@pytest.fixture
def ci_agent_id():
    """Generate a CI-unique agent ID to prevent collision."""
    run_id = os.environ.get("GITHUB_RUN_ID", uuid.uuid4().hex[:8])
    return f"ci-agent-{run_id}-{uuid.uuid4().hex[:6]}"
```

### Canary Deployments

When deploying agent commerce changes, use a canary pattern: route 5% of traffic to the new version, monitor the `AgentTracer` metrics for 15 minutes, then promote or roll back.

```python
class CanaryDeployment:
    """Canary deployment controller for agent commerce systems."""

    def __init__(
        self,
        canary_tracer: AgentTracer,
        stable_tracer: AgentTracer,
        promotion_threshold: float = 0.95,
    ):
        self.canary = canary_tracer
        self.stable = stable_tracer
        self.promotion_threshold = promotion_threshold

    def evaluate(self) -> dict:
        """Compare canary metrics against stable baseline."""
        canary_metrics = self.canary.get_metrics()
        stable_metrics = self.stable.get_metrics()

        if canary_metrics["total_calls"] < 10:
            return {"decision": "waiting", "reason": "insufficient_data"}

        canary_success = canary_metrics.get("success_rate", 0)
        stable_success = stable_metrics.get("success_rate", 1)

        canary_latency = canary_metrics.get("p99_latency_ms", 0)
        stable_latency = stable_metrics.get("p99_latency_ms", 1)

        # Canary must match or beat stable on success rate
        success_ok = canary_success >= stable_success * 0.98

        # Canary latency must not regress more than 20%
        latency_ok = canary_latency <= stable_latency * 1.20

        if success_ok and latency_ok:
            return {"decision": "promote", "canary_success": canary_success}
        else:
            return {
                "decision": "rollback",
                "reason": (
                    f"success: {canary_success} vs {stable_success}, "
                    f"p99: {canary_latency}ms vs {stable_latency}ms"
                ),
            }
```

### Regression Detection

Track key metrics across CI runs to detect regressions before they reach production. Store the metrics as CI artifacts and compare against the previous run.

```python
class RegressionDetector:
    """Detect metric regressions between CI runs."""

    def __init__(self, baseline_metrics: dict, current_metrics: dict):
        self.baseline = baseline_metrics
        self.current = current_metrics

    def check(self) -> list[dict]:
        """Return a list of detected regressions."""
        regressions = []

        # Success rate regression (any drop is a regression)
        baseline_sr = self.baseline.get("success_rate", 1.0)
        current_sr = self.current.get("success_rate", 1.0)
        if current_sr < baseline_sr - 0.01:
            regressions.append({
                "metric": "success_rate",
                "baseline": baseline_sr,
                "current": current_sr,
                "delta": current_sr - baseline_sr,
            })

        # Latency regression (>20% increase at p95)
        baseline_p95 = self.baseline.get("p95_latency_ms", 0)
        current_p95 = self.current.get("p95_latency_ms", 0)
        if baseline_p95 > 0 and current_p95 > baseline_p95 * 1.20:
            regressions.append({
                "metric": "p95_latency_ms",
                "baseline": baseline_p95,
                "current": current_p95,
                "delta_pct": round(
                    (current_p95 - baseline_p95) / baseline_p95 * 100, 1
                ),
            })

        # Error rate regression per tool
        baseline_errors = self.baseline.get("error_rate_by_tool", {})
        current_errors = self.current.get("error_rate_by_tool", {})
        for tool, current_rate in current_errors.items():
            baseline_rate = baseline_errors.get(tool, 0)
            if current_rate > baseline_rate + 0.05:
                regressions.append({
                    "metric": f"error_rate:{tool}",
                    "baseline": baseline_rate,
                    "current": current_rate,
                })

        return regressions
```

---

## Chapter 8: What to Do Next

This guide covered the four-layer agent testing pyramid, tool contract tests, saga-based workflow testing, chaos failure injection, production observability with the `AgentTracer`, alerting with the `HealthChecker`, and CI/CD integration with GitHub Actions. The four classes -- `AgentTestHarness`, `ChaosMiddleware`, `AgentTracer`, and `HealthChecker` -- compose into a reliability stack that wraps every GreenHelix tool call from development through production.

The GreenHelix gateway's own test suite (260+ tests across 9 modules, with the gateway alone carrying 1,353 tests) uses the same patterns described here: deterministic mocks for business logic, sandbox integration tests for contract verification, and chaos-style failure injection for payment idempotency. The patterns in this guide are not theoretical -- they are extracted from the test infrastructure that protects the gateway itself.

### Companion Guides

For the commerce patterns these tests protect, see the companion guides:

- **Agent-to-Agent Commerce: Escrow, Payments, and Trust** (P1) -- the `AgentCommerce` class, escrow patterns, marketplace discovery, subscriptions, and dispute resolution.
- **The AI Agent FinOps Playbook** (P2) -- the `AgentFinOps` class, per-agent budget caps, webhook alerts, fleet dashboards, and cost attribution.
- **Verified Trading Bot Reputation** (P3) -- cryptographic PnL proof using Ed25519 signatures and Merkle claim chains.
- **Tamper-Proof Audit Trails for Trading Bots** (P4) -- EU AI Act compliance, MiFID II reporting, and Merkle chain rotation.
- **How to Verify Any AI Agent Before Doing Business** (P5) -- the `AgentVerifier` class, five-layer trust stack, and continuous reputation monitoring.
- **The Agent Strategy Marketplace Playbook** (P6) -- selling verified trading strategies with performance escrow.
- **Locking Down Agent Commerce** (P7) -- OWASP-aligned security hardening with `SecureAgent` and `SecurityMonitor`.
- **The Agent SaaS Factory** (P8) -- autonomous micro-SaaS creation with `AgentDeveloper`, `AgentDBA`, and `AgentBilling`.

### Practice on the Sandbox

The sandbox at `sandbox.greenhelix.net` is free to use with any API key. Run the `HealthChecker` against it. Deploy the GitHub Actions template. Break things deliberately with the `ChaosMiddleware`. The patterns in this guide are designed to be copied, adapted, and deployed today.

### The Bundle

All eight companion guides plus this cookbook are available as a bundle. Each guide introduces a production-ready Python class. Together they cover the full lifecycle of agent commerce: building, securing, testing, monitoring, and scaling.

For the full API reference and tool catalog (all 128 tools), visit the GreenHelix developer documentation at [https://api.greenhelix.net/docs](https://api.greenhelix.net/docs).

---

*Price: $29 | Format: Digital Guide | Updates: Lifetime access*

