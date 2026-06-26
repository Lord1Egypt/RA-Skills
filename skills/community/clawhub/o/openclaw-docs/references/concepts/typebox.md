# TypeBox

Source: https://docs.openclaw.ai/concepts/typebox

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationConcept internalsTypeBoxGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpCLI commands
CLI ReferenceagentagentsapprovalsbrowserchannelsconfigurecrondashboarddirectorydnsdocsdoctorgatewayhealthhookslogsmemorymessagemodelsnodesonboardpairingpluginsresetSandbox CLIsecuritysessionssetupskillsstatussystemtuiuninstallupdatevoicecall
RPC and API
RPC AdaptersDevice Model Database
Templates
Default AGENTS.mdAGENTS.md TemplateBOOT.md TemplateBOOTSTRAP.md TemplateHEARTBEAT.md TemplateIDENTITYSOUL.md TemplateTOOLS.md TemplateUSER
Technical reference
Wizard ReferenceToken Use and CostsgrammY
Concept internals
TypeBoxMarkdown FormattingTyping IndicatorsUsage TrackingTimezones
Project
Credits
Release notes
Release ChecklistTests
Experiments
Onboarding and Config ProtocolCron Add HardeningTelegram Allowlist HardeningWorkspace Memory ResearchModel Config Exploration
On this page
- [TypeBox as protocol source of truth](#typebox-as-protocol-source-of-truth)
- [Mental model (30 seconds)](#mental-model-30-seconds)
- [Where the schemas live](#where-the-schemas-live)
- [Current pipeline](#current-pipeline)
- [How the schemas are used at runtime](#how-the-schemas-are-used-at-runtime)
- [Example frames](#example-frames)
- [Minimal client (Node.js)](#minimal-client-node-js)
- [Worked example: add a method end‑to‑end](#worked-example-add-a-method-end%E2%80%91to%E2%80%91end)
- [Swift codegen behavior](#swift-codegen-behavior)
- [Versioning + compatibility](#versioning-%2B-compatibility)
- [Schema patterns and conventions](#schema-patterns-and-conventions)
- [Live schema JSON](#live-schema-json)
- [When you change schemas](#when-you-change-schemas)

​TypeBox as protocol source of truth
Last updated: 2026-01-10
TypeBox is a TypeScript-first schema library. We use it to define the **Gateway
WebSocket protocol** (handshake, request/response, server events). Those schemas
drive **runtime validation**, **JSON Schema export**, and **Swift codegen** for
the macOS app. One source of truth; everything else is generated.
If you want the higher-level protocol context, start with
[Gateway architecture](/concepts/architecture).
​Mental model (30 seconds)
Every Gateway WS message is one of three frames:

- **Request**: `{ type: "req", id, method, params }`

- **Response**: `{ type: "res", id, ok, payload | error }`

- **Event**: `{ type: "event", event, payload, seq?, stateVersion? }`

The first frame **must** be a `connect` request. After that, clients can call
methods (e.g. `health`, `send`, `chat.send`) and subscribe to events (e.g.
`presence`, `tick`, `agent`).
Connection flow (minimal):
Copy```
Client                    Gateway
  |---- req:connect -------->|
  |<---- res:hello-ok --------|
  |<---- event:tick ----------|
  |---- req:health ---------->|
  |<---- res:health ----------|

```

Common methods + events:
CategoryExamplesNotesCore`connect`, `health`, `status``connect` must be firstMessaging`send`, `poll`, `agent`, `agent.wait`side-effects need `idempotencyKey`Chat`chat.history`, `chat.send`, `chat.abort`, `chat.inject`WebChat uses theseSessions`sessions.list`, `sessions.patch`, `sessions.delete`session adminNodes`node.list`, `node.invoke`, `node.pair.*`Gateway WS + node actionsEvents`tick`, `presence`, `agent`, `chat`, `health`, `shutdown`server push
Authoritative list lives in `src/gateway/server.ts` (`METHODS`, `EVENTS`).
​Where the schemas live

- Source: `src/gateway/protocol/schema.ts`

- Runtime validators (AJV): `src/gateway/protocol/index.ts`

- Server handshake + method dispatch: `src/gateway/server.ts`

- Node client: `src/gateway/client.ts`

- Generated JSON Schema: `dist/protocol.schema.json`

- Generated Swift models: `apps/macos/Sources/OpenClawProtocol/GatewayModels.swift`

​Current pipeline

`pnpm protocol:gen`

- writes JSON Schema (draft‑07) to `dist/protocol.schema.json`

`pnpm protocol:gen:swift`

- generates Swift gateway models

`pnpm protocol:check`

- runs both generators and verifies the output is committed

​How the schemas are used at runtime

- **Server side**: every inbound frame is validated with AJV. The handshake only
accepts a `connect` request whose params match `ConnectParams`.

- **Client side**: the JS client validates event and response frames before
using them.

- **Method surface**: the Gateway advertises the supported `methods` and
`events` in `hello-ok`.

​Example frames
Connect (first message):
Copy```
{
  "type": "req",
  "id": "c1",
  "method": "connect",
  "params": {
    "minProtocol": 2,
    "maxProtocol": 2,
    "client": {
      "id": "openclaw-macos",
      "displayName": "macos",
      "version": "1.0.0",
      "platform": "macos 15.1",
      "mode": "ui",
      "instanceId": "A1B2"
    }
  }
}

```

Hello-ok response:
Copy```
{
  "type": "res",
  "id": "c1",
  "ok": true,
  "payload": {
    "type": "hello-ok",
    "protocol": 2,
    "server": { "version": "dev", "connId": "ws-1" },
    "features": { "methods": ["health"], "events": ["tick"] },
    "snapshot": {
      "presence": [],
      "health": {},
      "stateVersion": { "presence": 0, "health": 0 },
      "uptimeMs": 0
    },
    "policy": { "maxPayload": 1048576, "maxBufferedBytes": 1048576, "tickIntervalMs": 30000 }
  }
}

```

Request + response:
Copy```
{ "type": "req", "id": "r1", "method": "health" }

```

Copy```
{ "type": "res", "id": "r1", "ok": true, "payload": { "ok": true } }

```

Event:
Copy```
{ "type": "event", "event": "tick", "payload": { "ts": 1730000000 }, "seq": 12 }

```

​Minimal client (Node.js)
Smallest useful flow: connect + health.
Copy```
import { WebSocket } from "ws";

const ws = new WebSocket("ws://127.0.0.1:18789");

ws.on("open", () => {
  ws.send(
    JSON.stringify({
      type: "req",
      id: "c1",
      method: "connect",
      params: {
        minProtocol: 3,
        maxProtocol: 3,
        client: {
          id: "cli",
          displayName: "example",
          version: "dev",
          platform: "node",
          mode: "cli",
        },
      },
    }),
  );
});

ws.on("message", (data) => {
  const msg = JSON.parse(String(data));
  if (msg.type === "res" && msg.id === "c1" && msg.ok) {
    ws.send(JSON.stringify({ type: "req", id: "h1", method: "health" }));
  }
  if (msg.type === "res" && msg.id === "h1") {
    console.log("health:", msg.payload);
    ws.close();
  }
});

```

​Worked example: add a method end‑to‑end
Example: add a new `system.echo` request that returns `{ ok: true, text }`.

- **Schema (source of truth)**

Add to `src/gateway/protocol/schema.ts`:
Copy```
export const SystemEchoParamsSchema = Type.Object(
  { text: NonEmptyString },
  { additionalProperties: false },
);

export const SystemEchoResultSchema = Type.Object(
  { ok: Type.Boolean(), text: NonEmptyString },
  { additionalProperties: false },
);

```

Add both to `ProtocolSchemas` and export types:
Copy```
  SystemEchoParams: SystemEchoParamsSchema,
  SystemEchoResult: SystemEchoResultSchema,

```

Copy```
export type SystemEchoParams = Static<typeof SystemEchoParamsSchema>;
export type SystemEchoResult = Static<typeof SystemEchoResultSchema>;

```

- **Validation**

In `src/gateway/protocol/index.ts`, export an AJV validator:
Copy```
export const validateSystemEchoParams = ajv.compile<SystemEchoParams>(SystemEchoParamsSchema);

```

- **Server behavior**

Add a handler in `src/gateway/server-methods/system.ts`:
Copy```
export const systemHandlers: GatewayRequestHandlers = {
  "system.echo": ({ params, respond }) => {
    const text = String(params.text ?? "");
    respond(true, { ok: true, text });
  },
};

```

Register it in `src/gateway/server-methods.ts` (already merges `systemHandlers`),
then add `"system.echo"` to `METHODS` in `src/gateway/server.ts`.

- **Regenerate**

Copy```
pnpm protocol:check

```

- **Tests + docs**

Add a server test in `src/gateway/server.*.test.ts` and note the method in docs.
​Swift codegen behavior
The Swift generator emits:

- `GatewayFrame` enum with `req`, `res`, `event`, and `unknown` cases

- Strongly typed payload structs/enums

- `ErrorCode` values and `GATEWAY_PROTOCOL_VERSION`

Unknown frame types are preserved as raw payloads for forward compatibility.
​Versioning + compatibility

- `PROTOCOL_VERSION` lives in `src/gateway/protocol/schema.ts`.

- Clients send `minProtocol` + `maxProtocol`; the server rejects mismatches.

- The Swift models keep unknown frame types to avoid breaking older clients.

​Schema patterns and conventions

- Most objects use `additionalProperties: false` for strict payloads.

- `NonEmptyString` is the default for IDs and method/event names.

- The top-level `GatewayFrame` uses a **discriminator** on `type`.

- Methods with side effects usually require an `idempotencyKey` in params
(example: `send`, `poll`, `agent`, `chat.send`).

​Live schema JSON
Generated JSON Schema is in the repo at `dist/protocol.schema.json`. The
published raw file is typically available at:

- [https://raw.githubusercontent.com/openclaw/openclaw/main/dist/protocol.schema.json](https://raw.githubusercontent.com/openclaw/openclaw/main/dist/protocol.schema.json)

​When you change schemas

- Update the TypeBox schemas.

- Run `pnpm protocol:check`.

- Commit the regenerated schema + Swift models.

grammYMarkdown Formatting⌘I