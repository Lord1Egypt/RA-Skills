---
name: latitude-observability
description: Export OpenClaw OTLP traces to Latitude for open-source LLM observability and evaluation. Use when configuring diagnostics.otel to send OpenClaw model-call, run, tool, and message spans to Latitude's ingest endpoint.
version: 1.0.0
tags: observability, opentelemetry, otlp, tracing, latitude, llm-observability, monitoring
homepage: https://docs.latitude.so/getting-started/mcp
emoji: 📡
metadata:
  openclaw:
    primaryEnv: LATITUDE_API_KEY
    envVars:
      - name: LATITUDE_API_KEY
        required: true
        description: Latitude API key, sent as the Authorization Bearer header to authenticate trace delivery.
      - name: LATITUDE_PROJECT
        required: true
        description: Latitude project slug, sent as the X-Latitude-Project header to route traces to a project. Must belong to the API key's organization.
---

# Latitude observability for OpenClaw

[Latitude](https://latitude.so) is an open-source LLM observability and
evaluation platform. It ingests OpenTelemetry traces, so OpenClaw activity
becomes spans you can inspect, search, and evaluate, with token usage, cost, and
latency aggregated at every level of the trace.

OpenClaw already exports OTLP/HTTP protobuf through its built-in
`diagnostics-otel` plugin. This skill configures that exporter to send traces to
Latitude. There is no extra code to install.

## When to use

Use this when you want OpenClaw model-call, run, tool, and message spans to land
in Latitude, or when someone asks how to wire OpenClaw telemetry into Latitude.

## Prerequisites

- A Latitude account and API key. Sign up at
  [console.latitude.so](https://console.latitude.so/login), or self-host.
- A Latitude project slug.
- Set the credentials in your environment:

  ```bash
  export LATITUDE_API_KEY=<your-api-key>
  export LATITUDE_PROJECT=<your-project-slug>
  ```

## Configure

Enable the `diagnostics-otel` plugin and point `diagnostics.otel` at Latitude's
ingestion endpoint, authenticating with two headers. Add this to your OpenClaw
config (`~/.openclaw/openclaw.json`):

```json5
{
  plugins: {
    allow: ["diagnostics-otel"],
    entries: {
      "diagnostics-otel": { enabled: true },
    },
  },
  diagnostics: {
    enabled: true,
    otel: {
      enabled: true,
      endpoint: "https://ingest.latitude.so",
      protocol: "http/protobuf",
      serviceName: "openclaw-gateway",
      headers: {
        Authorization: "Bearer ${LATITUDE_API_KEY}",
        "X-Latitude-Project": "${LATITUDE_PROJECT}",
      },
      traces: true,
      metrics: false,
      logs: false,
    },
  },
}
```

For packaged installs, install the plugin first:

```bash
openclaw plugins install clawhub:@openclaw/diagnostics-otel
```

## Notes

- OpenClaw appends `/v1/traces` to the base `endpoint`, so set `endpoint` to
  `https://ingest.latitude.so` (no path). If you self-host Latitude, point it at
  your own ingestion host instead.
- `protocol` must be `http/protobuf`. OpenClaw ignores `grpc` today, and
  Latitude ingests OTLP/HTTP protobuf.
- Latitude ingests OTLP traces, so this config leaves `metrics` and `logs` off.
  Route those signals to a separate metrics or logs backend if you need them.
- Raw prompt and response content is not exported by default. Enable
  `diagnostics.otel.captureContent.*` only when your retention policy allows it.

## Verify

Run an OpenClaw agent turn that calls a model and a tool, then open your project
in the [Latitude dashboard](https://console.latitude.so/login). You should see a
trace with nested spans for the run, model call, and tool call, with token
usage, cost, and latency aggregated per trace.
