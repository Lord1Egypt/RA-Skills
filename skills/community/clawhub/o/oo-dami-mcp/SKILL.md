---
name: oo-dami-mcp
description: "DAMI (tikclubs.com). Use this skill for ANY DAMI request — reading, creating, updating, and deleting data. Whenever a task involves DAMI, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "DAMI"
  author: "OOMOL"
  version: "1.0.2"
  services: ["dami_mcp"]
  icon: "https://static.oomol.com/logo/third-party/dami_mcp.png"
---

# DAMI

Operate **DAMI** through your OOMOL-connected account. This skill calls the `dami_mcp` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected DAMI. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "dami_mcp" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "dami_mcp" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `call_tool` — Call a DAMI TikTok Shop tool after inspecting list_tools. Available tools cover shops, products, creator discovery, competitor research, outreach tasks and creator conversations. Calls can consume DAMI credits and may send invitations or messages. [destructive]
- `competitor_product_list` — Search competitor TikTok Shop products through DAMI. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `conversation_create` — Create a DAMI conversation with one TikTok creator for direct outreach. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known. [write]
- `conversation_send` — Send a message in an existing DAMI creator conversation. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known. [write]
- `creator_filter_options` — Get creator-filter options for DAMI's full creator database or an authorized shop's TikTok creator marketplace. FULL source does not require shopId; MARKET source requires an authorized shopId returned by shop_auth_list. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `creator_first_category` — List first-level creator categories available for DAMI creator discovery. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `creator_list_by_product_id` — List creators associated with or promoting a selected competitor product in DAMI. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `creator_list_filter_all` — Search and filter creators in DAMI's full creator database. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `creator_list_filter_square` — Search and filter creators in an authorized shop's TikTok creator marketplace through DAMI. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `creator_recommend_by_product` — Recommend DAMI creators for a selected TikTok Shop product. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `creator_second_category` — List second-level creator categories for a parent creator category in DAMI. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `filter_creators_for_invite` — Check and filter creators before creating a DAMI invitation task, excluding creators that cannot be invited. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `filter_creators_for_message` — Check and filter creators before creating a DAMI messaging task, excluding creators that cannot be messaged. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `get_consumption_balance` — Get the connected DAMI account's current shared CRM credit balance. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `invite_auto_match_config_update` — Update the configuration for a DAMI automatic creator-invitation workflow. This can replace existing workflow settings. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known. [destructive]
- `invite_auto_match_create` — Create and start a DAMI automatic creator-invitation task after reviewing its prepared configuration. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known. [write]
- `invite_auto_match_prepare` — Prepare and preview a DAMI automatic creator-invitation workflow before creating the task. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `invite_config_sources` — Get the products, creators and other source options used to configure a DAMI automatic invitation workflow. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `invite_content_generate` — Generate invitation content for a DAMI creator-outreach workflow. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `list_tools` — Discover the DAMI TikTok Shop tools currently enabled for the connected account, API key, package and server allowlist, including live argument schemas and behavior hints.
- `message_auto_match_create` — Create and start a DAMI automatic creator-messaging task after reviewing its prepared configuration. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known. [write]
- `message_auto_match_prepare` — Prepare and preview a DAMI automatic creator-messaging workflow before creating the task. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `message_config_sources` — Get the creators, content and other source options used to configure a DAMI automatic messaging workflow. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `message_config_update` — Update the configuration for a DAMI automatic creator-messaging workflow. This can replace existing workflow settings. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known. [destructive]
- `message_content_generate` — Generate message content for a DAMI creator-outreach workflow. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `product_first_category` — List DAMI's first-level TikTok Shop product categories. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `product_second_category` — List second-level TikTok Shop product categories for a parent category in DAMI. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `product_third_category` — List third-level TikTok Shop product categories for a parent category in DAMI. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `query_competitor_shop_list` — Search competitor TikTok Shop stores through DAMI. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `query_creator_invite_records` — Query DAMI creator invitation history and statuses. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `query_creator_message_records` — Query DAMI creator messaging history and statuses. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `query_public_plan_products` — List public-plan products available to an authorized TikTok Shop store in DAMI. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.
- `shop_auth_list` — List TikTok Shop stores currently authorized in DAMI. Use the returned shop ID for tools that require shop context. DAMI publishes the current argument fields through list_tools; inspect that action before calling when the live schema is not already known.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change DAMI state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — DAMI is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/dami_mcp
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- DAMI homepage: https://www.tikclubs.com/
- API documentation: https://vnfrxfa5wp.feishu.cn/wiki/UpXTwU4vJiWBPmk3iY5cY7HAnSg
