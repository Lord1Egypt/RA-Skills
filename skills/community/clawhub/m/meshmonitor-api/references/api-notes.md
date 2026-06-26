# MeshMonitor API Notes

## Auth

- Bearer token required on `/api/v1/*`
- Docs indicate format like `Authorization: Bearer mm_v1_<token>`
- Tokens are user-managed and may be revoked or replaced at any time

## Docs discovery

Useful docs paths when available:

- `/api/v1/docs/`
- `/api/v1/docs/swagger-ui-init.js`

The Swagger bootstrap JS often contains the full OpenAPI document and is useful for endpoint discovery when a raw OpenAPI JSON file is not exposed directly.

## Observed endpoint groups

The API documentation advertises these main groups:

- `/`
- `/nodes`
- `/nodes/{nodeId}`
- `/nodes/{nodeId}/position-history`
- `/channels`
- `/channels/{channelId}`
- `/telemetry`
- `/telemetry/count`
- `/telemetry/{nodeId}`
- `/messages`
- `/messages/{messageId}`
- `/traceroutes`
- `/traceroutes/{fromNodeId}/{toNodeId}`
- `/network`
- `/network/topology`
- `/packets`
- `/packets/{id}`
- `/solar`
- `/solar/range`

## Node endpoint notes

### List nodes

Common query params include:

- `active`
- `sinceDays`

### Position history

Common query params include:

- `since`
- `before`
- `limit`

Docs may use mixed node identifier formats depending on endpoint:

- hex with leading `!` for many node endpoints
- decimal-string node number for some history-style endpoints

If one identifier format fails, try the alternate representation supported by the API.

## Messages endpoint notes

`POST /messages` supports:

- channel messages using `channel`
- direct messages using `toNodeId`
- optional `replyId`

Do **not** provide both `channel` and `toNodeId` in the same request.

Longer messages may be split/queued by the server depending on implementation limits.

## Solar endpoint notes

`GET /solar/range` expects:

- `start` as Unix seconds
- `end` as Unix seconds

Empty solar results do not necessarily indicate failure; they may simply mean no solar data is available for the requested node/time range.

## Practical approach

1. Load docs.
2. Extract endpoint list.
3. Test a minimal authenticated request.
4. Probe high-value read endpoints first:
   - info
   - nodes
   - network
   - messages
   - telemetry
5. Only then build reports, automation, or write flows.

## Generic integration gotchas

- Tokens may be expired, revoked, truncated, or copied incorrectly.
- Docs pages may load without authentication while API calls still require Bearer auth.
- Some endpoints may exist but return empty datasets on healthy installs.
- Write endpoints should be tested carefully on a live mesh because they may queue or relay through radio infrastructure.
