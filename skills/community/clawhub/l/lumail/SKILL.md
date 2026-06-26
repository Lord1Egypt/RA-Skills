---
name: lumail
version: "0.1.0"
tags: ["email", "marketing", "newsletter", "mcp", "api", "cli"]
description: >-
  Manage Lumail email marketing platform via CLI and TypeScript SDK.

  Use this skill whenever working with email marketing, subscriber management,
  campaign creation, or any Lumail API interaction. This includes managing
  subscribers, sending campaigns, tagging contacts, sending transactional
  emails, verifying emails, tracking events, and running V2 tools.

  Common scenarios:
  - adding or managing email subscribers
  - creating, updating, or sending campaigns
  - managing tags and segments
  - sending transactional emails
  - verifying email addresses
  - tracking subscriber events
  - running V2 AI tools (generate subject lines, writing style, etc.)

  Prefer this skill whenever the user mentions "lumail", "email campaign",
  "subscribers", "newsletter", "email marketing", "lumail cli", "send email",
  "email list", "tags", or any email marketing task.
---

# Lumail - Email Marketing CLI & SDK

Interact with the Lumail API using either the CLI (`pnpm lumail`) or the TypeScript SDK (`import { Lumail } from "@/lib/lumail-sdk"`).

## Quick Start

```bash
# Set your API key first
pnpm lumail auth set <your-api-key>

# Verify it works
pnpm lumail auth test
```

## CLI Reference

All CLI commands run via `pnpm lumail <command>`. Every command supports global flags.

### Global Flags

| Flag | Description |
|------|-------------|
| `--json` | Output as JSON |
| `--format <text\|json\|csv>` | Output format (default: text) |
| `--verbose` | Enable debug logging |
| `--no-color` | Disable colored output |
| `--no-header` | Omit table headers (for piping) |

### Authentication

```bash
pnpm lumail auth set <token>       # Save API key (~/.config/lumail/token)
pnpm lumail auth show              # Show masked token
pnpm lumail auth show --raw        # Show full token
pnpm lumail auth remove            # Delete saved token
pnpm lumail auth test              # Verify token is valid
```

### Subscribers

```bash
# Create or upsert a subscriber
pnpm lumail subscribers create --email user@example.com --name "John" --tags vip beta

# Get subscriber by email or ID
pnpm lumail subscribers get user@example.com

# Update subscriber
pnpm lumail subscribers update user@example.com --name "John Doe"
pnpm lumail subscribers update user@example.com --tags premium --replace-tags

# Delete subscriber
pnpm lumail subscribers delete user@example.com

# Unsubscribe
pnpm lumail subscribers unsubscribe user@example.com

# Manage tags
pnpm lumail subscribers add-tags user@example.com --tags vip premium
pnpm lumail subscribers remove-tags user@example.com --tags old-tag

# List events
pnpm lumail subscribers events user@example.com --take 50 --order desc
```

### Campaigns

```bash
# List campaigns
pnpm lumail campaigns list
pnpm lumail campaigns list --status DRAFT --page 1 --limit 50
pnpm lumail campaigns list --query "welcome" --json

# Create campaign
pnpm lumail campaigns create --subject "Welcome!" --name "Welcome Campaign"

# Get campaign details
pnpm lumail campaigns get <campaignId>

# Update campaign (DRAFT only)
pnpm lumail campaigns update <campaignId> --subject "Updated Subject" --preview "Preview text"

# Delete campaign (DRAFT only)
pnpm lumail campaigns delete <campaignId>

# Send immediately
pnpm lumail campaigns send <campaignId>

# Schedule for later
pnpm lumail campaigns send <campaignId> --scheduled-at 2025-12-25T10:00:00Z --timezone UTC
```

### Tags

```bash
pnpm lumail tags list
pnpm lumail tags create --name "premium"
pnpm lumail tags get premium          # By name or ID
pnpm lumail tags update <id> --name "gold"
```

### Emails (Transactional)

```bash
# Send transactional email
pnpm lumail emails send \
  --to user@example.com \
  --from noreply@yourdomain.com \
  --subject "Order Confirmation" \
  --content "Your order #123 is confirmed." \
  --content-type MARKDOWN

# With tracking disabled
pnpm lumail emails send --to x --from y --subject z --content "Hello" --transactional

# Verify email address
pnpm lumail emails verify user@example.com
```

### Events

```bash
pnpm lumail events create \
  --type SUBSCRIBER_PAYMENT \
  --subscriber user@example.com \
  --data '{"amount": 99, "plan": "pro"}'
```

Event types: `SUBSCRIBED`, `UNSUBSCRIBED`, `TAG_ADDED`, `TAG_REMOVED`, `EMAIL_OPENED`, `EMAIL_CLICKED`, `EMAIL_SENT`, `EMAIL_RECEIVED`, `WORKFLOW_STARTED`, `WORKFLOW_COMPLETED`, `WORKFLOW_CANCELED`, `FIELD_UPDATED`, `EMAIL_BOUNCED`, `EMAIL_COMPLAINED`, `WEBHOOK_EXECUTED`, `SUBSCRIBER_PAYMENT`, `SUBSCRIBER_REFUND`

### Tools (V2 API)

The V2 tools API provides 59+ tools for AI agents and advanced operations.

```bash
# List all available tools
pnpm lumail tools list

# Get tool schema
pnpm lumail tools get list_subscribers

# Run a tool
pnpm lumail tools run list_subscribers --params '{"limit": 10, "status": "SUBSCRIBED"}'
pnpm lumail tools run create_campaign --params '{"name": "Test", "subject": "Hello"}'
pnpm lumail tools run send_campaign --params '{"campaignId": "abc123"}'
```

## SDK Reference

The SDK lives at `src/lib/lumail-sdk/` and is importable via `@/lib/lumail-sdk`.

### Setup

```typescript
import { Lumail } from "@/lib/lumail-sdk";

const lumail = new Lumail({
  apiKey: "lm_...",
  baseUrl: "https://lumail.io/api", // optional, defaults to this
});
```

### Subscribers

```typescript
// Create/upsert
const { subscriber } = await lumail.subscribers.create({
  email: "user@example.com",
  name: "John",
  tags: ["vip", "beta"],
  fields: { company: "Acme" },
  triggerWorkflows: true,
});

// Get by email or ID
const { subscriber } = await lumail.subscribers.get("user@example.com");

// Update
await lumail.subscribers.update("user@example.com", { name: "John Doe" });

// Delete
await lumail.subscribers.delete("user@example.com");

// Unsubscribe
await lumail.subscribers.unsubscribe("user@example.com");

// Tags
await lumail.subscribers.addTags("user@example.com", ["premium"]);
await lumail.subscribers.removeTags("user@example.com", ["old-tag"]);

// Events (cursor-based pagination)
const { events, nextCursor } = await lumail.subscribers.listEvents("user@example.com", {
  take: 20,
  order: "desc",
  eventTypes: ["EMAIL_OPENED", "EMAIL_CLICKED"],
});
```

### Campaigns

```typescript
// List with pagination
const { campaigns, total, pageCount } = await lumail.campaigns.list({
  status: "DRAFT",
  page: 1,
  limit: 20,
  query: "welcome",
});

// Create
const { campaign, campaignId } = await lumail.campaigns.create({
  subject: "Welcome!",
  name: "Welcome Campaign",
  contentType: "MARKDOWN",
});

// Get
const { campaign } = await lumail.campaigns.get(campaignId);

// Update (DRAFT only)
await lumail.campaigns.update(campaignId, { subject: "Updated Subject" });

// Delete (DRAFT only)
await lumail.campaigns.delete(campaignId);

// Send immediately
await lumail.campaigns.send(campaignId);

// Schedule
await lumail.campaigns.send(campaignId, {
  scheduledAt: "2025-12-25T10:00:00Z",
  timezone: "UTC",
});
```

### Emails (Transactional)

```typescript
const { qstashMessageId } = await lumail.emails.send({
  to: "user@example.com",
  from: "noreply@yourdomain.com",
  subject: "Order Confirmation",
  content: "Your order is confirmed.",
  contentType: "MARKDOWN", // "MARKDOWN" | "HTML" | "TIPTAP"
  tracking: { links: true, open: true },
});

// Verify email
const { isValid } = await lumail.emails.verify({ email: "test@example.com" });
```

### Tags

```typescript
const { tags } = await lumail.tags.list();
const { tag } = await lumail.tags.create({ name: "premium" });
const { tag } = await lumail.tags.get("premium"); // by name or ID
await lumail.tags.update("premium", { name: "gold" });
```

### Events

```typescript
await lumail.events.create({
  eventType: "SUBSCRIBER_PAYMENT",
  subscriber: "user@example.com",
  data: { amount: 99, plan: "pro" },
});
```

### Tools (V2 API)

```typescript
// List all tools
const { tools, grouped } = await lumail.tools.list();

// Get tool schema
const { tool } = await lumail.tools.get("list_subscribers");

// Run a tool with typed response
const result = await lumail.tools.run<{ subscribers: unknown[] }>(
  "list_subscribers",
  { limit: 10 },
);
```

### Error Handling

The SDK throws typed errors - catch specific error types:

```typescript
import {
  Lumail,
  LumailAuthenticationError,
  LumailNotFoundError,
  LumailRateLimitError,
  LumailValidationError,
  LumailPaymentRequiredError,
} from "@/lib/lumail-sdk";

try {
  await lumail.subscribers.get("unknown@example.com");
} catch (error) {
  if (error instanceof LumailNotFoundError) {
    // 404 - subscriber not found
  } else if (error instanceof LumailAuthenticationError) {
    // 401 - invalid API key
  } else if (error instanceof LumailRateLimitError) {
    // 429 - rate limited, error.retryAfter has delay in ms
  } else if (error instanceof LumailPaymentRequiredError) {
    // 402 - plan limit reached
  } else if (error instanceof LumailValidationError) {
    // 400 - invalid request
  }
}
```

### Retry Behavior

- GET/PUT/DELETE requests retry up to 3 times on network errors and 429s
- POST/PATCH requests do NOT retry (prevents duplicate subscribers/emails)
- Retry delays: 1s, 2s, 4s (exponential backoff)
- Respects `Retry-After` header from rate limit responses
- Default timeout: 30s per request

## npm Package

Published as `lumail` on npm. Dual CLI + library:

```bash
# CLI usage (after npm install -g lumail)
npx lumail auth set <token>
npx lumail subscribers create --email user@example.com

# Library usage
import { Lumail } from "lumail";
const lumail = new Lumail({ apiKey: "lm_..." });
```

Package source: `packages/lumail/`
Build: `bun run build` (in packages/lumail/)
Auto-release: pushes to main trigger GitHub Actions release

## File Locations

| Component | Path |
|-----------|------|
| SDK source | `src/lib/lumail-sdk/` |
| CLI source | `src/cli/` |
| npm package | `packages/lumail/` |
| Build script | `packages/lumail/build.ts` |
| Tests | `__tests__/lumail-sdk.test.ts`, `__tests__/lumail-cli.test.ts` |
| API docs | `content/docs/api-reference/` |
| GH Action | `.github/workflows/release-lumail.yml` |
