---
name: instantly-outreach
description: "Manage cold email campaigns, leads, and outreach analytics via Instantly AI through the superagnt unified API."
version: 2.0.14
author: superagnt
license: MIT-0
platforms: [macos, linux, windows]
required_environment_variables:
  - SUPERAGNT_API_KEY
metadata:
  hermes:
    tags: [instantly, integration, api, ai-agent]
  openclaw:
    requires:
      env:
        - SUPERAGNT_API_KEY
      bins:
        - curl
    primaryEnv: SUPERAGNT_API_KEY
    emoji: "📧"
    homepage: https://superagnt.com/r/ch-instantly-outreach-docs
---

# Instantly AI Integration

The Instantly AI integration connects your Instantly account to superagnt, enabling AI agents and workflows to manage cold email campaigns, leads, analytics, and account settings programmatically. Supports campaign CRUD, lead management, sending accounts, warmup settings, and detailed analytics.

## Alternative install: the MCP server

If this client speaks MCP, you can connect the workspace server instead of
using this skill's curl calls — after the user connects their
Instantly AI account in the superagnt app, the same endpoints below are exposed
as native MCP tools:

```
https://mcp.superagnt.com/mcp
```

The URL publishes full OAuth discovery — an MCP-capable client needs the URL
and nothing else (approve once in the browser). Per-client setup lines:
https://www.superagnt.com/install

Everything below works on curl-only environments with just the API key.

## Capabilities and safety

This skill documents the Instantly AI API surface the user's connected
account can reach — which can include destructive operations (updates,
deletes) and, where the vendor supports them, actions performed as the user
(sending messages, modifying records, changing settings). Two hard rules:

- **Confirm before destructive or outbound actions.** Never delete, overwrite,
  or send on the user's behalf without their explicit confirmation in the
  conversation.
- **Stay inside the user's request.** Use only the endpoints the task needs;
  this skill grants no access beyond the Instantly AI connection the user
  set up themselves.

**Disclosure:** Account administration: beyond outreach, the Instantly API includes workspace administration, billing, API-key, and account-procurement endpoints. Use those only when the user explicitly asks for account administration, and always confirm before creating keys, changing billing, or purchasing anything.

## Prerequisites

1. An API key — get one from the [superagnt app](https://superagnt.com/r/ch-instantly-outreach-key) and export it as
   `SUPERAGNT_API_KEY`.
2. A connected Instantly AI account — connect it on the
   [Connections page](https://app.superagnt.com/dashboard/connections). Calls fail with a clear error
   until the vendor is connected; that error is the signal to send the user to
   the connections page, not a bug.

Note: `/v1/connections/*` calls run on the USER'S Instantly AI credentials —
vendor-side rate limits and billing are theirs, not platform credits.

## Authentication

```
Authorization: Bearer $SUPERAGNT_API_KEY
```

If the variable is not set, ask the user for their key or point them at
https://superagnt.com/r/ch-instantly-outreach-key.

## Verify the install (do this first)

```bash
curl -s https://api.superagnt.com/v1/credits \
  -H &#x27;Authorization: Bearer $SUPERAGNT_API_KEY&#x27;
```

A JSON result proves the key end to end. 401 = bad key; an error naming the
connection means the Instantly AI account is not connected yet.

## Base URL

```
https://api.superagnt.com/v1/connections/instantly
```

## Available Endpoints

| Method | Path | Summary |
|--------|------|---------|
| `GET` | `/api/v2/account-campaign-mappings/{email}` | Get campaigns associated with an email |
| `GET` | `/api/v2/accounts` | List account |
| `POST` | `/api/v2/accounts` | Create account |
| `GET` | `/api/v2/accounts/{email}` | Get account |
| `PATCH` | `/api/v2/accounts/{email}` | Patch account |
| `DELETE` | `/api/v2/accounts/{email}` | Delete account |
| `POST` | `/api/v2/accounts/warmup/enable` | Enable warmup for accounts |
| `POST` | `/api/v2/accounts/warmup/disable` | Disable warmup for accounts |
| `POST` | `/api/v2/accounts/warmup-analytics` | Get warmup analytics |
| `GET` | `/api/v2/accounts/analytics/daily` | Get daily account analytics |
| `POST` | `/api/v2/accounts/{email}/pause` | Pause an account |
| `POST` | `/api/v2/accounts/{email}/resume` | Resume a paused account |
| `POST` | `/api/v2/accounts/{email}/mark-fixed` | Mark an account as fixed |
| `GET` | `/api/v2/accounts/ctd/status` | Get custom tracking domain status |
| `POST` | `/api/v2/accounts/test/vitals` | Test account vitals |
| `POST` | `/api/v2/accounts/move` | Move accounts between workspaces |
| `GET` | `/api/v2/api-keys` | List api key |
| `POST` | `/api/v2/api-keys` | Create api key |
| `DELETE` | `/api/v2/api-keys/{id}` | Delete api key |
| `GET` | `/api/v2/audit-logs` | List audit log |
| `GET` | `/api/v2/background-jobs` | List background job |
| `GET` | `/api/v2/background-jobs/{id}` | Get background job |
| `GET` | `/api/v2/block-lists-entries` | List block list entry |
| `POST` | `/api/v2/block-lists-entries` | Create block list entry |
| `DELETE` | `/api/v2/block-lists-entries` | Delete all block list entries |
| `GET` | `/api/v2/block-lists-entries/{id}` | Get block list entry |
| `PATCH` | `/api/v2/block-lists-entries/{id}` | Patch block list entry |
| `DELETE` | `/api/v2/block-lists-entries/{id}` | Delete block list entry |
| `POST` | `/api/v2/block-lists-entries/bulk-create` | Bulk create block list entry |
| `POST` | `/api/v2/block-lists-entries/bulk-delete` | Bulk delete block list entry |
| `GET` | `/api/v2/block-lists-entries/download` | Download all block list entries as CSV |
| `GET` | `/api/v2/campaigns` | List campaign |
| `POST` | `/api/v2/campaigns` | Create campaign |
| `POST` | `/api/v2/campaigns/{id}/activate` | Activate(start), or resume a campaign |
| `POST` | `/api/v2/campaigns/{id}/pause` | Stop(or pause) a campaign |
| `GET` | `/api/v2/campaigns/{id}` | Get campaign |
| `PATCH` | `/api/v2/campaigns/{id}` | Patch campaign |
| `DELETE` | `/api/v2/campaigns/{id}` | Delete campaign |
| `GET` | `/api/v2/campaigns/search-by-contact` | Search campaigns by lead email |
| `GET` | `/api/v2/campaigns/analytics` | Get campaign(s) analytics |
| `GET` | `/api/v2/campaigns/analytics/overview` | Get campaign(s) analytics overview |
| `GET` | `/api/v2/campaigns/analytics/daily` | Get daily campaign analytics |
| `GET` | `/api/v2/campaigns/analytics/steps` | Get campaign steps analytics |
| `POST` | `/api/v2/campaigns/{id}/share` | Share a campaign |
| `POST` | `/api/v2/campaigns/{id}/from-export` | Create campaign from shared one |
| `POST` | `/api/v2/campaigns/{id}/export` | Export campaign to JSON format |
| `POST` | `/api/v2/campaigns/{id}/duplicate` | Duplicate campaign |
| `GET` | `/api/v2/campaigns/count-launched` | Get launched campaigns count |
| `POST` | `/api/v2/campaigns/{id}/variables` | Add campaign variables |
| `GET` | `/api/v2/campaigns/{id}/sending-status` | Get campaign sending status |
| `GET` | `/api/v2/crm-actions/phone-numbers` | List phone numbers |
| `DELETE` | `/api/v2/crm-actions/phone-numbers/{id}` | Delete phone number |
| `GET` | `/api/v2/custom-tag-mappings` | List custom tag mapping |
| `GET` | `/api/v2/custom-tags` | List custom tag |
| `POST` | `/api/v2/custom-tags` | Create custom tag |
| `GET` | `/api/v2/custom-tags/{id}` | Get custom tag |
| `PATCH` | `/api/v2/custom-tags/{id}` | Patch custom tag |
| `DELETE` | `/api/v2/custom-tags/{id}` | Delete custom tag |
| `POST` | `/api/v2/custom-tags/toggle-resource` | Assign or unassign tags to resources |
| `GET` | `/api/v2/dfy-email-account-orders` | List dfy email account order |
| `POST` | `/api/v2/dfy-email-account-orders` | Place a DFY email account order |
| `POST` | `/api/v2/dfy-email-account-orders/domains/similar` | Generate similar available domains |
| `POST` | `/api/v2/dfy-email-account-orders/domains/check` | Check domains availability |
| `POST` | `/api/v2/dfy-email-account-orders/domains/pre-warmed-up-list` | Get pre-warmed up domains |
| `GET` | `/api/v2/dfy-email-account-orders/accounts` | List DFY ordered email accounts |
| `POST` | `/api/v2/dfy-email-account-orders/accounts/cancel` | Cancel dfy email accounts |
| `POST` | `/api/v2/emails/test` | Send a test email |
| `POST` | `/api/v2/emails/reply` | Reply to an email |
| `POST` | `/api/v2/emails/forward` | Forward an email |
| `GET` | `/api/v2/emails` | List email |
| `GET` | `/api/v2/emails/{id}` | Get email |
| `PATCH` | `/api/v2/emails/{id}` | Patch email |
| `DELETE` | `/api/v2/emails/{id}` | Delete email |
| `GET` | `/api/v2/emails/unread/count` | Count unread emails |
| `POST` | `/api/v2/emails/threads/{thread_id}/mark-as-read` | Mark all emails in a thread as read |
| `GET` | `/api/v2/inbox-placement-analytics` | List inbox placement analytics |
| `GET` | `/api/v2/inbox-placement-analytics/{id}` | Get inbox placement analytics |
| `POST` | `/api/v2/inbox-placement-analytics/stats-by-test-id` | Retrieve inbox placement analytics stats by test id |
| `POST` | `/api/v2/inbox-placement-analytics/deliverability-insights` | Retrieve inbox placement analytics deliverability insights |
| `POST` | `/api/v2/inbox-placement-analytics/stats-by-date` | Get inbox placement analytics stats by date |
| `GET` | `/api/v2/inbox-placement-reports` | List inbox placement blacklist &amp; spamassassin report |
| `GET` | `/api/v2/inbox-placement-reports/{id}` | Get inbox placement blacklist &amp; spamassassin report |
| `GET` | `/api/v2/inbox-placement-tests` | List inbox placement test |
| `POST` | `/api/v2/inbox-placement-tests` | Create inbox placement test |
| `GET` | `/api/v2/inbox-placement-tests/{id}` | Get inbox placement test |
| `PATCH` | `/api/v2/inbox-placement-tests/{id}` | Patch inbox placement test |
| `DELETE` | `/api/v2/inbox-placement-tests/{id}` | Delete inbox placement test |
| `GET` | `/api/v2/inbox-placement-tests/email-service-provider-options` | Get ESP options |
| `GET` | `/api/v2/lead-labels` | List lead label |
| `POST` | `/api/v2/lead-labels` | Create lead label |
| `GET` | `/api/v2/lead-labels/{id}` | Get lead label |
| `PATCH` | `/api/v2/lead-labels/{id}` | Patch lead label |
| `DELETE` | `/api/v2/lead-labels/{id}` | Delete lead label |
| `POST` | `/api/v2/lead-labels/ai-reply-label` | Test AI reply label prediction |
| `GET` | `/api/v2/lead-lists` | List lead list |
| `POST` | `/api/v2/lead-lists` | Create lead list |
| `GET` | `/api/v2/lead-lists/{id}` | Get lead list |
| `PATCH` | `/api/v2/lead-lists/{id}` | Patch lead list |
| `DELETE` | `/api/v2/lead-lists/{id}` | Delete lead list |
| `GET` | `/api/v2/lead-lists/{id}/verification-stats` | Get verification statistics for a lead list |
| `POST` | `/api/v2/leads` | Create lead |
| `DELETE` | `/api/v2/leads` | Delete leads in bulk |
| `POST` | `/api/v2/leads/list` | List leads |
| `GET` | `/api/v2/leads/{id}` | Get lead |
| `PATCH` | `/api/v2/leads/{id}` | Patch lead |
| `DELETE` | `/api/v2/leads/{id}` | Delete lead |
| `POST` | `/api/v2/leads/merge` | Merge two leads |
| `POST` | `/api/v2/leads/update-interest-status` | Update the interest status of a lead |
| `POST` | `/api/v2/leads/subsequence/remove` | Remove a lead from a subsequence |
| `POST` | `/api/v2/leads/bulk-assign` | Bulk assign leads to organization users |
| `POST` | `/api/v2/leads/move` | Move leads to a campaign or list |
| `POST` | `/api/v2/leads/subsequence/move` | Move a lead to a subsequence |
| `POST` | `/api/v2/leads/add` | Add leads in bulk to a campaign or list |
| `POST` | `/api/v2/oauth/google/init` | Initialize google oauth |
| `POST` | `/api/v2/oauth/microsoft/init` | Initialize microsoft oauth |
| `GET` | `/api/v2/oauth/session/status/{sessionId}` | Get oauth session status |
| `GET` | `/api/v2/subsequences` | List campaign subsequence |
| `POST` | `/api/v2/subsequences` | Create campaign subsequence |
| `POST` | `/api/v2/subsequences/{id}/duplicate` | Duplicate a subsequence |
| `POST` | `/api/v2/subsequences/{id}/pause` | Pause a subsequence |
| `POST` | `/api/v2/subsequences/{id}/resume` | Resume a paused subsequence |
| `GET` | `/api/v2/subsequences/{id}` | Get campaign subsequence |
| `PATCH` | `/api/v2/subsequences/{id}` | Patch campaign subsequence |
| `DELETE` | `/api/v2/subsequences/{id}` | Delete campaign subsequence |
| `GET` | `/api/v2/subsequences/{id}/sending-status` | Get subsequence sending status |
| `POST` | `/api/v2/supersearch-enrichment/enrich-leads-from-supersearch` | Enrich leads from supersearch |
| `GET` | `/api/v2/supersearch-enrichment/{resource_id}` | Get enrichment for resource |
| `POST` | `/api/v2/supersearch-enrichment` | Create an enrichment |
| `PATCH` | `/api/v2/supersearch-enrichment/{resource_id}/settings` | Update enrichment settings for resource |
| `POST` | `/api/v2/supersearch-enrichment/ai` | Create AI enrichment |
| `GET` | `/api/v2/supersearch-enrichment/ai/{resource_id}/in-progress` | Get AI enrichment for resource |
| `GET` | `/api/v2/supersearch-enrichment/history/{resource_id}` | Get enrichment history |
| `POST` | `/api/v2/supersearch-enrichment/run` | Run enrichment for resource |
| `POST` | `/api/v2/supersearch-enrichment/count-leads-from-supersearch` | Count leads from supersearch |
| `POST` | `/api/v2/supersearch-enrichment/preview-leads-from-supersearch` | Preview leads from supersearch |
| `GET` | `/api/v2/webhook-events` | List webhook event |
| `GET` | `/api/v2/webhook-events/{id}` | Get webhook event |
| `GET` | `/api/v2/webhook-events/summary` | Get overview aggregates for webhook events |
| `GET` | `/api/v2/webhook-events/summary-by-date` | Get overview aggregates for webhook events by date |
| `GET` | `/api/v2/webhooks` | List webhooks |
| `POST` | `/api/v2/webhooks` | Create webhook |
| `GET` | `/api/v2/webhooks/{id}` | Get webhook |
| `PATCH` | `/api/v2/webhooks/{id}` | Patch webhook |
| `DELETE` | `/api/v2/webhooks/{id}` | Delete webhook |
| `GET` | `/api/v2/webhooks/event-types` | List available event types |
| `POST` | `/api/v2/webhooks/{id}/test` | Test a webhook |
| `POST` | `/api/v2/webhooks/{id}/resume` | Resume a webhook |
| `GET` | `/api/v2/workspace-billing/plan-details` | Get workspace plan details |
| `GET` | `/api/v2/workspace-billing/subscription-details` | Get workspace subscription details |
| `GET` | `/api/v2/workspace-group-members` | List workspace group member |
| `POST` | `/api/v2/workspace-group-members` | Create workspace group member |
| `GET` | `/api/v2/workspace-group-members/{id}` | Get workspace group member |
| `DELETE` | `/api/v2/workspace-group-members/{id}` | Delete workspace group member |
| `GET` | `/api/v2/workspace-group-members/admin` | Get the current workspace admin workspace |
| `GET` | `/api/v2/workspace-members` | List workspace member |
| `POST` | `/api/v2/workspace-members` | Create workspace member |
| `GET` | `/api/v2/workspace-members/{id}` | Get workspace member |
| `PATCH` | `/api/v2/workspace-members/{id}` | Patch workspace member |
| `DELETE` | `/api/v2/workspace-members/{id}` | Delete workspace member |
| `GET` | `/api/v2/workspaces/current` | Get workspace |
| `PATCH` | `/api/v2/workspaces/current` | Patch workspace |
| `GET` | `/api/v2/workspaces/current/whitelabel-domain` | Get organization verified agency domain information |
| `POST` | `/api/v2/workspaces/current/whitelabel-domain` | Set the agency domain for the workspace |
| `DELETE` | `/api/v2/workspaces/current/whitelabel-domain` | Delete organization agency domain |
| `POST` | `/api/v2/workspaces/current/change-owner` | Change workspace owner |

## Tool Schemas

The following JSON defines every operation with its parameters. Each tool maps
to an API endpoint under the base URL.

```json
[
  {
    "name": "superagnt_connection_instantly_getAccountCampaignMapping",
    "description": "Get campaigns associated with an email",
    "method": "GET",
    "path": "/api/v2/account-campaign-mappings/{email}",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "number",
          "description": "limit"
        },
        "starting_after": {
          "type": "string",
          "description": "starting_after"
        },
        "email": {
          "type": "string",
          "description": "Email"
        }
      },
      "required": [
        "email"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_listAccount",
    "description": "List account",
    "method": "GET",
    "path": "/api/v2/accounts",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "Pagination cursor from `next_starting_after`, in `timestamp_created&email` format. Legacy ISO date-time cursor is still supported."
        },
        "search": {
          "type": "string",
          "description": "search"
        },
        "status": {
          "type": "number",
          "description": "status"
        },
        "provider_code": {
          "type": "number",
          "description": "provider_code"
        },
        "tag_ids": {
          "type": "string",
          "description": "Filter accounts by tag ids. Returns accounts that have any of the specified tags assigned. You can specify multiple tag ids by separating them with a comma."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_createAccount",
    "description": "Create account",
    "method": "POST",
    "path": "/api/v2/accounts",
    "parameters": {
      "type": "object",
      "properties": {
        "email": {
          "type": "string",
          "description": "Email address of the account"
        },
        "first_name": {
          "type": "string",
          "description": "First name associated with the account"
        },
        "last_name": {
          "type": "string",
          "description": "Last name associated with the account"
        },
        "warmup": {
          "type": "object",
          "description": "Warmup configuration for the account"
        },
        "daily_limit": {
          "type": [
            "number",
            "null"
          ],
          "description": "Daily email sending limit"
        },
        "tracking_domain_name": {
          "type": [
            "string",
            "null"
          ],
          "description": "Tracking domain"
        },
        "tracking_domain_status": {
          "type": [
            "string",
            "null"
          ],
          "description": "Tracking domain status"
        },
        "enable_slow_ramp": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to enable slow ramp up for sending limits"
        },
        "inbox_placement_test_limit": {
          "type": [
            "number",
            "null"
          ],
          "description": "The limit for inbox placement tests"
        },
        "provider_code": {
          "type": "number",
          "description": "Provider code for the account. Please make sure to specify the right provider code, otherwise your account will not work."
        },
        "sending_gap": {
          "type": "number",
          "description": "The gap between emails sent from this account in minutes (minimum wait time when used with multiple campaigns)"
        },
        "signature": {
          "type": [
            "string",
            "null"
          ],
          "description": "Email signature for the account"
        },
        "imap_username": {
          "type": "string",
          "description": "imap_username"
        },
        "imap_password": {
          "type": "string",
          "description": "imap_password"
        },
        "imap_host": {
          "type": "string",
          "description": "imap_host"
        },
        "imap_port": {
          "type": "number",
          "description": "imap_port"
        },
        "smtp_username": {
          "type": "string",
          "description": "smtp_username"
        },
        "smtp_password": {
          "type": "string",
          "description": "smtp_password"
        },
        "smtp_host": {
          "type": "string",
          "description": "smtp_host"
        },
        "smtp_port": {
          "type": "number",
          "description": "smtp_port"
        },
        "reply_to": {
          "type": "string",
          "description": "reply_to"
        },
        "warmup_custom_ftag": {
          "type": "string",
          "description": "warmup_custom_ftag"
        },
        "skip_cname_check": {
          "type": "boolean",
          "description": "skip_cname_check"
        }
      },
      "required": [
        "email",
        "first_name",
        "last_name",
        "provider_code",
        "imap_username",
        "imap_password",
        "imap_host",
        "imap_port",
        "smtp_username",
        "smtp_password",
        "smtp_host",
        "smtp_port"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getAccount",
    "description": "Get account",
    "method": "GET",
    "path": "/api/v2/accounts/{email}",
    "parameters": {
      "type": "object",
      "properties": {
        "email": {
          "type": "string",
          "description": "The email of the account to get"
        }
      },
      "required": [
        "email"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_patchAccount",
    "description": "Patch account",
    "method": "PATCH",
    "path": "/api/v2/accounts/{email}",
    "parameters": {
      "type": "object",
      "properties": {
        "email": {
          "type": "string",
          "description": "The email of the account to update"
        },
        "first_name": {
          "type": "string",
          "description": "First name associated with the account"
        },
        "last_name": {
          "type": "string",
          "description": "Last name associated with the account"
        },
        "warmup": {
          "type": "object",
          "description": "Warmup configuration for the account"
        },
        "daily_limit": {
          "type": [
            "number",
            "null"
          ],
          "description": "Daily email sending limit"
        },
        "tracking_domain_name": {
          "type": [
            "string",
            "null"
          ],
          "description": "Tracking domain"
        },
        "tracking_domain_status": {
          "type": [
            "string",
            "null"
          ],
          "description": "Tracking domain status"
        },
        "enable_slow_ramp": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to enable slow ramp up for sending limits"
        },
        "inbox_placement_test_limit": {
          "type": [
            "number",
            "null"
          ],
          "description": "The limit for inbox placement tests"
        },
        "sending_gap": {
          "type": "number",
          "description": "The gap between emails sent from this account in minutes (minimum wait time when used with multiple campaigns)"
        },
        "signature": {
          "type": [
            "string",
            "null"
          ],
          "description": "Email signature for the account"
        },
        "skip_cname_check": {
          "type": "boolean",
          "description": "skip_cname_check"
        },
        "remove_tracking_domain": {
          "type": "boolean",
          "description": "remove_tracking_domain"
        }
      },
      "required": [
        "email"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_deleteAccount",
    "description": "Delete account",
    "method": "DELETE",
    "path": "/api/v2/accounts/{email}",
    "parameters": {
      "type": "object",
      "properties": {
        "email": {
          "type": "string",
          "description": "The email of the account to get"
        }
      },
      "required": [
        "email"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_enableWarmupForAccounts",
    "description": "Enable warmup for accounts",
    "method": "POST",
    "path": "/api/v2/accounts/warmup/enable",
    "parameters": {
      "type": "object",
      "properties": {
        "emails": {
          "type": "array",
          "description": "List of emails to enable warmup accounts for. The emails should be attached to accounts in your workspace."
        },
        "include_all_emails": {
          "type": "boolean",
          "description": "If true, it will enable warmup to all accounts"
        },
        "excluded_emails": {
          "type": "array",
          "description": "List of emails to exclude when `include_all_emails` is `true`."
        },
        "filter": {
          "type": [
            "object",
            "null"
          ],
          "description": "Optional filter to apply when `include_all_emails` is `true`. Can contain tag_id or other filter criteria."
        },
        "search": {
          "type": "string",
          "description": "Optional search query to filter accounts when `include_all_emails` is `true`."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_disableWarmupForAccounts",
    "description": "Disable warmup for accounts",
    "method": "POST",
    "path": "/api/v2/accounts/warmup/disable",
    "parameters": {
      "type": "object",
      "properties": {
        "emails": {
          "type": "array",
          "description": "List of emails to disable warmup accounts for. The emails should be attached to accounts in your workspace."
        },
        "include_all_emails": {
          "type": "boolean",
          "description": "If true, it will disable warmup to all accounts"
        },
        "excluded_emails": {
          "type": "array",
          "description": "List of emails to exclude when `include_all_emails` is `true`."
        },
        "filter": {
          "type": [
            "object",
            "null"
          ],
          "description": "Optional filter to apply when `include_all_emails` is `true`. Can contain tag_id or other filter criteria."
        },
        "search": {
          "type": "string",
          "description": "Optional search query to filter accounts when `include_all_emails` is `true`."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_getWarmupAnalytics",
    "description": "Get warmup analytics",
    "method": "POST",
    "path": "/api/v2/accounts/warmup-analytics",
    "parameters": {
      "type": "object",
      "properties": {
        "emails": {
          "type": "array",
          "description": "List of emails to get warmup analytics for. The emails should be attached to accounts in your workspace."
        }
      },
      "required": [
        "emails"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getDailyAccountAnalytics",
    "description": "Get daily account analytics",
    "method": "GET",
    "path": "/api/v2/accounts/analytics/daily",
    "parameters": {
      "type": "object",
      "properties": {
        "start_date": {
          "type": "string",
          "description": "Start date for the analytics period (optional). If not provided, returns data for the last 30 days."
        },
        "end_date": {
          "type": "string",
          "description": "End date for the analytics period (optional). If not provided, defaults to current date."
        },
        "emails": {
          "type": "array",
          "description": "Filter by specific email accounts (optional). If not provided, returns data for all accounts in your workspace."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_pauseAccount",
    "description": "Pause an account",
    "method": "POST",
    "path": "/api/v2/accounts/{email}/pause",
    "parameters": {
      "type": "object",
      "properties": {
        "email": {
          "type": "string",
          "description": "The email of the account to pause"
        }
      },
      "required": [
        "email"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_resumeAccount",
    "description": "Resume a paused account",
    "method": "POST",
    "path": "/api/v2/accounts/{email}/resume",
    "parameters": {
      "type": "object",
      "properties": {
        "email": {
          "type": "string",
          "description": "Account email"
        }
      },
      "required": [
        "email"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_markAccountFixed",
    "description": "Mark an account as fixed",
    "method": "POST",
    "path": "/api/v2/accounts/{email}/mark-fixed",
    "parameters": {
      "type": "object",
      "properties": {
        "email": {
          "type": "string",
          "description": "Account email"
        }
      },
      "required": [
        "email"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getCtdStatus",
    "description": "Get custom tracking domain status",
    "method": "GET",
    "path": "/api/v2/accounts/ctd/status",
    "parameters": {
      "type": "object",
      "properties": {
        "host": {
          "type": "string",
          "description": "Custom tracking domain host"
        }
      },
      "required": [
        "host"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_testAccountVitals",
    "description": "Test account vitals",
    "method": "POST",
    "path": "/api/v2/accounts/test/vitals",
    "parameters": {
      "type": "object",
      "properties": {
        "accounts": {
          "type": "array",
          "description": "accounts"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_moveAccounts",
    "description": "Move accounts between workspaces",
    "method": "POST",
    "path": "/api/v2/accounts/move",
    "parameters": {
      "type": "object",
      "properties": {
        "emails": {
          "type": "array",
          "description": "Array of email addresses of the accounts to move"
        },
        "source_workspace_id": {
          "type": "string",
          "description": "ID of the source workspace (the workspace that the accounts are currently in)"
        },
        "destination_workspace_id": {
          "type": "string",
          "description": "ID of the destination workspace (the workspace that the accounts will be moved to)"
        }
      },
      "required": [
        "emails",
        "source_workspace_id",
        "destination_workspace_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_listAPIKey",
    "description": "List api key",
    "method": "GET",
    "path": "/api/v2/api-keys",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "The ID of the last item in the previous page - used for pagination. You can use the value of the `next_starting_after` field from the previous response."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_createAPIKey",
    "description": "Create api key",
    "method": "POST",
    "path": "/api/v2/api-keys",
    "parameters": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "name"
        },
        "scopes": {
          "type": "array",
          "description": "scopes"
        }
      },
      "required": [
        "name",
        "scopes"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_deleteAPIKey",
    "description": "Delete api key",
    "method": "DELETE",
    "path": "/api/v2/api-keys/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to delete"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_listAuditLog",
    "description": "List audit log",
    "method": "GET",
    "path": "/api/v2/audit-logs",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "The ID of the last item in the previous page - used for pagination. You can use the value of the `next_starting_after` field from the previous response."
        },
        "activity_type": {
          "type": "number",
          "description": "Filter by activity type"
        },
        "search": {
          "type": "string",
          "description": "Search term to filter logs"
        },
        "start_date": {
          "type": "string",
          "description": "Start date to filter logs"
        },
        "end_date": {
          "type": "string",
          "description": "End date to filter logs"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_listBackgroundJob",
    "description": "List background job",
    "method": "GET",
    "path": "/api/v2/background-jobs",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "starting_after"
        },
        "ids": {
          "type": "string",
          "description": "The ID of the job. Multiple IDs can be provided as a comma-separated list"
        },
        "included_ids": {
          "type": "string",
          "description": "The ID of the job to be included in the response. Multiple IDs can be provided as a comma-separated list"
        },
        "excluded_ids": {
          "type": "string",
          "description": "The ID of the job to be excluded from the response. Multiple IDs can be provided as a comma-separated list"
        },
        "type": {
          "type": "string",
          "description": "The type of the job"
        },
        "entity_type": {
          "type": "string",
          "description": "The type of the entity"
        },
        "entity_id": {
          "type": "string",
          "description": "The ID of the entity. Multiple IDs can be provided as a comma-separated list"
        },
        "status": {
          "type": "string",
          "description": "The status of the job. Multiple statuses can be provided as a comma-separated list. Valid statuses are: pending, in-progress, success, failed"
        },
        "sort_column": {
          "type": "string",
          "description": "The column to sort the results by"
        },
        "sort_order": {
          "type": "string",
          "description": "The order to sort the results by"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_getBackgroundJob",
    "description": "Get background job",
    "method": "GET",
    "path": "/api/v2/background-jobs/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "data_fields": {
          "type": "string",
          "description": "Comma-separated list of fields to include from the `data` object (e.g., \"success_count,failed_count\")."
        },
        "id": {
          "type": "string",
          "description": "The ID of the requested item"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_listBlockListEntry",
    "description": "List block list entry",
    "method": "GET",
    "path": "/api/v2/block-lists-entries",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "The ID of the last item in the previous page - used for pagination. You can use the value of the `next_starting_after` field from the previous response."
        },
        "domains_only": {
          "type": "boolean",
          "description": "Filter by domain"
        },
        "search": {
          "type": "string",
          "description": "Search by value"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_createBlockListEntry",
    "description": "Create block list entry",
    "method": "POST",
    "path": "/api/v2/block-lists-entries",
    "parameters": {
      "type": "object",
      "properties": {
        "bl_value": {
          "type": "string",
          "description": "The email or domain to block"
        }
      },
      "required": [
        "bl_value"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_deleteallBlockListEntry",
    "description": "Delete all block list entries",
    "method": "DELETE",
    "path": "/api/v2/block-lists-entries",
    "parameters": {
      "type": "object",
      "properties": {
        "domains_only": {
          "type": "boolean",
          "description": "Filter by domain"
        },
        "search": {
          "type": "string",
          "description": "Search by value"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_getBlockListEntry",
    "description": "Get block list entry",
    "method": "GET",
    "path": "/api/v2/block-lists-entries/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the requested item"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_patchBlockListEntry",
    "description": "Patch block list entry",
    "method": "PATCH",
    "path": "/api/v2/block-lists-entries/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to update"
        },
        "bl_value": {
          "type": "string",
          "description": "The email or domain to block"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_deleteBlockListEntry",
    "description": "Delete block list entry",
    "method": "DELETE",
    "path": "/api/v2/block-lists-entries/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to delete"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_createblukBlockListEntry",
    "description": "Bulk create block list entry",
    "method": "POST",
    "path": "/api/v2/block-lists-entries/bulk-create",
    "parameters": {
      "type": "object",
      "properties": {
        "bl_values": {
          "type": "array",
          "description": "List of domains or emails to block"
        }
      },
      "required": [
        "bl_values"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_deletebulkBlockListEntry",
    "description": "Bulk delete block list entry",
    "method": "POST",
    "path": "/api/v2/block-lists-entries/bulk-delete",
    "parameters": {
      "type": "object",
      "properties": {
        "ids": {
          "type": "array",
          "description": "List block list entry ids to delete"
        }
      },
      "required": [
        "ids"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_downloadBlockListEntry",
    "description": "Download all block list entries as CSV",
    "method": "GET",
    "path": "/api/v2/block-lists-entries/download",
    "parameters": {
      "type": "object",
      "properties": {
        "domains_only": {
          "type": "boolean",
          "description": "Filter by domain"
        },
        "search": {
          "type": "string",
          "description": "Search by value"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_listCampaign",
    "description": "List campaign",
    "method": "GET",
    "path": "/api/v2/campaigns",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "The ID of the last item in the previous page - used for pagination. You can use the value of the `next_starting_after` field from the previous response."
        },
        "search": {
          "type": "string",
          "description": "Search by campaign name"
        },
        "tag_ids": {
          "type": "string",
          "description": "Filter campaigns by tag ids. Returns campaigns that have any of the specified tags assigned. You can specify multiple tag ids by separating them with a comma."
        },
        "ai_sales_agent_id": {
          "type": "string",
          "description": "Filter campaigns by AI Sales Agent ID. Returns campaigns that were created by the specified AI Sales Agent."
        },
        "status": {
          "type": "number",
          "description": "Filter campaigns by status using the campaign status enum value (e.g., ACTIVE, PAUSED)."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_createCampaign",
    "description": "Create campaign",
    "method": "POST",
    "path": "/api/v2/campaigns",
    "parameters": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "Name of the campaign"
        },
        "pl_value": {
          "type": [
            "number",
            "null"
          ],
          "description": "Value of every positive lead"
        },
        "is_evergreen": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether the campaign is evergreen"
        },
        "campaign_schedule": {
          "type": "object",
          "description": "Campaign schedule"
        },
        "sequences": {
          "type": "array",
          "description": "List of sequences (the actual email copy). Even though this field is an array, only the first element is used, so please provide only one array item, and add the steps to that array"
        },
        "email_gap": {
          "type": [
            "number",
            "null"
          ],
          "description": "The gap between emails in minutes"
        },
        "random_wait_max": {
          "type": [
            "number",
            "null"
          ],
          "description": "The maximum random wait time in minutes"
        },
        "text_only": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether the campaign is text only"
        },
        "first_email_text_only": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether the campaign is send the first email as a text only"
        },
        "email_list": {
          "type": "array",
          "description": "List of accounts to use for sending emails"
        },
        "daily_limit": {
          "type": [
            "number",
            "null"
          ],
          "description": "The daily limit for sending emails"
        },
        "stop_on_reply": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to stop the campaign on reply"
        },
        "email_tag_list": {
          "type": "array",
          "description": "List of tags to use for sending emails"
        },
        "link_tracking": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to track links in emails"
        },
        "open_tracking": {
          "type": "boolean",
          "description": "Whether to track opens in emails"
        },
        "stop_on_auto_reply": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to stop the campaign on auto reply"
        },
        "daily_max_leads": {
          "type": [
            "number",
            "null"
          ],
          "description": "The daily maximum new leads to contact"
        },
        "prioritize_new_leads": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to prioritize new leads"
        },
        "auto_variant_select": {
          "type": [
            "object",
            "null"
          ],
          "description": "Auto variant select settings"
        },
        "match_lead_esp": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to match leads by ESP"
        },
        "stop_for_company": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to stop the campaign for the entire company(domain) when a lead replies"
        },
        "insert_unsubscribe_header": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to insert an unsubscribe header in emails"
        },
        "allow_risky_contacts": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to allow risky contacts"
        },
        "disable_bounce_protect": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to disable bounce protection"
        },
        "limit_emails_per_company_override": {
          "type": [
            "object",
            "null"
          ],
          "description": "Overrides the workspace-wide limit emails per company setting for this campaign."
        },
        "cc_list": {
          "type": "array",
          "description": "List of accounts to CC on emails"
        },
        "bcc_list": {
          "type": "array",
          "description": "List of accounts to BCC on emails"
        },
        "owned_by": {
          "type": [
            "string",
            "null"
          ],
          "description": "Owner ID"
        },
        "ai_sdr_id": {
          "type": [
            "string",
            "null"
          ],
          "description": "AI Sales Agent ID that created this campaign"
        },
        "provider_routing_rules": {
          "type": "array",
          "description": "Auto variant select settings"
        }
      },
      "required": [
        "name",
        "campaign_schedule"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_activateCampaign",
    "description": "Activate(start), or resume a campaign",
    "method": "POST",
    "path": "/api/v2/campaigns/{id}/activate",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Campaign ID"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_pauseCampaign",
    "description": "Stop(or pause) a campaign",
    "method": "POST",
    "path": "/api/v2/campaigns/{id}/pause",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Campaign ID"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getCampaign",
    "description": "Get campaign",
    "method": "GET",
    "path": "/api/v2/campaigns/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the requested item"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_patchCampaign",
    "description": "Patch campaign",
    "method": "PATCH",
    "path": "/api/v2/campaigns/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to update"
        },
        "name": {
          "type": "string",
          "description": "Name of the campaign"
        },
        "pl_value": {
          "type": [
            "number",
            "null"
          ],
          "description": "Value of every positive lead"
        },
        "is_evergreen": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether the campaign is evergreen"
        },
        "campaign_schedule": {
          "type": "object",
          "description": "Campaign schedule"
        },
        "sequences": {
          "type": "array",
          "description": "List of sequences (the actual email copy). Even though this field is an array, only the first element is used, so please provide only one array item, and add the steps to that array"
        },
        "email_gap": {
          "type": [
            "number",
            "null"
          ],
          "description": "The gap between emails in minutes"
        },
        "random_wait_max": {
          "type": [
            "number",
            "null"
          ],
          "description": "The maximum random wait time in minutes"
        },
        "text_only": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether the campaign is text only"
        },
        "first_email_text_only": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether the campaign is send the first email as a text only"
        },
        "email_list": {
          "type": "array",
          "description": "List of accounts to use for sending emails"
        },
        "daily_limit": {
          "type": [
            "number",
            "null"
          ],
          "description": "The daily limit for sending emails"
        },
        "stop_on_reply": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to stop the campaign on reply"
        },
        "email_tag_list": {
          "type": "array",
          "description": "List of tags to use for sending emails"
        },
        "link_tracking": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to track links in emails"
        },
        "open_tracking": {
          "type": "boolean",
          "description": "Whether to track opens in emails"
        },
        "stop_on_auto_reply": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to stop the campaign on auto reply"
        },
        "daily_max_leads": {
          "type": [
            "number",
            "null"
          ],
          "description": "The daily maximum new leads to contact"
        },
        "prioritize_new_leads": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to prioritize new leads"
        },
        "auto_variant_select": {
          "type": [
            "object",
            "null"
          ],
          "description": "Auto variant select settings"
        },
        "match_lead_esp": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to match leads by ESP"
        },
        "stop_for_company": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to stop the campaign for the entire company(domain) when a lead replies"
        },
        "insert_unsubscribe_header": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to insert an unsubscribe header in emails"
        },
        "allow_risky_contacts": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to allow risky contacts"
        },
        "disable_bounce_protect": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether to disable bounce protection"
        },
        "limit_emails_per_company_override": {
          "type": [
            "object",
            "null"
          ],
          "description": "Overrides the workspace-wide limit emails per company setting for this campaign."
        },
        "cc_list": {
          "type": "array",
          "description": "List of accounts to CC on emails"
        },
        "bcc_list": {
          "type": "array",
          "description": "List of accounts to BCC on emails"
        },
        "owned_by": {
          "type": [
            "string",
            "null"
          ],
          "description": "Owner ID"
        },
        "provider_routing_rules": {
          "type": "array",
          "description": "Auto variant select settings"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_deleteCampaign",
    "description": "Delete campaign",
    "method": "DELETE",
    "path": "/api/v2/campaigns/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to delete"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_searchByContact",
    "description": "Search campaigns by lead email",
    "method": "GET",
    "path": "/api/v2/campaigns/search-by-contact",
    "parameters": {
      "type": "object",
      "properties": {
        "search": {
          "type": "string",
          "description": "Search by lead email"
        },
        "sort_column": {
          "type": "string",
          "description": "Sort campaigns by column name"
        },
        "sort_order": {
          "type": "string",
          "description": "Sort direction"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_getCampaignAnalytics",
    "description": "Get campaign(s) analytics",
    "method": "GET",
    "path": "/api/v2/campaigns/analytics",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "A campaign ID to get the analytics for. Leave this field empty to get the analytics for all campaigns"
        },
        "ids": {
          "type": "array",
          "description": "ids"
        },
        "start_date": {
          "type": "string",
          "description": "Start date"
        },
        "end_date": {
          "type": "string",
          "description": "End date"
        },
        "exclude_total_leads_count": {
          "type": "boolean",
          "description": "Exclude the total leads from the result. Setting this to true will considerably decrease the response time"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_getCampaignAnalyticsOverview",
    "description": "Get campaign(s) analytics overview",
    "method": "GET",
    "path": "/api/v2/campaigns/analytics/overview",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "A campaign ID to get the analytics overview for. Leave this field empty to get the analytics overview for all campaigns"
        },
        "ids": {
          "type": "array",
          "description": "ids"
        },
        "start_date": {
          "type": "string",
          "description": "Start date"
        },
        "end_date": {
          "type": "string",
          "description": "End date"
        },
        "campaign_status": {
          "type": "number",
          "description": "Filter by campaign status (only the analytics for the campaigns with the specified status will be returned)"
        },
        "expand_crm_events": {
          "type": "boolean",
          "description": "When `true`, calculates the total of all the lead interest status update events instead of only the first occurrence for each contact. This will affect the following fields: `total_opportunities`, `total_interested`, `total_meeting_booked`, `total_meeting_completed`, and `total_closed`. Example: if a lead goes from interested to meeting booked to closed, it will count as 3 events (total_interested: 1, total_meeting_booked_1, and total_closed: 1) when this parameter is set to true, and as 1 event (total_interested) when it is set to false (default)."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_getDailyCampaignAnalytics",
    "description": "Get daily campaign analytics",
    "method": "GET",
    "path": "/api/v2/campaigns/analytics/daily",
    "parameters": {
      "type": "object",
      "properties": {
        "campaign_id": {
          "type": "string",
          "description": "Campaign ID (optional). Leave this field empty to get the analytics for all campaigns"
        },
        "start_date": {
          "type": "string",
          "description": "Start date"
        },
        "end_date": {
          "type": "string",
          "description": "End date"
        },
        "campaign_status": {
          "type": "number",
          "description": "Filter by campaign status (only the analytics for the campaigns with the specified status will be returned)"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_getCampaignStepsAnalytics",
    "description": "Get campaign steps analytics",
    "method": "GET",
    "path": "/api/v2/campaigns/analytics/steps",
    "parameters": {
      "type": "object",
      "properties": {
        "campaign_id": {
          "type": "string",
          "description": "Campaign ID (optional). Leave this field empty to get the analytics for all campaigns"
        },
        "start_date": {
          "type": "string",
          "description": "Start date"
        },
        "end_date": {
          "type": "string",
          "description": "End date"
        },
        "include_opportunities_count": {
          "type": "boolean",
          "description": "Whether to include the opportunities count per step. If this field is true then `opportunities` and `unique_opportunities` fields will be included in the response"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_shareCampaign",
    "description": "Share a campaign",
    "method": "POST",
    "path": "/api/v2/campaigns/{id}/share",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Campaign ID"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_createFromExport",
    "description": "Create campaign from shared one",
    "method": "POST",
    "path": "/api/v2/campaigns/{id}/from-export",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Campaign ID"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_exportCampaign",
    "description": "Export campaign to JSON format",
    "method": "POST",
    "path": "/api/v2/campaigns/{id}/export",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Campaign ID"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_duplicate",
    "description": "Duplicate campaign",
    "method": "POST",
    "path": "/api/v2/campaigns/{id}/duplicate",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Campaign ID"
        },
        "name": {
          "type": "string",
          "description": "Campaign new name (optional). If not provided, it will default to CAMPAIGN NAME (copy)."
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_countLaunched",
    "description": "Get launched campaigns count",
    "method": "GET",
    "path": "/api/v2/campaigns/count-launched",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_instantly_addVariables",
    "description": "Add campaign variables",
    "method": "POST",
    "path": "/api/v2/campaigns/{id}/variables",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Campaign ID"
        },
        "variables": {
          "type": "array",
          "description": "variables"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getCampaignSendingStatus",
    "description": "Get campaign sending status",
    "method": "GET",
    "path": "/api/v2/campaigns/{id}/sending-status",
    "parameters": {
      "type": "object",
      "properties": {
        "with_ai_summary": {
          "type": "boolean",
          "description": "Include AI-generated summary"
        },
        "id": {
          "type": "string",
          "description": "Campaign ID"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_listPhoneNumbers",
    "description": "List phone numbers",
    "method": "GET",
    "path": "/api/v2/crm-actions/phone-numbers",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_instantly_deletePhoneNumber",
    "description": "Delete phone number",
    "method": "DELETE",
    "path": "/api/v2/crm-actions/phone-numbers/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The phone number record id to delete"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_listCustomTagMapping",
    "description": "List custom tag mapping",
    "method": "GET",
    "path": "/api/v2/custom-tag-mappings",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "The ID of the last item in the previous page - used for pagination. You can use the value of the `next_starting_after` field from the previous response."
        },
        "resource_ids": {
          "type": "string",
          "description": "The list of resource ids to filter custom tag mappings by. A resource id is the id of an account or a campaign."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_listCustomTag",
    "description": "List custom tag",
    "method": "GET",
    "path": "/api/v2/custom-tags",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "The ID of the last item in the previous page - used for pagination. You can use the value of the `next_starting_after` field from the previous response."
        },
        "search": {
          "type": "string",
          "description": "The search query to filter custom tags."
        },
        "resource_ids": {
          "type": "string",
          "description": "The list of resource ids to filter custom tags by. A resource id is the id of an account or a campaign."
        },
        "tag_ids": {
          "type": "string",
          "description": "The list of tag ids to filter custom tags by."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_createCustomTag",
    "description": "Create custom tag",
    "method": "POST",
    "path": "/api/v2/custom-tags",
    "parameters": {
      "type": "object",
      "properties": {
        "label": {
          "type": "string",
          "description": "Display label for the custom tag"
        },
        "description": {
          "type": [
            "string",
            "null"
          ],
          "description": "Detailed description of the custom tag purpose"
        }
      },
      "required": [
        "label"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getCustomTag",
    "description": "Get custom tag",
    "method": "GET",
    "path": "/api/v2/custom-tags/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the requested item"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_patchCustomTag",
    "description": "Patch custom tag",
    "method": "PATCH",
    "path": "/api/v2/custom-tags/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to update"
        },
        "label": {
          "type": "string",
          "description": "Display label for the custom tag"
        },
        "description": {
          "type": [
            "string",
            "null"
          ],
          "description": "Detailed description of the custom tag purpose"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_deleteCustomTag",
    "description": "Delete custom tag",
    "method": "DELETE",
    "path": "/api/v2/custom-tags/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to delete"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_toggleTagResource",
    "description": "Assign or unassign tags to resources",
    "method": "POST",
    "path": "/api/v2/custom-tags/toggle-resource",
    "parameters": {
      "type": "object",
      "properties": {
        "tag_ids": {
          "type": "array",
          "description": "The list of tag ids to assign or unassign"
        },
        "resource_type": {
          "type": "number",
          "description": "The resource type to assign or unassign the tags to"
        },
        "resource_ids": {
          "type": "array",
          "description": "The list of resource ids to assign or unassign. A resource id is the id of an account or a campaign."
        },
        "assign": {
          "type": "boolean",
          "description": "Whether to assign the tags to the resources."
        },
        "selected_all": {
          "type": "boolean",
          "description": "Whether to select all resources."
        },
        "filter": {
          "type": "object",
          "description": "The filter to apply to the resources. These are only used when `selected_all` is true."
        }
      },
      "required": [
        "tag_ids",
        "resource_type",
        "resource_ids",
        "assign"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_listDFYEmailAccountOrder",
    "description": "List dfy email account order",
    "method": "GET",
    "path": "/api/v2/dfy-email-account-orders",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "The ID of the last item in the previous page - used for pagination. You can use the value of the `next_starting_after` field from the previous response."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_createDFYEmailAccountOrder",
    "description": "Place a DFY email account order",
    "method": "POST",
    "path": "/api/v2/dfy-email-account-orders",
    "parameters": {
      "type": "object",
      "properties": {
        "items": {
          "type": "array",
          "description": "List of domains and accounts to order"
        },
        "order_type": {
          "type": "string",
          "description": "The type of order to place. Please check the docs because this endpoint performs different actions based on the order type."
        },
        "simulation": {
          "type": "boolean",
          "description": "Whether to run a simulation of the order ot not. If set to true, the order will NOT be placed, your card will NOT be charged, and only a price quote will be returned. We will still check the validity of the order and the accounts, and return the results of the validation (if the order_is_valid field is true, then the order would be valid and could be placed)."
        }
      },
      "required": [
        "items",
        "order_type"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_generateSimilarDomains",
    "description": "Generate similar available domains",
    "method": "POST",
    "path": "/api/v2/dfy-email-account-orders/domains/similar",
    "parameters": {
      "type": "object",
      "properties": {
        "domain": {
          "type": "string",
          "description": "The domain to base the suggestions on"
        },
        "tlds": {
          "type": "array",
          "description": "The extensions (tlds) to use for generating similar domains. By default, we will use com and org."
        }
      },
      "required": [
        "domain"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_checkDomainsAvailability",
    "description": "Check domains availability",
    "method": "POST",
    "path": "/api/v2/dfy-email-account-orders/domains/check",
    "parameters": {
      "type": "object",
      "properties": {
        "domains": {
          "type": "array",
          "description": "List of domains to check"
        }
      },
      "required": [
        "domains"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_preWarmedUpDomainsList",
    "description": "Get pre-warmed up domains",
    "method": "POST",
    "path": "/api/v2/dfy-email-account-orders/domains/pre-warmed-up-list",
    "parameters": {
      "type": "object",
      "properties": {
        "extensions": {
          "type": "array",
          "description": "A list of domain extensions to filter the results by. If not provided, all available extensions will be returned."
        },
        "search": {
          "type": "string",
          "description": "A search string to filter the domains by. This can be a partial or full domain name."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_list_dfy_accounts",
    "description": "List DFY ordered email accounts",
    "method": "GET",
    "path": "/api/v2/dfy-email-account-orders/accounts",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "The ID of the last item in the previous page - used for pagination. You can use the value of the `next_starting_after` field from the previous response."
        },
        "with_passwords": {
          "type": "boolean",
          "description": "Whether to include passwords in the response"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_cancelDFYEmailAccounts",
    "description": "Cancel dfy email accounts",
    "method": "POST",
    "path": "/api/v2/dfy-email-account-orders/accounts/cancel",
    "parameters": {
      "type": "object",
      "properties": {
        "accounts": {
          "type": "array",
          "description": "List of emails to cancel the DFY email accounts for."
        }
      },
      "required": [
        "accounts"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_sendTestEmail",
    "description": "Send a test email",
    "method": "POST",
    "path": "/api/v2/emails/test",
    "parameters": {
      "type": "object",
      "properties": {
        "eaccount": {
          "type": "string",
          "description": "The email account that will be used to send this email. It has to be an email account connected to your workspace."
        },
        "to_address_email_list": {
          "type": "string",
          "description": "Comma-separated list of recipients that will receive the test email."
        },
        "subject": {
          "type": "string",
          "description": "Subject line of the test email."
        },
        "body": {
          "type": "object",
          "description": "HTML body of the test email."
        }
      },
      "required": [
        "eaccount",
        "to_address_email_list",
        "subject",
        "body"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_replyToEmail",
    "description": "Reply to an email",
    "method": "POST",
    "path": "/api/v2/emails/reply",
    "parameters": {
      "type": "object",
      "properties": {
        "eaccount": {
          "type": "string",
          "description": "The email account that will be used to send this email. It has to be an email account connected to your workspace"
        },
        "reply_to_uuid": {
          "type": "string",
          "description": "The id of the email to reply to"
        },
        "subject": {
          "type": "string",
          "description": "Subject line of the email message"
        },
        "body": {
          "type": "object",
          "description": "The email body. You can specify either the `html` or the `text` field, or both"
        },
        "cc_address_email_list": {
          "type": "string",
          "description": "Comma-separated list of CC email addresses"
        },
        "bcc_address_email_list": {
          "type": "string",
          "description": "Comma-separated list of BCC email addresses"
        },
        "reminder_ts": {
          "type": "string",
          "description": "If provided then a reminder will be attached to this email, you will see this reminder in the Unibox in the web app"
        },
        "assigned_to": {
          "type": "string",
          "description": "The user id assigned to the lead"
        }
      },
      "required": [
        "reply_to_uuid",
        "eaccount",
        "subject",
        "body"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_forwardEmail",
    "description": "Forward an email",
    "method": "POST",
    "path": "/api/v2/emails/forward",
    "parameters": {
      "type": "object",
      "properties": {
        "eaccount": {
          "type": "string",
          "description": "The email account that will be used to send this email. It has to be an email account connected to your workspace"
        },
        "reply_to_uuid": {
          "type": "string",
          "description": "The id of the email you want to forward"
        },
        "to_address_email_list": {
          "type": "string",
          "description": "Comma-separated list of recipients that will receive the forwarded email"
        },
        "subject": {
          "type": "string",
          "description": "Subject line of the forwarded email message"
        },
        "body": {
          "type": "object",
          "description": "The email body. You can specify either the `html` or the `text` field, or both"
        },
        "cc_address_email_list": {
          "type": "string",
          "description": "Comma-separated list of CC email addresses"
        },
        "bcc_address_email_list": {
          "type": "string",
          "description": "Comma-separated list of BCC email addresses"
        },
        "reply_to": {
          "type": "string",
          "description": "Reply-to email address that recipients should use when replying"
        },
        "forwarded_attachments": {
          "type": "string",
          "description": "JSON-encoded forwarded attachment metadata from the original email"
        },
        "assigned_to": {
          "type": "string",
          "description": "The user id assigned to the lead"
        }
      },
      "required": [
        "reply_to_uuid",
        "to_address_email_list",
        "eaccount",
        "subject",
        "body"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_listEmail",
    "description": "List email",
    "method": "GET",
    "path": "/api/v2/emails",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "The ID of the last item in the previous page - used for pagination. You can use the value of the `next_starting_after` field from the previous response."
        },
        "search": {
          "type": "string",
          "description": "The search query to filter emails. It can be an email address (the lead email address), or a special string that starts with \"thread:\" to search for emails in a specific thread. If you want to search for emails in a specific thread, use the \"thread:\" prefix followed by the thread ID (e.g., \"thread:123e4567-e89b-12d3-a456-426614174000\")."
        },
        "campaign_id": {
          "type": "string",
          "description": "The ID of the campaign to filter emails by."
        },
        "list_id": {
          "type": "string",
          "description": "The ID of the lead list to filter emails by."
        },
        "i_status": {
          "type": "number",
          "description": "The status of the emails to filter by."
        },
        "eaccount": {
          "type": "string",
          "description": "The email account that was used to send this email. You can filter by multiple email accounts by providing a comma-separated list of email addresses."
        },
        "is_unread": {
          "type": "boolean",
          "description": "Whether the email is unread."
        },
        "has_reminder": {
          "type": "boolean",
          "description": "has_reminder"
        },
        "mode": {
          "type": "string",
          "description": "The mode to filter emails by."
        },
        "preview_only": {
          "type": "boolean",
          "description": "Whether to only return the preview of the emails."
        },
        "sort_order": {
          "type": "string",
          "description": "The order to sort the emails by (based on the email creation date). Default is \"desc\"."
        },
        "scheduled_only": {
          "type": "boolean",
          "description": "Whether to only return the scheduled emails."
        },
        "assigned_to": {
          "type": "string",
          "description": "The ID of the user to filter emails by."
        },
        "lead": {
          "type": "string",
          "description": "The email of the lead to filter emails by."
        },
        "company_domain": {
          "type": "string",
          "description": "The domain of the company to filter emails by."
        },
        "marked_as_done": {
          "type": "boolean",
          "description": "Whether the email is marked as done."
        },
        "email_type": {
          "type": "string",
          "description": "The type of the email to filter by."
        },
        "min_timestamp_created": {
          "type": "string",
          "description": "Filter emails created after this timestamp (ISO format)"
        },
        "max_timestamp_created": {
          "type": "string",
          "description": "Filter emails created before this timestamp (ISO format)"
        },
        "latest_of_thread": {
          "type": "boolean",
          "description": "Whether to only return the latest email in each thread."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_getEmail",
    "description": "Get email",
    "method": "GET",
    "path": "/api/v2/emails/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the requested item"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_patchEmail",
    "description": "Patch email",
    "method": "PATCH",
    "path": "/api/v2/emails/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to update"
        },
        "is_unread": {
          "type": [
            "number",
            "null"
          ],
          "description": "Indicates if the email is unread"
        },
        "reminder_ts": {
          "type": [
            "string",
            "null"
          ],
          "description": "Timestamp for the reminder."
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_deleteEmail",
    "description": "Delete email",
    "method": "DELETE",
    "path": "/api/v2/emails/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to delete"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_countUnreadEmails",
    "description": "Count unread emails",
    "method": "GET",
    "path": "/api/v2/emails/unread/count",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_instantly_markThreadAsRead",
    "description": "Mark all emails in a thread as read",
    "method": "POST",
    "path": "/api/v2/emails/threads/{thread_id}/mark-as-read",
    "parameters": {
      "type": "object",
      "properties": {
        "thread_id": {
          "type": "string",
          "description": "thread_id"
        }
      },
      "required": [
        "thread_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_listInboxPlacementAnalytics",
    "description": "List inbox placement analytics",
    "method": "GET",
    "path": "/api/v2/inbox-placement-analytics",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "The ID of the last item in the previous page - used for pagination. You can use the value of the `next_starting_after` field from the previous response."
        },
        "test_id": {
          "type": "string",
          "description": "test_id"
        },
        "date_from": {
          "type": "string",
          "description": "date_from"
        },
        "date_to": {
          "type": "string",
          "description": "date_to"
        },
        "recipient_geo": {
          "type": "string",
          "description": "A comma-separated list of recipient geo values."
        },
        "recipient_type": {
          "type": "string",
          "description": "A comma-separated list of recipient type values."
        },
        "recipient_esp": {
          "type": "string",
          "description": "A comma-separated list of recipient ESP values."
        },
        "sender_email": {
          "type": "string",
          "description": "sender_email"
        }
      },
      "required": [
        "test_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getInboxPlacementAnalytics",
    "description": "Get inbox placement analytics",
    "method": "GET",
    "path": "/api/v2/inbox-placement-analytics/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the requested item"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_inbox_stats_by_test_id",
    "description": "Retrieve inbox placement analytics stats by test id",
    "method": "POST",
    "path": "/api/v2/inbox-placement-analytics/stats-by-test-id",
    "parameters": {
      "type": "object",
      "properties": {
        "test_ids": {
          "type": "array",
          "description": "test_ids"
        },
        "date_from": {
          "type": "string",
          "description": "date_from"
        },
        "date_to": {
          "type": "string",
          "description": "date_to"
        },
        "recipient_geo": {
          "type": "array",
          "description": "recipient_geo"
        },
        "recipient_type": {
          "type": "array",
          "description": "recipient_type"
        },
        "recipient_esp": {
          "type": "array",
          "description": "recipient_esp"
        },
        "sender_email": {
          "type": "string",
          "description": "sender_email"
        }
      },
      "required": [
        "test_ids"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_inbox_deliverability",
    "description": "Retrieve inbox placement analytics deliverability insights",
    "method": "POST",
    "path": "/api/v2/inbox-placement-analytics/deliverability-insights",
    "parameters": {
      "type": "object",
      "properties": {
        "test_id": {
          "type": "string",
          "description": "test_id"
        },
        "date_from": {
          "type": "string",
          "description": "date_from"
        },
        "date_to": {
          "type": "string",
          "description": "date_to"
        },
        "previous_date_from": {
          "type": "string",
          "description": "previous_date_from"
        },
        "previous_date_to": {
          "type": "string",
          "description": "previous_date_to"
        },
        "show_previous": {
          "type": "boolean",
          "description": "show_previous"
        },
        "recipient_geo": {
          "type": "array",
          "description": "recipient_geo"
        },
        "recipient_type": {
          "type": "array",
          "description": "recipient_type"
        },
        "recipient_esp": {
          "type": "array",
          "description": "recipient_esp"
        }
      },
      "required": [
        "test_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_inbox_stats_by_date",
    "description": "Get inbox placement analytics stats by date",
    "method": "POST",
    "path": "/api/v2/inbox-placement-analytics/stats-by-date",
    "parameters": {
      "type": "object",
      "properties": {
        "test_id": {
          "type": "string",
          "description": "test_id"
        },
        "date_from": {
          "type": "string",
          "description": "date_from"
        },
        "date_to": {
          "type": "string",
          "description": "date_to"
        },
        "recipient_geo": {
          "type": "array",
          "description": "recipient_geo"
        },
        "recipient_type": {
          "type": "array",
          "description": "recipient_type"
        },
        "recipient_esp": {
          "type": "array",
          "description": "recipient_esp"
        },
        "sender_email": {
          "type": "string",
          "description": "sender_email"
        }
      },
      "required": [
        "test_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_list_inbox_reports",
    "description": "List inbox placement blacklist & spamassassin report",
    "method": "GET",
    "path": "/api/v2/inbox-placement-reports",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "The ID of the last item in the previous page - used for pagination. You can use the value of the `next_starting_after` field from the previous response."
        },
        "test_id": {
          "type": "string",
          "description": "test_id"
        },
        "date_from": {
          "type": "string",
          "description": "date_from"
        },
        "date_to": {
          "type": "string",
          "description": "date_to"
        },
        "skip_spam_assassin_report": {
          "type": "boolean",
          "description": "Flag to skip including spam_assassin_report JSON"
        },
        "skip_blacklist_report": {
          "type": "boolean",
          "description": "Flag to skip including blacklist_report JSON"
        }
      },
      "required": [
        "test_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_get_inbox_report",
    "description": "Get inbox placement blacklist & spamassassin report",
    "method": "GET",
    "path": "/api/v2/inbox-placement-reports/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the requested item"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_listInboxPlacementTest",
    "description": "List inbox placement test",
    "method": "GET",
    "path": "/api/v2/inbox-placement-tests",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "The ID of the last item in the previous page - used for pagination. You can use the value of the `next_starting_after` field from the previous response."
        },
        "search": {
          "type": "string",
          "description": "search"
        },
        "status": {
          "type": "number",
          "description": "status"
        },
        "sort_order": {
          "type": "string",
          "description": "Sort order for the results. Results are always sorted by id (which is timestamp-sorted due to UUIDv7)."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_createInboxPlacementTest",
    "description": "Create inbox placement test",
    "method": "POST",
    "path": "/api/v2/inbox-placement-tests",
    "parameters": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "Name of the inbox placement test"
        },
        "delivery_mode": {
          "type": [
            "null",
            "number"
          ],
          "description": "Whether to send emails one by one or all together"
        },
        "description": {
          "type": [
            "string",
            "null"
          ],
          "description": "Description of the inbox placement test"
        },
        "schedule": {
          "type": "object",
          "description": "Specifies the date and time when the automated inbox placement tests will be sent."
        },
        "type": {
          "type": "number",
          "description": "Whether the inbox placement test is a one-time test or an automated test"
        },
        "sending_method": {
          "type": "number",
          "description": "Whether the inbox placement test will be sent from Instantly or from outside Instantly"
        },
        "campaign_id": {
          "type": [
            "null",
            "string"
          ],
          "description": "Campaign ID"
        },
        "email_subject": {
          "type": "string",
          "description": "Email subject of the inbox placement test"
        },
        "email_body": {
          "type": "string",
          "description": "Email body of the inbox placement test"
        },
        "emails": {
          "type": "array",
          "description": "Emails to send the inbox placement test to"
        },
        "test_code": {
          "type": [
            "string",
            "null"
          ],
          "description": "Code for identifying the inbox placement tests in the email body from outside Instantly"
        },
        "tags": {
          "type": [
            "array",
            "null"
          ],
          "description": "List of tag IDs to use for sending emails"
        },
        "text_only": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Disables open tracking"
        },
        "recipients_labels": {
          "type": "array",
          "description": "A list of email providers and their corresponding types to which emails will be sent. To retrieve the available options, use the `GET: /inbox-placement-tests/email-service-provider-options` endpoint"
        },
        "timestamp_next_run": {
          "type": [
            "string",
            "null"
          ],
          "description": "Timestamp when the inbox placement test will run next"
        },
        "automations": {
          "type": [
            "null",
            "array"
          ],
          "description": "Optional automations to trigger based on conditions"
        },
        "status": {
          "type": [
            "number",
            "null"
          ],
          "description": "Status of the inbox placement test"
        },
        "not_sending_status": {
          "type": [
            "string",
            "null"
          ],
          "description": "Why the inbox placement test is currently not sending. It will be an empty string if there are no issues."
        },
        "run_immediately": {
          "type": "boolean",
          "description": "Run the test immediately after creation, as well as on the schedule"
        }
      },
      "required": [
        "name",
        "type",
        "sending_method",
        "email_subject",
        "email_body",
        "emails"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getInboxPlacementTest",
    "description": "Get inbox placement test",
    "method": "GET",
    "path": "/api/v2/inbox-placement-tests/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "with_metadata": {
          "type": "boolean",
          "description": "Whether to include additional metadata about the inbox placement test"
        },
        "id": {
          "type": "string",
          "description": "The ID of the requested item"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_patchInboxPlacementTest",
    "description": "Patch inbox placement test",
    "method": "PATCH",
    "path": "/api/v2/inbox-placement-tests/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to update"
        },
        "name": {
          "type": "string",
          "description": "Name of the inbox placement test"
        },
        "schedule": {
          "type": "object",
          "description": "Specifies the date and time when the automated inbox placement tests will be sent."
        },
        "automations": {
          "type": [
            "null",
            "array"
          ],
          "description": "Optional automations to trigger based on conditions"
        },
        "status": {
          "type": [
            "number",
            "null"
          ],
          "description": "Status of the inbox placement test"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_deleteInboxPlacementTest",
    "description": "Delete inbox placement test",
    "method": "DELETE",
    "path": "/api/v2/inbox-placement-tests/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to delete"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_inbox_test_esp_options",
    "description": "Get ESP options",
    "method": "GET",
    "path": "/api/v2/inbox-placement-tests/email-service-provider-options",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_instantly_listLeadLabel",
    "description": "List lead label",
    "method": "GET",
    "path": "/api/v2/lead-labels",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "The starting after timestamp to filter lead labels by."
        },
        "search": {
          "type": "string",
          "description": "The search query to filter lead labels."
        },
        "interest_status": {
          "type": "string",
          "description": "The interest status to filter lead labels by."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_createLeadLabel",
    "description": "Create lead label",
    "method": "POST",
    "path": "/api/v2/lead-labels",
    "parameters": {
      "type": "object",
      "properties": {
        "label": {
          "type": "string",
          "description": "Display label for the custom lead label"
        },
        "interest_status_label": {
          "type": "string",
          "description": "Interest status label associated with this label"
        },
        "description": {
          "type": [
            "string",
            "null"
          ],
          "description": "Detailed description of the custom lead label purpose"
        },
        "use_with_ai": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether this label should be used with AI features"
        }
      },
      "required": [
        "label",
        "interest_status_label"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getLeadLabel",
    "description": "Get lead label",
    "method": "GET",
    "path": "/api/v2/lead-labels/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the requested item"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_patchLeadLabel",
    "description": "Patch lead label",
    "method": "PATCH",
    "path": "/api/v2/lead-labels/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to update"
        },
        "label": {
          "type": "string",
          "description": "Display label for the custom lead label"
        },
        "interest_status_label": {
          "type": "string",
          "description": "Interest status label associated with this label"
        },
        "description": {
          "type": [
            "string",
            "null"
          ],
          "description": "Detailed description of the custom lead label purpose"
        },
        "use_with_ai": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether this label should be used with AI features"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_deleteLeadLabel",
    "description": "Delete lead label",
    "method": "DELETE",
    "path": "/api/v2/lead-labels/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to delete"
        },
        "reassigned_status": {
          "type": "number",
          "description": "The interest status to reassign leads and emails to."
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_testAiReplyLabelLeadLabels",
    "description": "Test AI reply label prediction",
    "method": "POST",
    "path": "/api/v2/lead-labels/ai-reply-label",
    "parameters": {
      "type": "object",
      "properties": {
        "reply_text": {
          "type": "string",
          "description": "The reply text to classify."
        }
      },
      "required": [
        "reply_text"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_listLeadList",
    "description": "List lead list",
    "method": "GET",
    "path": "/api/v2/lead-lists",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "The starting after timestamp to filter lead lists by."
        },
        "has_enrichment_task": {
          "type": "boolean",
          "description": "Whether the list has an enrichment task."
        },
        "search": {
          "type": "string",
          "description": "The search query to filter lead lists by."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_createLeadList",
    "description": "Create lead list",
    "method": "POST",
    "path": "/api/v2/lead-lists",
    "parameters": {
      "type": "object",
      "properties": {
        "has_enrichment_task": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether this list runs the enrichment process on every added lead or not"
        },
        "owned_by": {
          "type": [
            "string",
            "null"
          ],
          "description": "User ID of the owner of this lead list. Defaults to the user that created the list"
        },
        "name": {
          "type": "string",
          "description": "Name of the lead list"
        }
      },
      "required": [
        "name"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getLeadList",
    "description": "Get lead list",
    "method": "GET",
    "path": "/api/v2/lead-lists/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the requested item"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_patchLeadList",
    "description": "Patch lead list",
    "method": "PATCH",
    "path": "/api/v2/lead-lists/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to update"
        },
        "has_enrichment_task": {
          "type": [
            "boolean",
            "null"
          ],
          "description": "Whether this list runs the enrichment process on every added lead or not"
        },
        "owned_by": {
          "type": [
            "string",
            "null"
          ],
          "description": "User ID of the owner of this lead list. Defaults to the user that created the list"
        },
        "name": {
          "type": "string",
          "description": "Name of the lead list"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_deleteLeadList",
    "description": "Delete lead list",
    "method": "DELETE",
    "path": "/api/v2/lead-lists/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to delete"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getVerificationStats",
    "description": "Get verification statistics for a lead list",
    "method": "GET",
    "path": "/api/v2/lead-lists/{id}/verification-stats",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "id"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_createLead",
    "description": "Create lead",
    "method": "POST",
    "path": "/api/v2/leads",
    "parameters": {
      "type": "object",
      "properties": {
        "campaign": {
          "type": [
            "string",
            "null"
          ],
          "description": "Campaign ID associated with the lead"
        },
        "email": {
          "type": [
            "string",
            "null"
          ],
          "description": "Email address of the lead"
        },
        "personalization": {
          "type": [
            "string",
            "null"
          ],
          "description": "Personalization of the lead"
        },
        "website": {
          "type": [
            "string",
            "null"
          ],
          "description": "Website of the lead"
        },
        "last_name": {
          "type": [
            "string",
            "null"
          ],
          "description": "Last name of the lead"
        },
        "first_name": {
          "type": [
            "string",
            "null"
          ],
          "description": "First name of the lead"
        },
        "company_name": {
          "type": [
            "string",
            "null"
          ],
          "description": "Company name of the lead"
        },
        "job_title": {
          "type": [
            "string",
            "null"
          ],
          "description": "Job title of the lead"
        },
        "phone": {
          "type": [
            "string",
            "null"
          ],
          "description": "Phone number of the lead"
        },
        "lt_interest_status": {
          "type": "number",
          "description": "Lead interest status. It can be either a static value (check below), or a custom status interest value"
        },
        "pl_value_lead": {
          "type": [
            "string",
            "null"
          ],
          "description": "Potential value of the lead"
        },
        "list_id": {
          "type": [
            "string",
            "null"
          ],
          "description": "List ID associated with the lead"
        },
        "assigned_to": {
          "type": [
            "string",
            "null"
          ],
          "description": "ID of the user assigned to the lead"
        },
        "skip_if_in_workspace": {
          "type": "boolean",
          "description": "Whether to skip if the lead is already in the workspace."
        },
        "skip_if_in_campaign": {
          "type": "boolean",
          "description": "Whether to skip if the lead is already in the campaign."
        },
        "skip_if_in_list": {
          "type": "boolean",
          "description": "Whether to skip if the lead is already in the list."
        },
        "blocklist_id": {
          "type": "string",
          "description": "The ID of the blocklist to check for the lead."
        },
        "verify_leads_for_lead_finder": {
          "type": "boolean",
          "description": "Whether to verify the leads for the lead finder."
        },
        "verify_leads_on_import": {
          "type": "boolean",
          "description": "Whether to verify the leads on import."
        },
        "custom_variables": {
          "type": "object",
          "description": "Custom variables can include any metadata about the lead that is relevant to the campaign, the campaign will be updated to allow all the other leads in the campaign to have the same custom variables. The custom variables will be added to the lead payload field"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_bulkDeleteLeads",
    "description": "Delete leads in bulk",
    "method": "DELETE",
    "path": "/api/v2/leads",
    "parameters": {
      "type": "object",
      "properties": {
        "campaign_id": {
          "type": "string",
          "description": "The ID of the campaign to delete leads from. Required if `list_id` is not provided."
        },
        "list_id": {
          "type": "string",
          "description": "The ID of the list to delete leads from. Required if `campaign_id` is not provided."
        },
        "status": {
          "type": "number",
          "description": "Optional status filter. Only delete leads with this status."
        },
        "ids": {
          "type": "array",
          "description": "Optional array of specific lead IDs to delete. When provided, only these leads will be deleted from the specified campaign or list."
        },
        "limit": {
          "type": "integer",
          "description": "Maximum number of leads to delete. If not specified, all matching leads will be deleted."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_listLeads",
    "description": "List leads",
    "method": "POST",
    "path": "/api/v2/leads/list",
    "parameters": {
      "type": "object",
      "properties": {
        "search": {
          "type": "string",
          "description": "A search string to search the leads against - can be First Name, Last Name, or Email"
        },
        "filter": {
          "type": "string",
          "description": "Filter criteria for leads. For custom lead labels, use the `interest_status` field."
        },
        "campaign": {
          "type": "string",
          "description": "Campaign ID to filter leads"
        },
        "list_id": {
          "type": "string",
          "description": "List ID to filter leads"
        },
        "in_campaign": {
          "type": "boolean",
          "description": "Whether the lead is in a campaign"
        },
        "in_list": {
          "type": "boolean",
          "description": "Whether the lead is in a list"
        },
        "ids": {
          "type": "array",
          "description": "Array of lead IDs to include"
        },
        "queries": {
          "type": "array",
          "description": "queries"
        },
        "excluded_ids": {
          "type": "array",
          "description": "Array of lead IDs to exclude"
        },
        "contacts": {
          "type": "array",
          "description": "Array of emails the leads needs to have"
        },
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "Forward pagination cursor. When distinct_contacts is false, provide the `id` value from the last lead of the previous page; when true, provide the lead's email."
        },
        "organization_user_ids": {
          "type": "array",
          "description": "Array of organization user IDs to filter leads"
        },
        "smart_view_id": {
          "type": "string",
          "description": "Smart view ID to filter leads"
        },
        "is_website_visitor": {
          "type": "boolean",
          "description": "Whether the lead is a website visitor"
        },
        "distinct_contacts": {
          "type": "boolean",
          "description": "Whether to return distinct contacts"
        },
        "enrichment_status": {
          "type": "number",
          "description": "Enrichment status to filter leads"
        },
        "esg_code": {
          "type": "string",
          "description": "ESG code to filter leads"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_getLead",
    "description": "Get lead",
    "method": "GET",
    "path": "/api/v2/leads/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the requested item"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_patchLead",
    "description": "Patch lead",
    "method": "PATCH",
    "path": "/api/v2/leads/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to update"
        },
        "personalization": {
          "type": [
            "string",
            "null"
          ],
          "description": "Personalization of the lead"
        },
        "website": {
          "type": [
            "string",
            "null"
          ],
          "description": "Website of the lead"
        },
        "last_name": {
          "type": [
            "string",
            "null"
          ],
          "description": "Last name of the lead"
        },
        "first_name": {
          "type": [
            "string",
            "null"
          ],
          "description": "First name of the lead"
        },
        "company_name": {
          "type": [
            "string",
            "null"
          ],
          "description": "Company name of the lead"
        },
        "job_title": {
          "type": [
            "string",
            "null"
          ],
          "description": "Job title of the lead"
        },
        "phone": {
          "type": [
            "string",
            "null"
          ],
          "description": "Phone number of the lead"
        },
        "lt_interest_status": {
          "type": "number",
          "description": "Lead interest status. It can be either a static value (check below), or a custom status interest value"
        },
        "pl_value_lead": {
          "type": [
            "string",
            "null"
          ],
          "description": "Potential value of the lead"
        },
        "assigned_to": {
          "type": [
            "string",
            "null"
          ],
          "description": "ID of the user assigned to the lead"
        },
        "custom_variables": {
          "type": "object",
          "description": "Custom variables can include any metadata about the lead that is relevant to the campaign, the campaign will be updated to allow all the other leads in the campaign to have the same custom variables. The custom variables will be added to the lead payload field"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_deleteLead",
    "description": "Delete lead",
    "method": "DELETE",
    "path": "/api/v2/leads/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to delete"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_mergeLeads",
    "description": "Merge two leads",
    "method": "POST",
    "path": "/api/v2/leads/merge",
    "parameters": {
      "type": "object",
      "properties": {
        "lead_id": {
          "type": "string",
          "description": "The ID of the lead to merge."
        },
        "destination_lead_id": {
          "type": "string",
          "description": "The ID of the destination lead to merge into."
        }
      },
      "required": [
        "lead_id",
        "destination_lead_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_updateLeadInterestStatus",
    "description": "Update the interest status of a lead",
    "method": "POST",
    "path": "/api/v2/leads/update-interest-status",
    "parameters": {
      "type": "object",
      "properties": {
        "lead_email": {
          "type": "string",
          "description": "The email of the lead to update the interest status of."
        },
        "interest_value": {
          "type": [
            "number",
            "null"
          ],
          "description": "Set this field to \"null\" to reset the lead value to \"Lead\". This is the same as moving the lead to the \"Lead\" status in the web app. Please check the `lt_interest_status` field for the list of possible values."
        },
        "campaign_id": {
          "type": "string",
          "description": "The ID of the campaign to update the interest status of."
        },
        "ai_interest_value": {
          "type": "number",
          "description": "The AI interest value to set for the lead."
        },
        "disable_auto_interest": {
          "type": "boolean",
          "description": "Whether to disable the auto interest."
        },
        "list_id": {
          "type": "string",
          "description": "The ID of the list to update the interest status of."
        }
      },
      "required": [
        "lead_email",
        "interest_value"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_removeLeadFromSubsequence",
    "description": "Remove a lead from a subsequence",
    "method": "POST",
    "path": "/api/v2/leads/subsequence/remove",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the lead to remove from the subsequence."
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_bulkAssignLeads",
    "description": "Bulk assign leads to organization users",
    "method": "POST",
    "path": "/api/v2/leads/bulk-assign",
    "parameters": {
      "type": "object",
      "properties": {
        "search": {
          "type": "string",
          "description": "The search query to filter leads by."
        },
        "filter": {
          "type": "string",
          "description": "The filter to apply to the leads."
        },
        "campaign": {
          "type": "string",
          "description": "The ID of the campaign to filter leads by."
        },
        "list_id": {
          "type": "string",
          "description": "The ID of the list to filter leads by."
        },
        "in_campaign": {
          "type": "boolean",
          "description": "Whether the leads are in the campaign."
        },
        "in_list": {
          "type": "boolean",
          "description": "Whether the leads are in the list."
        },
        "organization_user_ids": {
          "type": "array",
          "description": "organization_user_ids"
        },
        "smart_view_id": {
          "type": "string",
          "description": "The ID of the smart view to filter leads by."
        },
        "ids": {
          "type": "array",
          "description": "The IDs of the leads to filter by."
        },
        "limit": {
          "type": "integer",
          "description": "The limit of the number of leads to return."
        },
        "queries": {
          "type": "array",
          "description": "queries"
        }
      },
      "required": [
        "organization_user_ids"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_moveLeads",
    "description": "Move leads to a campaign or list",
    "method": "POST",
    "path": "/api/v2/leads/move",
    "parameters": {
      "type": "object",
      "properties": {
        "search": {
          "type": "string",
          "description": "A search string to search the leads against - can be First Name, Last Name, or Email"
        },
        "filter": {
          "type": "string",
          "description": "Filter criteria for leads. For custom lead labels, use the `interest_status` field."
        },
        "campaign": {
          "type": "string",
          "description": "Campaign ID to filter leads"
        },
        "list_id": {
          "type": "string",
          "description": "List ID to filter leads"
        },
        "in_campaign": {
          "type": "boolean",
          "description": "Whether the lead is in a campaign"
        },
        "in_list": {
          "type": "boolean",
          "description": "Whether the lead is in a list"
        },
        "ids": {
          "type": "array",
          "description": "Array of lead IDs to include. When using this parameter, you must provide either `campaign` or `list_id` to specify which campaign or list to filter the leads from. This parameter acts as a filter within the specified campaign or list, not as a standalone way to select leads."
        },
        "queries": {
          "type": "array",
          "description": "queries"
        },
        "excluded_ids": {
          "type": "array",
          "description": "Array of lead IDs to exclude"
        },
        "contacts": {
          "type": "array",
          "description": "Array of emails the leads needs to have"
        },
        "to_campaign_id": {
          "type": "string",
          "description": "The ID of the campaign to move the leads to."
        },
        "to_list_id": {
          "type": "string",
          "description": "The ID of the list to move the leads to."
        },
        "ignore_resource_filter_clauses": {
          "type": "boolean",
          "description": "Whether to ignore saved lead-finder clauses for the source campaign/list when selecting leads to move."
        },
        "check_duplicates_in_campaigns": {
          "type": "boolean",
          "description": "Whether to check duplicates in campaigns."
        },
        "skip_leads_in_verification": {
          "type": "boolean",
          "description": "Whether to skip leads in verification."
        },
        "limit": {
          "type": "number",
          "description": "The limit of the number of leads to move."
        },
        "assigned_to": {
          "type": "string",
          "description": "The ID of the user to assign the leads to."
        },
        "esp_code": {
          "type": "number",
          "description": "The ESP code to move the leads for."
        },
        "esg_code": {
          "type": "string",
          "description": "The ESG code to move the leads for."
        },
        "copy_leads": {
          "type": "boolean",
          "description": "Whether to copy the leads."
        },
        "check_duplicates": {
          "type": "boolean",
          "description": "Whether to check duplicates."
        },
        "reset_interest_status": {
          "type": "boolean",
          "description": "Whether to reset the interest status of leads when moving or copying them. When true, the interest status will be reset. When false, the existing interest status will be preserved; for non-copy campaign-to-campaign moves, opportunities will also be migrated to the target campaign."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_moveLeadToSubsequence",
    "description": "Move a lead to a subsequence",
    "method": "POST",
    "path": "/api/v2/leads/subsequence/move",
    "parameters": {
      "type": "object",
      "properties": {
        "subsequence_id": {
          "type": "string",
          "description": "subsequence_id"
        },
        "id": {
          "type": "string",
          "description": "id"
        }
      },
      "required": [
        "id",
        "subsequence_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_bulkAddLeads",
    "description": "Add leads in bulk to a campaign or list",
    "method": "POST",
    "path": "/api/v2/leads/add",
    "parameters": {
      "type": "object",
      "properties": {
        "campaign_id": {
          "type": "string",
          "description": "The unique identifier for the campaign to add leads to. Use this field OR `list_id`, but not both."
        },
        "list_id": {
          "type": "string",
          "description": "The unique identifier for the list to add leads to. Use this field OR `campaign_id`, but not both."
        },
        "leads": {
          "type": "array",
          "description": "An array of lead objects to create. When using `campaign_id`: Each lead object must contain an `email`. When using `list_id` Each lead object must contain at least one of the following: `email`, `first_name`, or `last_name`."
        },
        "blocklist_id": {
          "type": [
            "string",
            "null"
          ],
          "description": "Optional blocklist ID to check leads against. If omitted, the workspace default blocklist is used."
        },
        "assigned_to": {
          "type": "string",
          "description": "Optional user ID to assign all imported leads to. If omitted, leads are assigned to the campaign owner when `campaign_id` is defined, or the user making the request."
        },
        "verify_leads_on_import": {
          "type": "boolean",
          "description": "If true, a background job will be created to verify the email addresses of the imported leads."
        },
        "skip_if_in_workspace": {
          "type": "boolean",
          "description": "If true, any lead that already exists anywhere in your workspace (in any campaign or list) will be skipped. This option overrides the other \"skip_if\" flags."
        },
        "skip_if_in_campaign": {
          "type": "boolean",
          "description": "If true, any lead that already exists in ANY campaign in your workspace will be skipped."
        },
        "skip_if_in_list": {
          "type": "boolean",
          "description": "If true, any lead that already exists in ANY list in your workspace will be skipped."
        }
      },
      "required": [
        "leads"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_initGoogleOAuth",
    "description": "Initialize google oauth",
    "method": "POST",
    "path": "/api/v2/oauth/google/init",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_instantly_initMicrosoftOAuth",
    "description": "Initialize microsoft oauth",
    "method": "POST",
    "path": "/api/v2/oauth/microsoft/init",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_instantly_getOAuthSessionStatus",
    "description": "Get oauth session status",
    "method": "GET",
    "path": "/api/v2/oauth/session/status/{sessionId}",
    "parameters": {
      "type": "object",
      "properties": {
        "sessionId": {
          "type": "string",
          "description": "Session ID from init response"
        }
      },
      "required": [
        "sessionId"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_listCampaignSubsequence",
    "description": "List campaign subsequence",
    "method": "GET",
    "path": "/api/v2/subsequences",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "The ID of the last item in the previous page - used for pagination. You can use the value of the `next_starting_after` field from the previous response."
        },
        "parent_campaign": {
          "type": "string",
          "description": "The ID of the campaign to list the subsequences of."
        },
        "search": {
          "type": "string",
          "description": "The search query to filter the subsequences by."
        }
      },
      "required": [
        "parent_campaign"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_createCampaignSubsequence",
    "description": "Create campaign subsequence",
    "method": "POST",
    "path": "/api/v2/subsequences",
    "parameters": {
      "type": "object",
      "properties": {
        "parent_campaign": {
          "type": "string",
          "description": "ID of the parent campaign"
        },
        "name": {
          "type": "string",
          "description": "Name of the subsequence"
        },
        "conditions": {
          "type": "object",
          "description": "Conditions that trigger the subsequence"
        },
        "subsequence_schedule": {
          "type": "object",
          "description": "Schedule configuration for the subsequence"
        },
        "sequences": {
          "type": "array",
          "description": "List of sequences (the actual email copy). Even though this field is an array, only the first element is used, so please provide only one array item, and add the steps to that array"
        },
        "daily_limit_mode": {
          "type": "string",
          "description": "Daily limit mode for the subsequence. \"inherit\" uses the parent campaign limit, \"custom\" uses a subsequence-specific limit, \"unlimited\" bypasses the campaign-level daily limit."
        },
        "daily_limit": {
          "type": [
            "number",
            "null"
          ],
          "description": "Custom daily limit for the subsequence. Only used when `daily_limit_mode` is \"custom\"."
        },
        "ignore_account_daily_limit": {
          "type": "boolean",
          "description": "When enabled, the subsequence will send even when sending accounts have reached their daily limit."
        }
      },
      "required": [
        "parent_campaign",
        "name",
        "conditions",
        "subsequence_schedule",
        "sequences"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_duplicateSubsequence",
    "description": "Duplicate a subsequence",
    "method": "POST",
    "path": "/api/v2/subsequences/{id}/duplicate",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the subsequence to duplicate."
        },
        "parent_campaign": {
          "type": "string",
          "description": "The ID of the campaign to duplicate the subsequence to."
        },
        "name": {
          "type": "string",
          "description": "The name of the duplicate subsequence."
        }
      },
      "required": [
        "id",
        "parent_campaign",
        "name"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_pauseSubsequence",
    "description": "Pause a subsequence",
    "method": "POST",
    "path": "/api/v2/subsequences/{id}/pause",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Subsequence ID"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_resumeSubsequence",
    "description": "Resume a paused subsequence",
    "method": "POST",
    "path": "/api/v2/subsequences/{id}/resume",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the subsequence to resume."
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getCampaignSubsequence",
    "description": "Get campaign subsequence",
    "method": "GET",
    "path": "/api/v2/subsequences/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the requested item"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_patchCampaignSubsequence",
    "description": "Patch campaign subsequence",
    "method": "PATCH",
    "path": "/api/v2/subsequences/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to update"
        },
        "name": {
          "type": "string",
          "description": "Name of the subsequence"
        },
        "daily_limit_mode": {
          "type": "string",
          "description": "Daily limit mode for the subsequence. \"inherit\" uses the parent campaign limit, \"custom\" uses a subsequence-specific limit, \"unlimited\" bypasses the campaign-level daily limit."
        },
        "daily_limit": {
          "type": [
            "number",
            "null"
          ],
          "description": "Custom daily limit for the subsequence. Only used when `daily_limit_mode` is \"custom\"."
        },
        "ignore_account_daily_limit": {
          "type": "boolean",
          "description": "When enabled, the subsequence will send even when sending accounts have reached their daily limit."
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_deleteCampaignSubsequence",
    "description": "Delete campaign subsequence",
    "method": "DELETE",
    "path": "/api/v2/subsequences/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to delete"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getSubsequenceSendingStatus",
    "description": "Get subsequence sending status",
    "method": "GET",
    "path": "/api/v2/subsequences/{id}/sending-status",
    "parameters": {
      "type": "object",
      "properties": {
        "with_ai_summary": {
          "type": "boolean",
          "description": "Include AI-generated summary"
        },
        "id": {
          "type": "string",
          "description": "Subsequence ID"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_enrichLeadsFromSupersearch",
    "description": "Enrich leads from supersearch",
    "method": "POST",
    "path": "/api/v2/supersearch-enrichment/enrich-leads-from-supersearch",
    "parameters": {
      "type": "object",
      "properties": {
        "search_filters": {
          "type": "object",
          "description": "Search filters to find leads."
        },
        "search_name": {
          "type": "string",
          "description": "Name of the search"
        },
        "work_email_enrichment": {
          "type": "boolean",
          "description": "Enable work email enrichment"
        },
        "fully_enriched_profile": {
          "type": "boolean",
          "description": "Enable LinkedIn profile enrichment"
        },
        "custom_flow": {
          "type": "array",
          "description": "Ordered list of providers for waterfall enrichment (enabled platforms only)"
        },
        "resource_id": {
          "type": "string",
          "description": "ID of the existing list to add leads to. A list is automatically created if no list is provided."
        },
        "auto_update": {
          "type": "boolean",
          "description": "Whether to auto-update new leads"
        },
        "evergreen": {
          "type": "object",
          "description": "evergreen"
        },
        "skip_rows_without_email": {
          "type": "boolean",
          "description": "Whether to skip leads without email"
        },
        "list_name": {
          "type": "string",
          "description": "Name for new list if resource_id not provided"
        },
        "limit": {
          "type": "number",
          "description": "Maximum number of leads to import"
        }
      },
      "required": [
        "search_filters",
        "limit"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getEnrichmentForResource",
    "description": "Get enrichment for resource",
    "method": "GET",
    "path": "/api/v2/supersearch-enrichment/{resource_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "resource_id": {
          "type": "string",
          "description": "The ID of the list or campaign to retrieve the enrichment."
        }
      },
      "required": [
        "resource_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_createSuperSearchEnrichment",
    "description": "Create an enrichment",
    "method": "POST",
    "path": "/api/v2/supersearch-enrichment",
    "parameters": {
      "type": "object",
      "properties": {
        "resource_id": {
          "type": "string",
          "description": "Unique identifier for the resource (list or campaign)"
        },
        "type": {
          "type": "string",
          "description": "Enrichment type to add to the resource"
        },
        "limit": {
          "type": "number",
          "description": "Maximum number of leads to enrich."
        },
        "filters": {
          "type": "array",
          "description": "Filters to apply to the enrichment"
        },
        "custom_flow": {
          "type": "array",
          "description": "Custom flow to apply to the enrichment"
        }
      },
      "required": [
        "resource_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_update_enrichment_settings",
    "description": "Update enrichment settings for resource",
    "method": "PATCH",
    "path": "/api/v2/supersearch-enrichment/{resource_id}/settings",
    "parameters": {
      "type": "object",
      "properties": {
        "resource_id": {
          "type": "string",
          "description": "Unique identifier for the resource (list or campaign)"
        },
        "auto_update": {
          "type": "boolean",
          "description": "Whether new leads added to the resource will be automatically enriched"
        },
        "skip_rows_without_email": {
          "type": "boolean",
          "description": "Whether the fully enriched profile enrichment will run even if we don't find an email"
        },
        "is_evergreen": {
          "type": "boolean",
          "description": "Whether the enrichment is evergreen"
        }
      },
      "required": [
        "resource_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_createAIEnrichment",
    "description": "Create AI enrichment",
    "method": "POST",
    "path": "/api/v2/supersearch-enrichment/ai",
    "parameters": {
      "type": "object",
      "properties": {
        "resource_id": {
          "type": "string",
          "description": "Id of the resource (list or campaign) to enrich"
        },
        "output_column": {
          "type": "string",
          "description": "Name of the column where the AI enrichment results will be stored"
        },
        "resource_type": {
          "type": "number",
          "description": "Type of the entity to enrich"
        },
        "input_columns": {
          "type": "array",
          "description": "List of column names to use as input data for the AI enrichment. These are the fields from your leads that will be used to generate content."
        },
        "model_version": {
          "type": "string",
          "description": "Version of the AI model to use for enrichment. Different models have different capabilities, costs, and token limits."
        },
        "use_instantly_account": {
          "type": "boolean",
          "description": "When true, the enrichment will use Instantly's account for API calls. When false, it will use your own API keys configured in settings."
        },
        "overwrite": {
          "type": "boolean",
          "description": "When true, will overwrite existing values in the output column. When false, only empty fields will be enriched."
        },
        "auto_update": {
          "type": "boolean",
          "description": "When true, new leads added to the campaign/list will be automatically enriched using these same settings."
        },
        "skip_leads_without_email": {
          "type": "boolean",
          "description": "When true, leads without an email will be skipped."
        },
        "limit": {
          "type": "number",
          "description": "Maximum number of leads to enrich."
        },
        "prompt": {
          "type": "string",
          "description": "Custom prompt to guide the AI enrichment. Use {{variables}} to reference input data. Only used when templateId is not provided."
        },
        "template_id": {
          "type": "number",
          "description": "ID of a predefined AI prompt template to use instead of a custom prompt. Templates are reusable prompt configurations."
        },
        "status": {
          "type": "number",
          "description": "Status of the job"
        },
        "show_state": {
          "type": "boolean",
          "description": "Whether to send the state of the enrichment"
        },
        "filters": {
          "type": "array",
          "description": "filters"
        }
      },
      "required": [
        "resource_id",
        "output_column",
        "resource_type",
        "model_version"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getAiEnrichmentForResource",
    "description": "Get AI enrichment for resource",
    "method": "GET",
    "path": "/api/v2/supersearch-enrichment/ai/{resource_id}/in-progress",
    "parameters": {
      "type": "object",
      "properties": {
        "resource_id": {
          "type": "string",
          "description": "The ID of the list or campaign to retrieve the AI enrichment."
        }
      },
      "required": [
        "resource_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getEnrichmentHistory",
    "description": "Get enrichment history",
    "method": "GET",
    "path": "/api/v2/supersearch-enrichment/history/{resource_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "offset": {
          "type": "number",
          "description": "offset"
        },
        "limit": {
          "type": "number",
          "description": "limit"
        },
        "resource_id": {
          "type": "string",
          "description": "ID of the resource to retrieve"
        }
      },
      "required": [
        "resource_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_runEnrichment",
    "description": "Run enrichment for resource",
    "method": "POST",
    "path": "/api/v2/supersearch-enrichment/run",
    "parameters": {
      "type": "object",
      "properties": {
        "resource_id": {
          "type": "string",
          "description": "The ID of the resource (list or campaign) to run enrichments for"
        },
        "lead_ids": {
          "type": "array",
          "description": "List of lead IDs to enrich (optional)"
        },
        "limit": {
          "type": "integer",
          "description": "If set, only the first N leads will be enriched"
        },
        "column_name": {
          "type": "string",
          "description": "AI enrichment column to run."
        },
        "overwrite": {
          "type": "boolean",
          "description": "(AI re-run parameter) If true, run even if column has value. If false (default), only process empty/null columns. Requires column_name."
        },
        "starting_row": {
          "type": "integer",
          "description": "(AI re-run parameter) Starting lead position (inclusive, 1-indexed). Defaults to 1 if not provided. Requires column_name."
        },
        "count": {
          "type": "integer",
          "description": "(AI re-run parameter) How many leads to process. If not provided, processes all remaining leads from starting_row to the end. Requires column_name."
        },
        "filters": {
          "type": "array",
          "description": "Conditional formula filters to apply when processing leads. Only leads matching all filters will be enriched."
        }
      },
      "required": [
        "resource_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_countLeadsFromSupersearch",
    "description": "Count leads from supersearch",
    "method": "POST",
    "path": "/api/v2/supersearch-enrichment/count-leads-from-supersearch",
    "parameters": {
      "type": "object",
      "properties": {
        "search_filters": {
          "type": "object",
          "description": "Search filters to find leads."
        },
        "skip_owned_leads": {
          "type": "boolean",
          "description": "Skip leads that belong to the current workspace."
        },
        "show_one_lead_per_company": {
          "type": "boolean",
          "description": "Return only one lead per company."
        }
      },
      "required": [
        "search_filters"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_previewLeadsFromSupersearch",
    "description": "Preview leads from supersearch",
    "method": "POST",
    "path": "/api/v2/supersearch-enrichment/preview-leads-from-supersearch",
    "parameters": {
      "type": "object",
      "properties": {
        "search_filters": {
          "type": "object",
          "description": "Search filters to find leads."
        },
        "skip_owned_leads": {
          "type": "boolean",
          "description": "Skip leads that belong to the current workspace"
        },
        "show_one_lead_per_company": {
          "type": "boolean",
          "description": "Return only one lead per company"
        }
      },
      "required": [
        "search_filters"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_listWebhookEvent",
    "description": "List webhook event",
    "method": "GET",
    "path": "/api/v2/webhook-events",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "The ID of the last item in the previous page - used for pagination. You can use the value of the `next_starting_after` field from the previous response."
        },
        "success": {
          "type": "boolean",
          "description": "Filter by success status"
        },
        "from": {
          "type": "string",
          "description": "Inclusive start of the window (YYYY-MM-DD)."
        },
        "to": {
          "type": "string",
          "description": "Inclusive end of the window (YYYY-MM-DD)."
        },
        "search": {
          "type": "string",
          "description": "Search by exact webhook URL or lead email match"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_getWebhookEvent",
    "description": "Get webhook event",
    "method": "GET",
    "path": "/api/v2/webhook-events/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the requested item"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getWebhookEventsSummary",
    "description": "Get overview aggregates for webhook events",
    "method": "GET",
    "path": "/api/v2/webhook-events/summary",
    "parameters": {
      "type": "object",
      "properties": {
        "from": {
          "type": "string",
          "description": "Inclusive start of the window (YYYY-MM-DD)."
        },
        "to": {
          "type": "string",
          "description": "Inclusive end of the window (YYYY-MM-DD)."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_getWebhookEventsSummaryByDate",
    "description": "Get overview aggregates for webhook events by date",
    "method": "GET",
    "path": "/api/v2/webhook-events/summary-by-date",
    "parameters": {
      "type": "object",
      "properties": {
        "from": {
          "type": "string",
          "description": "Inclusive start of the window (YYYY-MM-DD)."
        },
        "to": {
          "type": "string",
          "description": "Inclusive end of the window (YYYY-MM-DD)."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_listWebhook",
    "description": "List webhooks",
    "method": "GET",
    "path": "/api/v2/webhooks",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "The ID of the last item in the previous page - used for pagination. You can use the value of the `next_starting_after` field from the previous response."
        },
        "campaign": {
          "type": "string",
          "description": "Filter by campaign ID"
        },
        "event_type": {
          "type": "string",
          "description": "Filter by event type (e.g., email_sent, lead_interested, all_events)"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_createWebhook",
    "description": "Create webhook",
    "method": "POST",
    "path": "/api/v2/webhooks",
    "parameters": {
      "type": "object",
      "properties": {
        "campaign": {
          "type": [
            "string",
            "null"
          ],
          "description": "Optional campaign UUID to filter events (null = all campaigns in workspace)"
        },
        "name": {
          "type": [
            "string",
            "null"
          ],
          "description": "Optional user-defined name for the webhook"
        },
        "target_hook_url": {
          "type": "string",
          "description": "Target URL to send webhook payloads"
        },
        "event_type": {
          "type": [
            "string",
            "null"
          ],
          "description": "Type of event to trigger the webhook (null for custom label events). Set to \"all_events\" to subscribe to all events - including custom label events"
        },
        "custom_interest_value": {
          "type": [
            "number",
            "null"
          ],
          "description": "Custom interest value - corresponds to LeadLabel.interest_status (used for custom label events)"
        },
        "headers": {
          "type": [
            "object",
            "null"
          ],
          "description": "Optional HTTP headers to include when delivering webhook payloads (key-value pairs)"
        }
      },
      "required": [
        "target_hook_url"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getWebhook",
    "description": "Get webhook",
    "method": "GET",
    "path": "/api/v2/webhooks/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the requested item"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_patchWebhook",
    "description": "Patch webhook",
    "method": "PATCH",
    "path": "/api/v2/webhooks/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to update"
        },
        "campaign": {
          "type": [
            "string",
            "null"
          ],
          "description": "Optional campaign UUID to filter events (null = all campaigns in workspace)"
        },
        "name": {
          "type": [
            "string",
            "null"
          ],
          "description": "Optional user-defined name for the webhook"
        },
        "target_hook_url": {
          "type": "string",
          "description": "Target URL to send webhook payloads"
        },
        "event_type": {
          "type": [
            "string",
            "null"
          ],
          "description": "Type of event to trigger the webhook (null for custom label events). Set to \"all_events\" to subscribe to all events - including custom label events"
        },
        "custom_interest_value": {
          "type": [
            "number",
            "null"
          ],
          "description": "Custom interest value - corresponds to LeadLabel.interest_status (used for custom label events)"
        },
        "headers": {
          "type": [
            "object",
            "null"
          ],
          "description": "Optional HTTP headers to include when delivering webhook payloads (key-value pairs)"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_deleteWebhook",
    "description": "Delete webhook",
    "method": "DELETE",
    "path": "/api/v2/webhooks/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to delete"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_listWebhookEventTypes",
    "description": "List available event types",
    "method": "GET",
    "path": "/api/v2/webhooks/event-types",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_instantly_testWebhook",
    "description": "Test a webhook",
    "method": "POST",
    "path": "/api/v2/webhooks/{id}/test",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "id"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_resumeWebhook",
    "description": "Resume a webhook",
    "method": "POST",
    "path": "/api/v2/webhooks/{id}/resume",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "id"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getWorkspacePlanDetails",
    "description": "Get workspace plan details",
    "method": "GET",
    "path": "/api/v2/workspace-billing/plan-details",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_instantly_get_subscription",
    "description": "Get workspace subscription details",
    "method": "GET",
    "path": "/api/v2/workspace-billing/subscription-details",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_instantly_listWorkspaceGroupMember",
    "description": "List workspace group member",
    "method": "GET",
    "path": "/api/v2/workspace-group-members",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "The ID of the last item in the previous page - used for pagination. You can use the value of the `next_starting_after` field from the previous response."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_createWorkspaceGroupMember",
    "description": "Create workspace group member",
    "method": "POST",
    "path": "/api/v2/workspace-group-members",
    "parameters": {
      "type": "object",
      "properties": {
        "sub_workspace_id": {
          "type": "string",
          "description": "The id of the sub workspace"
        }
      },
      "required": [
        "sub_workspace_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getWorkspaceGroupMember",
    "description": "Get workspace group member",
    "method": "GET",
    "path": "/api/v2/workspace-group-members/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the requested item"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_deleteWorkspaceGroupMember",
    "description": "Delete workspace group member",
    "method": "DELETE",
    "path": "/api/v2/workspace-group-members/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to delete"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getAdminWorkspaceGroupMember",
    "description": "Get the current workspace admin workspace",
    "method": "GET",
    "path": "/api/v2/workspace-group-members/admin",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_instantly_listWorkspaceMember",
    "description": "List workspace member",
    "method": "GET",
    "path": "/api/v2/workspace-members",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "The number of items to return"
        },
        "starting_after": {
          "type": "string",
          "description": "The ID of the last item in the previous page - used for pagination. You can use the value of the `next_starting_after` field from the previous response."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_createWorkspaceMember",
    "description": "Create workspace member",
    "method": "POST",
    "path": "/api/v2/workspace-members",
    "parameters": {
      "type": "object",
      "properties": {
        "email": {
          "type": "string",
          "description": "Email address of the workspace member"
        },
        "user_email": {
          "type": [
            "string",
            "null"
          ],
          "description": "Email address of the user"
        },
        "role": {
          "type": "string",
          "description": "THe role of the workspace member defining their access level. While the \"owner\" role is listed in the enum, it cannot be created via the API, and is only assigned to the user who creates the workspace."
        },
        "permissions": {
          "type": [
            "array",
            "null"
          ],
          "description": "The permissions for this workspace member. Used in the app to restrict access to certain sections"
        }
      },
      "required": [
        "email",
        "role"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getWorkspaceMember",
    "description": "Get workspace member",
    "method": "GET",
    "path": "/api/v2/workspace-members/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the requested item"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_patchWorkspaceMember",
    "description": "Patch workspace member",
    "method": "PATCH",
    "path": "/api/v2/workspace-members/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to update"
        },
        "role": {
          "type": "string",
          "description": "THe role of the workspace member defining their access level. While the \"owner\" role is listed in the enum, it cannot be created via the API, and is only assigned to the user who creates the workspace."
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_deleteWorkspaceMember",
    "description": "Delete workspace member",
    "method": "DELETE",
    "path": "/api/v2/workspace-members/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the item to delete"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_getWorkspace",
    "description": "Get workspace",
    "method": "GET",
    "path": "/api/v2/workspaces/current",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_instantly_patchWorkspace",
    "description": "Patch workspace",
    "method": "PATCH",
    "path": "/api/v2/workspaces/current",
    "parameters": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "Name of the workspace"
        },
        "org_logo_url": {
          "type": [
            "string",
            "null"
          ],
          "description": "URL to workspace logo"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_instantly_getWorkspaceDomainInfo",
    "description": "Get organization verified agency domain information",
    "method": "GET",
    "path": "/api/v2/workspaces/current/whitelabel-domain",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_instantly_addWorkspaceAgencyDomain",
    "description": "Set the agency domain for the workspace",
    "method": "POST",
    "path": "/api/v2/workspaces/current/whitelabel-domain",
    "parameters": {
      "type": "object",
      "properties": {
        "domain": {
          "type": "string",
          "description": "The agency domain to set for the workspace"
        }
      },
      "required": [
        "domain"
      ]
    }
  },
  {
    "name": "superagnt_connection_instantly_deleteWorkspaceDomain",
    "description": "Delete organization agency domain",
    "method": "DELETE",
    "path": "/api/v2/workspaces/current/whitelabel-domain",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_instantly_changeWorkspaceOwner",
    "description": "Change workspace owner",
    "method": "POST",
    "path": "/api/v2/workspaces/current/change-owner",
    "parameters": {
      "type": "object",
      "properties": {
        "email": {
          "type": "string",
          "description": "email"
        },
        "sec": {
          "type": "string",
          "description": "sec"
        }
      },
      "required": [
        "email",
        "sec"
      ]
    }
  }
]
```

## Example

```bash
curl -X GET &#x27;https://api.superagnt.com/v1/connections/instantly/api/v2/campaigns/list&#x27; \
  -H &#x27;Authorization: Bearer $SUPERAGNT_API_KEY&#x27;
```

## Use Cases

- Automate outbound sales campaigns from CRM triggers
- Sync leads between your database and Instantly campaigns
- Build AI agents that monitor and optimize email deliverability
- Create dashboards tracking outreach performance across campaigns
- Automate lead enrichment workflows
- Orchestrate multi-step outreach sequences with AI-driven personalization

## Links

- [Documentation](https://superagnt.com/r/ch-instantly-outreach-docs)
- [superagnt app / API keys](https://superagnt.com/r/ch-instantly-outreach-key)
- [Connections page](https://app.superagnt.com/dashboard/connections)
- [This listing](https://clawhub.ai/superagnt/skills/instantly-outreach)
