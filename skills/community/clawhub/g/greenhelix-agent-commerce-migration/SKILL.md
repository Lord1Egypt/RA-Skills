---
name: greenhelix-agent-commerce-migration
version: "1.3.1"
description: "Agent Commerce Migration Guide: Retrofit Your REST APIs for Autonomous Agent Buyers. Step-by-step migration guide for teams with existing REST APIs that need to add agent commerce capabilities. Assessment framework, x402 retrofit patterns, authentication bridging, gradual migration strategies, testing, rollback procedures, and performance comparison."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [migration, rest-api, retrofit, x402, guide, greenhelix, openclaw, ai-agent]
price_usd: 39.0
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
# Agent Commerce Migration Guide: Retrofit Your REST APIs for Autonomous Agent Buyers

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `GREENHELIX_API_KEY`: API authentication for GreenHelix gateway (read/write access to purchased API tools only)
> - `AGENT_SIGNING_KEY`: Cryptographic signing key for agent identity (Ed25519 key pair for request signing)


You have a working REST API. It serves human users through a web frontend. Maybe it powers a SaaS product, a data marketplace, or a specialized computation service. The endpoints are tested, the authentication works, and your customers are happy. Now AI agents want to buy your services programmatically. They don't want to fill out a signup form, navigate a dashboard, or read your documentation the way a human does. They want to discover your capabilities through structured metadata, negotiate a price via HTTP headers, pay per call with cryptographic proof, and consume your response — all in a single request cycle. The instinct is to build a separate "agent API" from scratch, but that is the wrong move. You already have the hard part: working business logic behind stable endpoints. What you need is a commerce layer on top of what exists. This guide shows how to retrofit any REST API with agent commerce capabilities: x402 payment headers for per-call pricing, GreenHelix escrow integration for trustless settlement, Ed25519 identity verification for agent authentication, and structured service discovery so agents can find and evaluate your offerings without human intervention. The approach is gradual. You can migrate one endpoint at a time while existing human users continue hitting the same URLs with the same authentication they have always used. No big bang rewrite. No downtime. No breaking changes. By the end of this guide you will have a complete migration framework — assessment tools, adapter classes, middleware patterns, validation harnesses, and rollback procedures — that transforms your existing REST API into an agent-ready commerce platform without sacrificing anything that already works.
> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## What You'll Learn
- Chapter 1: Migration Assessment
- Chapter 2: LegacyApiAdapter Class
- Chapter 3: x402 Retrofit Patterns
- Chapter 4: Authentication Bridging
- Chapter 5: Gradual Migration Strategies
- Chapter 6: MigrationValidator Class
- Chapter 7: Testing Migration
- Chapter 8: Performance Comparison
- What's Next

## Full Guide

# Agent Commerce Migration Guide: Retrofit Your REST APIs for Autonomous Agent Buyers

You have a working REST API. It serves human users through a web frontend. Maybe it powers a SaaS product, a data marketplace, or a specialized computation service. The endpoints are tested, the authentication works, and your customers are happy. Now AI agents want to buy your services programmatically. They don't want to fill out a signup form, navigate a dashboard, or read your documentation the way a human does. They want to discover your capabilities through structured metadata, negotiate a price via HTTP headers, pay per call with cryptographic proof, and consume your response — all in a single request cycle. The instinct is to build a separate "agent API" from scratch, but that is the wrong move. You already have the hard part: working business logic behind stable endpoints. What you need is a commerce layer on top of what exists. This guide shows how to retrofit any REST API with agent commerce capabilities: x402 payment headers for per-call pricing, GreenHelix escrow integration for trustless settlement, Ed25519 identity verification for agent authentication, and structured service discovery so agents can find and evaluate your offerings without human intervention. The approach is gradual. You can migrate one endpoint at a time while existing human users continue hitting the same URLs with the same authentication they have always used. No big bang rewrite. No downtime. No breaking changes. By the end of this guide you will have a complete migration framework — assessment tools, adapter classes, middleware patterns, validation harnesses, and rollback procedures — that transforms your existing REST API into an agent-ready commerce platform without sacrificing anything that already works.

---


> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## Chapter 1: Migration Assessment

Before writing any migration code, you need an honest evaluation of where your API stands today and what it will take to make it agent-commerce ready. This assessment phase saves weeks of wasted effort by identifying blockers early, surfacing hidden dependencies, and prioritizing the endpoints that will generate the most agent revenue with the least migration risk.

### The Four Pillars of Agent Commerce Readiness

Every REST API migration touches four areas. Your current implementation might already satisfy some of them partially, but each one needs explicit attention.

**Authentication readiness.** Agents do not use browser cookies or OAuth redirect flows. They present cryptographic identity — typically an Ed25519 public key with a signed request payload. Your API needs to verify these signatures alongside whatever auth mechanism already exists. The question is not whether you can replace your current auth, but whether you can layer agent auth on top of it.

**Payment readiness.** Human users pay through subscriptions, invoices, or credit cards processed asynchronously. Agent commerce is synchronous: the agent includes a payment token in the request header, your API verifies it before processing, and settlement happens atomically. If your API currently has no concept of per-call pricing, you need to add one. If it already has usage-based billing, you have a head start.

**Response structure readiness.** Human-facing APIs often return loosely structured JSON with messages meant for UI rendering — status strings like "Success!", nested error objects with display text, pagination metadata mixed into the response body. Agents need machine-parseable responses with predictable schemas, consistent error codes, and clear separation between data and metadata. The more disciplined your current response format, the less transformation work ahead.

**Discovery readiness.** Agents find services through structured manifests — A2A protocol cards, OpenAPI specifications with pricing extensions, or capability registries. If your API has no machine-readable description of what it offers and what it costs, agents cannot evaluate it. Most REST APIs have some form of documentation, but rarely in a format an agent can consume autonomously.

### The Assessment Checklist

Run through this checklist for every endpoint you are considering for migration. Score each item 0 (not present), 1 (partially present), or 2 (fully present):

```python
MIGRATION_ASSESSMENT = {
    "authentication": [
        "Stateless auth supported (tokens, not sessions)",
        "Auth info passed via headers (not cookies)",
        "Auth can be extended without breaking existing clients",
        "Rate limiting is per-identity, not per-IP",
    ],
    "payments": [
        "Usage tracking exists at per-call granularity",
        "Pricing model defined for individual operations",
        "Billing system can handle micropayments",
        "Idempotency keys supported on payment-related endpoints",
    ],
    "response_structure": [
        "Consistent JSON envelope across all endpoints",
        "Error responses use numeric codes, not just strings",
        "Pagination uses cursors, not page numbers",
        "Response schemas are documented and stable",
    ],
    "discovery": [
        "OpenAPI / Swagger spec exists and is current",
        "Endpoint capabilities described in machine-readable format",
        "Versioning strategy is explicit (URL or header)",
        "Health check endpoint exists",
    ],
}

def score_api(scores: dict[str, list[int]]) -> dict:
    results = {}
    for category, items in scores.items():
        total = sum(items)
        max_score = len(MIGRATION_ASSESSMENT[category]) * 2
        results[category] = {
            "score": total,
            "max": max_score,
            "percentage": round(total / max_score * 100),
            "ready": total >= max_score * 0.75,
        }
    results["overall_ready"] = all(r["ready"] for r in results.values())
    return results
```

An overall score above 75% means you can proceed with migration directly. Between 50% and 75%, plan for prerequisite work on the weakest pillar before starting. Below 50%, consider whether the API needs structural improvements first — migration on top of a fragile foundation creates compounding problems.

### The LegacyApiAdapter Pattern Overview

The core architectural pattern for this migration is the `LegacyApiAdapter`: a wrapper class that sits between incoming agent requests and your existing endpoint handlers. It performs three functions. First, it intercepts agent-specific headers (x402 payment tokens, Ed25519 signatures, capability queries) and processes them before the request reaches your business logic. Second, it transforms your existing response format into the agent-expected envelope if needed. Third, it passes through requests from non-agent clients completely unchanged, so your existing users never notice the migration happened.

This is not a proxy in the traditional sense. It runs in the same process as your existing API, adds no network hops, and shares the same database connections and caches. Think of it as a decorator pattern applied at the HTTP layer.

### Identifying High-Value Migration Targets

Not every endpoint is worth migrating. Start with endpoints that satisfy three criteria:

**High agent utility.** Data retrieval endpoints (search, lookup, analytics) are the most immediately useful to agents. Agents are information consumers first. An endpoint that returns structured data an agent can act on is more valuable than a CRUD endpoint for managing user profiles.

**Low migration complexity.** Endpoints with simple request/response schemas, no file uploads, no streaming responses, and no multi-step workflows are easiest to migrate. Save the complex ones for later phases.

**Clear pricing model.** You need to assign a per-call price. Endpoints where the cost of serving a request is predictable (fixed computation, bounded database queries) are easier to price than endpoints with variable resource consumption. If you cannot state a price, you are not ready to migrate that endpoint.

Rank your endpoints by (utility x 1/complexity x pricing_clarity) and migrate the top five first. This gives you a working agent commerce surface quickly, generates early revenue, and builds confidence in the migration pattern before tackling harder endpoints.

---

## Chapter 2: LegacyApiAdapter Class

The `LegacyApiAdapter` is the central abstraction for this entire migration. It wraps your existing endpoint handlers and adds agent commerce capabilities without modifying the underlying business logic. Every request flows through the adapter, which decides whether to apply agent commerce processing or pass the request through unchanged.

### Design Principles

The adapter follows three rules. First, zero regression: any request that worked before the adapter was installed must continue to work identically. Second, opt-in activation: agent commerce features activate only when the request contains agent-specific headers. Third, fail-open for humans: if agent commerce processing fails (payment verification timeout, identity service unavailable), non-agent requests still succeed. Agent requests fail explicitly with structured error responses.

### The Complete Adapter Class

```python
import time
import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional
from functools import wraps

import httpx
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse


class CallerType(str, Enum):
    HUMAN = "human"
    AGENT = "agent"
    UNKNOWN = "unknown"


@dataclass
class PricingConfig:
    """Per-endpoint pricing configuration."""
    price_usd: float
    currency: str = "USD"
    escrow_required: bool = True
    min_deposit: float = 0.01
    max_deposit: float = 100.00
    settlement_timeout_seconds: int = 300


@dataclass
class MigrationConfig:
    """Configuration for the adapter's behavior."""
    greenhelix_url: str = "https://api.greenhelix.net"
    greenhelix_api_key: str = ""
    verify_payments: bool = True
    verify_identity: bool = True
    transform_responses: bool = True
    pass_through_on_failure: bool = False
    pricing: dict[str, PricingConfig] = field(default_factory=dict)


@dataclass
class AgentContext:
    """Extracted agent information from request headers."""
    caller_type: CallerType
    agent_id: Optional[str] = None
    payment_token: Optional[str] = None
    signature: Optional[str] = None
    public_key: Optional[str] = None
    requested_capabilities: list[str] = field(default_factory=list)


class LegacyApiAdapter:
    """
    Wraps existing REST API endpoints with agent commerce capabilities.

    Intercepts agent-specific headers, verifies payments and identity,
    transforms responses, and passes through non-agent requests unchanged.
    """

    def __init__(self, config: MigrationConfig):
        self.config = config
        self._http_client = httpx.AsyncClient(
            base_url=config.greenhelix_url,
            timeout=10.0,
        )
        self._payment_cache: dict[str, float] = {}

    def classify_caller(self, request: Request) -> AgentContext:
        """Determine whether the request comes from a human or an agent."""
        payment_token = request.headers.get("x-402-payment-token")
        agent_id = request.headers.get("x-agent-id")
        signature = request.headers.get("x-agent-signature")
        public_key = request.headers.get("x-agent-public-key")

        if payment_token or agent_id:
            return AgentContext(
                caller_type=CallerType.AGENT,
                agent_id=agent_id,
                payment_token=payment_token,
                signature=signature,
                public_key=public_key,
            )

        user_agent = request.headers.get("user-agent", "")
        agent_indicators = ["bot", "agent", "crawler", "a2a-client"]
        if any(indicator in user_agent.lower() for indicator in agent_indicators):
            return AgentContext(caller_type=CallerType.AGENT, agent_id=agent_id)

        return AgentContext(caller_type=CallerType.HUMAN)

    async def verify_payment(
        self, payment_token: str, endpoint: str, price: PricingConfig
    ) -> dict:
        """Verify a payment token against GreenHelix escrow."""
        response = await self._http_client.post(
            "/v1/payments/verify",
            json={
                "token": payment_token,
                "expected_amount": str(price.price_usd),
                "currency": price.currency,
                "endpoint": endpoint,
            },
            headers={"Authorization": f"Bearer {self.config.greenhelix_api_key}"},
        )

        if response.status_code != 200:
            return {"valid": False, "error": response.text}

        result = response.json()
        return {
            "valid": result.get("verified", False),
            "escrow_id": result.get("escrow_id"),
            "amount": result.get("amount"),
        }

    async def verify_identity(self, ctx: AgentContext) -> dict:
        """Verify agent identity via Ed25519 signature."""
        if not ctx.public_key or not ctx.signature:
            return {"verified": False, "error": "Missing signature or public key"}

        response = await self._http_client.post(
            "/v1/identity/verify",
            json={
                "agent_id": ctx.agent_id,
                "public_key": ctx.public_key,
                "signature": ctx.signature,
            },
            headers={"Authorization": f"Bearer {self.config.greenhelix_api_key}"},
        )

        if response.status_code != 200:
            return {"verified": False, "error": response.text}

        return response.json()

    def transform_response(
        self, response_data: Any, endpoint: str, escrow_id: Optional[str] = None
    ) -> dict:
        """Transform legacy response format into agent-expected envelope."""
        return {
            "data": response_data,
            "meta": {
                "endpoint": endpoint,
                "timestamp": time.time(),
                "escrow_id": escrow_id,
                "schema_version": "1.0",
            },
        }

    def wrap_endpoint(self, endpoint_path: str):
        """
        Decorator that wraps an existing endpoint handler with agent commerce.

        Usage:
            adapter = LegacyApiAdapter(config)

            @app.get("/api/data")
            @adapter.wrap_endpoint("/api/data")
            async def get_data(request: Request):
                return {"results": [...]}
        """
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(request: Request, *args, **kwargs):
                ctx = self.classify_caller(request)

                # Pass through non-agent requests unchanged
                if ctx.caller_type == CallerType.HUMAN:
                    return await func(request, *args, **kwargs)

                # Agent request: verify payment if pricing is configured
                pricing = self.config.pricing.get(endpoint_path)
                escrow_id = None

                if pricing and self.config.verify_payments:
                    if not ctx.payment_token:
                        return JSONResponse(
                            status_code=402,
                            content={
                                "error": "payment_required",
                                "detail": "This endpoint requires payment",
                                "price": str(pricing.price_usd),
                                "currency": pricing.currency,
                                "payment_url": (
                                    f"{self.config.greenhelix_url}"
                                    f"/v1/payments/create"
                                ),
                            },
                            headers={
                                "X-Price": str(pricing.price_usd),
                                "X-Currency": pricing.currency,
                                "X-Payment-URL": (
                                    f"{self.config.greenhelix_url}"
                                    f"/v1/payments/create"
                                ),
                            },
                        )

                    payment_result = await self.verify_payment(
                        ctx.payment_token, endpoint_path, pricing
                    )
                    if not payment_result["valid"]:
                        return JSONResponse(
                            status_code=402,
                            content={
                                "error": "payment_invalid",
                                "detail": payment_result.get("error", "Payment verification failed"),
                            },
                        )
                    escrow_id = payment_result.get("escrow_id")

                # Verify agent identity if configured
                if self.config.verify_identity and ctx.agent_id:
                    identity_result = await self.verify_identity(ctx)
                    if not identity_result.get("verified", False):
                        return JSONResponse(
                            status_code=403,
                            content={
                                "error": "identity_verification_failed",
                                "detail": identity_result.get("error", "Could not verify agent identity"),
                            },
                        )

                # Execute the original handler
                result = await func(request, *args, **kwargs)

                # Transform response for agents if configured
                if self.config.transform_responses:
                    if isinstance(result, Response):
                        # If the handler returned a Response object, extract the body
                        body = json.loads(result.body) if hasattr(result, 'body') else result
                        return JSONResponse(
                            content=self.transform_response(body, endpoint_path, escrow_id),
                            status_code=result.status_code if hasattr(result, 'status_code') else 200,
                        )
                    else:
                        return JSONResponse(
                            content=self.transform_response(result, endpoint_path, escrow_id),
                        )

                return result

            return wrapper
        return decorator

    async def close(self):
        """Clean up HTTP client resources."""
        await self._http_client.aclose()
```

### How the Adapter Routes Requests

The `classify_caller` method is the decision point. It checks for the `x-402-payment-token` and `x-agent-id` headers first — these are definitive agent indicators. If those are absent, it falls back to user-agent string inspection as a heuristic. This two-tier classification means agents that follow the x402 protocol get full commerce support, while agents that merely identify via user-agent get classified but may still need to provide payment headers for paid endpoints.

The `wrap_endpoint` decorator is designed to be non-invasive. You add it to an existing route handler with a single line. The original function signature does not change. The original return value is preserved for human callers. Only agent callers see the transformed response envelope. This means you can add the decorator to every endpoint in your API and nothing changes for existing users — they continue to get exactly the same responses they always got.

### Request and Response Transformation

Response transformation deserves attention because it is where most migration bugs appear. The adapter wraps the original response in a standardized envelope with `data` and `meta` fields. The `data` field contains exactly what the original endpoint returned. The `meta` field adds context that agents need: which endpoint served the response, when it was generated, and the escrow ID if a payment was involved. This separation means agents can always find the business data in `response["data"]` and the transaction metadata in `response["meta"]`, regardless of how different endpoints structure their responses internally.

For endpoints that return `Response` objects directly (common in FastAPI when you need to set custom status codes or headers), the adapter extracts the body, deserializes it, wraps it, and re-serializes. This adds negligible overhead — JSON parsing of a response that was going to be serialized anyway.

---

## Chapter 3: x402 Retrofit Patterns

The x402 protocol uses HTTP status code 402 (Payment Required) to signal that an endpoint requires payment before it will process the request. This status code has been reserved in the HTTP specification since 1997 but was rarely used until agent commerce gave it a concrete purpose. Retrofitting x402 onto existing endpoints means adding payment negotiation to the HTTP layer without modifying business logic.

### The Payment Negotiation Flow

When an agent hits a paid endpoint without a payment token, the flow works like this:

1. Agent sends `GET /api/v1/data` with no payment headers.
2. Server responds with `402 Payment Required`, including price and payment URL in headers.
3. Agent creates a payment escrow via the payment URL.
4. Agent retries `GET /api/v1/data` with the `X-402-Payment-Token` header.
5. Server verifies the token, processes the request, and returns data.
6. Settlement happens automatically after the response is delivered.

This is a two-request flow for the agent: one to discover the price, one to pay and consume. Agents that already know the price (from cached discovery or manifest data) can skip step 1 and go straight to step 4.

### Payment Header Specification

The x402 headers used in negotiation:

```
# Response headers on 402:
X-Price: 0.05
X-Currency: USD
X-Payment-URL: https://api.greenhelix.net/v1/payments/create
X-Payment-Methods: greenhelix-escrow, x402-direct
X-Price-Window: 300  # price valid for 300 seconds

# Request headers on paid request:
X-402-Payment-Token: ght_abc123...
X-Agent-Id: agent-buyer-001
X-Idempotency-Key: req_unique_id_here
```

### FastAPI Middleware Implementation

The cleanest way to add x402 support across multiple endpoints in FastAPI is through middleware combined with a pricing registry:

```python
import time
from typing import Optional

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

import httpx


# Pricing registry: maps endpoint patterns to prices
ENDPOINT_PRICING: dict[str, dict] = {
    "/api/v1/search": {
        "price_usd": "0.02",
        "currency": "USD",
        "settlement_timeout": 300,
    },
    "/api/v1/analyze": {
        "price_usd": "0.10",
        "currency": "USD",
        "settlement_timeout": 600,
    },
    "/api/v1/generate": {
        "price_usd": "0.25",
        "currency": "USD",
        "settlement_timeout": 600,
    },
}

GREENHELIX_URL = "https://api.greenhelix.net"
GREENHELIX_API_KEY = ""  # Set from environment


class X402PaymentMiddleware(BaseHTTPMiddleware):
    """
    Middleware that enforces x402 payment on configured endpoints.

    Non-agent requests pass through. Agent requests to priced
    endpoints must include a valid payment token.
    """

    def __init__(self, app: FastAPI, greenhelix_api_key: str):
        super().__init__(app)
        self.api_key = greenhelix_api_key
        self._client = httpx.AsyncClient(
            base_url=GREENHELIX_URL, timeout=10.0
        )

    async def dispatch(self, request: Request, call_next) -> Response:
        # Check if this endpoint has pricing
        pricing = self._match_pricing(request.url.path)
        if pricing is None:
            return await call_next(request)

        # Check if this is an agent request
        payment_token = request.headers.get("x-402-payment-token")
        agent_id = request.headers.get("x-agent-id")

        # No agent headers — pass through to existing handler
        if not payment_token and not agent_id:
            return await call_next(request)

        # Agent request without payment token — return 402
        if not payment_token:
            return self._payment_required_response(request.url.path, pricing)

        # Agent request with payment token — verify it
        verification = await self._verify_token(payment_token, request.url.path, pricing)
        if not verification["valid"]:
            return JSONResponse(
                status_code=402,
                content={
                    "error": "payment_invalid",
                    "detail": verification.get("error", "Token verification failed"),
                },
            )

        # Payment verified — attach escrow info and proceed
        request.state.escrow_id = verification.get("escrow_id")
        request.state.payment_verified = True
        response = await call_next(request)

        # Add settlement headers to the response
        response.headers["X-Escrow-Id"] = verification.get("escrow_id", "")
        response.headers["X-Settlement-Status"] = "pending"

        return response

    def _match_pricing(self, path: str) -> Optional[dict]:
        """Match request path to pricing config, supporting wildcards."""
        if path in ENDPOINT_PRICING:
            return ENDPOINT_PRICING[path]
        # Check prefix matches for versioned endpoints
        for pattern, pricing in ENDPOINT_PRICING.items():
            if path.startswith(pattern):
                return pricing
        return None

    def _payment_required_response(self, path: str, pricing: dict) -> JSONResponse:
        """Build a 402 response with payment negotiation headers."""
        return JSONResponse(
            status_code=402,
            content={
                "error": "payment_required",
                "endpoint": path,
                "price": pricing["price_usd"],
                "currency": pricing["currency"],
                "payment_url": f"{GREENHELIX_URL}/v1/payments/create",
                "price_valid_seconds": pricing.get("settlement_timeout", 300),
            },
            headers={
                "X-Price": pricing["price_usd"],
                "X-Currency": pricing["currency"],
                "X-Payment-URL": f"{GREENHELIX_URL}/v1/payments/create",
                "X-Payment-Methods": "greenhelix-escrow",
                "X-Price-Window": str(pricing.get("settlement_timeout", 300)),
            },
        )

    async def _verify_token(
        self, token: str, endpoint: str, pricing: dict
    ) -> dict:
        """Verify payment token with GreenHelix."""
        try:
            response = await self._client.post(
                "/v1/payments/verify",
                json={
                    "token": token,
                    "expected_amount": pricing["price_usd"],
                    "currency": pricing["currency"],
                    "endpoint": endpoint,
                },
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            if response.status_code == 200:
                return response.json()
            return {"valid": False, "error": f"Verification returned {response.status_code}"}
        except httpx.TimeoutException:
            return {"valid": False, "error": "Payment verification timed out"}


# Application setup
app = FastAPI()
app.add_middleware(X402PaymentMiddleware, greenhelix_api_key=GREENHELIX_API_KEY)
```

### Flask Middleware Equivalent

For Flask applications, the same pattern uses `before_request` and `after_request` hooks:

```python
import time
from flask import Flask, request, jsonify, g
import httpx

app = Flask(__name__)

ENDPOINT_PRICING = {
    "/api/v1/search": {"price_usd": "0.02", "currency": "USD"},
    "/api/v1/analyze": {"price_usd": "0.10", "currency": "USD"},
}

GREENHELIX_URL = "https://api.greenhelix.net"
GREENHELIX_API_KEY = ""


@app.before_request
def check_agent_payment():
    """Intercept agent requests and enforce payment."""
    pricing = ENDPOINT_PRICING.get(request.path)
    if pricing is None:
        return None  # No pricing — pass through

    payment_token = request.headers.get("X-402-Payment-Token")
    agent_id = request.headers.get("X-Agent-Id")

    if not payment_token and not agent_id:
        return None  # Not an agent — pass through

    if not payment_token:
        response = jsonify({
            "error": "payment_required",
            "price": pricing["price_usd"],
            "currency": pricing["currency"],
            "payment_url": f"{GREENHELIX_URL}/v1/payments/create",
        })
        response.status_code = 402
        response.headers["X-Price"] = pricing["price_usd"]
        response.headers["X-Currency"] = pricing["currency"]
        return response

    # Verify payment synchronously (use async client in production)
    with httpx.Client(base_url=GREENHELIX_URL, timeout=10.0) as client:
        result = client.post(
            "/v1/payments/verify",
            json={
                "token": payment_token,
                "expected_amount": pricing["price_usd"],
                "endpoint": request.path,
            },
            headers={"Authorization": f"Bearer {GREENHELIX_API_KEY}"},
        )

    if result.status_code != 200 or not result.json().get("verified"):
        return jsonify({"error": "payment_invalid"}), 402

    g.escrow_id = result.json().get("escrow_id")
    g.payment_verified = True
    return None


@app.after_request
def add_settlement_headers(response):
    """Add escrow headers to responses for verified agent requests."""
    if hasattr(g, "payment_verified") and g.payment_verified:
        response.headers["X-Escrow-Id"] = getattr(g, "escrow_id", "")
        response.headers["X-Settlement-Status"] = "pending"
    return response
```

### Django Middleware Equivalent

Django uses a class-based middleware approach:

```python
import json
import httpx
from django.http import JsonResponse

ENDPOINT_PRICING = {
    "/api/v1/search/": {"price_usd": "0.02", "currency": "USD"},
    "/api/v1/analyze/": {"price_usd": "0.10", "currency": "USD"},
}

GREENHELIX_URL = "https://api.greenhelix.net"
GREENHELIX_API_KEY = ""


class X402PaymentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        pricing = ENDPOINT_PRICING.get(request.path)

        if pricing is None:
            return self.get_response(request)

        payment_token = request.META.get("HTTP_X_402_PAYMENT_TOKEN")
        agent_id = request.META.get("HTTP_X_AGENT_ID")

        if not payment_token and not agent_id:
            return self.get_response(request)

        if not payment_token:
            response = JsonResponse(
                {
                    "error": "payment_required",
                    "price": pricing["price_usd"],
                    "currency": pricing["currency"],
                },
                status=402,
            )
            response["X-Price"] = pricing["price_usd"]
            response["X-Currency"] = pricing["currency"]
            return response

        # Verify payment token
        with httpx.Client(base_url=GREENHELIX_URL, timeout=10.0) as client:
            result = client.post(
                "/v1/payments/verify",
                json={
                    "token": payment_token,
                    "expected_amount": pricing["price_usd"],
                    "endpoint": request.path,
                },
                headers={"Authorization": f"Bearer {GREENHELIX_API_KEY}"},
            )

        if result.status_code != 200:
            return JsonResponse({"error": "payment_invalid"}, status=402)

        data = result.json()
        if not data.get("verified"):
            return JsonResponse({"error": "payment_invalid"}, status=402)

        request.escrow_id = data.get("escrow_id")
        request.payment_verified = True

        response = self.get_response(request)
        response["X-Escrow-Id"] = getattr(request, "escrow_id", "")
        response["X-Settlement-Status"] = "pending"
        return response
```

### Token Verification Caching

Payment verification adds a network round-trip to every agent request. For high-throughput endpoints, this is unacceptable. Implement a short-lived verification cache:

```python
import hashlib
import time
from typing import Optional


class PaymentVerificationCache:
    """Short-lived cache for payment verification results."""

    def __init__(self, ttl_seconds: int = 30):
        self.ttl = ttl_seconds
        self._cache: dict[str, tuple[float, dict]] = {}

    def _key(self, token: str, endpoint: str) -> str:
        return hashlib.sha256(f"{token}:{endpoint}".encode()).hexdigest()

    def get(self, token: str, endpoint: str) -> Optional[dict]:
        key = self._key(token, endpoint)
        entry = self._cache.get(key)
        if entry is None:
            return None
        timestamp, result = entry
        if time.time() - timestamp > self.ttl:
            del self._cache[key]
            return None
        return result

    def set(self, token: str, endpoint: str, result: dict) -> None:
        key = self._key(token, endpoint)
        self._cache[key] = (time.time(), result)

    def evict_expired(self) -> int:
        """Remove all expired entries. Returns count of evicted entries."""
        now = time.time()
        expired = [k for k, (ts, _) in self._cache.items() if now - ts > self.ttl]
        for k in expired:
            del self._cache[k]
        return len(expired)
```

The cache TTL should be short — 30 seconds is usually sufficient. A payment token verified 30 seconds ago is still valid for the same endpoint. But do not cache across endpoints: a token valid for `/search` is not necessarily valid for `/analyze` at a different price point.

---

## Chapter 4: Authentication Bridging

Most REST APIs already have authentication. The migration challenge is not replacing that auth but running agent authentication alongside it. Agents authenticate differently from humans — they use cryptographic key pairs instead of passwords, sign requests instead of presenting session tokens, and identify themselves by public key hash instead of username. Authentication bridging lets both systems coexist.

### The Dual-Auth Architecture

The bridging architecture has three layers:

**Layer 1: Header inspection.** Every request is classified as human-auth, agent-auth, or unauthenticated based on which headers are present. Human requests carry `Authorization: Bearer <jwt>` or `X-API-Key`. Agent requests carry `X-Agent-Id`, `X-Agent-Public-Key`, and `X-Agent-Signature`.

**Layer 2: Verification.** Human auth goes through your existing verification pipeline (JWT decode, API key lookup, OAuth token introspection). Agent auth goes through Ed25519 signature verification against the claimed public key, followed by identity resolution against GreenHelix.

**Layer 3: Identity normalization.** Both paths produce a unified identity object that downstream handlers consume. The handler does not know or care whether the caller is human or agent — it gets the same interface.

```python
import time
import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.exceptions import InvalidSignature
import base64


class AuthMethod(str, Enum):
    JWT = "jwt"
    API_KEY = "api_key"
    AGENT_SIGNATURE = "agent_signature"
    NONE = "none"


@dataclass
class UnifiedIdentity:
    """Normalized identity produced by either auth path."""
    identity_id: str
    display_name: str
    auth_method: AuthMethod
    is_agent: bool
    permissions: list[str]
    tier: str = "free"
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions or "*" in self.permissions


class AuthBridge:
    """
    Bridges existing human auth with agent Ed25519 auth.
    Produces a UnifiedIdentity regardless of auth method.
    """

    def __init__(
        self,
        jwt_secret: str,
        api_key_lookup: callable,
        greenhelix_client: object,
    ):
        self.jwt_secret = jwt_secret
        self.api_key_lookup = api_key_lookup
        self.greenhelix = greenhelix_client

    async def authenticate(self, request) -> UnifiedIdentity:
        """
        Authenticate the request using whichever method is present.
        Raises HTTPException on failure.
        """
        # Check for agent auth first (more specific headers)
        agent_id = request.headers.get("x-agent-id")
        agent_sig = request.headers.get("x-agent-signature")
        agent_pubkey = request.headers.get("x-agent-public-key")

        if agent_id and agent_sig and agent_pubkey:
            return await self._authenticate_agent(
                agent_id, agent_sig, agent_pubkey, request
            )

        # Check for JWT
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            return self._authenticate_jwt(token)

        # Check for API key
        api_key = request.headers.get("x-api-key")
        if api_key:
            return self._authenticate_api_key(api_key)

        # No auth provided
        return UnifiedIdentity(
            identity_id="anonymous",
            display_name="Anonymous",
            auth_method=AuthMethod.NONE,
            is_agent=False,
            permissions=["read:public"],
            tier="free",
        )

    async def _authenticate_agent(
        self,
        agent_id: str,
        signature_b64: str,
        public_key_b64: str,
        request,
    ) -> UnifiedIdentity:
        """Verify agent Ed25519 signature and resolve identity."""
        # Step 1: Reconstruct the signed payload
        # The agent signs: METHOD + PATH + TIMESTAMP + BODY_HASH
        timestamp = request.headers.get("x-agent-timestamp", "")
        body = await request.body()
        body_hash = hashlib.sha256(body).hexdigest() if body else ""

        signed_payload = (
            f"{request.method}:{request.url.path}:{timestamp}:{body_hash}"
        )

        # Step 2: Verify the Ed25519 signature
        try:
            public_key_bytes = base64.b64decode(public_key_b64)
            signature_bytes = base64.b64decode(signature_b64)

            public_key = Ed25519PublicKey.from_public_key_der(public_key_bytes)
            public_key.verify(signature_bytes, signed_payload.encode("utf-8"))
        except (InvalidSignature, ValueError, Exception) as exc:
            raise HTTPException(
                status_code=401,
                detail={
                    "error": "signature_invalid",
                    "message": "Ed25519 signature verification failed",
                },
            )

        # Step 3: Check timestamp freshness (prevent replay attacks)
        try:
            req_time = float(timestamp)
            if abs(time.time() - req_time) > 300:  # 5-minute window
                raise HTTPException(
                    status_code=401,
                    detail={
                        "error": "timestamp_expired",
                        "message": "Request timestamp outside acceptable window",
                    },
                )
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=401,
                detail={"error": "timestamp_invalid", "message": "Invalid timestamp format"},
            )

        # Step 4: Resolve agent identity from GreenHelix
        agent_info = await self.greenhelix.resolve_agent(agent_id, public_key_b64)

        return UnifiedIdentity(
            identity_id=agent_id,
            display_name=agent_info.get("display_name", agent_id),
            auth_method=AuthMethod.AGENT_SIGNATURE,
            is_agent=True,
            permissions=agent_info.get("permissions", ["read:public", "execute:paid"]),
            tier=agent_info.get("tier", "standard"),
            metadata={
                "public_key": public_key_b64,
                "reputation_score": agent_info.get("reputation_score", 0),
                "total_transactions": agent_info.get("total_transactions", 0),
            },
        )

    def _authenticate_jwt(self, token: str) -> UnifiedIdentity:
        """Verify JWT and extract identity (existing auth path)."""
        import jwt as pyjwt

        try:
            payload = pyjwt.decode(token, self.jwt_secret, algorithms=["HS256"])
        except pyjwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail={"error": "token_expired"})
        except pyjwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail={"error": "token_invalid"})

        return UnifiedIdentity(
            identity_id=payload["sub"],
            display_name=payload.get("name", ""),
            auth_method=AuthMethod.JWT,
            is_agent=False,
            permissions=payload.get("permissions", ["read:public"]),
            tier=payload.get("tier", "free"),
        )

    def _authenticate_api_key(self, api_key: str) -> UnifiedIdentity:
        """Verify API key and extract identity (existing auth path)."""
        key_data = self.api_key_lookup(api_key)
        if key_data is None:
            raise HTTPException(status_code=401, detail={"error": "api_key_invalid"})

        return UnifiedIdentity(
            identity_id=key_data["user_id"],
            display_name=key_data.get("name", ""),
            auth_method=AuthMethod.API_KEY,
            is_agent=False,
            permissions=key_data.get("permissions", ["read:public"]),
            tier=key_data.get("tier", "free"),
        )
```

### Using the AuthBridge in FastAPI

Integrate the bridge as a dependency that replaces your existing auth dependency:

```python
from fastapi import Depends, FastAPI, Request

app = FastAPI()

# Initialize the bridge once at startup
auth_bridge = AuthBridge(
    jwt_secret="your-jwt-secret",
    api_key_lookup=lambda key: db.lookup_api_key(key),
    greenhelix_client=greenhelix_client,
)


async def get_identity(request: Request) -> UnifiedIdentity:
    """FastAPI dependency that authenticates via the bridge."""
    return await auth_bridge.authenticate(request)


@app.get("/api/v1/data")
async def get_data(identity: UnifiedIdentity = Depends(get_identity)):
    # identity.is_agent tells you the caller type
    # identity.permissions controls access
    # identity.tier determines rate limits
    if not identity.has_permission("read:data"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    return {"results": [...], "caller": identity.identity_id}
```

### Session Management for Agents

Human sessions rely on cookies and server-side state. Agent sessions are stateless by design — each request is independently authenticated. But some APIs have multi-step workflows (start a job, poll for status, download results) that require session continuity. For agents, implement session continuity through idempotency keys and request correlation:

```python
from dataclasses import dataclass, field
from typing import Optional
import time
import uuid


@dataclass
class AgentSession:
    """Lightweight session for multi-step agent workflows."""
    session_id: str
    agent_id: str
    created_at: float
    last_activity: float
    workflow_state: dict = field(default_factory=dict)
    ttl_seconds: int = 3600


class AgentSessionStore:
    """In-memory session store for agent workflows."""

    def __init__(self):
        self._sessions: dict[str, AgentSession] = {}

    def create(self, agent_id: str) -> AgentSession:
        session = AgentSession(
            session_id=str(uuid.uuid4()),
            agent_id=agent_id,
            created_at=time.time(),
            last_activity=time.time(),
        )
        self._sessions[session.session_id] = session
        return session

    def get(self, session_id: str, agent_id: str) -> Optional[AgentSession]:
        session = self._sessions.get(session_id)
        if session is None:
            return None
        if session.agent_id != agent_id:
            return None  # Session belongs to a different agent
        if time.time() - session.last_activity > session.ttl_seconds:
            del self._sessions[session_id]
            return None
        session.last_activity = time.time()
        return session

    def update_state(self, session_id: str, key: str, value: object) -> None:
        session = self._sessions.get(session_id)
        if session:
            session.workflow_state[key] = value
            session.last_activity = time.time()

    def cleanup_expired(self) -> int:
        now = time.time()
        expired = [
            sid for sid, s in self._sessions.items()
            if now - s.last_activity > s.ttl_seconds
        ]
        for sid in expired:
            del self._sessions[sid]
        return len(expired)
```

Agents include `X-Session-Id` on follow-up requests. The session ID is returned in the response to the first request in a workflow. This is optional — agents that perform only single-call operations never need sessions.

---

## Chapter 5: Gradual Migration Strategies

Big-bang migrations fail. You do not flip a switch and convert your entire API to agent commerce overnight. Instead, you migrate one endpoint at a time, verify it works, and move to the next. This chapter covers the practical strategies for incremental migration without disrupting existing traffic.

### Endpoint-by-Endpoint Migration

The migration order matters. Start with read-only endpoints (GET requests), then move to write endpoints (POST/PUT), and finish with complex workflows (multi-step operations). Each endpoint goes through four stages:

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class MigrationStage(str, Enum):
    LEGACY = "legacy"           # No agent support
    DISCOVERY = "discovery"     # Returns 402 with pricing, but doesn't process payments
    PAYMENT = "payment"         # Accepts and verifies payments
    FULL = "full"               # Full agent commerce: payment + identity + response transform


@dataclass
class EndpointMigrationState:
    path: str
    stage: MigrationStage
    migrated_at: Optional[float] = None
    migration_notes: str = ""


class MigrationRegistry:
    """Tracks which endpoints are at which migration stage."""

    def __init__(self):
        self._endpoints: dict[str, EndpointMigrationState] = {}

    def register(self, path: str, stage: MigrationStage, notes: str = "") -> None:
        self._endpoints[path] = EndpointMigrationState(
            path=path,
            stage=stage,
            migrated_at=time.time() if stage != MigrationStage.LEGACY else None,
            migration_notes=notes,
        )

    def get_stage(self, path: str) -> MigrationStage:
        state = self._endpoints.get(path)
        return state.stage if state else MigrationStage.LEGACY

    def advance(self, path: str) -> MigrationStage:
        """Move an endpoint to the next migration stage."""
        current = self.get_stage(path)
        stages = list(MigrationStage)
        current_index = stages.index(current)
        if current_index < len(stages) - 1:
            new_stage = stages[current_index + 1]
            self.register(path, new_stage)
            return new_stage
        return current

    def summary(self) -> dict[str, int]:
        counts = {stage.value: 0 for stage in MigrationStage}
        for state in self._endpoints.values():
            counts[state.stage.value] += 1
        return counts


# Usage
registry = MigrationRegistry()
registry.register("/api/v1/search", MigrationStage.FULL)
registry.register("/api/v1/analyze", MigrationStage.PAYMENT)
registry.register("/api/v1/users", MigrationStage.LEGACY)

print(registry.summary())
# {'legacy': 1, 'discovery': 0, 'payment': 1, 'full': 1}
```

The discovery stage is critical and often skipped. At this stage, the endpoint returns 402 with correct pricing headers when an agent hits it, but does not actually process payments. This lets agents discover your pricing and capabilities without you needing to handle real money yet. Run in discovery mode for at least a week to see what agents query your API, what prices they encounter, and how they react.

### Feature Flags for Agent Commerce

Feature flags let you enable and disable agent commerce per endpoint, per agent, or globally without deploying new code:

```python
from dataclasses import dataclass, field
from typing import Optional
import json
import os


@dataclass
class AgentCommerceFlags:
    """Feature flags controlling agent commerce behavior."""
    global_enabled: bool = True
    payment_required: bool = True
    identity_verification: bool = True
    response_transformation: bool = True
    allowed_agent_ids: list[str] = field(default_factory=list)  # Empty = allow all
    blocked_agent_ids: list[str] = field(default_factory=list)
    endpoint_overrides: dict[str, dict] = field(default_factory=dict)

    @classmethod
    def from_env(cls) -> "AgentCommerceFlags":
        """Load flags from environment variables or config file."""
        config_path = os.getenv("AGENT_COMMERCE_CONFIG", "agent_commerce_flags.json")
        if os.path.exists(config_path):
            with open(config_path) as f:
                data = json.load(f)
            return cls(**data)
        return cls(
            global_enabled=os.getenv("AGENT_COMMERCE_ENABLED", "true").lower() == "true",
            payment_required=os.getenv("AGENT_PAYMENT_REQUIRED", "true").lower() == "true",
        )

    def is_enabled_for(self, endpoint: str, agent_id: Optional[str] = None) -> bool:
        """Check if agent commerce is enabled for a specific endpoint and agent."""
        if not self.global_enabled:
            return False

        if agent_id and agent_id in self.blocked_agent_ids:
            return False

        if self.allowed_agent_ids and agent_id not in self.allowed_agent_ids:
            return False

        override = self.endpoint_overrides.get(endpoint, {})
        return override.get("enabled", True)

    def get_price_override(self, endpoint: str) -> Optional[str]:
        """Get endpoint-specific price override, if any."""
        override = self.endpoint_overrides.get(endpoint, {})
        return override.get("price_usd")
```

### Traffic Routing with Reverse Proxy

For APIs running behind nginx or a similar reverse proxy, you can route agent traffic to a separate upstream that has the commerce middleware enabled, while human traffic hits the original upstream unchanged:

```nginx
# nginx.conf — agent traffic routing

upstream legacy_api {
    server 127.0.0.1:8000;
}

upstream agent_commerce_api {
    server 127.0.0.1:8001;
}

map $http_x_agent_id $is_agent {
    default 0;
    "~.+" 1;
}

map $http_x_402_payment_token $has_payment {
    default 0;
    "~.+" 1;
}

server {
    listen 443 ssl;
    server_name api.example.com;

    location /api/v1/ {
        # Route to agent commerce API if agent headers are present
        if ($is_agent) {
            proxy_pass http://agent_commerce_api;
            break;
        }
        if ($has_payment) {
            proxy_pass http://agent_commerce_api;
            break;
        }

        # Default: route to legacy API
        proxy_pass http://legacy_api;
    }
}
```

This approach lets you run the agent commerce version of your API as a separate process. The legacy API process remains completely untouched. If anything goes wrong with agent commerce, you adjust the nginx config to route all traffic back to the legacy upstream. Zero-downtime rollback.

### A/B Testing Human vs Agent Traffic

Track metrics separately for human and agent callers to detect regressions:

```python
import time
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class TrafficMetrics:
    request_count: int = 0
    error_count: int = 0
    total_latency_ms: float = 0.0
    p95_latencies: list[float] = field(default_factory=list)

    @property
    def avg_latency_ms(self) -> float:
        if self.request_count == 0:
            return 0.0
        return self.total_latency_ms / self.request_count

    @property
    def error_rate(self) -> float:
        if self.request_count == 0:
            return 0.0
        return self.error_count / self.request_count


class MigrationMetricsCollector:
    """Collects metrics split by caller type for migration monitoring."""

    def __init__(self):
        self._metrics: dict[str, dict[str, TrafficMetrics]] = defaultdict(
            lambda: {"human": TrafficMetrics(), "agent": TrafficMetrics()}
        )

    def record(
        self,
        endpoint: str,
        caller_type: str,
        latency_ms: float,
        is_error: bool = False,
    ) -> None:
        metrics = self._metrics[endpoint][caller_type]
        metrics.request_count += 1
        metrics.total_latency_ms += latency_ms
        metrics.p95_latencies.append(latency_ms)
        if is_error:
            metrics.error_count += 1

        # Keep only last 1000 latencies for p95 calculation
        if len(metrics.p95_latencies) > 1000:
            metrics.p95_latencies = metrics.p95_latencies[-1000:]

    def compare(self, endpoint: str) -> dict:
        """Compare human vs agent metrics for an endpoint."""
        human = self._metrics[endpoint]["human"]
        agent = self._metrics[endpoint]["agent"]
        return {
            "endpoint": endpoint,
            "human": {
                "requests": human.request_count,
                "avg_latency_ms": round(human.avg_latency_ms, 2),
                "error_rate": round(human.error_rate, 4),
            },
            "agent": {
                "requests": agent.request_count,
                "avg_latency_ms": round(agent.avg_latency_ms, 2),
                "error_rate": round(agent.error_rate, 4),
            },
            "latency_delta_ms": round(agent.avg_latency_ms - human.avg_latency_ms, 2),
        }
```

The `latency_delta_ms` is the key metric during migration. If agent requests are significantly slower than human requests at the same endpoint, the commerce middleware is adding too much overhead. The target is under 50ms of additional latency for the payment verification and response transformation layer.

---

## Chapter 6: MigrationValidator Class

Migration validation answers one question: does the migrated endpoint behave identically to the original for all non-commerce concerns? The business logic should produce the same output, the response schemas should be compatible, and performance should not degrade beyond acceptable bounds. The `MigrationValidator` automates these checks.

### The Validator Architecture

The validator works by sending the same request to both the legacy endpoint and the migrated endpoint, then comparing the responses. For endpoints that have already replaced the legacy version (same URL, new middleware), it compares captured legacy response snapshots against live migrated responses.

```python
import json
import time
import hashlib
from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum

import httpx


class ValidationResult(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"


@dataclass
class ValidationReport:
    endpoint: str
    result: ValidationResult
    checks: list[dict] = field(default_factory=list)
    duration_ms: float = 0.0
    timestamp: float = field(default_factory=time.time)

    def add_check(self, name: str, result: ValidationResult, detail: str = "") -> None:
        self.checks.append({
            "name": name,
            "result": result.value,
            "detail": detail,
        })
        # Overall result is the worst individual result
        if result == ValidationResult.FAIL:
            self.result = ValidationResult.FAIL
        elif result == ValidationResult.WARN and self.result != ValidationResult.FAIL:
            self.result = ValidationResult.WARN

    @property
    def passed(self) -> bool:
        return self.result != ValidationResult.FAIL

    def summary(self) -> str:
        total = len(self.checks)
        passed = sum(1 for c in self.checks if c["result"] == "pass")
        return f"{self.endpoint}: {passed}/{total} checks passed ({self.result.value})"


@dataclass
class ResponseSnapshot:
    """Captured response for comparison."""
    status_code: int
    headers: dict[str, str]
    body: Any
    latency_ms: float
    captured_at: float = field(default_factory=time.time)

    def body_hash(self) -> str:
        return hashlib.sha256(json.dumps(self.body, sort_keys=True).encode()).hexdigest()


class MigrationValidator:
    """
    Validates that migrated endpoints preserve original behavior.

    Compares response schemas, status codes, data content, and
    performance between legacy and migrated versions.
    """

    def __init__(
        self,
        legacy_base_url: str,
        migrated_base_url: str,
        tolerance_ms: float = 100.0,
        schema_strict: bool = False,
    ):
        self.legacy_url = legacy_base_url.rstrip("/")
        self.migrated_url = migrated_base_url.rstrip("/")
        self.tolerance_ms = tolerance_ms
        self.schema_strict = schema_strict
        self._client = httpx.AsyncClient(timeout=30.0)
        self._snapshots: dict[str, list[ResponseSnapshot]] = {}

    async def capture_legacy_snapshot(
        self, endpoint: str, method: str = "GET", body: Any = None, headers: dict = None,
    ) -> ResponseSnapshot:
        """Capture a response from the legacy endpoint for later comparison."""
        request_headers = headers or {}
        start = time.time()

        if method.upper() == "GET":
            response = await self._client.get(
                f"{self.legacy_url}{endpoint}", headers=request_headers
            )
        else:
            response = await self._client.request(
                method, f"{self.legacy_url}{endpoint}",
                json=body, headers=request_headers,
            )

        latency_ms = (time.time() - start) * 1000

        snapshot = ResponseSnapshot(
            status_code=response.status_code,
            headers=dict(response.headers),
            body=response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
            latency_ms=latency_ms,
        )

        if endpoint not in self._snapshots:
            self._snapshots[endpoint] = []
        self._snapshots[endpoint].append(snapshot)

        return snapshot

    async def validate_endpoint(
        self,
        endpoint: str,
        method: str = "GET",
        body: Any = None,
        human_headers: dict = None,
        agent_headers: dict = None,
    ) -> ValidationReport:
        """Run full validation suite on a migrated endpoint."""
        report = ValidationReport(endpoint=endpoint, result=ValidationResult.PASS)
        start = time.time()

        # Test 1: Human request produces same response as legacy
        human_headers = human_headers or {}
        try:
            legacy_resp = await self._request(self.legacy_url, endpoint, method, body, human_headers)
            migrated_resp = await self._request(self.migrated_url, endpoint, method, body, human_headers)

            self._check_status_code(report, legacy_resp, migrated_resp)
            self._check_schema_compatibility(report, legacy_resp, migrated_resp)
            self._check_data_equivalence(report, legacy_resp, migrated_resp)
        except httpx.RequestError as exc:
            report.add_check("connectivity", ValidationResult.FAIL, str(exc))
            report.duration_ms = (time.time() - start) * 1000
            return report

        # Test 2: Agent request without payment returns 402
        if agent_headers:
            agent_no_payment = {k: v for k, v in agent_headers.items() if k.lower() != "x-402-payment-token"}
            try:
                agent_resp = await self._request(
                    self.migrated_url, endpoint, method, body, agent_no_payment
                )
                if agent_resp.status_code == 402:
                    report.add_check("402_response", ValidationResult.PASS, "Returns 402 for unpaid agent requests")
                    self._check_402_headers(report, agent_resp)
                else:
                    report.add_check(
                        "402_response", ValidationResult.WARN,
                        f"Expected 402, got {agent_resp.status_code}",
                    )
            except httpx.RequestError as exc:
                report.add_check("agent_request", ValidationResult.FAIL, str(exc))

        # Test 3: Performance regression check
        await self._check_performance(report, endpoint, method, body, human_headers)

        report.duration_ms = (time.time() - start) * 1000
        return report

    async def _request(
        self, base_url: str, endpoint: str, method: str, body: Any, headers: dict,
    ) -> httpx.Response:
        if method.upper() == "GET":
            return await self._client.get(f"{base_url}{endpoint}", headers=headers)
        return await self._client.request(
            method, f"{base_url}{endpoint}", json=body, headers=headers
        )

    def _check_status_code(
        self, report: ValidationReport, legacy: httpx.Response, migrated: httpx.Response,
    ) -> None:
        if legacy.status_code == migrated.status_code:
            report.add_check("status_code", ValidationResult.PASS)
        else:
            report.add_check(
                "status_code", ValidationResult.FAIL,
                f"Legacy returned {legacy.status_code}, migrated returned {migrated.status_code}",
            )

    def _check_schema_compatibility(
        self, report: ValidationReport, legacy: httpx.Response, migrated: httpx.Response,
    ) -> None:
        """Compare response structure (keys at each level)."""
        try:
            legacy_body = legacy.json()
            migrated_body = migrated.json()
        except (json.JSONDecodeError, ValueError):
            report.add_check("schema", ValidationResult.WARN, "Could not parse response as JSON")
            return

        legacy_keys = self._extract_keys(legacy_body)
        migrated_keys = self._extract_keys(migrated_body)

        missing = legacy_keys - migrated_keys
        added = migrated_keys - legacy_keys

        if not missing and not added:
            report.add_check("schema", ValidationResult.PASS)
        elif missing:
            report.add_check(
                "schema", ValidationResult.FAIL,
                f"Missing keys in migrated response: {missing}",
            )
        elif added and self.schema_strict:
            report.add_check(
                "schema", ValidationResult.FAIL,
                f"Unexpected keys in migrated response: {added}",
            )
        else:
            report.add_check(
                "schema", ValidationResult.WARN,
                f"New keys in migrated response: {added}",
            )

    def _check_data_equivalence(
        self, report: ValidationReport, legacy: httpx.Response, migrated: httpx.Response,
    ) -> None:
        """Check that the actual data values match."""
        try:
            legacy_body = legacy.json()
            migrated_body = migrated.json()
        except (json.JSONDecodeError, ValueError):
            return

        # If migrated response wraps data in an envelope, unwrap it
        if isinstance(migrated_body, dict) and "data" in migrated_body and "meta" in migrated_body:
            migrated_body = migrated_body["data"]

        legacy_hash = hashlib.sha256(json.dumps(legacy_body, sort_keys=True).encode()).hexdigest()
        migrated_hash = hashlib.sha256(json.dumps(migrated_body, sort_keys=True).encode()).hexdigest()

        if legacy_hash == migrated_hash:
            report.add_check("data_equivalence", ValidationResult.PASS)
        else:
            report.add_check(
                "data_equivalence", ValidationResult.WARN,
                "Response data differs (may be expected for dynamic fields like timestamps)",
            )

    def _check_402_headers(self, report: ValidationReport, response: httpx.Response) -> None:
        """Verify that 402 responses include required negotiation headers."""
        required_headers = ["x-price", "x-currency", "x-payment-url"]
        missing = [h for h in required_headers if h not in response.headers]

        if not missing:
            report.add_check("402_headers", ValidationResult.PASS)
        else:
            report.add_check(
                "402_headers", ValidationResult.FAIL,
                f"Missing 402 headers: {missing}",
            )

    async def _check_performance(
        self, report: ValidationReport, endpoint: str, method: str, body: Any, headers: dict,
    ) -> None:
        """Check that migration hasn't introduced unacceptable latency."""
        # Run 5 requests against each and compare average
        legacy_latencies = []
        migrated_latencies = []

        for _ in range(5):
            start = time.time()
            await self._request(self.legacy_url, endpoint, method, body, headers)
            legacy_latencies.append((time.time() - start) * 1000)

            start = time.time()
            await self._request(self.migrated_url, endpoint, method, body, headers)
            migrated_latencies.append((time.time() - start) * 1000)

        avg_legacy = sum(legacy_latencies) / len(legacy_latencies)
        avg_migrated = sum(migrated_latencies) / len(migrated_latencies)
        delta = avg_migrated - avg_legacy

        if delta <= self.tolerance_ms:
            report.add_check(
                "performance", ValidationResult.PASS,
                f"Latency delta: {delta:.1f}ms (within {self.tolerance_ms}ms tolerance)",
            )
        elif delta <= self.tolerance_ms * 2:
            report.add_check(
                "performance", ValidationResult.WARN,
                f"Latency delta: {delta:.1f}ms (approaching tolerance of {self.tolerance_ms}ms)",
            )
        else:
            report.add_check(
                "performance", ValidationResult.FAIL,
                f"Latency delta: {delta:.1f}ms (exceeds tolerance of {self.tolerance_ms}ms)",
            )

    def _extract_keys(self, obj: Any, prefix: str = "") -> set[str]:
        """Recursively extract all key paths from a JSON object."""
        keys = set()
        if isinstance(obj, dict):
            for k, v in obj.items():
                full_key = f"{prefix}.{k}" if prefix else k
                keys.add(full_key)
                keys.update(self._extract_keys(v, full_key))
        elif isinstance(obj, list) and obj:
            keys.update(self._extract_keys(obj[0], f"{prefix}[]"))
        return keys

    async def close(self):
        await self._client.aclose()
```

### Running Validation

Run the validator as part of your CI pipeline or as a standalone validation script:

```python
import asyncio


async def validate_migration():
    validator = MigrationValidator(
        legacy_base_url="http://localhost:8000",
        migrated_base_url="http://localhost:8001",
        tolerance_ms=50.0,
    )

    endpoints_to_validate = [
        {
            "endpoint": "/api/v1/search",
            "method": "GET",
            "human_headers": {"Authorization": "Bearer test-jwt-token"},
            "agent_headers": {"X-Agent-Id": "test-agent-001"},
        },
        {
            "endpoint": "/api/v1/analyze",
            "method": "POST",
            "body": {"text": "sample input for validation"},
            "human_headers": {"Authorization": "Bearer test-jwt-token"},
            "agent_headers": {"X-Agent-Id": "test-agent-001"},
        },
    ]

    reports = []
    for ep in endpoints_to_validate:
        report = await validator.validate_endpoint(**ep)
        reports.append(report)
        print(report.summary())
        for check in report.checks:
            status = "OK" if check["result"] == "pass" else check["result"].upper()
            detail = f" - {check['detail']}" if check["detail"] else ""
            print(f"  [{status}] {check['name']}{detail}")

    await validator.close()

    # Fail CI if any endpoint fails validation
    all_passed = all(r.passed for r in reports)
    if not all_passed:
        print("\nMigration validation FAILED")
        exit(1)
    else:
        print("\nAll migration validations passed")


asyncio.run(validate_migration())
```

### Contract Testing Between Old and New

Beyond schema comparison, contract tests verify specific response invariants that your API consumers depend on. Define these contracts explicitly:

```python
@dataclass
class ResponseContract:
    """Defines expected properties of a response that must not change during migration."""
    endpoint: str
    status_code: int
    required_fields: list[str]
    field_types: dict[str, type]
    value_constraints: dict[str, callable]  # field -> validator function

    def validate(self, response_body: dict) -> list[str]:
        """Returns list of contract violations."""
        violations = []

        for field_path in self.required_fields:
            if not self._has_field(response_body, field_path):
                violations.append(f"Missing required field: {field_path}")

        for field_path, expected_type in self.field_types.items():
            value = self._get_field(response_body, field_path)
            if value is not None and not isinstance(value, expected_type):
                violations.append(
                    f"Type mismatch for {field_path}: expected {expected_type.__name__}, "
                    f"got {type(value).__name__}"
                )

        for field_path, validator in self.value_constraints.items():
            value = self._get_field(response_body, field_path)
            if value is not None and not validator(value):
                violations.append(f"Value constraint failed for {field_path}: {value}")

        return violations

    def _has_field(self, obj: dict, path: str) -> bool:
        parts = path.split(".")
        current = obj
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return False
        return True

    def _get_field(self, obj: dict, path: str) -> Any:
        parts = path.split(".")
        current = obj
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return current


# Example contract definition
search_contract = ResponseContract(
    endpoint="/api/v1/search",
    status_code=200,
    required_fields=["results", "total_count"],
    field_types={
        "results": list,
        "total_count": int,
    },
    value_constraints={
        "total_count": lambda v: v >= 0,
    },
)
```

---

## Chapter 7: Testing Migration

Testing a migration is not the same as testing new code. You are not verifying that something works — you are verifying that it works the same way it did before, plus new capabilities. The testing strategy has three phases: pre-migration baseline capture, parallel validation during migration, and post-migration regression testing.

### Phase 1: Baseline Capture

Before touching any code, capture baseline responses for every endpoint you plan to migrate. These baselines become the ground truth for comparison:

```python
import json
import time
import os
from dataclasses import dataclass, asdict
from typing import Any

import httpx


@dataclass
class BaselineCapture:
    endpoint: str
    method: str
    request_body: Any
    response_status: int
    response_body: Any
    response_headers: dict[str, str]
    latency_ms: float
    captured_at: float


class BaselineRecorder:
    """Records baseline API responses for migration comparison."""

    def __init__(self, base_url: str, output_dir: str = "./migration_baselines"):
        self.base_url = base_url.rstrip("/")
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    async def capture(
        self, endpoint: str, method: str = "GET", body: Any = None,
        headers: dict = None, iterations: int = 10,
    ) -> list[BaselineCapture]:
        """Capture multiple baseline responses for statistical comparison."""
        captures = []
        async with httpx.AsyncClient(timeout=30.0) as client:
            for _ in range(iterations):
                start = time.time()
                if method.upper() == "GET":
                    resp = await client.get(
                        f"{self.base_url}{endpoint}", headers=headers or {}
                    )
                else:
                    resp = await client.request(
                        method, f"{self.base_url}{endpoint}",
                        json=body, headers=headers or {},
                    )
                latency = (time.time() - start) * 1000

                try:
                    resp_body = resp.json()
                except ValueError:
                    resp_body = resp.text

                capture = BaselineCapture(
                    endpoint=endpoint,
                    method=method,
                    request_body=body,
                    response_status=resp.status_code,
                    response_body=resp_body,
                    response_headers=dict(resp.headers),
                    latency_ms=latency,
                    captured_at=time.time(),
                )
                captures.append(capture)

        # Save to disk
        filename = endpoint.replace("/", "_").strip("_") + ".json"
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w") as f:
            json.dump([asdict(c) for c in captures], f, indent=2, default=str)

        return captures
```

Run the baseline recorder against every endpoint in your migration list. Store the output in version control. These files serve as regression evidence — if something breaks during migration, you have concrete proof of what the correct behavior was.

### Phase 2: Shadow Traffic Validation

Shadow traffic sends a copy of every real production request to the migrated endpoint and compares responses without affecting the actual client. The client gets the legacy response, but the migrated response is captured and compared asynchronously:

```python
import asyncio
import time
import json
import logging
from typing import Any

import httpx

logger = logging.getLogger("shadow_traffic")


class ShadowTrafficValidator:
    """
    Replays production traffic against migrated endpoints.
    Compares responses without affecting production clients.
    """

    def __init__(
        self,
        migrated_base_url: str,
        mismatch_log: str = "./shadow_mismatches.jsonl",
    ):
        self.migrated_url = migrated_base_url.rstrip("/")
        self.mismatch_log = mismatch_log
        self._client = httpx.AsyncClient(timeout=10.0)
        self._stats = {"total": 0, "matched": 0, "mismatched": 0, "errors": 0}

    async def shadow_request(
        self,
        endpoint: str,
        method: str,
        body: Any,
        headers: dict,
        legacy_status: int,
        legacy_body: Any,
    ) -> None:
        """Send shadow request and compare with legacy response."""
        self._stats["total"] += 1

        # Remove auth headers that might not work against the migrated version
        shadow_headers = {
            k: v for k, v in headers.items()
            if k.lower() not in ("cookie", "x-csrf-token")
        }

        try:
            start = time.time()
            if method.upper() == "GET":
                resp = await self._client.get(
                    f"{self.migrated_url}{endpoint}", headers=shadow_headers
                )
            else:
                resp = await self._client.request(
                    method, f"{self.migrated_url}{endpoint}",
                    json=body, headers=shadow_headers,
                )
            latency = (time.time() - start) * 1000

            # Compare status codes
            if resp.status_code != legacy_status:
                self._log_mismatch(endpoint, "status_code", legacy_status, resp.status_code)
                self._stats["mismatched"] += 1
                return

            # Compare response bodies (ignoring dynamic fields)
            try:
                migrated_body = resp.json()
                if not self._bodies_equivalent(legacy_body, migrated_body):
                    self._log_mismatch(endpoint, "body", legacy_body, migrated_body)
                    self._stats["mismatched"] += 1
                    return
            except (json.JSONDecodeError, ValueError):
                pass

            self._stats["matched"] += 1

        except Exception as exc:
            self._stats["errors"] += 1
            logger.error(f"Shadow request failed for {endpoint}: {exc}")

    def _bodies_equivalent(self, legacy: Any, migrated: Any) -> bool:
        """Compare bodies, ignoring known dynamic fields."""
        dynamic_fields = {"timestamp", "request_id", "trace_id", "generated_at"}

        if isinstance(legacy, dict) and isinstance(migrated, dict):
            # If migrated wraps in envelope, unwrap
            if "data" in migrated and "meta" in migrated:
                migrated = migrated["data"]

            for key in set(legacy.keys()) | set(migrated.keys()):
                if key in dynamic_fields:
                    continue
                if key not in legacy or key not in migrated:
                    return False
                if not self._bodies_equivalent(legacy[key], migrated[key]):
                    return False
            return True

        if isinstance(legacy, list) and isinstance(migrated, list):
            if len(legacy) != len(migrated):
                return False
            return all(
                self._bodies_equivalent(a, b) for a, b in zip(legacy, migrated)
            )

        return legacy == migrated

    def _log_mismatch(
        self, endpoint: str, field: str, expected: Any, actual: Any,
    ) -> None:
        entry = {
            "timestamp": time.time(),
            "endpoint": endpoint,
            "field": field,
            "expected": str(expected)[:500],
            "actual": str(actual)[:500],
        }
        with open(self.mismatch_log, "a") as f:
            f.write(json.dumps(entry) + "\n")

    @property
    def match_rate(self) -> float:
        if self._stats["total"] == 0:
            return 0.0
        return self._stats["matched"] / self._stats["total"]

    async def close(self):
        await self._client.aclose()
```

Integrate shadow validation into your production middleware. After the legacy handler returns a response to the client, fire off the shadow request asynchronously:

```python
import asyncio
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

shadow_validator = ShadowTrafficValidator(migrated_base_url="http://localhost:8001")


class ShadowTrafficMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Process request normally
        body = await request.body()
        response = await call_next(request)

        # Fire shadow request in background (don't block the response)
        try:
            resp_body = json.loads(response.body) if hasattr(response, "body") else None
        except (json.JSONDecodeError, ValueError):
            resp_body = None

        asyncio.create_task(
            shadow_validator.shadow_request(
                endpoint=request.url.path,
                method=request.method,
                body=json.loads(body) if body else None,
                headers=dict(request.headers),
                legacy_status=response.status_code,
                legacy_body=resp_body,
            )
        )

        return response
```

### Rollback Procedures

Every migration needs a rollback plan. Document rollback steps for each migration stage:

**Stage 1 rollback (Discovery).** Remove the `wrap_endpoint` decorator or disable the middleware via feature flag. No data to clean up — discovery mode does not create escrows or process payments.

**Stage 2 rollback (Payment).** Disable payment verification in the feature flags. Any in-flight escrows will expire and refund automatically after the settlement timeout. Communicate the maintenance window to agent consumers via your A2A protocol card status field.

**Stage 3 rollback (Full).** Revert to the pre-migration code deployment. If using the reverse proxy routing approach, switch the nginx config to route all traffic to the legacy upstream. Agent sessions in progress will fail — this is acceptable because agent sessions are designed to be retryable.

### Monitoring During Migration

Set up alerts for these conditions during each migration phase:

```python
MIGRATION_ALERTS = {
    "error_rate_spike": {
        "condition": "error_rate > baseline_error_rate * 1.5",
        "action": "Pause migration, investigate",
        "severity": "high",
    },
    "latency_regression": {
        "condition": "p95_latency > baseline_p95 + 100ms",
        "action": "Check payment verification service health",
        "severity": "medium",
    },
    "402_misconfiguration": {
        "condition": "402_responses_for_human_callers > 0",
        "action": "Immediate rollback — caller classification is broken",
        "severity": "critical",
    },
    "shadow_mismatch_rate": {
        "condition": "shadow_match_rate < 0.95",
        "action": "Stop migration, review mismatches",
        "severity": "high",
    },
    "payment_verification_timeout": {
        "condition": "payment_verification_p95 > 5000ms",
        "action": "Enable verification cache, check GreenHelix status",
        "severity": "medium",
    },
}
```

The most critical alert is `402_misconfiguration`. If human callers ever receive a 402 response, the caller classification logic is broken and the migration must be rolled back immediately. This is the one failure mode that directly impacts existing users.

---

## Chapter 8: Performance Comparison

Adding a commerce layer to your API adds latency. The question is how much and whether it matters. This chapter provides the benchmarking framework to measure the exact overhead and the optimization strategies to minimize it.

### Benchmarking Framework

```python
import asyncio
import time
import statistics
from dataclasses import dataclass, field
from typing import Optional

import httpx


@dataclass
class BenchmarkResult:
    endpoint: str
    variant: str  # "legacy" or "migrated"
    requests: int
    avg_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    min_latency_ms: float
    max_latency_ms: float
    error_count: int
    throughput_rps: float


class MigrationBenchmark:
    """Benchmarks legacy vs migrated endpoint performance."""

    def __init__(
        self,
        legacy_url: str,
        migrated_url: str,
        concurrency: int = 10,
        duration_seconds: int = 30,
    ):
        self.legacy_url = legacy_url.rstrip("/")
        self.migrated_url = migrated_url.rstrip("/")
        self.concurrency = concurrency
        self.duration = duration_seconds

    async def run(
        self,
        endpoint: str,
        method: str = "GET",
        body: object = None,
        headers: dict = None,
    ) -> dict[str, BenchmarkResult]:
        """Run benchmark against both legacy and migrated endpoints."""
        legacy_result = await self._benchmark_variant(
            self.legacy_url, endpoint, method, body, headers or {}, "legacy"
        )
        migrated_result = await self._benchmark_variant(
            self.migrated_url, endpoint, method, body, headers or {}, "migrated"
        )

        return {
            "legacy": legacy_result,
            "migrated": migrated_result,
            "overhead_ms": migrated_result.avg_latency_ms - legacy_result.avg_latency_ms,
            "overhead_pct": (
                (migrated_result.avg_latency_ms - legacy_result.avg_latency_ms)
                / legacy_result.avg_latency_ms * 100
                if legacy_result.avg_latency_ms > 0 else 0
            ),
            "throughput_delta_rps": (
                migrated_result.throughput_rps - legacy_result.throughput_rps
            ),
        }

    async def _benchmark_variant(
        self,
        base_url: str,
        endpoint: str,
        method: str,
        body: object,
        headers: dict,
        variant: str,
    ) -> BenchmarkResult:
        latencies: list[float] = []
        errors = 0
        start_time = time.time()

        async def worker():
            nonlocal errors
            async with httpx.AsyncClient(timeout=30.0) as client:
                while time.time() - start_time < self.duration:
                    req_start = time.time()
                    try:
                        if method.upper() == "GET":
                            resp = await client.get(
                                f"{base_url}{endpoint}", headers=headers
                            )
                        else:
                            resp = await client.request(
                                method, f"{base_url}{endpoint}",
                                json=body, headers=headers,
                            )
                        latency = (time.time() - req_start) * 1000
                        latencies.append(latency)
                        if resp.status_code >= 500:
                            errors += 1
                    except Exception:
                        errors += 1

        workers = [asyncio.create_task(worker()) for _ in range(self.concurrency)]
        await asyncio.gather(*workers)

        total_time = time.time() - start_time

        if not latencies:
            return BenchmarkResult(
                endpoint=endpoint, variant=variant, requests=0,
                avg_latency_ms=0, p50_latency_ms=0, p95_latency_ms=0,
                p99_latency_ms=0, min_latency_ms=0, max_latency_ms=0,
                error_count=errors, throughput_rps=0,
            )

        sorted_latencies = sorted(latencies)
        p50_idx = int(len(sorted_latencies) * 0.50)
        p95_idx = int(len(sorted_latencies) * 0.95)
        p99_idx = int(len(sorted_latencies) * 0.99)

        return BenchmarkResult(
            endpoint=endpoint,
            variant=variant,
            requests=len(latencies),
            avg_latency_ms=round(statistics.mean(latencies), 2),
            p50_latency_ms=round(sorted_latencies[p50_idx], 2),
            p95_latency_ms=round(sorted_latencies[p95_idx], 2),
            p99_latency_ms=round(sorted_latencies[min(p99_idx, len(sorted_latencies) - 1)], 2),
            min_latency_ms=round(sorted_latencies[0], 2),
            max_latency_ms=round(sorted_latencies[-1], 2),
            error_count=errors,
            throughput_rps=round(len(latencies) / total_time, 2),
        )
```

### Understanding the Latency Breakdown

The commerce layer adds latency at four points:

1. **Caller classification** (< 1ms): Header inspection and string matching. Negligible.

2. **Payment verification** (10-100ms): Network call to GreenHelix to verify the payment token. This is the dominant cost. With the verification cache enabled, repeat requests from the same agent with the same token skip this call entirely, reducing it to < 1ms.

3. **Identity verification** (5-50ms): Ed25519 signature verification is a local CPU operation (< 1ms), but resolving the agent identity against GreenHelix adds a network call. Cache agent identity lookups for 5 minutes to amortize this cost.

4. **Response transformation** (< 1ms): JSON wrapping is a memory operation. Even for large responses (1MB+), the transformation adds under 1ms.

The total expected overhead for a cache-miss agent request is 15-150ms, dominated by payment and identity verification network calls. With warm caches, the overhead drops to 1-3ms.

### Optimization Strategies

**Connection pooling.** The `httpx.AsyncClient` used for GreenHelix communication should be a long-lived singleton with connection pooling enabled. Creating a new HTTP client per request adds 50-100ms of connection setup overhead:

```python
# Bad: new client per request
async def verify_payment(token):
    async with httpx.AsyncClient() as client:  # Connection setup every time
        return await client.post(...)

# Good: shared client with connection pool
_greenhelix_client = httpx.AsyncClient(
    base_url="https://api.greenhelix.net",
    timeout=10.0,
    limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
)

async def verify_payment(token):
    return await _greenhelix_client.post(...)  # Reuses connections
```

**Batch verification.** If your API serves requests in bursts (common with agent orchestration patterns where one agent dispatches multiple sub-tasks), batch multiple payment verifications into a single GreenHelix API call:

```python
async def verify_payments_batch(tokens: list[dict]) -> list[dict]:
    """Verify multiple payment tokens in one API call."""
    response = await _greenhelix_client.post(
        "/v1/payments/verify-batch",
        json={"tokens": tokens},
        headers={"Authorization": f"Bearer {api_key}"},
    )
    return response.json()["results"]
```

**Preemptive caching.** Agents that frequently call the same endpoint can be given a bulk payment token that covers N future requests. The verification cache stores the token with a remaining-uses counter instead of a simple boolean:

```python
@dataclass
class BulkTokenEntry:
    token: str
    remaining_uses: int
    endpoint: str
    verified_at: float
    ttl_seconds: int = 3600

    @property
    def is_valid(self) -> bool:
        return self.remaining_uses > 0 and time.time() - self.verified_at < self.ttl_seconds

    def consume(self) -> bool:
        if not self.is_valid:
            return False
        self.remaining_uses -= 1
        return True
```

**Async settlement.** Payment settlement (releasing escrow funds to the seller) does not need to happen before the response is sent. Verify the token synchronously, send the response, then settle asynchronously. This removes settlement latency from the request path entirely:

```python
async def handle_agent_request(request: Request):
    # Verify payment (synchronous, blocks response)
    payment = await verify_payment(request.headers["x-402-payment-token"])

    # Process business logic
    result = await business_logic(request)

    # Settle payment (asynchronous, does not block response)
    asyncio.create_task(settle_payment(payment["escrow_id"]))

    return result
```

### Throughput Considerations

Agent traffic patterns differ from human traffic. Humans send requests with natural pauses (reading, clicking, thinking). Agents send bursts of requests as fast as the API can respond. Your API might handle 100 requests per second from human users comfortably but struggle at 1000 requests per second from agents, even though the per-request processing time is the same. The bottleneck shifts from business logic to the commerce layer — specifically, the connection pool to GreenHelix for payment verification.

Size your connection pool based on expected agent throughput. A pool of 20 keepalive connections to GreenHelix can handle approximately 200 verification requests per second (assuming 100ms average verification time). For higher throughput, increase the pool or enable the verification cache aggressively.

Monitor these throughput metrics during migration:

- Requests per second by caller type (human vs agent)
- GreenHelix verification latency (p50, p95, p99)
- Connection pool utilization (active vs idle connections)
- Cache hit rate for payment verification
- Queue depth if you implement request queuing

---

## What's Next

You now have a complete framework for migrating any REST API to support agent commerce. The `LegacyApiAdapter` wraps your existing endpoints without modifying business logic. The x402 middleware handles payment negotiation at the HTTP layer. The `AuthBridge` runs agent Ed25519 authentication alongside your existing auth system. The `MigrationValidator` automates regression testing throughout the migration. And the benchmarking framework quantifies the exact performance cost of each component.

The migration order should be:

1. Run the assessment checklist on your API.
2. Deploy the `LegacyApiAdapter` in discovery mode (402 responses, no payment processing) on your highest-value read endpoints.
3. Monitor agent traffic patterns for one to two weeks.
4. Enable payment processing on the endpoints where agents are actually sending requests.
5. Roll out identity verification.
6. Migrate the remaining endpoints based on observed demand.
7. Run the `MigrationValidator` continuously in CI.

The GreenHelix platform documentation at [https://docs.greenhelix.net](https://docs.greenhelix.net) covers escrow API details, A2A protocol card registration, and agent identity management. The x402 specification at [https://www.x402.org](https://www.x402.org) defines the full payment header protocol.

Start with one endpoint. Prove it works. Then migrate the rest.

