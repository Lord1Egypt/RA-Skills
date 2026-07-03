---
name: homebox-skill
description: "Tool for interacting with self-hosted HomeBox inventory management service via its REST API. Use when user wants to: (1) Find where an item is (e.g., 'where is my wallet?', 'where did I put my keys?'), (2) Search inventory by name/tag/location (e.g., 'find my electronics', 'whats in my desk drawer'), (3) Add new items (e.g., 'add my new laptop to inventory'), (4) Update items (e.g., 'update the location of my passport'), (5) Remove items (e.g., 'delete my old phone from inventory'), (6) List items by category or location, (7) Check item details, (8) Create/manage locations and tags. Invoke when user mentions HomeBox, home inventory, or asks about item locations in their home."
---

# HomeBox Skill

Use the HomeBox REST API to manage your home inventory. This skill provides a cross-platform Node.js CLI script and references the full API spec.

## Self-Signed TLS Certificate

If your HomeBox instance uses a self-signed cert (like a Docker `.nas.io` domain), set `NODE_TLS_REJECT_UNAUTHORIZED=0` in the environment before running any commands. The script relies on Node.js `fetch` which respects this env var.

```bash
# PowerShell
$env:NODE_TLS_REJECT_UNAUTHORIZED = 0
node scripts/homebox.js ...

# Bash
NODE_TLS_REJECT_UNAUTHORIZED=0 node scripts/homebox.js ...
```

> This disables TLS verification globally — use with caution and only in trusted networks.

## Prerequisites

Requires Node.js >= 18 and two environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `HOMEBOX_BASE_URL` | Your HomeBox server URL | `http://192.168.1.100:3100` |
| `HOMEBOX_TOKEN` | Bearer token for API auth | `your-api-token-string` |
| `HOMEBOX_API_VERSION` | Force API version (`v1` or `v2`). Omit to auto-detect. | `v1` |

The script auto-detects API version by probing `GET /api/v1/entities`:
- **v1** (hay-kot): uses `/api/v1/items`, `/api/v1/locations`, `/api/v1/labels`
- **v2** (sysadminsmedia): uses `/api/v1/entities`, `/api/v1/tags`, `/api/v1/entity-types`

Set `HOMEBOX_API_VERSION=v1` or `HOMEBOX_API_VERSION=v2` to skip auto-detect.

**Getting a token:** Login via the script: `node {baseDir}/scripts/homebox.js login <username>` (will prompt for password). Then set `HOMEBOX_TOKEN` to the returned token.

## Using the CLI Script

All operations use the cross-platform Node.js script at `{baseDir}/scripts/homebox.js`:

```bash
node {baseDir}/scripts/homebox.js <command> [options]
```

Run `node {baseDir}/scripts/homebox.js --help` for full usage.

### Core Operations

| Task | Command |
|------|---------|
| **Find an item** | `node {baseDir}/scripts/homebox.js search wallet` |
| **List all items** | `node {baseDir}/scripts/homebox.js list` |
| **Get item details** | `node {baseDir}/scripts/homebox.js get <id>` |
| **Add an item** | `node {baseDir}/scripts/homebox.js add "My Wallet" --description "Brown leather" --parentId <location-id>` |
| **Update an item** | `node {baseDir}/scripts/homebox.js update <id> --description "Moved to drawer" --parentId <new-location>` |
| **Partial update** | `node {baseDir}/scripts/homebox.js patch <id> --parentId <new-location>` |
| **Delete an item** | `node {baseDir}/scripts/homebox.js delete <id>` |
| **Browse locations** | `node {baseDir}/scripts/homebox.js tree` |
| **List tags** | `node {baseDir}/scripts/homebox.js tags` |
| **View stats** | `node {baseDir}/scripts/homebox.js stats` |

### Search Examples

Natural language queries should be mapped to search terms:
- "Where are my keys?" → `homebox.js search keys`
- "What electronics do I have?" → `homebox.js search --tags <electronics-tag-id>`
- "What's in my desk drawer?" → `homebox.js search --parents <desk-drawer-id>`

### Adding Items with Full Details

```bash
node {baseDir}/scripts/homebox.js add "MacBook Pro" \
  --description "14-inch M3 Pro" \
  --manufacturer "Apple" \
  --modelNumber "MRXJ3LL/A" \
  --serialNumber "FVLK..." \
  --purchasePrice 1999.00 \
  --purchaseDate "2024-03-15" \
  --purchaseFrom "Apple Store" \
  --insured true \
  --lifetimeWarranty false \
  --warrantyExpires "2025-03-15" \
  --warrantyDetails "AppleCare+" \
  --tagIds "tag-id-1,tag-id-2" \
  --parentId "location-id"
```

## Response Fields

Fields vary by API version:

| Field | v1 (hay-kot) | v2 (sysadminsmedia) |
|-------|-------------|---------------------|
| `id` | UUID | UUID |
| `name`, `description` | Same | Same |
| Location | `location: {id, name}` nested object | `parentId` (string, nullable) |
| Tags/Labels | `labels: [{id, name, color}]` | `tags: [{id, name, color}]` |
| Type | N/A (items only) | `entityType: {id, name, icon, isLocation}` |
| `quantity` | Same | Same |
| Manufacturer/Model/Serial | Same | Same |
| Purchase info | `purchaseTime`, `purchasePrice`, `purchaseFrom` | `purchaseDate`, `purchasePrice`, `purchaseFrom` |
| Warranty | Same field names | Same |
| Sold info | `soldTime`, `soldPrice`, `soldTo`, `soldNotes` | `soldDate`, `soldPrice`, `soldTo`, `soldNotes` |
| `notes` | Same | Same |
| `assetId` | Same | Same |
| Attachments | `imageId`, `thumbnailId` | Same |
| Sync children | `syncChildItemsLocations` | `syncChildEntityLocations` |
| Timestamps | `createdAt`, `updatedAt` | Same |

Paginated queries return: `items[]`, `total`, `page`, `pageSize`, `totalPrice`.

**Location management:** v1 has a separate `/api/v1/locations` resource. v2 treats locations as entities with `entityType.isLocation = true`; the tree endpoint is `/api/v1/entities/tree`.

## Interaction Philosophy

The goal is **natural, low-friction inventory management** — not filling out forms.

### Core Principles

1. **Accept any input style.** A sentence ("add my AirPods I bought last month for 1299"), fragments ("AirPods bedroom"), or structured flags — all fine. Parse what's given, ignore what's not.

2. **Ask only what's essential.** For adding an item, the only must-have is a name. Everything else (location, description, tags, price, dates, brand, serial) is optional. Don't walk through fields one by one.

3. **Batch updates naturally.** If the user gives multiple details in one message ("price 1299, Apple, bought Feb 2025"), merge them into a single update — don't process each field separately.

4. **Proactive, not pushy.** After adding an item, briefly note what else could be filled in (e.g., "serial number and warranty can be added too") and let the user decide. If they say no, move on.

5. **Confirm writes, but don't over-confirm.** Summarize what will be done and ask once. Don't ask "confirm?" for every individual field.
   - **Delete** is the only hard rule: never execute without explicit, unambiguous confirmation.
   - **Add / update / patch** need user sign-off, but a single "Proceed?" after summarizing the changes is sufficient.

6. **Match the user's language.** This skill documentation is in English for universal access, but all conversation with the user should be in whatever language they use — don't switch to English just because the skill file is.

7. **Be conversational, not mechanical.**  Instead of replying with rigid structured messages or error codes, reply naturally in the user's language — guide them, offer suggestions, and keep the interaction feeling like a helpful person, not a robot.

### Search & Query

- Interpret natural language ("where are my keys?" → `search keys`). Try partial/fuzzy matches first.
- After showing results, optionally note items with missing useful fields (no brand, no price, no warranty).

### Operational Notes

- **Always fetch fresh IDs.** HomeBox UUIDs (labels, locations, items) may change if the database is reset between sessions. Never rely on IDs cached earlier in the conversation.
- **PUT 500 with `labelIds`?** Most likely a stale label UUID. Re-fetch labels and retry.
- **Self-signed TLS cert?** Set `NODE_TLS_REJECT_UNAUTHORIZED=0` (see above).
- **Missing token?** Drive the setup yourself: when env vars are missing, ask once for URL + credentials, run `login`, and proceed — no commentary, no "shall I save?", and advise setting `HOMEBOX_TOKEN`.  Note that `login` returns a token with "Bearer " prefix — strip it before setting `HOMEBOX_TOKEN` since the script prepends its own "Bearer ".

### Search & Query
- **Script mechanics?** The script requires Node.js >= 18. Resolve all script mechanics by reading source files directly. 

## Detailed API Reference

For all available endpoints, request/response schemas, and advanced operations (attachments, maintenance logs, exports, group management, etc.), see `{baseDir}/references/api-reference.md`.
