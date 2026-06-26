---
name: greenhelix-agent-observability-stack
version: "1.3.1"
description: "Agent Observability Stack: Distributed Tracing, Metrics, and Alerting for Multi-Agent Systems. Build a complete observability stack for agent commerce: OpenTelemetry integration, distributed tracing across agent calls, custom metrics, anomaly detection, dashboard design, SLA monitoring, and cost attribution. Includes detailed Python code examples with full API integration."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [observability, monitoring, tracing, metrics, opentelemetry, guide, greenhelix, openclaw, ai-agent]
price_usd: 49.0
content_type: markdown
executable: false
install: none
credentials: none
---
# Agent Observability Stack: Distributed Tracing, Metrics, and Alerting for Multi-Agent Systems

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code, require credentials, or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.


When Agent A calls Agent B which calls Agent C, and the transaction takes 12 seconds instead of 200ms, where is the bottleneck? When your agent fleet processes 10,000 transactions per day and revenue drops 15%, which agent is underperforming? When an escrow settlement fails silently at 3am, how quickly do you find out? Traditional monitoring tools -- ping checks, CPU graphs, uptime dashboards -- cannot answer these questions for distributed agent systems. They were built for monoliths and simple request-response services. Agent commerce is fundamentally different: transactions span multiple autonomous agents, each with its own state, pricing, and failure modes. A single customer-facing operation might traverse five agents, two escrow contracts, and three separate billing events before completing. The failure surface is combinatorial, not linear.
You need observability, not just monitoring. Monitoring tells you something is broken. Observability tells you why, where, and how to fix it. For agent commerce, this means distributed tracing to follow transactions across agent boundaries, custom metrics to measure business outcomes (not just infrastructure health), and intelligent alerting to catch problems before your users do. The difference between a 15-minute outage and a 4-hour revenue leak is whether your observability stack understands agent-to-agent transaction flows.
This guide builds a complete observability stack from scratch. We use OpenTelemetry standards for interoperability, integrate directly with GreenHelix's metrics and event tools for agent-specific telemetry, and build anomaly detection that understands the patterns unique to agent commerce. Every component is production Python code you can deploy today. By the end, you will have distributed tracing across agent calls, custom business metrics, anomaly detection, dashboards, alerting with escalation policies, and SLA monitoring with cost attribution.

## What You'll Learn
- Chapter 1: The Three Pillars of Agent Observability
- Chapter 2: AgentTracer Class
- Chapter 3: Distributed Tracing Across Agent Calls
- Chapter 4: MetricsCollector Class
- Chapter 5: Anomaly Detection
- Chapter 6: Dashboard Design
- Chapter 7: AlertManager Class
- Chapter 8: SLA Monitoring and Cost Attribution
- What's Next

## Full Guide

# Agent Observability Stack: Distributed Tracing, Metrics, and Alerting for Multi-Agent Systems

When Agent A calls Agent B which calls Agent C, and the transaction takes 12 seconds instead of 200ms, where is the bottleneck? When your agent fleet processes 10,000 transactions per day and revenue drops 15%, which agent is underperforming? When an escrow settlement fails silently at 3am, how quickly do you find out? Traditional monitoring tools -- ping checks, CPU graphs, uptime dashboards -- cannot answer these questions for distributed agent systems. They were built for monoliths and simple request-response services. Agent commerce is fundamentally different: transactions span multiple autonomous agents, each with its own state, pricing, and failure modes. A single customer-facing operation might traverse five agents, two escrow contracts, and three separate billing events before completing. The failure surface is combinatorial, not linear.

You need observability, not just monitoring. Monitoring tells you something is broken. Observability tells you why, where, and how to fix it. For agent commerce, this means distributed tracing to follow transactions across agent boundaries, custom metrics to measure business outcomes (not just infrastructure health), and intelligent alerting to catch problems before your users do. The difference between a 15-minute outage and a 4-hour revenue leak is whether your observability stack understands agent-to-agent transaction flows.

This guide builds a complete observability stack from scratch. We use OpenTelemetry standards for interoperability, integrate directly with GreenHelix's metrics and event tools for agent-specific telemetry, and build anomaly detection that understands the patterns unique to agent commerce. Every component is production Python code you can deploy today. By the end, you will have distributed tracing across agent calls, custom business metrics, anomaly detection, dashboards, alerting with escalation policies, and SLA monitoring with cost attribution.

---


> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## Chapter 1: The Three Pillars of Agent Observability

Observability for distributed systems rests on three pillars: traces, metrics, and logs. Each answers a different class of question, and none is sufficient alone. For agent commerce, each pillar has specific requirements that differ from traditional web service observability.

### Traces: Following a Transaction Across Agent Boundaries

A trace is the complete record of a single transaction as it flows through your system. In agent commerce, a trace might begin when a customer agent requests a service, pass through a gateway agent, invoke a specialist agent, trigger an escrow creation, wait for fulfillment, and end with settlement and payment distribution. Each step in that journey is a span, and the collection of spans forms a trace.

The critical difference from traditional distributed tracing is that agent boundaries are not just service boundaries -- they are trust boundaries. When Agent A calls Agent B, there is an economic transaction embedded in that call. The trace must capture not just latency and status codes, but also billing events, escrow state transitions, and the economic context of each span. A span that shows "200 OK in 150ms" is incomplete if it does not also show "billed 0.003 credits, escrow ID esw_abc123 created."

Traces answer questions like: Why did this specific transaction fail? Where did the latency come from? Which agent in the chain was the bottleneck? Did the billing event match the actual work performed?

### Metrics: Measuring Agent Health, Performance, and Business Outcomes

Metrics are aggregated numerical measurements over time. Where traces give you detail about individual transactions, metrics give you the big picture. For agent commerce, metrics fall into three categories.

Infrastructure metrics measure the health of your agents as software systems: CPU usage, memory consumption, request queue depth, connection pool utilization. These are table stakes and most monitoring tools handle them well.

Performance metrics measure how your agents behave under load: request latency (p50, p95, p99), throughput (requests per second), error rates, and timeout rates. These require histograms and percentile calculations, not just averages.

Business metrics are where agent commerce diverges from traditional services. You need to track revenue per agent, cost per transaction, escrow settlement rates, dispute rates, SLA compliance percentages, and customer satisfaction proxies. These metrics directly measure whether your agent fleet is making money or losing it.

GreenHelix's `submit_metrics` tool accepts custom metric submissions, making it the natural sink for all three categories. The tool accepts metric name, value, dimensions, and timestamp, allowing you to build rich, queryable metric series.

### Logs: Structured Event Logging for Debugging

Logs are discrete events with context. In agent commerce, structured logs are essential because you need to correlate log events across agent boundaries. A plain text log line like "Error processing request" is useless when you have 50 agents each producing thousands of log lines per hour.

Structured logs include the trace ID, span ID, agent ID, transaction ID, and any relevant business context as machine-parseable fields. When something goes wrong, you filter logs by trace ID and see every event from every agent involved in that transaction, in chronological order.

GreenHelix's `get_events` tool retrieves event streams that serve as a structured log source. Events include agent interactions, billing events, escrow state changes, and webhook deliveries. By correlating your application logs with GreenHelix events, you get a complete picture of what happened and why.

### Why All Three Matter

Metrics tell you something is wrong: "Error rate spiked to 5% at 14:32." Traces tell you where and why: "Transaction txn_789 failed at Agent C because the escrow creation timed out after 30 seconds." Logs give you the details: "Agent C's connection pool was exhausted because Agent D was not releasing connections after failed settlements."

Without metrics, you do not know there is a problem until users complain. Without traces, you cannot pinpoint which agent or which step is responsible. Without logs, you cannot understand the root cause well enough to fix it. Agent commerce multiplies this dependency because the interactions are more complex, the failure modes are more subtle, and the economic consequences of missed problems are direct and measurable.

### GreenHelix Tools for Observability

Three GreenHelix tools form the foundation of our observability stack:

**submit_metrics** accepts custom metric data points with dimensions. We use this to push agent performance metrics, business metrics, and custom counters into GreenHelix's metric store.

**get_events** retrieves event streams filtered by agent, time range, and event type. We use this to pull structured event data for trace correlation and log enrichment.

**register_webhook** creates webhook subscriptions for specific event types. We use this to trigger real-time alerts when critical events occur, rather than polling for problems.

```python
from greenhelix import GreenHelixClient

client = GreenHelixClient(api_key="your-api-key")

# Submit a custom metric
client.execute_tool("submit_metrics", {
    "agent_id": "agent-payment-processor",
    "metrics": [
        {
            "name": "transaction.latency_ms",
            "value": 245.3,
            "dimensions": {
                "agent": "agent-payment-processor",
                "operation": "process_payment",
                "status": "success"
            },
            "timestamp": "2026-04-07T14:30:00Z"
        }
    ]
})

# Retrieve events for trace correlation
events = client.execute_tool("get_events", {
    "agent_id": "agent-payment-processor",
    "event_types": ["escrow.created", "escrow.settled", "billing.charged"],
    "start_time": "2026-04-07T14:00:00Z",
    "end_time": "2026-04-07T15:00:00Z"
})

# Register a webhook for real-time alerting
client.execute_tool("register_webhook", {
    "url": "https://alerts.myfleet.com/webhook",
    "event_types": ["escrow.failed", "billing.error"],
    "agent_id": "agent-payment-processor"
})
```

These three tools, combined with OpenTelemetry's tracing and metrics APIs, give us everything we need to build a production observability stack.

---

## Chapter 2: AgentTracer Class

The core of our observability stack is a tracer that understands agent commerce. Standard OpenTelemetry tracers create spans for HTTP requests and database calls. Our `AgentTracer` wraps OpenTelemetry to add agent-specific context: billing events, escrow state, economic metadata, and cross-agent trace propagation.

### Design Principles

The tracer must be lightweight. Adding observability should not measurably increase transaction latency. We target less than 1ms overhead per span, which means in-memory buffering with asynchronous export.

The tracer must be OpenTelemetry-compatible. This means traces can be exported to Jaeger, Zipkin, Grafana Tempo, or any other OTel-compatible backend. We do not lock you into a proprietary format.

The tracer must understand agent commerce primitives. Spans should automatically capture billing amounts, escrow IDs, agent identities, and transaction types without requiring manual instrumentation at every call site.

### The AgentTracer Implementation

```python
import time
import uuid
import threading
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    SpanExporter,
    SpanExportResult,
)
from opentelemetry.trace import StatusCode, SpanKind
from opentelemetry.context import attach, detach, set_value, get_value


@dataclass
class AgentSpanAttributes:
    """Standard attributes for agent commerce spans."""
    AGENT_ID = "agent.id"
    AGENT_ROLE = "agent.role"
    TRANSACTION_ID = "agent.transaction.id"
    ESCROW_ID = "agent.escrow.id"
    BILLING_AMOUNT = "agent.billing.amount"
    BILLING_CURRENCY = "agent.billing.currency"
    OPERATION_TYPE = "agent.operation.type"
    PEER_AGENT_ID = "agent.peer.id"
    SLA_TIER = "agent.sla.tier"
    COST_CENTER = "agent.cost_center"


class GreenHelixSpanExporter(SpanExporter):
    """Exports spans as metrics to GreenHelix submit_metrics."""

    def __init__(self, client, agent_id: str, batch_size: int = 50):
        self._client = client
        self._agent_id = agent_id
        self._batch_size = batch_size

    def export(self, spans) -> SpanExportResult:
        metrics_batch = []
        for span in spans:
            duration_ms = (span.end_time - span.start_time) / 1_000_000
            attrs = dict(span.attributes) if span.attributes else {}

            metrics_batch.append({
                "name": "agent.span.duration_ms",
                "value": duration_ms,
                "dimensions": {
                    "agent": self._agent_id,
                    "operation": span.name,
                    "status": "ok" if span.status.status_code == StatusCode.OK
                             else "error",
                    "span_kind": span.kind.name if span.kind else "INTERNAL",
                    "peer_agent": attrs.get(AgentSpanAttributes.PEER_AGENT_ID, ""),
                },
                "timestamp": _ns_to_iso(span.end_time),
            })

            if AgentSpanAttributes.BILLING_AMOUNT in attrs:
                metrics_batch.append({
                    "name": "agent.billing.amount",
                    "value": float(attrs[AgentSpanAttributes.BILLING_AMOUNT]),
                    "dimensions": {
                        "agent": self._agent_id,
                        "operation": span.name,
                        "currency": attrs.get(
                            AgentSpanAttributes.BILLING_CURRENCY, "credits"
                        ),
                    },
                    "timestamp": _ns_to_iso(span.end_time),
                })

            if len(metrics_batch) >= self._batch_size:
                self._flush(metrics_batch)
                metrics_batch = []

        if metrics_batch:
            self._flush(metrics_batch)

        return SpanExportResult.SUCCESS

    def _flush(self, metrics):
        try:
            self._client.execute_tool("submit_metrics", {
                "agent_id": self._agent_id,
                "metrics": metrics,
            })
        except Exception:
            return SpanExportResult.FAILURE

    def shutdown(self):
        pass


def _ns_to_iso(ns_timestamp: int) -> str:
    """Convert nanosecond timestamp to ISO 8601."""
    import datetime
    dt = datetime.datetime.fromtimestamp(
        ns_timestamp / 1e9, tz=datetime.timezone.utc
    )
    return dt.isoformat()


class AgentTracer:
    """OpenTelemetry-compatible tracer for agent commerce."""

    def __init__(
        self,
        agent_id: str,
        client=None,
        service_name: str = None,
        exporters: List[SpanExporter] = None,
    ):
        self.agent_id = agent_id
        self._client = client
        self._service_name = service_name or f"agent-{agent_id}"

        provider = TracerProvider()

        if client:
            gh_exporter = GreenHelixSpanExporter(client, agent_id)
            provider.add_span_processor(BatchSpanProcessor(gh_exporter))

        if exporters:
            for exporter in exporters:
                provider.add_span_processor(BatchSpanProcessor(exporter))

        self._provider = provider
        self._tracer = provider.get_tracer(
            self._service_name, schema_url="https://greenhelix.net/schemas/agent/1.0"
        )

    @contextmanager
    def start_span(
        self,
        name: str,
        kind: SpanKind = SpanKind.INTERNAL,
        attributes: Dict[str, Any] = None,
        peer_agent_id: str = None,
    ):
        """Start a new span with agent commerce context."""
        attrs = {
            AgentSpanAttributes.AGENT_ID: self.agent_id,
        }
        if peer_agent_id:
            attrs[AgentSpanAttributes.PEER_AGENT_ID] = peer_agent_id
        if attributes:
            attrs.update(attributes)

        with self._tracer.start_as_current_span(
            name, kind=kind, attributes=attrs
        ) as span:
            yield span

    @contextmanager
    def trace_agent_call(
        self,
        target_agent_id: str,
        operation: str,
        transaction_id: str = None,
    ):
        """Trace a call from this agent to another agent."""
        txn_id = transaction_id or str(uuid.uuid4())
        attrs = {
            AgentSpanAttributes.OPERATION_TYPE: operation,
            AgentSpanAttributes.TRANSACTION_ID: txn_id,
        }

        with self.start_span(
            f"call.{target_agent_id}.{operation}",
            kind=SpanKind.CLIENT,
            attributes=attrs,
            peer_agent_id=target_agent_id,
        ) as span:
            yield span

    @contextmanager
    def trace_escrow(self, escrow_id: str, operation: str):
        """Trace an escrow lifecycle operation."""
        attrs = {
            AgentSpanAttributes.ESCROW_ID: escrow_id,
            AgentSpanAttributes.OPERATION_TYPE: f"escrow.{operation}",
        }

        with self.start_span(
            f"escrow.{operation}",
            kind=SpanKind.INTERNAL,
            attributes=attrs,
        ) as span:
            yield span

    @contextmanager
    def trace_billing(self, amount: float, currency: str = "credits"):
        """Trace a billing event."""
        attrs = {
            AgentSpanAttributes.BILLING_AMOUNT: amount,
            AgentSpanAttributes.BILLING_CURRENCY: currency,
            AgentSpanAttributes.OPERATION_TYPE: "billing.charge",
        }

        with self.start_span(
            "billing.charge",
            kind=SpanKind.INTERNAL,
            attributes=attrs,
        ) as span:
            yield span

    def get_trace_context(self) -> Dict[str, str]:
        """Extract current trace context for propagation to other agents."""
        span = trace.get_current_span()
        ctx = span.get_span_context()
        if not ctx or not ctx.is_valid:
            return {}

        return {
            "traceparent": f"00-{format(ctx.trace_id, '032x')}-"
                           f"{format(ctx.span_id, '016x')}-"
                           f"{'01' if ctx.trace_flags & 1 else '00'}",
            "x-agent-id": self.agent_id,
        }

    def inject_context(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Inject trace context into outgoing request headers."""
        headers.update(self.get_trace_context())
        return headers

    def shutdown(self):
        """Flush pending spans and shut down the tracer."""
        self._provider.shutdown()
```

### Using the AgentTracer

The tracer integrates naturally with GreenHelix client calls. Each API interaction gets a span, and the spans automatically capture timing, status, and agent commerce attributes.

```python
from greenhelix import GreenHelixClient

client = GreenHelixClient(api_key="your-api-key")
tracer = AgentTracer(agent_id="agent-marketplace", client=client)

# Trace a multi-step transaction
with tracer.trace_agent_call("agent-data-provider", "fetch_dataset") as span:
    result = client.execute_tool("call_agent", {
        "target": "agent-data-provider",
        "operation": "fetch_dataset",
        "params": {"dataset_id": "ds_12345"},
        "headers": tracer.get_trace_context(),
    })
    span.set_attribute("dataset.size_bytes", result.get("size", 0))

    if result.get("status") == "error":
        span.set_status(StatusCode.ERROR, result.get("message", ""))
    else:
        span.set_status(StatusCode.OK)

# Trace an escrow lifecycle
with tracer.trace_escrow("esw_abc123", "create") as span:
    escrow = client.execute_tool("create_escrow", {
        "amount": 5.00,
        "payer": "agent-buyer",
        "payee": "agent-seller",
    })
    span.set_attribute("escrow.amount", 5.00)
    span.set_status(StatusCode.OK)
```

The key design choice is that `AgentTracer` wraps OpenTelemetry rather than replacing it. You can add any standard OTel exporter (Jaeger, OTLP, console) alongside the GreenHelix exporter. This means your agent traces show up in your existing observability infrastructure without any migration.

The `GreenHelixSpanExporter` converts spans to metrics via `submit_metrics`. This dual-purpose export means every traced operation automatically generates latency and billing metrics, eliminating the need to instrument metrics separately for operations you are already tracing.

---

## Chapter 3: Distributed Tracing Across Agent Calls

Single-agent tracing is straightforward. The real challenge is tracing a transaction as it flows through multiple independent agents, each potentially running on different infrastructure, operated by different teams, and communicating through the GreenHelix gateway.

### The Problem: Trace Context Propagation

When Agent A calls Agent B, Agent B has no inherent knowledge of Agent A's trace. Without explicit context propagation, Agent B starts a new, disconnected trace. You end up with five isolated traces instead of one unified trace showing the complete transaction flow.

The W3C Trace Context standard solves this with two HTTP headers: `traceparent` (containing trace ID, span ID, and sampling flags) and `tracestate` (containing vendor-specific data). Our `AgentTracer` already generates these headers via `get_trace_context()`. The challenge is ensuring every agent in the chain extracts, uses, and propagates these headers.

### Trace Context in Agent-to-Agent Calls

Here is the pattern for traced agent-to-agent calls. The calling agent injects context into outgoing headers. The receiving agent extracts context and creates child spans.

```python
# === Calling Agent (Agent A) ===

class TracedAgentClient:
    """HTTP client that automatically propagates trace context."""

    def __init__(self, tracer: AgentTracer, client):
        self._tracer = tracer
        self._client = client

    def call_agent(
        self,
        target_agent: str,
        operation: str,
        params: Dict[str, Any],
        transaction_id: str = None,
    ) -> Dict[str, Any]:
        """Call another agent with automatic trace propagation."""
        with self._tracer.trace_agent_call(
            target_agent, operation, transaction_id
        ) as span:
            headers = self._tracer.get_trace_context()
            headers["x-transaction-id"] = transaction_id or ""

            result = self._client.execute_tool("call_agent", {
                "target": target_agent,
                "operation": operation,
                "params": params,
                "headers": headers,
            })

            span.set_attribute("response.status", result.get("status", "unknown"))

            if result.get("error"):
                span.set_status(StatusCode.ERROR, result["error"])
            else:
                span.set_status(StatusCode.OK)

            return result


# === Receiving Agent (Agent B) ===

from opentelemetry.trace.propagation import TraceContextTextMapPropagator
from opentelemetry.context import Context

class TracedAgentHandler:
    """Request handler that extracts and continues trace context."""

    def __init__(self, tracer: AgentTracer):
        self._tracer = tracer
        self._propagator = TraceContextTextMapPropagator()

    def handle_request(
        self,
        operation: str,
        params: Dict[str, Any],
        headers: Dict[str, str],
    ) -> Dict[str, Any]:
        """Handle an incoming agent request, continuing the trace."""
        # Extract trace context from incoming headers
        ctx = self._propagator.extract(carrier=headers)

        # Create a child span under the extracted context
        token = attach(ctx)
        try:
            with self._tracer.start_span(
                f"handle.{operation}",
                kind=SpanKind.SERVER,
                attributes={
                    "caller.agent_id": headers.get("x-agent-id", "unknown"),
                    AgentSpanAttributes.OPERATION_TYPE: operation,
                },
            ) as span:
                result = self._dispatch(operation, params, span)
                return result
        finally:
            detach(token)

    def _dispatch(
        self, operation: str, params: Dict[str, Any], span
    ) -> Dict[str, Any]:
        """Route to the appropriate operation handler."""
        handler = getattr(self, f"op_{operation}", None)
        if not handler:
            span.set_status(StatusCode.ERROR, f"Unknown operation: {operation}")
            return {"error": f"Unknown operation: {operation}"}
        return handler(params, span)
```

### Tracing a Complete Transaction Through Five Agents

Consider an agent commerce transaction where a customer agent orders a data analysis report. The transaction flows through five agents:

1. **Customer Agent** -- initiates the request
2. **Marketplace Agent** -- matches request to provider
3. **Data Provider Agent** -- supplies raw data
4. **Analysis Agent** -- processes and analyzes data
5. **Delivery Agent** -- formats and delivers the report

```python
def traced_execute(
    client: TracedAgentClient,
    tracer: AgentTracer,
    request: Dict[str, Any],
) -> Dict[str, Any]:
    """Execute a full traced transaction across multiple agents."""
    transaction_id = str(uuid.uuid4())

    with tracer.start_span(
        "transaction.data_analysis_report",
        kind=SpanKind.INTERNAL,
        attributes={
            AgentSpanAttributes.TRANSACTION_ID: transaction_id,
            AgentSpanAttributes.OPERATION_TYPE: "data_analysis_report",
        },
    ) as root_span:

        # Step 1: Find a provider through the marketplace
        with tracer.start_span("step.find_provider") as step_span:
            match = client.call_agent(
                "agent-marketplace",
                "find_provider",
                {"capability": "data_analysis", "budget": request["budget"]},
                transaction_id=transaction_id,
            )
            step_span.set_attribute("provider.matched", match.get("provider_id", ""))

        provider_id = match["provider_id"]

        # Step 2: Create escrow for the transaction
        with tracer.trace_escrow(f"esw_{transaction_id[:8]}", "create") as esc_span:
            escrow = client.call_agent(
                "agent-marketplace",
                "create_escrow",
                {
                    "amount": match["price"],
                    "payer": request["customer_agent"],
                    "payee": provider_id,
                },
                transaction_id=transaction_id,
            )
            esc_span.set_attribute("escrow.id", escrow.get("escrow_id", ""))

        # Step 3: Fetch raw data
        with tracer.start_span("step.fetch_data") as step_span:
            data = client.call_agent(
                match["data_source"],
                "fetch_dataset",
                {"dataset_id": request["dataset_id"]},
                transaction_id=transaction_id,
            )
            step_span.set_attribute("data.records", data.get("record_count", 0))

        # Step 4: Run analysis
        with tracer.start_span("step.analyze") as step_span:
            analysis = client.call_agent(
                provider_id,
                "analyze_data",
                {"data": data["data"], "analysis_type": request["analysis_type"]},
                transaction_id=transaction_id,
            )
            step_span.set_attribute("analysis.confidence", analysis.get("confidence", 0))

        # Step 5: Deliver report
        with tracer.start_span("step.deliver") as step_span:
            delivery = client.call_agent(
                "agent-delivery",
                "deliver_report",
                {
                    "report": analysis["report"],
                    "recipient": request["customer_agent"],
                    "format": request.get("format", "pdf"),
                },
                transaction_id=transaction_id,
            )
            step_span.set_attribute("delivery.channel", delivery.get("channel", ""))

        # Step 6: Settle escrow
        with tracer.trace_escrow(escrow["escrow_id"], "settle") as esc_span:
            settlement = client.call_agent(
                "agent-marketplace",
                "settle_escrow",
                {"escrow_id": escrow["escrow_id"]},
                transaction_id=transaction_id,
            )
            esc_span.set_attribute("settlement.status", settlement.get("status", ""))

        root_span.set_status(StatusCode.OK)
        return {
            "transaction_id": transaction_id,
            "report_url": delivery.get("url"),
            "total_cost": match["price"],
        }
```

### Trace Correlation with GreenHelix Events

GreenHelix events have their own event IDs. To get a complete picture, you need to correlate your OpenTelemetry trace IDs with GreenHelix event IDs. The approach is to embed the trace ID in your GreenHelix API calls and then join on it during analysis.

```python
def trace_escrow_lifecycle(
    tracer: AgentTracer,
    client,
    escrow_id: str,
) -> Dict[str, Any]:
    """Trace and correlate an escrow's full lifecycle with GreenHelix events."""
    trace_ctx = tracer.get_trace_context()
    trace_id = trace_ctx.get("traceparent", "").split("-")[1] if trace_ctx else ""

    with tracer.trace_escrow(escrow_id, "lifecycle") as span:
        # Fetch GreenHelix events for this escrow
        events = client.execute_tool("get_events", {
            "filters": {"escrow_id": escrow_id},
            "start_time": "2026-04-07T00:00:00Z",
            "end_time": "2026-04-07T23:59:59Z",
        })

        lifecycle = {
            "escrow_id": escrow_id,
            "trace_id": trace_id,
            "events": [],
        }

        for event in events.get("events", []):
            event_type = event.get("type", "")
            lifecycle["events"].append({
                "type": event_type,
                "timestamp": event.get("timestamp"),
                "greenhelix_event_id": event.get("event_id"),
                "trace_id": trace_id,
            })

            # Create a child span for each GreenHelix event
            with tracer.start_span(
                f"greenhelix.event.{event_type}",
                attributes={
                    "greenhelix.event_id": event.get("event_id", ""),
                    "greenhelix.event_type": event_type,
                    AgentSpanAttributes.ESCROW_ID: escrow_id,
                },
            ) as event_span:
                event_span.set_status(StatusCode.OK)

        span.set_attribute("lifecycle.event_count", len(lifecycle["events"]))
        return lifecycle
```

### Parent-Child Span Relationships

OpenTelemetry automatically manages parent-child relationships through Python context managers. When you nest `start_span` calls, each inner span becomes a child of the outer span. This creates the tree structure visible in trace visualization tools like Jaeger.

For agent commerce, the hierarchy typically looks like:

```
transaction.data_analysis_report (root)
  |-- step.find_provider
  |     |-- call.agent-marketplace.find_provider (CLIENT)
  |-- escrow.create
  |     |-- call.agent-marketplace.create_escrow (CLIENT)
  |-- step.fetch_data
  |     |-- call.agent-data-source.fetch_dataset (CLIENT)
  |-- step.analyze
  |     |-- call.agent-analysis.analyze_data (CLIENT)
  |-- step.deliver
  |     |-- call.agent-delivery.deliver_report (CLIENT)
  |-- escrow.settle
        |-- call.agent-marketplace.settle_escrow (CLIENT)
```

Each CLIENT span on the calling side has a corresponding SERVER span on the receiving side. The trace ID is the same across all agents, so a trace visualization tool shows the entire transaction as a single, unified trace spanning all five agents.

---

## Chapter 4: MetricsCollector Class

Tracing gives you per-transaction detail. Metrics give you the aggregate view: how is the fleet performing right now, how does today compare to yesterday, and are we meeting our business targets? The `MetricsCollector` class provides a clean API for collecting, buffering, and exporting metrics from your agent fleet.

### Metric Types

There are three fundamental metric types for agent commerce:

**Counters** are monotonically increasing values. Use them for total requests, total errors, total revenue, and total transactions. Counters answer "how many" questions.

**Gauges** are point-in-time values that can go up or down. Use them for active connections, queue depth, current balance, and active escrows. Gauges answer "how much right now" questions.

**Histograms** track the distribution of values. Use them for latency, transaction amounts, and response sizes. Histograms answer "what is the distribution" questions, giving you percentiles (p50, p95, p99) rather than just averages.

### The MetricsCollector Implementation

```python
import time
import math
import threading
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any


@dataclass
class MetricPoint:
    """A single metric data point."""
    name: str
    value: float
    dimensions: Dict[str, str]
    timestamp: float
    metric_type: str  # "counter", "gauge", "histogram"


class HistogramBuckets:
    """Tracks value distribution for histogram metrics."""

    def __init__(self, boundaries: List[float] = None):
        self.boundaries = boundaries or [
            5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000
        ]
        self.buckets = [0] * (len(self.boundaries) + 1)
        self.sum = 0.0
        self.count = 0
        self.min = float("inf")
        self.max = float("-inf")
        self._values: List[float] = []

    def observe(self, value: float):
        self.sum += value
        self.count += 1
        self.min = min(self.min, value)
        self.max = max(self.max, value)
        self._values.append(value)

        for i, boundary in enumerate(self.boundaries):
            if value <= boundary:
                self.buckets[i] += 1
                return
        self.buckets[-1] += 1

    def percentile(self, p: float) -> float:
        if not self._values:
            return 0.0
        sorted_vals = sorted(self._values)
        idx = int(math.ceil(p / 100.0 * len(sorted_vals))) - 1
        return sorted_vals[max(0, idx)]

    def reset(self):
        self.buckets = [0] * (len(self.boundaries) + 1)
        self.sum = 0.0
        self.count = 0
        self.min = float("inf")
        self.max = float("-inf")
        self._values = []


class MetricsCollector:
    """Collects, buffers, and exports agent commerce metrics."""

    def __init__(
        self,
        agent_id: str,
        client=None,
        flush_interval_seconds: float = 60.0,
        buffer_size: int = 1000,
    ):
        self.agent_id = agent_id
        self._client = client
        self._flush_interval = flush_interval_seconds
        self._buffer_size = buffer_size

        self._counters: Dict[str, float] = defaultdict(float)
        self._gauges: Dict[str, float] = {}
        self._histograms: Dict[str, HistogramBuckets] = {}
        self._buffer: List[MetricPoint] = []
        self._lock = threading.Lock()

        self._dimensions_registry: Dict[str, Dict[str, str]] = {}
        self._flush_callbacks: List[Callable] = []

        self._running = False
        self._flush_thread: Optional[threading.Thread] = None

    def start(self):
        """Start the background flush thread."""
        self._running = True
        self._flush_thread = threading.Thread(
            target=self._flush_loop, daemon=True
        )
        self._flush_thread.start()

    def stop(self):
        """Stop the background flush thread and flush remaining metrics."""
        self._running = False
        if self._flush_thread:
            self._flush_thread.join(timeout=5.0)
        self.flush()

    # --- Counter Operations ---

    def increment(
        self,
        name: str,
        value: float = 1.0,
        dimensions: Dict[str, str] = None,
    ):
        """Increment a counter metric."""
        key = self._make_key(name, dimensions)
        with self._lock:
            self._counters[key] += value
            self._dimensions_registry[key] = dimensions or {}
            self._buffer_point(name, self._counters[key], dimensions, "counter")

    # --- Gauge Operations ---

    def gauge_set(
        self,
        name: str,
        value: float,
        dimensions: Dict[str, str] = None,
    ):
        """Set a gauge metric to an absolute value."""
        key = self._make_key(name, dimensions)
        with self._lock:
            self._gauges[key] = value
            self._dimensions_registry[key] = dimensions or {}
            self._buffer_point(name, value, dimensions, "gauge")

    def gauge_increment(
        self,
        name: str,
        value: float = 1.0,
        dimensions: Dict[str, str] = None,
    ):
        """Increment a gauge metric."""
        key = self._make_key(name, dimensions)
        with self._lock:
            self._gauges[key] = self._gauges.get(key, 0.0) + value
            self._dimensions_registry[key] = dimensions or {}
            self._buffer_point(name, self._gauges[key], dimensions, "gauge")

    # --- Histogram Operations ---

    def observe(
        self,
        name: str,
        value: float,
        dimensions: Dict[str, str] = None,
        boundaries: List[float] = None,
    ):
        """Record an observation in a histogram metric."""
        key = self._make_key(name, dimensions)
        with self._lock:
            if key not in self._histograms:
                self._histograms[key] = HistogramBuckets(boundaries)
            self._histograms[key].observe(value)
            self._dimensions_registry[key] = dimensions or {}
            self._buffer_point(name, value, dimensions, "histogram")

    # --- Business Metric Helpers ---

    def record_transaction(
        self,
        operation: str,
        duration_ms: float,
        amount: float,
        status: str,
        peer_agent: str = "",
    ):
        """Record a complete transaction with all standard metrics."""
        dims = {
            "operation": operation,
            "status": status,
            "peer_agent": peer_agent,
        }

        self.increment("transactions.total", 1.0, dims)
        self.observe("transactions.duration_ms", duration_ms, dims)
        self.observe("transactions.amount", amount, dims)

        if status == "error":
            self.increment("transactions.errors", 1.0, dims)

    def record_revenue(self, amount: float, source: str, currency: str = "credits"):
        """Record revenue from an agent operation."""
        dims = {"source": source, "currency": currency}
        self.increment("revenue.total", amount, dims)

    def record_cost(self, amount: float, category: str, currency: str = "credits"):
        """Record a cost incurred by the agent."""
        dims = {"category": category, "currency": currency}
        self.increment("costs.total", amount, dims)

    def record_escrow_event(self, event_type: str, amount: float, escrow_id: str):
        """Record an escrow lifecycle event."""
        dims = {"event_type": event_type}
        self.increment(f"escrow.{event_type}", 1.0, dims)
        self.observe("escrow.amount", amount, dims)

    # --- Export and Flush ---

    def flush(self):
        """Flush buffered metrics to GreenHelix."""
        with self._lock:
            if not self._buffer:
                return
            batch = self._buffer[:]
            self._buffer.clear()

        if self._client:
            metrics_payload = [
                {
                    "name": point.name,
                    "value": point.value,
                    "dimensions": {
                        "agent": self.agent_id,
                        **point.dimensions,
                    },
                    "timestamp": _ts_to_iso(point.timestamp),
                }
                for point in batch
            ]

            try:
                self._client.execute_tool("submit_metrics", {
                    "agent_id": self.agent_id,
                    "metrics": metrics_payload,
                })
            except Exception as e:
                # Re-buffer on failure for retry
                with self._lock:
                    self._buffer = batch + self._buffer
                    # Prevent unbounded growth
                    if len(self._buffer) > self._buffer_size * 2:
                        self._buffer = self._buffer[-self._buffer_size:]

        for callback in self._flush_callbacks:
            try:
                callback(batch)
            except Exception:
                pass

    def get_histogram_summary(
        self, name: str, dimensions: Dict[str, str] = None
    ) -> Dict[str, float]:
        """Get summary statistics for a histogram metric."""
        key = self._make_key(name, dimensions)
        with self._lock:
            hist = self._histograms.get(key)
            if not hist or hist.count == 0:
                return {}
            return {
                "count": hist.count,
                "sum": hist.sum,
                "min": hist.min,
                "max": hist.max,
                "avg": hist.sum / hist.count,
                "p50": hist.percentile(50),
                "p95": hist.percentile(95),
                "p99": hist.percentile(99),
            }

    def on_flush(self, callback: Callable):
        """Register a callback to be called on each flush."""
        self._flush_callbacks.append(callback)

    # --- Internal ---

    def _buffer_point(
        self,
        name: str,
        value: float,
        dimensions: Dict[str, str],
        metric_type: str,
    ):
        point = MetricPoint(
            name=name,
            value=value,
            dimensions=dimensions or {},
            timestamp=time.time(),
            metric_type=metric_type,
        )
        self._buffer.append(point)

        if len(self._buffer) >= self._buffer_size:
            threading.Thread(target=self.flush, daemon=True).start()

    def _flush_loop(self):
        while self._running:
            time.sleep(self._flush_interval)
            self.flush()

    @staticmethod
    def _make_key(name: str, dimensions: Dict[str, str] = None) -> str:
        if not dimensions:
            return name
        dim_str = ",".join(f"{k}={v}" for k, v in sorted(dimensions.items()))
        return f"{name}{{{dim_str}}}"


def _ts_to_iso(ts: float) -> str:
    import datetime
    dt = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)
    return dt.isoformat()
```

### Using the MetricsCollector

```python
client = GreenHelixClient(api_key="your-api-key")
metrics = MetricsCollector(agent_id="agent-marketplace", client=client)
metrics.start()

# Record a transaction
start = time.time()
result = process_order(order)
duration_ms = (time.time() - start) * 1000

metrics.record_transaction(
    operation="process_order",
    duration_ms=duration_ms,
    amount=order["amount"],
    status="success" if result["ok"] else "error",
    peer_agent=order["seller_agent"],
)

# Record revenue and costs
metrics.record_revenue(order["commission"], source="marketplace_fee")
metrics.record_cost(order["gateway_fee"], category="gateway")

# Record escrow events
metrics.record_escrow_event("created", order["amount"], result["escrow_id"])

# Get latency percentiles
summary = metrics.get_histogram_summary(
    "transactions.duration_ms",
    {"operation": "process_order", "status": "success"},
)
print(f"p50={summary['p50']:.0f}ms  p95={summary['p95']:.0f}ms  p99={summary['p99']:.0f}ms")

# Clean shutdown
metrics.stop()
```

The `MetricsCollector` buffers metrics in memory and flushes them periodically (default 60 seconds) or when the buffer fills. This batching reduces API calls to GreenHelix while ensuring metrics are not lost. The retry logic on flush failure re-buffers metrics for the next flush cycle, with a cap to prevent unbounded memory growth.

---

## Chapter 5: Anomaly Detection

Raw metrics are necessary but not sufficient. An agent operator managing a fleet of 50 agents cannot watch 200 dashboards for problems. You need automated anomaly detection that understands normal patterns and alerts on deviations.

### Statistical Anomaly Detection for Agent Metrics

Anomaly detection for agent commerce differs from traditional infrastructure monitoring in two ways. First, agent traffic patterns are often bursty and non-uniform: a marketplace agent might handle 100 requests per minute during business hours and 5 per minute overnight. Second, business metrics like revenue have seasonal patterns (daily, weekly, monthly) that must be accounted for.

Our `AnomalyDetector` uses three complementary detection methods: Z-score for sudden spikes, percentage change for trend shifts, and seasonal decomposition for pattern violations.

```python
import math
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class AnomalyType(Enum):
    SPIKE = "spike"
    DROP = "drop"
    TREND_CHANGE = "trend_change"
    SEASONAL_VIOLATION = "seasonal_violation"


class Severity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Anomaly:
    """A detected anomaly in a metric series."""
    metric_name: str
    anomaly_type: AnomalyType
    severity: Severity
    current_value: float
    expected_value: float
    deviation: float
    timestamp: float
    dimensions: Dict[str, str] = field(default_factory=dict)
    message: str = ""


class MetricWindow:
    """Sliding window of metric values for statistical analysis."""

    def __init__(self, window_size: int = 60):
        self._values: deque = deque(maxlen=window_size)
        self._timestamps: deque = deque(maxlen=window_size)

    def add(self, value: float, timestamp: float = None):
        self._values.append(value)
        self._timestamps.append(timestamp or time.time())

    @property
    def count(self) -> int:
        return len(self._values)

    @property
    def mean(self) -> float:
        if not self._values:
            return 0.0
        return sum(self._values) / len(self._values)

    @property
    def std(self) -> float:
        if len(self._values) < 2:
            return 0.0
        m = self.mean
        variance = sum((v - m) ** 2 for v in self._values) / (len(self._values) - 1)
        return math.sqrt(variance)

    @property
    def values(self) -> List[float]:
        return list(self._values)

    @property
    def latest(self) -> Optional[float]:
        return self._values[-1] if self._values else None

    def rate_of_change(self, periods: int = 5) -> Optional[float]:
        """Calculate rate of change over the last N periods."""
        if len(self._values) < periods + 1:
            return None
        recent = list(self._values)[-periods:]
        older = list(self._values)[-(periods + 1)]
        if older == 0:
            return None
        return (recent[-1] - older) / older


class SeasonalProfile:
    """Tracks seasonal patterns for a metric (hourly buckets)."""

    def __init__(self, num_buckets: int = 24):
        self._num_buckets = num_buckets
        self._bucket_values: Dict[int, List[float]] = {
            i: [] for i in range(num_buckets)
        }

    def add(self, value: float, timestamp: float):
        import datetime
        dt = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
        bucket = dt.hour  # Hourly buckets
        self._bucket_values[bucket].append(value)

    def expected_value(self, timestamp: float) -> Optional[Tuple[float, float]]:
        """Return (mean, std) for the expected value at this time."""
        import datetime
        dt = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
        bucket = dt.hour
        values = self._bucket_values.get(bucket, [])
        if len(values) < 7:  # Need at least a week of data
            return None
        m = sum(values) / len(values)
        variance = sum((v - m) ** 2 for v in values) / (len(values) - 1)
        return m, math.sqrt(variance)


class AnomalyDetector:
    """Detects anomalies in agent commerce metric streams."""

    def __init__(
        self,
        z_score_threshold: float = 3.0,
        pct_change_threshold: float = 0.30,
        seasonal_z_threshold: float = 2.5,
        min_data_points: int = 20,
    ):
        self._z_threshold = z_score_threshold
        self._pct_threshold = pct_change_threshold
        self._seasonal_z_threshold = seasonal_z_threshold
        self._min_data_points = min_data_points

        self._windows: Dict[str, MetricWindow] = {}
        self._seasonal: Dict[str, SeasonalProfile] = {}
        self._anomaly_callbacks: List = []

    def observe(
        self,
        metric_name: str,
        value: float,
        dimensions: Dict[str, str] = None,
        timestamp: float = None,
    ) -> List[Anomaly]:
        """Observe a metric value and check for anomalies."""
        ts = timestamp or time.time()
        key = self._make_key(metric_name, dimensions)

        if key not in self._windows:
            self._windows[key] = MetricWindow(window_size=120)
            self._seasonal[key] = SeasonalProfile()

        window = self._windows[key]
        seasonal = self._seasonal[key]

        window.add(value, ts)
        seasonal.add(value, ts)

        anomalies = []

        if window.count >= self._min_data_points:
            # Z-score detection
            z_anomaly = self._check_z_score(
                metric_name, value, window, dimensions, ts
            )
            if z_anomaly:
                anomalies.append(z_anomaly)

            # Percentage change detection
            pct_anomaly = self._check_pct_change(
                metric_name, value, window, dimensions, ts
            )
            if pct_anomaly:
                anomalies.append(pct_anomaly)

        # Seasonal detection
        seasonal_anomaly = self._check_seasonal(
            metric_name, value, seasonal, dimensions, ts
        )
        if seasonal_anomaly:
            anomalies.append(seasonal_anomaly)

        for anomaly in anomalies:
            for callback in self._anomaly_callbacks:
                try:
                    callback(anomaly)
                except Exception:
                    pass

        return anomalies

    def on_anomaly(self, callback):
        """Register a callback for detected anomalies."""
        self._anomaly_callbacks.append(callback)

    def _check_z_score(
        self,
        metric_name: str,
        value: float,
        window: MetricWindow,
        dimensions: Dict[str, str],
        timestamp: float,
    ) -> Optional[Anomaly]:
        """Detect anomalies using Z-score (standard deviations from mean)."""
        std = window.std
        if std == 0:
            return None

        z_score = abs(value - window.mean) / std
        if z_score < self._z_threshold:
            return None

        anomaly_type = AnomalyType.SPIKE if value > window.mean else AnomalyType.DROP
        severity = self._z_to_severity(z_score)

        return Anomaly(
            metric_name=metric_name,
            anomaly_type=anomaly_type,
            severity=severity,
            current_value=value,
            expected_value=window.mean,
            deviation=z_score,
            timestamp=timestamp,
            dimensions=dimensions or {},
            message=f"{metric_name} is {z_score:.1f} standard deviations "
                    f"{'above' if value > window.mean else 'below'} the mean "
                    f"(current={value:.2f}, mean={window.mean:.2f}, std={std:.2f})",
        )

    def _check_pct_change(
        self,
        metric_name: str,
        value: float,
        window: MetricWindow,
        dimensions: Dict[str, str],
        timestamp: float,
    ) -> Optional[Anomaly]:
        """Detect anomalies using percentage change over recent periods."""
        roc = window.rate_of_change(periods=5)
        if roc is None or abs(roc) < self._pct_threshold:
            return None

        anomaly_type = (
            AnomalyType.TREND_CHANGE
        )
        severity = Severity.MEDIUM if abs(roc) < 0.5 else Severity.HIGH

        return Anomaly(
            metric_name=metric_name,
            anomaly_type=anomaly_type,
            severity=severity,
            current_value=value,
            expected_value=window.mean,
            deviation=roc,
            timestamp=timestamp,
            dimensions=dimensions or {},
            message=f"{metric_name} changed by {roc*100:.1f}% over the last 5 periods "
                    f"(current={value:.2f})",
        )

    def _check_seasonal(
        self,
        metric_name: str,
        value: float,
        seasonal: SeasonalProfile,
        dimensions: Dict[str, str],
        timestamp: float,
    ) -> Optional[Anomaly]:
        """Detect anomalies relative to seasonal patterns."""
        expected = seasonal.expected_value(timestamp)
        if expected is None:
            return None

        mean, std = expected
        if std == 0:
            return None

        z_score = abs(value - mean) / std
        if z_score < self._seasonal_z_threshold:
            return None

        return Anomaly(
            metric_name=metric_name,
            anomaly_type=AnomalyType.SEASONAL_VIOLATION,
            severity=self._z_to_severity(z_score),
            current_value=value,
            expected_value=mean,
            deviation=z_score,
            timestamp=timestamp,
            dimensions=dimensions or {},
            message=f"{metric_name} deviates {z_score:.1f} std from seasonal expectation "
                    f"(current={value:.2f}, expected={mean:.2f} +/- {std:.2f})",
        )

    @staticmethod
    def _z_to_severity(z_score: float) -> Severity:
        if z_score >= 5.0:
            return Severity.CRITICAL
        elif z_score >= 4.0:
            return Severity.HIGH
        elif z_score >= 3.0:
            return Severity.MEDIUM
        return Severity.LOW

    @staticmethod
    def _make_key(name: str, dimensions: Dict[str, str] = None) -> str:
        if not dimensions:
            return name
        dim_str = ",".join(f"{k}={v}" for k, v in sorted(dimensions.items()))
        return f"{name}{{{dim_str}}}"
```

### Integrating Anomaly Detection with Metrics Collection

The `AnomalyDetector` works alongside the `MetricsCollector`. Feed every metric observation to both:

```python
detector = AnomalyDetector(
    z_score_threshold=3.0,
    pct_change_threshold=0.30,
    min_data_points=20,
)
metrics = MetricsCollector(agent_id="agent-marketplace", client=client)

def record_and_detect(
    metric_name: str,
    value: float,
    dimensions: Dict[str, str] = None,
):
    """Record a metric and check for anomalies in one call."""
    metrics.observe(metric_name, value, dimensions)
    anomalies = detector.observe(metric_name, value, dimensions)

    for anomaly in anomalies:
        print(f"ANOMALY: {anomaly.message}")
        # Feed anomaly back as a metric for meta-monitoring
        metrics.increment(
            "anomalies.detected",
            1.0,
            {
                "metric": anomaly.metric_name,
                "type": anomaly.anomaly_type.value,
                "severity": anomaly.severity.value,
            },
        )

    return anomalies

# Example: detect latency spike
record_and_detect(
    "transactions.duration_ms",
    12500.0,  # 12.5 seconds -- likely anomalous
    {"operation": "process_order"},
)
```

The detector's sliding window approach means it adapts to changing baselines. If your agent's latency gradually increases from 200ms to 300ms over a week, the detector adjusts its baseline and does not fire false alerts. But if latency jumps from 300ms to 3000ms in one minute, the Z-score catches it immediately.

The seasonal profile prevents false alerts during known traffic patterns. If your agent processes fewer transactions overnight, a drop from 100 req/s to 10 req/s at midnight is not anomalous -- the seasonal profile knows that is normal for that hour.

---

## Chapter 6: Dashboard Design

Anomaly detection catches problems automatically, but operators still need dashboards for situational awareness, capacity planning, and stakeholder reporting. This chapter describes the three essential dashboards for agent commerce operations, with the data sources and queries needed to populate them.

### Dashboard 1: Fleet Health Overview

The fleet health dashboard is the first thing you look at when something might be wrong. It answers: "Is everything healthy right now?"

**Key panels:**

1. **Agent Status Grid** -- A grid showing every agent with color-coded health status (green/yellow/red). Data source: gauge metrics for each agent's last heartbeat timestamp and error rate. An agent is green if error rate is below 1% and last heartbeat was within 60 seconds, yellow if error rate is 1-5% or heartbeat is 60-120 seconds stale, and red otherwise.

2. **Fleet Error Rate** -- A time series chart showing the aggregate error rate across all agents over the last 24 hours, with the anomaly detection threshold overlaid. Data source: counter metrics `transactions.errors` / `transactions.total`, aggregated per minute.

3. **Active Escrows** -- A gauge showing the current number of open (unsettled) escrows, with a trend line. A rising trend indicates settlement failures or slow processing. Data source: gauge metric `escrow.active_count`.

4. **Latency Heatmap** -- A heatmap showing p95 latency for each agent over the last 6 hours. Columns are time buckets (15-minute intervals), rows are agents, and color intensity represents latency. This makes it easy to spot both fleet-wide issues (a hot column) and per-agent issues (a hot row). Data source: histogram metric `transactions.duration_ms`, p95 aggregation.

5. **Alert Summary** -- A table of currently active alerts grouped by severity, with acknowledge/resolve buttons. Data source: the AlertManager's active alerts state (covered in Chapter 7).

```python
def build_fleet_health_query(agent_ids: List[str]) -> Dict[str, Any]:
    """Build the query configuration for the fleet health dashboard."""
    return {
        "panels": [
            {
                "title": "Agent Status Grid",
                "type": "status_grid",
                "query": {
                    "metrics": ["agent.heartbeat.age_seconds", "transactions.errors"],
                    "group_by": ["agent"],
                    "thresholds": {
                        "green": {"error_rate": 0.01, "heartbeat_age": 60},
                        "yellow": {"error_rate": 0.05, "heartbeat_age": 120},
                        "red": {"error_rate": 1.0, "heartbeat_age": float("inf")},
                    },
                },
            },
            {
                "title": "Fleet Error Rate",
                "type": "time_series",
                "query": {
                    "metric": "transactions.errors",
                    "aggregation": "rate",
                    "interval": "1m",
                    "time_range": "24h",
                },
            },
            {
                "title": "Active Escrows",
                "type": "gauge_with_trend",
                "query": {
                    "metric": "escrow.active_count",
                    "aggregation": "latest",
                    "trend_window": "6h",
                },
            },
            {
                "title": "Latency Heatmap",
                "type": "heatmap",
                "query": {
                    "metric": "transactions.duration_ms",
                    "aggregation": "p95",
                    "group_by": ["agent"],
                    "interval": "15m",
                    "time_range": "6h",
                },
            },
        ],
    }
```

### Dashboard 2: Transaction Flow

The transaction flow dashboard shows how transactions move through your agent fleet. It answers: "What is happening to our transactions?"

**Key panels:**

1. **Transaction Funnel** -- A funnel visualization showing transactions at each stage: initiated, matched, escrowed, fulfilled, settled, completed. Drop-off at each stage reveals where transactions are failing. Data source: counter metrics per transaction stage.

2. **Agent-to-Agent Flow** -- A Sankey diagram or chord chart showing traffic volume between agent pairs. Thick lines indicate high-volume relationships. Clicking a flow line drills down to latency and error metrics for that specific agent pair. Data source: counter metric `transactions.total` with `peer_agent` dimension.

3. **Escrow Lifecycle** -- A state diagram showing escrows in each state (pending, funded, fulfilled, settled, disputed, expired) with transition rates. Data source: counter metrics per escrow state transition.

4. **Slow Transactions** -- A table of the 20 slowest transactions in the last hour, with trace IDs linked to the trace viewer. This gives operators one-click access to detailed trace analysis for the worst-performing transactions. Data source: histogram metric `transactions.duration_ms`, top-N query.

5. **Transaction Volume** -- A stacked area chart showing transaction volume per operation type over the last 24 hours. Data source: counter metric `transactions.total` grouped by `operation` dimension.

### Dashboard 3: Revenue and Cost

The revenue and cost dashboard is for business stakeholders and capacity planning. It answers: "Are we making money, and where is it going?"

**Key panels:**

1. **Net Revenue** -- A single large number showing today's net revenue (revenue minus costs), with comparison to same day last week. Data source: counter metrics `revenue.total` minus `costs.total`.

2. **Revenue by Agent** -- A bar chart showing revenue contribution per agent. Identifies your most and least profitable agents. Data source: counter metric `revenue.total` grouped by `agent` dimension.

3. **Cost Breakdown** -- A pie chart showing costs by category: gateway fees, escrow fees, infrastructure, third-party API calls. Data source: counter metric `costs.total` grouped by `category` dimension.

4. **Revenue Trend** -- A time series comparing daily revenue over the last 30 days, with the anomaly detection band overlaid. Revenue drops outside the expected band trigger alerts. Data source: counter metric `revenue.total`, daily aggregation.

5. **Per-Transaction Economics** -- A table showing average revenue, cost, and margin per operation type. Identifies operations that are losing money. Data source: derived from `revenue.total` and `costs.total` metrics divided by `transactions.total`, grouped by `operation`.

Each dashboard should auto-refresh on a cadence appropriate to its purpose: fleet health every 30 seconds, transaction flow every minute, revenue and cost every 5 minutes. The underlying data all comes from the `MetricsCollector` metrics pushed to GreenHelix via `submit_metrics`, queried back for visualization.

---

## Chapter 7: AlertManager Class

Dashboards require someone to be watching them. Alerts push problems to the right people at the right time. The `AlertManager` evaluates alert rules against incoming metrics, deduplicates and groups related alerts, routes them through appropriate channels, and escalates when problems are not acknowledged.

### Alert Rule Types

Three types of alert rules cover the scenarios that matter for agent commerce:

**Threshold alerts** fire when a metric crosses a static or dynamic boundary. Example: "Error rate exceeds 5%." These are simple and reliable for known boundaries.

**Rate-of-change alerts** fire when a metric changes too quickly. Example: "Transaction volume dropped more than 30% in 10 minutes." These catch problems that threshold alerts miss because the absolute value might still be "normal."

**Anomaly-based alerts** fire when the `AnomalyDetector` identifies a statistical anomaly. These adapt to changing baselines and seasonal patterns, catching subtle issues that would require constantly adjusting threshold values.

### The AlertManager Implementation

```python
import time
import uuid
import threading
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any
from enum import Enum
from collections import defaultdict


class AlertState(Enum):
    FIRING = "firing"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class AlertChannel(Enum):
    WEBHOOK = "webhook"
    EMAIL = "email"
    SLACK = "slack"
    PAGERDUTY = "pagerduty"


@dataclass
class AlertRule:
    """Definition of an alert rule."""
    name: str
    metric_name: str
    condition: str  # "threshold", "rate_of_change", "anomaly"
    threshold: Optional[float] = None
    comparison: str = "gt"  # "gt", "lt", "gte", "lte"
    window_minutes: int = 5
    severity: str = "medium"
    channels: List[AlertChannel] = field(default_factory=list)
    dimensions_filter: Dict[str, str] = field(default_factory=dict)
    cooldown_minutes: int = 15
    escalation_minutes: int = 30
    description: str = ""
    runbook_url: str = ""


@dataclass
class Alert:
    """An active alert instance."""
    id: str
    rule: AlertRule
    state: AlertState
    fired_at: float
    last_value: float
    message: str
    acknowledged_at: Optional[float] = None
    acknowledged_by: Optional[str] = None
    resolved_at: Optional[float] = None
    escalated: bool = False
    notification_count: int = 0
    dimensions: Dict[str, str] = field(default_factory=dict)


class AlertManager:
    """Manages alert rules, routing, deduplication, and escalation."""

    def __init__(
        self,
        agent_id: str,
        client=None,
        anomaly_detector: "AnomalyDetector" = None,
    ):
        self.agent_id = agent_id
        self._client = client
        self._detector = anomaly_detector

        self._rules: Dict[str, AlertRule] = {}
        self._active_alerts: Dict[str, Alert] = {}
        self._alert_history: List[Alert] = []
        self._cooldowns: Dict[str, float] = {}
        self._lock = threading.Lock()

        # Channel handlers
        self._channel_handlers: Dict[AlertChannel, Callable] = {}

        # Escalation thread
        self._running = False
        self._escalation_thread: Optional[threading.Thread] = None

    def start(self):
        """Start the escalation monitoring thread."""
        self._running = True
        self._escalation_thread = threading.Thread(
            target=self._escalation_loop, daemon=True
        )
        self._escalation_thread.start()

    def stop(self):
        self._running = False
        if self._escalation_thread:
            self._escalation_thread.join(timeout=5.0)

    # --- Rule Management ---

    def add_rule(self, rule: AlertRule):
        """Add an alert rule."""
        self._rules[rule.name] = rule

    def remove_rule(self, name: str):
        """Remove an alert rule."""
        self._rules.pop(name, None)

    # --- Channel Configuration ---

    def register_channel(self, channel: AlertChannel, handler: Callable):
        """Register a notification handler for a channel."""
        self._channel_handlers[channel] = handler

    def configure_webhook(self, url: str):
        """Configure webhook channel with a URL."""
        import urllib.request

        def webhook_handler(alert: Alert, message: str):
            payload = json.dumps({
                "alert_id": alert.id,
                "rule": alert.rule.name,
                "severity": alert.rule.severity,
                "state": alert.state.value,
                "message": message,
                "value": alert.last_value,
                "fired_at": alert.fired_at,
                "agent_id": self.agent_id,
                "dimensions": alert.dimensions,
            }).encode()

            req = urllib.request.Request(
                url,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            try:
                urllib.request.urlopen(req, timeout=10)
            except Exception:
                pass

        self._channel_handlers[AlertChannel.WEBHOOK] = webhook_handler

    def configure_slack(self, webhook_url: str, default_channel: str = "#alerts"):
        """Configure Slack channel."""
        import urllib.request

        def slack_handler(alert: Alert, message: str):
            severity_emoji = {
                "critical": ":red_circle:",
                "high": ":large_orange_circle:",
                "medium": ":large_yellow_circle:",
                "low": ":white_circle:",
            }
            emoji = severity_emoji.get(alert.rule.severity, ":grey_question:")

            payload = json.dumps({
                "channel": default_channel,
                "text": f"{emoji} *{alert.rule.name}*\n{message}",
                "attachments": [
                    {
                        "color": {
                            "critical": "#ff0000",
                            "high": "#ff8800",
                            "medium": "#ffcc00",
                            "low": "#cccccc",
                        }.get(alert.rule.severity, "#cccccc"),
                        "fields": [
                            {"title": "Agent", "value": self.agent_id, "short": True},
                            {"title": "Value", "value": str(alert.last_value), "short": True},
                            {"title": "Severity", "value": alert.rule.severity, "short": True},
                            {"title": "Alert ID", "value": alert.id, "short": True},
                        ],
                    }
                ],
            }).encode()

            req = urllib.request.Request(
                webhook_url,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            try:
                urllib.request.urlopen(req, timeout=10)
            except Exception:
                pass

        self._channel_handlers[AlertChannel.SLACK] = slack_handler

    # --- Alert Evaluation ---

    def evaluate(
        self,
        metric_name: str,
        value: float,
        dimensions: Dict[str, str] = None,
    ) -> List[Alert]:
        """Evaluate all rules against a metric value."""
        new_alerts = []
        dims = dimensions or {}

        for rule in self._rules.values():
            if rule.metric_name != metric_name:
                continue

            # Check dimension filter
            if rule.dimensions_filter:
                if not all(
                    dims.get(k) == v for k, v in rule.dimensions_filter.items()
                ):
                    continue

            # Check cooldown
            cooldown_key = f"{rule.name}:{self._dim_key(dims)}"
            if cooldown_key in self._cooldowns:
                if time.time() - self._cooldowns[cooldown_key] < rule.cooldown_minutes * 60:
                    continue

            triggered = False

            if rule.condition == "threshold":
                triggered = self._check_threshold(rule, value)
            elif rule.condition == "rate_of_change":
                triggered = self._check_rate_of_change(rule, value, metric_name, dims)
            elif rule.condition == "anomaly" and self._detector:
                anomalies = self._detector.observe(metric_name, value, dims)
                triggered = len(anomalies) > 0

            if triggered:
                alert = self._fire_alert(rule, value, dims)
                if alert:
                    new_alerts.append(alert)
                    self._cooldowns[cooldown_key] = time.time()

        # Check for auto-resolution
        self._check_resolutions(metric_name, value, dims)

        return new_alerts

    def acknowledge(self, alert_id: str, acknowledged_by: str = "operator"):
        """Acknowledge an active alert."""
        with self._lock:
            alert = self._active_alerts.get(alert_id)
            if alert and alert.state == AlertState.FIRING:
                alert.state = AlertState.ACKNOWLEDGED
                alert.acknowledged_at = time.time()
                alert.acknowledged_by = acknowledged_by

    def resolve(self, alert_id: str):
        """Manually resolve an alert."""
        with self._lock:
            alert = self._active_alerts.get(alert_id)
            if alert:
                alert.state = AlertState.RESOLVED
                alert.resolved_at = time.time()
                self._alert_history.append(alert)
                del self._active_alerts[alert_id]
                self._notify(alert, f"RESOLVED: {alert.rule.name}")

    def get_active_alerts(
        self, severity: str = None
    ) -> List[Alert]:
        """Get all active (firing or acknowledged) alerts."""
        with self._lock:
            alerts = list(self._active_alerts.values())
            if severity:
                alerts = [a for a in alerts if a.rule.severity == severity]
            return sorted(alerts, key=lambda a: a.fired_at, reverse=True)

    # --- Internal ---

    def _check_threshold(self, rule: AlertRule, value: float) -> bool:
        if rule.threshold is None:
            return False
        ops = {
            "gt": lambda v, t: v > t,
            "lt": lambda v, t: v < t,
            "gte": lambda v, t: v >= t,
            "lte": lambda v, t: v <= t,
        }
        op = ops.get(rule.comparison, ops["gt"])
        return op(value, rule.threshold)

    def _check_rate_of_change(
        self,
        rule: AlertRule,
        value: float,
        metric_name: str,
        dimensions: Dict[str, str],
    ) -> bool:
        if not self._detector:
            return False
        key = self._detector._make_key(metric_name, dimensions)
        window = self._detector._windows.get(key)
        if not window:
            return False
        roc = window.rate_of_change(periods=5)
        if roc is None or rule.threshold is None:
            return False
        return abs(roc) > rule.threshold

    def _fire_alert(
        self,
        rule: AlertRule,
        value: float,
        dimensions: Dict[str, str],
    ) -> Optional[Alert]:
        # Deduplicate: check if same rule + dimensions already firing
        dedup_key = f"{rule.name}:{self._dim_key(dimensions)}"
        with self._lock:
            for alert in self._active_alerts.values():
                existing_key = f"{alert.rule.name}:{self._dim_key(alert.dimensions)}"
                if existing_key == dedup_key:
                    # Update existing alert instead of creating new one
                    alert.last_value = value
                    alert.notification_count += 1
                    return None

            alert = Alert(
                id=f"alert_{uuid.uuid4().hex[:12]}",
                rule=rule,
                state=AlertState.FIRING,
                fired_at=time.time(),
                last_value=value,
                message=f"{rule.name}: {rule.metric_name} = {value} "
                        f"(threshold: {rule.comparison} {rule.threshold})",
                dimensions=dimensions,
            )
            self._active_alerts[alert.id] = alert

        self._notify(alert, alert.message)
        return alert

    def _notify(self, alert: Alert, message: str):
        for channel in alert.rule.channels:
            handler = self._channel_handlers.get(channel)
            if handler:
                try:
                    handler(alert, message)
                except Exception:
                    pass

        # Also register webhook with GreenHelix for event-driven alerts
        if self._client and alert.state == AlertState.FIRING:
            try:
                self._client.execute_tool("submit_metrics", {
                    "agent_id": self.agent_id,
                    "metrics": [{
                        "name": "alerts.fired",
                        "value": 1,
                        "dimensions": {
                            "rule": alert.rule.name,
                            "severity": alert.rule.severity,
                            "agent": self.agent_id,
                        },
                    }],
                })
            except Exception:
                pass

    def _check_resolutions(
        self,
        metric_name: str,
        value: float,
        dimensions: Dict[str, str],
    ):
        """Auto-resolve alerts when the condition clears."""
        with self._lock:
            to_resolve = []
            for alert_id, alert in self._active_alerts.items():
                if alert.rule.metric_name != metric_name:
                    continue
                if alert.rule.condition == "threshold":
                    if not self._check_threshold(alert.rule, value):
                        to_resolve.append(alert_id)

            for alert_id in to_resolve:
                alert = self._active_alerts[alert_id]
                alert.state = AlertState.RESOLVED
                alert.resolved_at = time.time()
                self._alert_history.append(alert)
                del self._active_alerts[alert_id]
                self._notify(alert, f"RESOLVED: {alert.rule.name}")

    def _escalation_loop(self):
        """Periodically check for alerts needing escalation."""
        while self._running:
            time.sleep(60)
            now = time.time()
            with self._lock:
                for alert in self._active_alerts.values():
                    if alert.state != AlertState.FIRING:
                        continue
                    if alert.escalated:
                        continue
                    age_minutes = (now - alert.fired_at) / 60
                    if age_minutes >= alert.rule.escalation_minutes:
                        alert.escalated = True
                        self._notify(
                            alert,
                            f"ESCALATION: {alert.rule.name} has been firing for "
                            f"{age_minutes:.0f} minutes without acknowledgment",
                        )

    @staticmethod
    def _dim_key(dimensions: Dict[str, str]) -> str:
        if not dimensions:
            return ""
        return ",".join(f"{k}={v}" for k, v in sorted(dimensions.items()))
```

### Configuring Alert Rules

Here is a practical configuration for an agent commerce deployment:

```python
alert_manager = AlertManager(
    agent_id="agent-marketplace",
    client=client,
    anomaly_detector=detector,
)

# Configure notification channels
alert_manager.configure_webhook("https://alerts.myfleet.com/webhook")
alert_manager.configure_slack(
    webhook_url="https://hooks.slack.com/services/T00/B00/xxx",
    default_channel="#agent-alerts",
)

# Rule 1: High error rate
alert_manager.add_rule(AlertRule(
    name="high_error_rate",
    metric_name="transactions.errors",
    condition="threshold",
    threshold=0.05,
    comparison="gt",
    severity="high",
    channels=[AlertChannel.SLACK, AlertChannel.WEBHOOK],
    cooldown_minutes=15,
    escalation_minutes=30,
    description="Transaction error rate exceeds 5%",
    runbook_url="https://wiki.myfleet.com/runbooks/high-error-rate",
))

# Rule 2: Latency spike
alert_manager.add_rule(AlertRule(
    name="latency_spike",
    metric_name="transactions.duration_ms",
    condition="threshold",
    threshold=5000,
    comparison="gt",
    severity="medium",
    channels=[AlertChannel.SLACK],
    cooldown_minutes=10,
    description="Transaction latency exceeds 5 seconds",
))

# Rule 3: Revenue drop
alert_manager.add_rule(AlertRule(
    name="revenue_drop",
    metric_name="revenue.total",
    condition="rate_of_change",
    threshold=0.30,  # 30% drop
    severity="critical",
    channels=[AlertChannel.SLACK, AlertChannel.PAGERDUTY, AlertChannel.WEBHOOK],
    cooldown_minutes=60,
    escalation_minutes=15,
    description="Revenue dropped more than 30% in 5 periods",
))

# Rule 4: Anomaly-based (uses AnomalyDetector)
alert_manager.add_rule(AlertRule(
    name="escrow_anomaly",
    metric_name="escrow.created",
    condition="anomaly",
    severity="medium",
    channels=[AlertChannel.SLACK],
    cooldown_minutes=30,
    description="Anomalous escrow creation pattern detected",
))

alert_manager.start()

# Evaluate metrics as they come in
alert_manager.evaluate("transactions.errors", 0.08, {"operation": "process_order"})
alert_manager.evaluate("transactions.duration_ms", 7500.0, {"operation": "process_order"})
```

The deduplication logic prevents alert storms: if the same rule fires for the same dimensions, the existing alert is updated rather than creating a new notification. The cooldown period prevents re-firing too quickly after an alert resolves and re-triggers. The escalation thread ensures that un-acknowledged alerts get escalated to additional channels after the configured timeout.

---

## Chapter 8: SLA Monitoring and Cost Attribution

The final piece of the observability stack ties technical metrics to business commitments. SLA monitoring tracks whether your agents are meeting their published service level agreements. Cost attribution tracks where money is being spent and whether each agent is profitable.

### SLA Definition and Tracking

An SLA for an agent commerce system typically includes:

- **Availability**: the percentage of time the agent is accepting and processing requests (target: 99.9%)
- **Latency**: the p95 or p99 response time for standard operations (target: under 500ms for p95)
- **Error rate**: the percentage of transactions that fail (target: under 0.1%)
- **Settlement time**: the time from escrow creation to settlement (target: under 24 hours)

```python
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class SLADefinition:
    """An SLA definition with target and measurement parameters."""
    name: str
    metric_name: str
    target_value: float
    comparison: str  # "lte" (latency), "gte" (availability), "lte" (error rate)
    measurement_window: str  # "1h", "24h", "7d", "30d"
    description: str = ""


@dataclass
class SLAStatus:
    """Current status of an SLA."""
    definition: SLADefinition
    current_value: float
    compliant: bool
    compliance_percentage: float  # % of measurement windows that met the SLA
    last_violation: Optional[float] = None
    violation_count: int = 0


class SLAMonitor:
    """Tracks SLA compliance for agent commerce operations."""

    def __init__(
        self,
        agent_id: str,
        metrics_collector: "MetricsCollector",
        client=None,
    ):
        self.agent_id = agent_id
        self._metrics = metrics_collector
        self._client = client
        self._sla_definitions: Dict[str, SLADefinition] = {}
        self._compliance_history: Dict[str, List[bool]] = defaultdict(list)
        self._violation_callbacks: List = []

    def define_sla(self, sla: SLADefinition):
        """Register an SLA definition."""
        self._sla_definitions[sla.name] = sla

    def on_violation(self, callback):
        """Register a callback for SLA violations."""
        self._violation_callbacks.append(callback)

    def check_sla(
        self,
        sla_name: str,
        current_value: float,
    ) -> SLAStatus:
        """Check if a metric value meets the SLA target."""
        sla = self._sla_definitions.get(sla_name)
        if not sla:
            raise ValueError(f"Unknown SLA: {sla_name}")

        ops = {
            "lte": lambda v, t: v <= t,
            "gte": lambda v, t: v >= t,
            "lt": lambda v, t: v < t,
            "gt": lambda v, t: v > t,
        }
        op = ops.get(sla.comparison, ops["lte"])
        compliant = op(current_value, sla.target_value)

        # Track compliance history
        self._compliance_history[sla_name].append(compliant)

        # Calculate compliance percentage (last 100 checks)
        history = self._compliance_history[sla_name][-100:]
        compliance_pct = sum(1 for c in history if c) / len(history) * 100

        status = SLAStatus(
            definition=sla,
            current_value=current_value,
            compliant=compliant,
            compliance_percentage=compliance_pct,
            violation_count=sum(1 for c in history if not c),
        )

        if not compliant:
            status.last_violation = time.time()

            # Record violation metric
            self._metrics.increment(
                "sla.violations",
                1.0,
                {"sla": sla_name, "agent": self.agent_id},
            )

            for callback in self._violation_callbacks:
                try:
                    callback(status)
                except Exception:
                    pass

        # Always record compliance percentage
        self._metrics.gauge_set(
            "sla.compliance_pct",
            compliance_pct,
            {"sla": sla_name, "agent": self.agent_id},
        )

        return status

    def get_all_sla_status(self) -> Dict[str, SLAStatus]:
        """Get the last known status for all SLAs."""
        results = {}
        for name in self._sla_definitions:
            history = self._compliance_history.get(name, [])
            if not history:
                continue
            last_100 = history[-100:]
            compliance_pct = sum(1 for c in last_100 if c) / len(last_100) * 100
            results[name] = SLAStatus(
                definition=self._sla_definitions[name],
                current_value=0.0,  # Would need last observed value
                compliant=last_100[-1] if last_100 else True,
                compliance_percentage=compliance_pct,
                violation_count=sum(1 for c in last_100 if not c),
            )
        return results
```

### Per-Agent Cost Attribution

In a multi-agent fleet, you need to know which agents are profitable and which are burning money. Cost attribution tracks every expense back to the agent that incurred it.

```python
@dataclass
class CostEntry:
    """A single cost entry attributed to an agent."""
    agent_id: str
    category: str
    amount: float
    currency: str
    timestamp: float
    transaction_id: str = ""
    description: str = ""


class CostAttributor:
    """Tracks and attributes costs across an agent fleet."""

    def __init__(self, metrics_collector: "MetricsCollector"):
        self._metrics = metrics_collector
        self._costs: Dict[str, List[CostEntry]] = defaultdict(list)
        self._budgets: Dict[str, float] = {}
        self._budget_callbacks: List = []

    def record_cost(
        self,
        agent_id: str,
        category: str,
        amount: float,
        currency: str = "credits",
        transaction_id: str = "",
        description: str = "",
    ):
        """Record a cost attributed to an agent."""
        entry = CostEntry(
            agent_id=agent_id,
            category=category,
            amount=amount,
            currency=currency,
            timestamp=time.time(),
            transaction_id=transaction_id,
            description=description,
        )
        self._costs[agent_id].append(entry)

        self._metrics.record_cost(amount, category, currency)
        self._metrics.increment(
            "cost_attribution.total",
            amount,
            {"agent": agent_id, "category": category},
        )

        # Check budget
        if agent_id in self._budgets:
            total = self.get_agent_total(agent_id)
            budget = self._budgets[agent_id]
            utilization = total / budget if budget > 0 else 0

            self._metrics.gauge_set(
                "budget.utilization_pct",
                utilization * 100,
                {"agent": agent_id},
            )

            if utilization >= 0.9:
                for callback in self._budget_callbacks:
                    try:
                        callback(agent_id, total, budget, utilization)
                    except Exception:
                        pass

    def set_budget(self, agent_id: str, budget: float):
        """Set a spending budget for an agent."""
        self._budgets[agent_id] = budget

    def on_budget_warning(self, callback):
        """Register a callback for budget threshold warnings."""
        self._budget_callbacks.append(callback)

    def get_agent_total(
        self,
        agent_id: str,
        since: float = None,
    ) -> float:
        """Get total costs for an agent since a given time."""
        costs = self._costs.get(agent_id, [])
        if since:
            costs = [c for c in costs if c.timestamp >= since]
        return sum(c.amount for c in costs)

    def get_agent_breakdown(
        self,
        agent_id: str,
        since: float = None,
    ) -> Dict[str, float]:
        """Get cost breakdown by category for an agent."""
        costs = self._costs.get(agent_id, [])
        if since:
            costs = [c for c in costs if c.timestamp >= since]
        breakdown = defaultdict(float)
        for cost in costs:
            breakdown[cost.category] += cost.amount
        return dict(breakdown)

    def generate_monthly_report(
        self,
        month_start: float,
        month_end: float,
    ) -> Dict[str, Any]:
        """Generate a monthly cost attribution report."""
        report = {
            "period_start": month_start,
            "period_end": month_end,
            "agents": {},
            "total_cost": 0.0,
            "top_categories": defaultdict(float),
        }

        for agent_id, costs in self._costs.items():
            month_costs = [
                c for c in costs
                if month_start <= c.timestamp <= month_end
            ]
            if not month_costs:
                continue

            agent_total = sum(c.amount for c in month_costs)
            breakdown = defaultdict(float)
            for cost in month_costs:
                breakdown[cost.category] += cost.amount
                report["top_categories"][cost.category] += cost.amount

            budget = self._budgets.get(agent_id, 0)
            report["agents"][agent_id] = {
                "total_cost": agent_total,
                "budget": budget,
                "utilization_pct": (agent_total / budget * 100) if budget else 0,
                "transaction_count": len(month_costs),
                "breakdown": dict(breakdown),
            }
            report["total_cost"] += agent_total

        report["top_categories"] = dict(
            sorted(
                report["top_categories"].items(),
                key=lambda x: x[1],
                reverse=True,
            )
        )

        return report
```

### Putting It All Together

Here is how all the observability components integrate for a production agent deployment:

```python
from greenhelix import GreenHelixClient

# Initialize core components
client = GreenHelixClient(api_key="your-api-key")
tracer = AgentTracer(agent_id="agent-marketplace", client=client)
metrics = MetricsCollector(agent_id="agent-marketplace", client=client)
detector = AnomalyDetector()
alert_manager = AlertManager(
    agent_id="agent-marketplace", client=client, anomaly_detector=detector
)
sla_monitor = SLAMonitor(
    agent_id="agent-marketplace", metrics_collector=metrics, client=client
)
cost_tracker = CostAttributor(metrics_collector=metrics)

# Define SLAs
sla_monitor.define_sla(SLADefinition(
    name="availability",
    metric_name="agent.availability_pct",
    target_value=99.9,
    comparison="gte",
    measurement_window="24h",
))

sla_monitor.define_sla(SLADefinition(
    name="latency_p95",
    metric_name="transactions.duration_ms",
    target_value=500,
    comparison="lte",
    measurement_window="1h",
))

# Set budgets
cost_tracker.set_budget("agent-marketplace", budget=1000.0)
cost_tracker.set_budget("agent-data-provider", budget=500.0)

# Wire SLA violations to alerts
sla_monitor.on_violation(lambda status: alert_manager.evaluate(
    status.definition.metric_name,
    status.current_value,
    {"sla": status.definition.name},
))

# Wire budget warnings to alerts
cost_tracker.on_budget_warning(
    lambda agent, total, budget, util: alert_manager.evaluate(
        "budget.utilization_pct",
        util * 100,
        {"agent": agent},
    )
)

# Start background threads
metrics.start()
alert_manager.start()

# Now every transaction is automatically traced, metered, checked,
# and alerted on:
def handle_transaction(request):
    with tracer.trace_agent_call(
        request["target"], request["operation"]
    ) as span:
        start = time.time()
        result = process(request)
        duration_ms = (time.time() - start) * 1000

        # Metrics
        metrics.record_transaction(
            operation=request["operation"],
            duration_ms=duration_ms,
            amount=request.get("amount", 0),
            status="success" if result["ok"] else "error",
            peer_agent=request["target"],
        )

        # Anomaly detection + alerting
        alert_manager.evaluate("transactions.duration_ms", duration_ms)
        alert_manager.evaluate(
            "transactions.errors",
            0 if result["ok"] else 1,
        )

        # SLA check
        sla_monitor.check_sla("latency_p95", duration_ms)

        # Cost attribution
        cost_tracker.record_cost(
            agent_id="agent-marketplace",
            category="gateway_fee",
            amount=result.get("fee", 0),
            transaction_id=result.get("transaction_id", ""),
        )

        return result
```

This integration means every transaction flowing through your agent automatically generates traces for debugging, metrics for dashboards, anomaly detection for automated problem finding, alerts for operator notification, SLA tracking for compliance reporting, and cost attribution for business analysis. The operational overhead is minimal -- a few milliseconds of in-process buffering per transaction -- and the visibility gain is transformative.

---

## What's Next

This guide built the observability stack from the bottom up: tracing, metrics, anomaly detection, dashboards, alerting, and SLA monitoring. Each component works independently but delivers maximum value when integrated.

To put this into production, start with the `AgentTracer` and `MetricsCollector`. These two components give you immediate visibility with minimal effort. Add the `AnomalyDetector` once you have a few days of baseline data. Configure the `AlertManager` with conservative thresholds and tighten them as you learn your system's normal patterns. Roll out `SLAMonitor` and `CostAttributor` when you have paying customers who need compliance reports.

The next guides in this series cover agent security hardening (protecting your fleet from adversarial agents), agent marketplace economics (pricing strategies and commission structures), and agent scaling patterns (handling 100x traffic growth without rewriting your stack). Each builds on the observability foundation established here because you cannot secure, price, or scale what you cannot see.

