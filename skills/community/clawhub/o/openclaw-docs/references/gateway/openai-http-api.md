# OpenAI Chat Completions

Source: https://docs.openclaw.ai/gateway/openai-http-api

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationProtocols and APIsOpenAI Chat CompletionsGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpGateway
Gateway RunbookConfiguration and operationsSecurity and sandboxingProtocols and APIs
Gateway ProtocolBridge ProtocolOpenAI Chat CompletionsTools Invoke APICLI BackendsLocal Models
Networking and discovery
Remote access
Remote AccessRemote Gateway SetupTailscale
Security
Formal Verification (Security Models)
Web interfaces
WebControl UIDashboardWebChatTUI
On this page
- [OpenAI Chat Completions (HTTP)](#openai-chat-completions-http)
- [Authentication](#authentication)
- [Choosing an agent](#choosing-an-agent)
- [Enabling the endpoint](#enabling-the-endpoint)
- [Disabling the endpoint](#disabling-the-endpoint)
- [Session behavior](#session-behavior)
- [Streaming (SSE)](#streaming-sse)
- [Examples](#examples)

​OpenAI Chat Completions (HTTP)
OpenClaw’s Gateway can serve a small OpenAI-compatible Chat Completions endpoint.
This endpoint is **disabled by default**. Enable it in config first.

- `POST /v1/chat/completions`

- Same port as the Gateway (WS + HTTP multiplex): `http://<gateway-host>:<port>/v1/chat/completions`

Under the hood, requests are executed as a normal Gateway agent run (same codepath as `openclaw agent`), so routing/permissions/config match your Gateway.
​Authentication
Uses the Gateway auth configuration. Send a bearer token:

- `Authorization: Bearer <token>`

Notes:

- When `gateway.auth.mode="token"`, use `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`).

- When `gateway.auth.mode="password"`, use `gateway.auth.password` (or `OPENCLAW_GATEWAY_PASSWORD`).

- If `gateway.auth.rateLimit` is configured and too many auth failures occur, the endpoint returns `429` with `Retry-After`.

​Choosing an agent
No custom headers required: encode the agent id in the OpenAI `model` field:

- `model: "openclaw:<agentId>"` (example: `"openclaw:main"`, `"openclaw:beta"`)

- `model: "agent:<agentId>"` (alias)

Or target a specific OpenClaw agent by header:

- `x-openclaw-agent-id: <agentId>` (default: `main`)

Advanced:

- `x-openclaw-session-key: <sessionKey>` to fully control session routing.

​Enabling the endpoint
Set `gateway.http.endpoints.chatCompletions.enabled` to `true`:
Copy```
{
  gateway: {
    http: {
      endpoints: {
        chatCompletions: { enabled: true },
      },
    },
  },
}

```

​Disabling the endpoint
Set `gateway.http.endpoints.chatCompletions.enabled` to `false`:
Copy```
{
  gateway: {
    http: {
      endpoints: {
        chatCompletions: { enabled: false },
      },
    },
  },
}

```

​Session behavior
By default the endpoint is **stateless per request** (a new session key is generated each call).
If the request includes an OpenAI `user` string, the Gateway derives a stable session key from it, so repeated calls can share an agent session.
​Streaming (SSE)
Set `stream: true` to receive Server-Sent Events (SSE):

- `Content-Type: text/event-stream`

- Each event line is `data: <json>`

- Stream ends with `data: [DONE]`

​Examples
Non-streaming:
Copy```
curl -sS http://127.0.0.1:18789/v1/chat/completions \
  -H &#x27;Authorization: Bearer YOUR_TOKEN&#x27; \
  -H &#x27;Content-Type: application/json&#x27; \
  -H &#x27;x-openclaw-agent-id: main&#x27; \
  -d &#x27;{
    "model": "openclaw",
    "messages": [{"role":"user","content":"hi"}]
  }&#x27;

```

Streaming:
Copy```
curl -N http://127.0.0.1:18789/v1/chat/completions \
  -H &#x27;Authorization: Bearer YOUR_TOKEN&#x27; \
  -H &#x27;Content-Type: application/json&#x27; \
  -H &#x27;x-openclaw-agent-id: main&#x27; \
  -d &#x27;{
    "model": "openclaw",
    "stream": true,
    "messages": [{"role":"user","content":"hi"}]
  }&#x27;

```

Bridge ProtocolTools Invoke API⌘I