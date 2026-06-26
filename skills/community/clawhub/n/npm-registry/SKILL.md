---
name: npm-registry
description: Search npm packages, inspect metadata and versions, review download stats, and check security advisories. Use this skill when users want to explore npm registry data, verify package integrity, or monitor package health via the npm API.
---

# npm Registry

![npm Registry](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/npm.svg)

Access the npm public registry via the npm API. Search packages, inspect metadata and versions, review download statistics, and check security advisories and registry health.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=npm-registry) for hosted connection flows and credentials so you do not need to configure npm API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect npm |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect npm |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   npm Registry    │
│   (User Chat)   │     │   (API Key)  │     │   (npmjs.com)    │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin │                       │
          │  2. Pair Device      │                       │
          │  3. Connect npm       │                       │
          │ │  4. Secure Proxy      │
          │                       │  5. API Requests │
          │                       │                       │
          ▼                       ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │  npm │
    │  File    │           │ Auth     │           │ Registry │
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for npm again."

## Quick Start

```bash
# Search for packages
clawlink_call_tool --tool "npm_search_packages" --params '{"query": "express", "size": 10}'

# Get package metadata
clawlink_call_tool --tool "npm_get_package" --params '{"package_name": "express"}'

# Get download statistics
clawlink_call_tool --tool "npm_get_download_stats" --params '{"package_name": "lodash", "period": "last-month"}'
```

## Authentication

All npm tool calls are authenticated automatically by ClawLink using the user's npm account.

**No API key is required in chat.** ClawLink handles authentication securely and injects it into every npm API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=npm and connect npm.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `npm` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration npm
```

**Response:** Returns the live tool catalog for npm.

### Reconnect

If npm tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=npm
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration npm`

## Security & Permissions

- Access is scoped to public and private package data within the connected npm account.
- **Write operations (token deletion, scope changes) require explicit user confirmation.**
- Read operations (search, metadata, downloads) are safe and do not modify any data.

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm npm is connected.
2. Call `clawlink_list_tools --integration npm` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `npm`.
5. If no npm tools appear, direct the user to https://claw-link.dev/dashboard?add=npm.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: Search packages → Read metadata → Show results    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute update                                  │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Code Examples

### Search packages

```bash
clawlink_call_tool --tool "npm_search_packages" \
  --params '{
    "query": "react framework",
    "size": 20,
    "quality": 0.8,
    "popularity": 0.5
  }'
```

### Get package details

```bash
clawlink_call_tool --tool "npm_get_package" \
  --params '{
    "package_name": "next",
    "version": "latest"
  }'
```

### Get download counts

```bash
clawlink_call_tool --tool "npm_get_download_counts" \
  --params '{
    "package_name": "axios",
    "start": "2024-01-01",
    "end": "2024-01-31"
  }'
```

### Check security advisories

```bash
clawlink_call_tool --tool "npm_get_advisories" \
  --params '{
    "package_name": "lodash"
  }'
```

## Notes

- npm Registry API has rate limits. Use exponential backoff when encountering 429 errors.
- Some endpoints require authentication for private packages — public package data is available without connection.
- Download statistics are available with a delay of up to 48 hours.
- Package names must be lowercase and may include scoped packages (e.g., `@org/package`).

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration npm`. |
| Missing connection | npm is not connected. Direct the user to https://claw-link.dev/dashboard?add=npm. |
| `not_found` | Package does not exist in the registry. Check the package name spelling. |
| `validation_error` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| Rate limited | Too many requests. Wait and retry with exponential backoff. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `npm`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [npm Documentation](https://docs.npmjs.com/)
- [npm Registry API](https://github.com/npm/registry)
- [npm Security Advisories](https://www.npmjs.com/advisories)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=npm-registry
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [GitHub Repos](https://clawhub.ai/hith3sh/github-repos) — For GitHub repository operations
- [npm](https://clawhub.ai/hith3sh/npm-registry) — For this skill's native documentation

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=npm-registry)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
