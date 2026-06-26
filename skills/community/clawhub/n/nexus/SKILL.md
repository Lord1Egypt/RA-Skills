\---

name: nexus-agent
description: Use Nexus as an AI agent through the hosted MCP server or direct Nexus API. Supports authenticated read operations by default and explicit-confirmation write operations for CRM, orders, inventory, messaging, shipping, internal chat, social publishing, invites, and conversation intelligence.
homepage: https://nexus-docs.aiforstartups.io
user-invocable: true
disable-model-invocation: true
metadata: {"openclaw":{"requires":{"env":\["NEXUS\_API\_KEY"]},"primaryEnv":"NEXUS\_API\_KEY","homepage":"https://nexus-docs.aiforstartups.io"}}
---

# Nexus Agent Skill

Nexus is a multi-tenant operations OS for ecommerce and retail workflows. Use this skill to authenticate an AI agent, access the hosted Nexus MCP server, and fall back to direct HTTP API access when MCP is not sufficient.

This skill is intentionally **user-invocable only** and is designed to be **read-first**. Any write operation requires explicit user confirmation.

## Required credential

This skill requires the environment variable:

* `NEXUS\_API\_KEY`

`NEXUS\_API\_KEY` must be an **agent API key**, not a human JWT and not a short-lived agent JWT.

### Credential handling rules

* Read only `NEXUS\_API\_KEY` from the runtime environment.
* If `NEXUS\_API\_KEY` is missing, ask the user or operator to configure it.
* Do not read unrelated environment variables, local files, or stored secrets.
* Do not hardcode live secrets into the skill.
* Use the raw API key **only** with `agent-auth`.
* After exchanging the API key for a short-lived JWT, use that JWT for MCP and direct API calls.

### Optional runtime config for direct PostgREST access

When calling PostgREST directly, the runtime must also provide an anon key header such as:

* `VITE\_SUPABASE\_ANON\_KEY`
* `NEXT\_PUBLIC\_SUPABASE\_ANON\_KEY`
* or an operator-provided equivalent runtime secret

Do not publish a live anon key inside distributed skills or public documentation.

### Example OpenClaw configuration

```json
{
  "skills": {
    "entries": {
      "nexus-agent": {
        "apiKey": {
          "source": "env",
          "provider": "default",
          "id": "NEXUS\_API\_KEY"
        }
      }
    }
  }
}
```

## Safety and execution policy

### Trusted domains only

Only call Nexus on these hosts:

* `api.nexus.aiforstartups.io`
* `nexus-docs.aiforstartups.io`

Do not send Nexus credentials or payloads to any other host.

### Read-first behavior

Default to read operations whenever possible.

Examples of read operations:

* list contacts, orders, inventory, conversations, call logs, invites, or internal conversations
* get a single contact, order, shipment, post, or annotation
* read MCP schema resources and organization info
* run search and analytics reads

### Write gate

Require explicit user confirmation before any write action, including:

* creating or updating contacts
* creating orders or updating order status
* sending customer messages
* sending internal team messages
* creating, updating, publishing, or deleting social posts
* inviting, resending, or cancelling organization invites
* updating message annotations, AI tag definitions, prompts, or org AI context
* initiating a phone call
* creating an AWB or triggering fulfillment steps

If the current API key has only `read` scope, do not attempt write actions.

### No autonomous onboarding or background writes

* Do not autonomously register organizations, create accounts, or start onboarding flows.
* Do not autonomously create orders, publish posts, send messages, or change records in the background.
* If the user explicitly asks to onboard or enable a Nexus integration, ask only for the minimum information required for that step.

## Authentication

AI agents do **not** use human user JWTs directly.

The correct flow is:

1. A human org admin creates an agent API key with `agent-api-key-create`
2. The agent exchanges that key for a short-lived JWT with `agent-auth`
3. The agent uses the short-lived JWT for MCP or direct API calls

### Step 1: human admin creates an API key

This is a human-admin operation.

```bash
POST https://api.nexus.aiforstartups.io/functions/v1/agent-api-key-create
Authorization: Bearer <human-admin-jwt>
Content-Type: application/json

{
  "name": "Bahig - Karim assistant",
  "scopes": \["read", "write"],
  "expires\_at": "2026-12-31T23:59:59Z"
}
```

Response:

```json
{
  "api\_key": "nxs\_ak\_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ12",
  "key\_prefix": "nxs\_ak\_ab12CD34",
  "organization\_id": "uuid",
  "name": "Bahig - Karim assistant",
  "scopes": \["read", "write"],
  "expires\_at": "2026-12-31T23:59:59.000Z",
  "message": "Store this API key now. It is only returned once."
}
```

Important:

* the raw key is returned **once only**
* Nexus stores only a **bcrypt hash**
* keys can be revoked

### Step 2: exchange API key for an agent JWT

```bash
POST https://api.nexus.aiforstartups.io/functions/v1/agent-auth
Content-Type: application/json

{"api\_key": "nxs\_ak\_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
```

Response:

```json
{
  "access\_token": "eyJ...",
  "organization\_id": "uuid",
  "expires\_in": 3600
}
```

Use the `access\_token` as `Authorization: Bearer <token>` on all subsequent requests.

### API key format

`nxs\_ak\_` prefix + 48 random alphanumeric characters.

### Scopes

* `read` = read-only operations
* `write` = read + create + update
* `admin` = full access

### MCP authentication

The hosted MCP endpoint accepts the **agent JWT**, not the raw API key:

```bash
POST https://api.nexus.aiforstartups.io/functions/v1/mcp-server
Authorization: Bearer <agent-jwt>
```

## Base URLs

|Service|URL|
|-|-|
|Edge Functions|`https://api.nexus.aiforstartups.io/functions/v1/<function-name>`|
|PostgREST (DB)|`https://api.nexus.aiforstartups.io/rest/v1/<table>`|
|MCP|`https://api.nexus.aiforstartups.io/functions/v1/mcp-server`|

For direct PostgREST calls, include both:

* `Authorization: Bearer <agent-jwt>`
* `apikey: <anon-key-from-secure-runtime-config>`

## Preferred integration path: MCP first

Prefer the hosted MCP server when possible. It exposes a stable, documented tool surface for common agent workflows.

### MCP tools

* `nexus\_list\_contacts`
* `nexus\_get\_contact`
* `nexus\_create\_contact`
* `nexus\_update\_contact`
* `nexus\_list\_orders`
* `nexus\_get\_order`
* `nexus\_create\_order`
* `nexus\_update\_order\_status`
* `nexus\_list\_inventory`
* `nexus\_check\_stock`
* `nexus\_list\_conversations`
* `nexus\_send\_message`
* `nexus\_search`
* `nexus\_sync\_social\_posts`
* `nexus\_list\_social\_posts`
* `nexus\_get\_social\_post`
* `nexus\_create\_social\_post`
* `nexus\_update\_social\_post`
* `nexus\_publish\_social\_post`
* `nexus\_delete\_social\_post`
* `nexus\_list\_social\_accounts`
* `nexus\_get\_social\_analytics`
* `nexus\_get\_content\_calendar`
* `nexus\_list\_organization\_invites`
* `nexus\_invite\_organization\_member`
* `nexus\_cancel\_organization\_invite`
* `nexus\_resend\_organization\_invite`
* `nexus\_list\_internal\_conversations`
* `nexus\_get\_internal\_messages`
* `nexus\_open\_internal\_dm`
* `nexus\_send\_internal\_message`
* `nexus\_list\_ai\_tag\_definitions`
* `nexus\_list\_message\_annotations`
* `nexus\_get\_message\_ai\_annotation`
* `nexus\_get\_org\_ai\_annotation\_settings`
* `nexus\_get\_customer\_conversation\_intelligence`
* `nexus\_get\_conversation\_intelligence\_dashboard`
* `nexus\_update\_message\_annotation`
* `nexus\_update\_ai\_tag\_definition`
* `nexus\_set\_org\_ai\_annotation\_prompt`
* `nexus\_update\_org\_conversation\_intelligence\_context`

### MCP resources

* `nexus://organization/info`
* `nexus://schema/contacts`
* `nexus://schema/orders`
* `nexus://schema/inventory`
* `nexus://schema/social`
* `nexus://schema/conversation-intelligence`

### When to use MCP vs direct API

Use MCP when:

* the client supports MCP
* you want a compact tool surface
* you want resource discovery and schema resources
* you need social or content-calendar operations through a stable agent interface

Use direct API when:

* the client does not support MCP
* you need raw PostgREST querying
* you are debugging a low-level integration
* you need a workflow not yet covered by the MCP wrapper

### Social MCP notes

* Social tools require at least the `starter` plan.
* Social write tools require `write` or `admin` scope.
* Facebook and Instagram drafts and publishing are supported from MCP.
* Instagram sync reads from the connected Instagram Business account and writes normalized rows into `social\_posts`.
* `twitter` and `linkedin` remain reserved in request enums for forward compatibility and are not yet writable from this MCP surface.

### Organization invites (MCP + `agent-invite`)

Agents can manage `organization\_invites` for **their JWT organization only**.

* **MCP tools:** `nexus\_list\_organization\_invites` (read scope), `nexus\_invite\_organization\_member`, `nexus\_cancel\_organization\_invite`, `nexus\_resend\_organization\_invite` (write scope)
* **HTTP API:** `POST /functions/v1/agent-invite` with `Authorization: Bearer <agent-jwt>` and JSON body `{ "action": "invite"|"cancel"|"resend"|"list", ... }`

Requires `BREVO\_KEY` on Edge Functions.

### Internal team chat (MCP)

Internal chat is separate from the customer omnichannel inbox (`chats` / `messages`). MCP tools talk to `internal\_conversations` and `internal\_messages`.

* the agent API key must be linked to an `agent\_accounts` row (`agent\_api\_keys.agent\_id`)
* `nexus\_open\_internal\_dm`: pass `user\_id` or `user\_email` of an active org member
* `nexus\_send\_internal\_message`: `sender\_id` is null server-side; humans still send with their user id in the app
* `nexus\_list\_internal\_conversations` and `nexus\_get\_internal\_messages`: only threads the agent created or has posted in

## Core operations

### Contacts (CRM)

> `journey\_stage\_id` is a UUID foreign key to `customer\_journey\_stages`, not a free-text field.

```bash
# List contacts
GET /rest/v1/customers?organization\_id=eq.<org\_id>\&order=created\_at.desc\&limit=25
Authorization: Bearer <agent-jwt>
apikey: <anon-key>

# Search by phone (URL-encode + as %2B)
GET /rest/v1/customers?phone\_number=eq.%2B201234567890\&organization\_id=eq.<org\_id>

# Create contact — requires explicit confirmation and write scope
POST /rest/v1/customers
{"first\_name":"Ahmed","last\_name":"Hassan","phone\_number":"+201234567890","organization\_id":"<org\_id>"}

# Update tags — requires explicit confirmation and write scope
PATCH /rest/v1/customers?id=eq.<uuid>
{"tags":\["vip","repeat-buyer"]}
```

### Messages (omnichannel inbox)

> `chats` has no `status` column. Use `is\_archived`. `messages` sorts by `timestamp`, not `created\_at`.

```bash
# List open conversations
GET /rest/v1/chats?organization\_id=eq.<org\_id>\&is\_archived=eq.false\&order=last\_message\_time.desc

# Get messages in a conversation
GET /rest/v1/messages?chat\_id=eq.<chat\_id>\&order=timestamp.asc

# Send WhatsApp message — requires explicit confirmation and write scope
POST /functions/v1/whatsapp-send-message
{"chatId":"<chat\_id>","message":"Hello from Nexus AI agent","organizationId":"<org\_id>"}

# Send WhatsApp template — requires explicit confirmation and write scope
POST /functions/v1/whatsapp-send-template
{"phone\_number":"+201234567890","template\_name":"order\_shipped","language":"ar","components":\[]}
```

### Orders

> The status column is `order\_status`, not `status`.

```bash
# List orders
GET /rest/v1/orders?organization\_id=eq.<org\_id>\&order=created\_at.desc\&limit=50

# Filter by status — use order\_status
GET /rest/v1/orders?organization\_id=eq.<org\_id>\&order\_status=eq.pending

# Create order — requires explicit confirmation and write scope
POST /rest/v1/orders
{"customer\_id":"<uuid>","organization\_id":"<org\_id>","order\_status":"pending","total\_amount":450,"currency":"EGP"}

# Update order status — requires explicit confirmation and write scope
PATCH /rest/v1/orders?id=eq.<uuid>
{"order\_status":"confirmed"}

# Get order items (qty column, not quantity)
GET /rest/v1/order\_items?order\_id=eq.<order\_id>
```

### Inventory

> Inventory uses `items` plus `stock\_balances`. There is no `inventory\_items` table.

```bash
# List products
GET /rest/v1/items?organization\_id=eq.<org\_id>\&is\_active=eq.true\&order=updated\_at.desc

# Search by SKU
GET /rest/v1/items?organization\_id=eq.<org\_id>\&sku=eq.TSHIRT-M-BLK

# Low stock
GET /rest/v1/stock\_balances?organization\_id=eq.<org\_id>\&available\_quantity=lt.10

# Stock for one item across warehouses
GET /rest/v1/stock\_balances?item\_id=eq.<uuid>
```

### Shipping

```bash
# Create AWB — requires explicit confirmation and write scope
POST /functions/v1/create-awb-bosta
{"order\_id":"<uuid>","pickup\_date":"2025-06-17"}

# List shipments
GET /rest/v1/awbs?organization\_id=eq.<org\_id>\&order=created\_at.desc

# Get tracking history
GET /rest/v1/awb\_status\_logs?awb\_id=eq.<awb\_id>\&order=timestamp.desc
```

### VoIP

```bash
# Initiate call — requires explicit confirmation and write scope
POST /functions/v1/call-initiate
{"phone\_number":"+201234567890"}

# Get call logs for a contact
GET /rest/v1/call\_logs?customer\_id=eq.<uuid>\&order=call\_date.desc
```

### Conversation intelligence and CS AI

Prefer the MCP tools for conversation intelligence. They map to the current schema and RPCs more safely than ad hoc direct queries.

Read-oriented MCP tools:

* `nexus\_list\_ai\_tag\_definitions`
* `nexus\_list\_message\_annotations`
* `nexus\_get\_message\_ai\_annotation`
* `nexus\_get\_org\_ai\_annotation\_settings`
* `nexus\_get\_customer\_conversation\_intelligence`
* `nexus\_get\_conversation\_intelligence\_dashboard`

Write-capable MCP tools that require explicit confirmation and write scope:

* `nexus\_update\_message\_annotation`
* `nexus\_update\_ai\_tag\_definition`
* `nexus\_set\_org\_ai\_annotation\_prompt`
* `nexus\_update\_org\_conversation\_intelligence\_context`

## Pagination

Use either the `Range` header or `offset` and `limit` query parameters.

```bash
GET /rest/v1/customers
Range: 0-24
```

Response includes `Content-Range: 0-24/1523`.

## Filtering

Common PostgREST operators: `eq`, `neq`, `gt`, `gte`, `lt`, `like`, `in`, `is`

```bash
# Multiple filters — note order\_status, not status
GET /rest/v1/orders?organization\_id=eq.<org\_id>\&order\_status=eq.shipped\&created\_at=gte.2025-01-01

# Null check
GET /rest/v1/orders?shopify\_order\_id=is.null
```

## Error handling

|Code|Meaning|Action|
|-|-|-|
|401|Invalid or expired token|Re-authenticate via `agent-auth`|
|403|Scope not allowed|Check API key scopes|
|404|Record not found|Verify the UUID and org scope|
|429|Rate limited|Retry after `Retry-After` seconds|

## Deployed endpoints for agents

### Agent bootstrap

* `POST /functions/v1/agent-api-key-create`
* `POST /functions/v1/agent-auth`
* `POST /functions/v1/mcp-server`

### Outbound messaging used by MCP

* `POST /functions/v1/whatsapp-send-message`
* `POST /functions/v1/facebook-send-message`
* `POST /functions/v1/instagram-send-message`

### Notes

* `agent-auth` is rate limited to **10 attempts per minute per IP**
* agent JWTs expire after **3600 seconds**
* use the raw API key only with `agent-auth`

## Support

If you encounter an error or undocumented behavior, contact:

* **To:** info@aiforstartups.io
* **CC:** karim.sherif@aiforstartups.io

Include the endpoint, the error message, and a short description of the attempted action.

## Additional resources

* Full API reference: [api-reference.md](api-reference.md)
* Hosted MCP docs: `https://nexus-docs.aiforstartups.io/api/ai-agents-mcp`
* OpenAPI spec: `https://nexus-docs.aiforstartups.io/openapi.yaml`
* Docs: `https://nexus-docs.aiforstartups.io`

