---
name: heyreach-outreach
description: "Manage LinkedIn outreach campaigns, leads, lists, inbox conversations, and analytics via HeyReach through the superagnt unified API."
version: 2.0.14
author: superagnt
license: MIT-0
platforms: [macos, linux, windows]
required_environment_variables:
  - SUPERAGNT_API_KEY
metadata:
  hermes:
    tags: [heyreach, integration, api, ai-agent]
  openclaw:
    requires:
      env:
        - SUPERAGNT_API_KEY
      bins:
        - curl
    primaryEnv: SUPERAGNT_API_KEY
    emoji: "🤝"
    homepage: https://superagnt.com/r/ch-heyreach-outreach-docs
---

# HeyReach Integration

The HeyReach integration connects your HeyReach workspace to superagnt, letting AI agents and workflows manage LinkedIn outreach programmatically. Read and control campaigns, push leads into running campaigns with the right sender account, sync conversations from the unified inbox, and pull aggregated outreach analytics — all proxied through your superagnt API key.

## Alternative install: the MCP server

If this client speaks MCP, you can connect the workspace server instead of
using this skill's curl calls — after the user connects their
HeyReach account in the superagnt app, the same endpoints below are exposed
as native MCP tools:

```
https://mcp.superagnt.com/mcp
```

The URL publishes full OAuth discovery — an MCP-capable client needs the URL
and nothing else (approve once in the browser). Per-client setup lines:
https://www.superagnt.com/install

Everything below works on curl-only environments with just the API key.

## Capabilities and safety

This skill documents the HeyReach API surface the user's connected
account can reach — which can include destructive operations (updates,
deletes) and, where the vendor supports them, actions performed as the user
(sending messages, modifying records, changing settings). Two hard rules:

- **Confirm before destructive or outbound actions.** Never delete, overwrite,
  or send on the user's behalf without their explicit confirmation in the
  conversation.
- **Stay inside the user's request.** Use only the endpoints the task needs;
  this skill grants no access beyond the HeyReach connection the user
  set up themselves.

**Disclosure:** Account administration: beyond outreach, the HeyReach API includes organization and workspace administration endpoints, including member invites and API-key creation. Use those only when the user explicitly asks for account administration, and always confirm before creating keys or changing team membership.

## Prerequisites

1. An API key — get one from the [superagnt app](https://superagnt.com/r/ch-heyreach-outreach-key) and export it as
   `SUPERAGNT_API_KEY`.
2. A connected HeyReach account — connect it on the
   [Connections page](https://app.superagnt.com/dashboard/connections). Calls fail with a clear error
   until the vendor is connected; that error is the signal to send the user to
   the connections page, not a bug.

Note: `/v1/connections/*` calls run on the USER'S HeyReach credentials —
vendor-side rate limits and billing are theirs, not platform credits.

## Authentication

```
Authorization: Bearer $SUPERAGNT_API_KEY
```

If the variable is not set, ask the user for their key or point them at
https://superagnt.com/r/ch-heyreach-outreach-key.

## Verify the install (do this first)

```bash
curl -s https://api.superagnt.com/v1/credits \
  -H &#x27;Authorization: Bearer $SUPERAGNT_API_KEY&#x27;
```

A JSON result proves the key end to end. 401 = bad key; an error naming the
connection means the HeyReach account is not connected yet.

## Base URL

```
https://api.superagnt.com/v1/connections/heyreach
```

## Available Endpoints

| Method | Path | Summary |
|--------|------|---------|
| `GET` | `/auth/CheckApiKey` | Check API Key |
| `POST` | `/campaign/GetAll` | List campaigns |
| `GET` | `/campaign/GetById` | Get campaign by ID |
| `POST` | `/campaign/Pause` | Pause campaign |
| `POST` | `/campaign/Resume` | Resume campaign |
| `POST` | `/campaign/StartCampaign` | Start campaign |
| `POST` | `/campaign/Create` | Create campaign |
| `POST` | `/campaign/CreateCampaignFromTemplate` | Create campaign from template |
| `POST` | `/campaign/UpdateSettings` | Update campaign settings |
| `POST` | `/campaign/UpdateSchedule` | Update campaign schedule |
| `POST` | `/campaign/UpdateAccounts` | Update campaign sender accounts |
| `POST` | `/campaign/AddLinkedInAccountsToCampaign` | Add sender accounts to campaign |
| `POST` | `/campaign/RemoveLinkedInAccountsFromCampaign` | Remove sender accounts from campaign |
| `POST` | `/campaign/UpdateSequence` | Update campaign sequence |
| `GET` | `/campaign/GetCampaignSequence` | Get campaign sequence |
| `POST` | `/campaign/AddLeadsToCampaignV2` | Add leads to campaign |
| `POST` | `/campaign/AddLeadsToCampaign` | Add leads to campaign (v1, legacy) |
| `POST` | `/campaign/StopLeadInCampaign` | Stop lead in campaign |
| `POST` | `/campaign/GetLeadsFromCampaign` | Get leads in campaign |
| `POST` | `/campaign/GetCampaignsForLead` | Get campaigns for lead |
| `PATCH` | `/campaign/UpdateLeadCustomFields/campaigns/{campaignId}/leads/custom-fields` | Update a campaign lead&#x27;s custom fields |
| `POST` | `/inbox/GetConversationsV2` | Get conversations |
| `POST` | `/inbox/GetConversationsV3` | Get conversations (cursor-paged) |
| `GET` | `/inbox/GetChatroom/{accountId}/{conversationId}` | Get chatroom (single conversation thread) |
| `POST` | `/inbox/SendMessage` | Send message in conversation |
| `POST` | `/inbox/SetSeenStatus` | Set conversation seen status |
| `POST` | `/li_account/GetAll` | List connected LinkedIn accounts |
| `GET` | `/li_account/GetById` | Get connected LinkedIn account by ID |
| `GET` | `/li_account/GetAccountStatus/{accountId}` | Get sender account connection status |
| `POST` | `/li_account/Reconnect` | Reconnect sender account |
| `POST` | `/li_account/ReloginSalesNavigator` | Re-authenticate Sales Navigator |
| `POST` | `/li_account/ReloginRecruiter` | Re-authenticate Recruiter |
| `POST` | `/li_account/Resync` | Resync sender account profile |
| `GET` | `/li_account/GetProxyCountries` | List proxy countries |
| `POST` | `/li_account/UpdateProxy` | Update sender account proxy |
| `POST` | `/li_account/UpdateInboxConfiguration` | Update sender inbox sync |
| `DELETE` | `/li_account/RemoveAccount/{accountId}` | Remove sender account |
| `POST` | `/list/GetAll` | List lead/company lists |
| `GET` | `/list/GetById` | Get list by ID |
| `POST` | `/list/CreateEmptyList` | Create empty list |
| `POST` | `/list/GetLeadsFromList` | Get leads from a list |
| `POST` | `/list/GetCompaniesFromList` | Get companies from a list |
| `POST` | `/list/AddLeadsToListV2` | Add leads to list |
| `POST` | `/list/AddLeadsToList` | Add leads to list (v1, legacy) |
| `DELETE` | `/list/DeleteLeadsFromList` | Delete leads from list by member ID |
| `DELETE` | `/list/DeleteLeadsFromListByProfileUrl` | Delete leads from list by profile URL |
| `POST` | `/list/GetListsForLead` | Get lists a lead belongs to |
| `PATCH` | `/list/UpdateLeadCustomFields/lists/{listId}/leads/custom-fields` | Update a list lead&#x27;s custom fields |
| `POST` | `/lead/GetLead` | Get lead by profile URL |
| `POST` | `/lead/AddTags` | Add tags to lead |
| `POST` | `/lead/ReplaceTags` | Replace lead tags |
| `POST` | `/lead/GetTags` | Get tags for a lead |
| `POST` | `/lead_tags/CreateTags` | Create workspace lead tags |
| `POST` | `/blacklist/GetLeads` | List blacklisted leads |
| `POST` | `/blacklist/AddLeads` | Blacklist leads |
| `POST` | `/blacklist/RemoveLeads` | Remove blacklisted leads |
| `POST` | `/blacklist/GetCompanies` | List blacklisted companies |
| `POST` | `/blacklist/AddCompanies` | Blacklist companies |
| `POST` | `/blacklist/RemoveCompanies` | Remove blacklisted companies |
| `POST` | `/enrichment/enrich-email` | Start an email enrichment |
| `GET` | `/enrichment/enrich-email/check-job/{jobId}` | Check an email enrichment |
| `POST` | `/stats/GetOverallStats` | Get overall stats |
| `POST` | `/stats/GetOverallStatsByCampaign` | Get overall stats grouped by campaign |
| `POST` | `/MyNetwork/GetMyNetworkForSender` | Get sender&#x27;s LinkedIn network |
| `POST` | `/MyNetwork/IsConnection` | Check if a lead is a 1st-degree connection |
| `POST` | `/webhooks/CreateWebhook` | Create webhook subscription |
| `GET` | `/webhooks/GetWebhookById` | Get webhook by ID |
| `POST` | `/webhooks/GetAllWebhooks` | List webhooks |
| `PATCH` | `/webhooks/UpdateWebhook` | Update webhook subscription |
| `DELETE` | `/webhooks/DeleteWebhook` | Delete webhook subscription |
| `GET` | `/management/organizations/workspaces` | List workspaces (organization-scoped key) |
| `POST` | `/management/organizations/workspaces` | Create workspace |
| `PATCH` | `/management/organizations/workspaces/{workspaceId}` | Update workspace |
| `GET` | `/management/organizations/api-keys/workspaces/{workspaceId}` | Get workspace API keys |
| `POST` | `/management/organizations/api-keys/workspaces/{workspaceId}` | Create workspace API key |
| `POST` | `/management/organizations/users` | List users in the organization |
| `GET` | `/management/organizations/users/{userId}` | Get user by ID |
| `POST` | `/management/organizations/users/workspaces/{workspaceId}` | List users in workspace |
| `POST` | `/management/organizations/users/invite/admins` | Invite admins |
| `POST` | `/management/organizations/users/invite/managers` | Invite managers |
| `POST` | `/management/organizations/users/invite/members` | Invite members |
| `POST` | `/management/organizations/linkedin-accounts` | List sender accounts across workspaces |
| `DELETE` | `/management/organizations/linkedin-accounts/{linkedInAccountId}` | Delete a sender account (organization) |
| `POST` | `/management/organizations/linkedin-accounts/MoveToWorkspace` | Move a sender account to another workspace |

## Tool Schemas

The following JSON defines every operation with its parameters. Each tool maps
to an API endpoint under the base URL.

```json
[
  {
    "name": "superagnt_connection_heyreach_auth_check_api_key",
    "description": "Check API Key",
    "method": "GET",
    "path": "/auth/CheckApiKey",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_heyreach_campaign_get_all",
    "description": "List campaigns",
    "method": "POST",
    "path": "/campaign/GetAll",
    "parameters": {
      "type": "object",
      "properties": {
        "offset": {
          "type": "integer",
          "description": "Number of records to skip."
        },
        "limit": {
          "type": "integer",
          "description": "Page size, at most 100."
        },
        "keyword": {
          "type": "string",
          "description": "Matches campaign names."
        },
        "statuses": {
          "type": "array",
          "description": "Only campaigns in these statuses."
        },
        "accountIds": {
          "type": "array",
          "description": "Only campaigns using these sender accounts."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_heyreach_campaign_get_by_id",
    "description": "Get campaign by ID",
    "method": "GET",
    "path": "/campaign/GetById",
    "parameters": {
      "type": "object",
      "properties": {
        "campaignId": {
          "type": "integer",
          "description": "Numeric identifier of the campaign."
        }
      },
      "required": [
        "campaignId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_campaign_pause",
    "description": "Pause campaign",
    "method": "POST",
    "path": "/campaign/Pause",
    "parameters": {
      "type": "object",
      "properties": {
        "campaignId": {
          "type": "integer",
          "description": "Numeric identifier of the campaign to pause."
        }
      },
      "required": [
        "campaignId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_campaign_resume",
    "description": "Resume campaign",
    "method": "POST",
    "path": "/campaign/Resume",
    "parameters": {
      "type": "object",
      "properties": {
        "campaignId": {
          "type": "integer",
          "description": "Numeric identifier of the campaign to resume."
        }
      },
      "required": [
        "campaignId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_campaign_start",
    "description": "Start campaign",
    "method": "POST",
    "path": "/campaign/StartCampaign",
    "parameters": {
      "type": "object",
      "properties": {
        "campaignId": {
          "type": "integer",
          "description": "Numeric identifier of the campaign to start."
        }
      },
      "required": [
        "campaignId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_campaign_create",
    "description": "Create campaign",
    "method": "POST",
    "path": "/campaign/Create",
    "parameters": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "Campaign name, 1-50 characters."
        },
        "linkedInUserListId": {
          "type": "integer",
          "description": "The lead list (`USER_LIST`) the campaign reads leads from."
        },
        "linkedInAccountIds": {
          "type": "array",
          "description": "Sender accounts that run the campaign; each must be connected with valid auth."
        },
        "excludeContactedFromOtherCampaigns": {
          "type": "boolean",
          "description": "Skip leads already in any other campaign."
        },
        "excludeHasOtherAccConversations": {
          "type": "boolean",
          "description": "Skip leads who already have a conversation with another sender account."
        },
        "excludeContactedFromSenderInOtherCampaign": {
          "type": "boolean",
          "description": "Skip leads the campaign's senders already contacted from another campaign."
        },
        "excludeListId": {
          "type": "integer",
          "description": "A lead list whose members are always skipped; must differ from `linkedInUserListId`."
        },
        "excludeFromLeadBlacklist": {
          "type": "boolean",
          "description": "Skip leads on the workspace's lead blacklist (`/blacklist/GetLeads`)."
        },
        "excludeFromCompanyBlacklist": {
          "type": "boolean",
          "description": "Skip leads whose company is on the workspace's company blacklist (`/blacklist/GetCompanies`)."
        },
        "schedule": {
          "type": "string",
          "description": "schedule"
        },
        "sequence": {
          "type": "string",
          "description": "sequence"
        }
      },
      "required": [
        "name",
        "linkedInUserListId",
        "linkedInAccountIds"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_campaign_create_from_template",
    "description": "Create campaign from template",
    "method": "POST",
    "path": "/campaign/CreateCampaignFromTemplate",
    "parameters": {
      "type": "object",
      "properties": {
        "campaignIdForTemplate": {
          "type": "integer",
          "description": "The campaign whose sequence and schedule are copied."
        },
        "name": {
          "type": "string",
          "description": "Campaign name, 1-50 characters."
        },
        "linkedInUserListId": {
          "type": "integer",
          "description": "The lead list (`USER_LIST`) for the new campaign."
        },
        "linkedInAcccountIdsForCampaign": {
          "type": "array",
          "description": "Sender accounts that run the new campaign. (The triple `c` matches HeyReach's API.)"
        },
        "excludeContactedFromOtherCampaigns": {
          "type": "boolean",
          "description": "Skip leads already in any other campaign."
        },
        "excludeHasOtherAccConversations": {
          "type": "boolean",
          "description": "Skip leads who already have a conversation with another sender account."
        },
        "excludeContactedFromSenderInOtherCampaign": {
          "type": "boolean",
          "description": "Skip leads the campaign's senders already contacted from another campaign."
        },
        "excludeListId": {
          "type": "integer",
          "description": "A lead list whose members are always skipped; must differ from `linkedInUserListId`."
        },
        "excludeFromLeadBlacklist": {
          "type": "boolean",
          "description": "Skip leads on the workspace's lead blacklist (`/blacklist/GetLeads`)."
        },
        "excludeFromCompanyBlacklist": {
          "type": "boolean",
          "description": "Skip leads whose company is on the workspace's company blacklist (`/blacklist/GetCompanies`)."
        }
      },
      "required": [
        "campaignIdForTemplate",
        "name",
        "linkedInUserListId",
        "linkedInAcccountIdsForCampaign"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_campaign_update_settings",
    "description": "Update campaign settings",
    "method": "POST",
    "path": "/campaign/UpdateSettings",
    "parameters": {
      "type": "object",
      "properties": {
        "campaignId": {
          "type": "integer",
          "description": "The campaign."
        },
        "name": {
          "type": "string",
          "description": "Campaign name, 1-50 characters."
        },
        "linkedInUserListId": {
          "type": "integer",
          "description": "The campaign's lead list (`USER_LIST`); send the current one to keep it."
        },
        "excludeContactedFromOtherCampaigns": {
          "type": "boolean",
          "description": "Skip leads already in any other campaign."
        },
        "excludeHasOtherAccConversations": {
          "type": "boolean",
          "description": "Skip leads who already have a conversation with another sender account."
        },
        "excludeContactedFromSenderInOtherCampaign": {
          "type": "boolean",
          "description": "Skip leads the campaign's senders already contacted from another campaign."
        },
        "excludeListId": {
          "type": "integer",
          "description": "A lead list whose members are always skipped; must differ from `linkedInUserListId`."
        },
        "excludeFromLeadBlacklist": {
          "type": "boolean",
          "description": "Skip leads on the workspace's lead blacklist (`/blacklist/GetLeads`)."
        },
        "excludeFromCompanyBlacklist": {
          "type": "boolean",
          "description": "Skip leads whose company is on the workspace's company blacklist (`/blacklist/GetCompanies`)."
        }
      },
      "required": [
        "campaignId",
        "name",
        "linkedInUserListId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_campaign_update_schedule",
    "description": "Update campaign schedule",
    "method": "POST",
    "path": "/campaign/UpdateSchedule",
    "parameters": {
      "type": "object",
      "properties": {
        "campaignId": {
          "type": "integer",
          "description": "campaignId"
        },
        "schedule": {
          "type": "string",
          "description": "schedule"
        }
      },
      "required": [
        "campaignId",
        "schedule"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_campaign_update_accounts",
    "description": "Update campaign sender accounts",
    "method": "POST",
    "path": "/campaign/UpdateAccounts",
    "parameters": {
      "type": "object",
      "properties": {
        "campaignId": {
          "type": "integer",
          "description": "campaignId"
        },
        "linkedInAccountIds": {
          "type": "array",
          "description": "linkedInAccountIds"
        }
      },
      "required": [
        "campaignId",
        "linkedInAccountIds"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_campaign_add_accounts",
    "description": "Add sender accounts to campaign",
    "method": "POST",
    "path": "/campaign/AddLinkedInAccountsToCampaign",
    "parameters": {
      "type": "object",
      "properties": {
        "campaignId": {
          "type": "integer",
          "description": "The campaign."
        },
        "linkedInAccountIds": {
          "type": "array",
          "description": "Sender accounts to add."
        }
      },
      "required": [
        "campaignId",
        "linkedInAccountIds"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_campaign_remove_accounts",
    "description": "Remove sender accounts from campaign",
    "method": "POST",
    "path": "/campaign/RemoveLinkedInAccountsFromCampaign",
    "parameters": {
      "type": "object",
      "properties": {
        "campaignId": {
          "type": "integer",
          "description": "The campaign."
        },
        "linkedInAccountIds": {
          "type": "array",
          "description": "Sender accounts to remove."
        }
      },
      "required": [
        "campaignId",
        "linkedInAccountIds"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_campaign_update_sequence",
    "description": "Update campaign sequence",
    "method": "POST",
    "path": "/campaign/UpdateSequence",
    "parameters": {
      "type": "object",
      "properties": {
        "campaignId": {
          "type": "integer",
          "description": "campaignId"
        },
        "sequence": {
          "type": "string",
          "description": "sequence"
        }
      },
      "required": [
        "campaignId",
        "sequence"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_campaign_get_sequence",
    "description": "Get campaign sequence",
    "method": "GET",
    "path": "/campaign/GetCampaignSequence",
    "parameters": {
      "type": "object",
      "properties": {
        "campaignId": {
          "type": "integer",
          "description": "The campaign."
        }
      },
      "required": [
        "campaignId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_campaign_add_leads_v2",
    "description": "Add leads to campaign",
    "method": "POST",
    "path": "/campaign/AddLeadsToCampaignV2",
    "parameters": {
      "type": "object",
      "properties": {
        "campaignId": {
          "type": "integer",
          "description": "Numeric identifier of the destination campaign."
        },
        "accountLeadPairs": {
          "type": "array",
          "description": "List of `{ lead, linkedInAccountId }` pairs. `linkedInAccountId` selects which connected sender account should own the outreach for that lead and must be one of the campaign's assigned sender accounts."
        },
        "resumePausedCampaign": {
          "type": "boolean",
          "description": "When true and the campaign is `PAUSED`, HeyReach resumes the campaign before adding the leads. Send `false` unless the operator asked for a resume."
        },
        "resumeFinishedCampaign": {
          "type": "boolean",
          "description": "When true and the campaign is `FINISHED`, HeyReach resumes it before adding the leads."
        }
      },
      "required": [
        "campaignId",
        "accountLeadPairs"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_campaign_add_leads",
    "description": "Add leads to campaign (v1, legacy)",
    "method": "POST",
    "path": "/campaign/AddLeadsToCampaign",
    "parameters": {
      "type": "object",
      "properties": {
        "campaignId": {
          "type": "integer",
          "description": "campaignId"
        },
        "accountLeadPairs": {
          "type": "array",
          "description": "accountLeadPairs"
        },
        "resumeFinishedCampaign": {
          "type": "boolean",
          "description": "When true and the campaign is `FINISHED`, HeyReach resumes it before adding the leads."
        },
        "resumePausedCampaign": {
          "type": "boolean",
          "description": "When true and the campaign is `PAUSED`, HeyReach resumes the campaign before adding the leads. Send `false` unless the operator asked for a resume."
        }
      },
      "required": [
        "campaignId",
        "accountLeadPairs"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_campaign_stop_lead",
    "description": "Stop lead in campaign",
    "method": "POST",
    "path": "/campaign/StopLeadInCampaign",
    "parameters": {
      "type": "object",
      "properties": {
        "campaignId": {
          "type": "integer",
          "description": "campaignId"
        },
        "leadMemberId": {
          "type": "string",
          "description": "HeyReach internal ID of the lead within the campaign (one of `leadMemberId` or `leadUrl` is required)."
        },
        "leadUrl": {
          "type": "string",
          "description": "Public LinkedIn profile URL of the lead (one of `leadMemberId` or `leadUrl` is required)."
        }
      },
      "required": [
        "campaignId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_campaign_get_leads",
    "description": "Get leads in campaign",
    "method": "POST",
    "path": "/campaign/GetLeadsFromCampaign",
    "parameters": {
      "type": "object",
      "properties": {
        "campaignId": {
          "type": "integer",
          "description": "The campaign."
        },
        "offset": {
          "type": "integer",
          "description": "offset"
        },
        "limit": {
          "type": "integer",
          "description": "Page size, at most 100."
        },
        "timeFrom": {
          "type": "string",
          "description": "Inclusive lower bound on the timestamp selected by `timeFilter`."
        },
        "timeTo": {
          "type": "string",
          "description": "Inclusive upper bound on the timestamp selected by `timeFilter`."
        },
        "timeFilter": {
          "type": "string",
          "description": "Which timestamp `timeFrom`/`timeTo` filter: `CreationTime`, `LastActionTakenTime`, `FailedTime`, `LastActionTakenOrFailedTime`, or `Everywhere` (no time filter, the default)."
        }
      },
      "required": [
        "campaignId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_campaign_get_for_lead",
    "description": "Get campaigns for lead",
    "method": "POST",
    "path": "/campaign/GetCampaignsForLead",
    "parameters": {
      "type": "object",
      "properties": {
        "email": {
          "type": "string",
          "description": "email"
        },
        "linkedinId": {
          "type": "string",
          "description": "linkedinId"
        },
        "profileUrl": {
          "type": "string",
          "description": "profileUrl"
        },
        "offset": {
          "type": "integer",
          "description": "offset"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_heyreach_campaign_update_lead_fields",
    "description": "Update a campaign lead's custom fields",
    "method": "PATCH",
    "path": "/campaign/UpdateLeadCustomFields/campaigns/{campaignId}/leads/custom-fields",
    "parameters": {
      "type": "object",
      "properties": {
        "campaignId": {
          "type": "integer",
          "description": "The campaign."
        },
        "leadMemberIdOrUrl": {
          "type": "string",
          "description": "The lead: its LinkedIn member id (`linkedin_id`) or its profile URL."
        },
        "customFields": {
          "type": "object",
          "description": "Field name → value. An existing field is updated, a new one created, and a null or empty value deletes the field. At most 100 fields; names up to 128 characters, values up to 2048."
        }
      },
      "required": [
        "campaignId",
        "leadMemberIdOrUrl",
        "customFields"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_inbox_get_conversations_v2",
    "description": "Get conversations",
    "method": "POST",
    "path": "/inbox/GetConversationsV2",
    "parameters": {
      "type": "object",
      "properties": {
        "offset": {
          "type": "integer",
          "description": "Number of records to skip."
        },
        "limit": {
          "type": "integer",
          "description": "Page size, at most 100."
        },
        "filters": {
          "type": "object",
          "description": "Optional filters."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_heyreach_inbox_get_conversations_v3",
    "description": "Get conversations (cursor-paged)",
    "method": "POST",
    "path": "/inbox/GetConversationsV3",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "Page size, at most 100."
        },
        "cursor": {
          "type": "string",
          "description": "The previous page's `nextCursor`; omit or null for the first page. An edited cursor is a 400."
        },
        "from": {
          "type": "string",
          "description": "Lower bound on `lastMessageAt` (UTC)."
        },
        "to": {
          "type": "string",
          "description": "Upper bound on `lastMessageAt` (UTC); defaults to now."
        },
        "filters": {
          "type": "object",
          "description": "Optional filters."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_heyreach_inbox_get_chatroom",
    "description": "Get chatroom (single conversation thread)",
    "method": "GET",
    "path": "/inbox/GetChatroom/{accountId}/{conversationId}",
    "parameters": {
      "type": "object",
      "properties": {
        "accountId": {
          "type": "integer",
          "description": "ID of the connected LinkedIn sender account that owns the chatroom."
        },
        "conversationId": {
          "type": "string",
          "description": "The conversation's `id` (from `/inbox/GetConversationsV2` or `/inbox/GetConversationsV3`)."
        }
      },
      "required": [
        "accountId",
        "conversationId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_inbox_send_message",
    "description": "Send message in conversation",
    "method": "POST",
    "path": "/inbox/SendMessage",
    "parameters": {
      "type": "object",
      "properties": {
        "message": {
          "type": "string",
          "description": "Plain-text body of the message."
        },
        "subject": {
          "type": "string",
          "description": "Subject line; required by HeyReach and shown only in InMail threads."
        },
        "conversationId": {
          "type": "string",
          "description": "The conversation's `id`."
        },
        "linkedInAccountId": {
          "type": "integer",
          "description": "ID of the connected LinkedIn sender account that should send the message."
        }
      },
      "required": [
        "message",
        "subject",
        "conversationId",
        "linkedInAccountId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_inbox_set_seen_status",
    "description": "Set conversation seen status",
    "method": "POST",
    "path": "/inbox/SetSeenStatus",
    "parameters": {
      "type": "object",
      "properties": {
        "conversationId": {
          "type": "string",
          "description": "conversationId"
        },
        "linkedInAccountId": {
          "type": "integer",
          "description": "linkedInAccountId"
        },
        "seen": {
          "type": "boolean",
          "description": "seen"
        }
      },
      "required": [
        "conversationId",
        "linkedInAccountId",
        "seen"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_li_account_get_all",
    "description": "List connected LinkedIn accounts",
    "method": "POST",
    "path": "/li_account/GetAll",
    "parameters": {
      "type": "object",
      "properties": {
        "offset": {
          "type": "integer",
          "description": "offset"
        },
        "limit": {
          "type": "integer",
          "description": "Page size, at most 100."
        },
        "keyword": {
          "type": "string",
          "description": "Matches the account's name."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_heyreach_li_account_get_by_id",
    "description": "Get connected LinkedIn account by ID",
    "method": "GET",
    "path": "/li_account/GetById",
    "parameters": {
      "type": "object",
      "properties": {
        "accountId": {
          "type": "integer",
          "description": "ID of the connected LinkedIn sender account."
        }
      },
      "required": [
        "accountId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_li_account_get_status",
    "description": "Get sender account connection status",
    "method": "GET",
    "path": "/li_account/GetAccountStatus/{accountId}",
    "parameters": {
      "type": "object",
      "properties": {
        "accountId": {
          "type": "integer",
          "description": "The sender account."
        }
      },
      "required": [
        "accountId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_li_account_reconnect",
    "description": "Reconnect sender account",
    "method": "POST",
    "path": "/li_account/Reconnect",
    "parameters": {
      "type": "object",
      "properties": {
        "accountId": {
          "type": "integer",
          "description": "The sender account (`/li_account/GetAll`)."
        }
      },
      "required": [
        "accountId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_li_account_relogin_navigator",
    "description": "Re-authenticate Sales Navigator",
    "method": "POST",
    "path": "/li_account/ReloginSalesNavigator",
    "parameters": {
      "type": "object",
      "properties": {
        "accountId": {
          "type": "integer",
          "description": "The sender account (`/li_account/GetAll`)."
        }
      },
      "required": [
        "accountId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_li_account_relogin_recruiter",
    "description": "Re-authenticate Recruiter",
    "method": "POST",
    "path": "/li_account/ReloginRecruiter",
    "parameters": {
      "type": "object",
      "properties": {
        "accountId": {
          "type": "integer",
          "description": "The sender account (`/li_account/GetAll`)."
        }
      },
      "required": [
        "accountId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_li_account_resync",
    "description": "Resync sender account profile",
    "method": "POST",
    "path": "/li_account/Resync",
    "parameters": {
      "type": "object",
      "properties": {
        "accountId": {
          "type": "integer",
          "description": "The sender account (`/li_account/GetAll`)."
        }
      },
      "required": [
        "accountId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_li_account_get_proxy_countries",
    "description": "List proxy countries",
    "method": "GET",
    "path": "/li_account/GetProxyCountries",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_heyreach_li_account_update_proxy",
    "description": "Update sender account proxy",
    "method": "POST",
    "path": "/li_account/UpdateProxy",
    "parameters": {
      "type": "object",
      "properties": {
        "accountId": {
          "type": "integer",
          "description": "The sender account (`/li_account/GetAll`)."
        },
        "proxyCountryCode": {
          "type": "string",
          "description": "Country of the HeyReach-managed proxy, e.g. `US`."
        }
      },
      "required": [
        "accountId",
        "proxyCountryCode"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_li_account_update_inbox_config",
    "description": "Update sender inbox sync",
    "method": "POST",
    "path": "/li_account/UpdateInboxConfiguration",
    "parameters": {
      "type": "object",
      "properties": {
        "accountId": {
          "type": "integer",
          "description": "The sender account (`/li_account/GetAll`)."
        },
        "inboxScrapeMode": {
          "type": "string",
          "description": "inboxScrapeMode"
        }
      },
      "required": [
        "accountId",
        "inboxScrapeMode"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_li_account_remove",
    "description": "Remove sender account",
    "method": "DELETE",
    "path": "/li_account/RemoveAccount/{accountId}",
    "parameters": {
      "type": "object",
      "properties": {
        "accountId": {
          "type": "integer",
          "description": "The sender account."
        },
        "force": {
          "type": "boolean",
          "description": "Take the account off its active campaigns first."
        }
      },
      "required": [
        "accountId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_list_get_all",
    "description": "List lead/company lists",
    "method": "POST",
    "path": "/list/GetAll",
    "parameters": {
      "type": "object",
      "properties": {
        "offset": {
          "type": "integer",
          "description": "offset"
        },
        "limit": {
          "type": "integer",
          "description": "Page size, at most 100."
        },
        "keyword": {
          "type": "string",
          "description": "Optional free-text filter applied to list names."
        },
        "listType": {
          "type": "string",
          "description": "Only lead lists (`USER_LIST`) or only company lists (`COMPANY_LIST`)."
        },
        "campaignIds": {
          "type": "array",
          "description": "Only lists used by these campaigns."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_heyreach_list_get_by_id",
    "description": "Get list by ID",
    "method": "GET",
    "path": "/list/GetById",
    "parameters": {
      "type": "object",
      "properties": {
        "listId": {
          "type": "integer",
          "description": "listId"
        }
      },
      "required": [
        "listId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_list_create_empty",
    "description": "Create empty list",
    "method": "POST",
    "path": "/list/CreateEmptyList",
    "parameters": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "Display name of the list."
        },
        "type": {
          "type": "string",
          "description": "`USER_LIST` for leads or `COMPANY_LIST` for companies."
        }
      },
      "required": [
        "name",
        "type"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_list_get_leads",
    "description": "Get leads from a list",
    "method": "POST",
    "path": "/list/GetLeadsFromList",
    "parameters": {
      "type": "object",
      "properties": {
        "listId": {
          "type": "integer",
          "description": "listId"
        },
        "offset": {
          "type": "integer",
          "description": "offset"
        },
        "limit": {
          "type": "integer",
          "description": "Page size, at most 1000."
        },
        "keyword": {
          "type": "string",
          "description": "Optional free-text filter applied to lead first/last name and headline."
        },
        "leadProfileUrl": {
          "type": "string",
          "description": "Optional — restrict to a single lead by LinkedIn profile URL."
        },
        "leadLinkedInId": {
          "type": "string",
          "description": "Optional — restrict to a single lead by HeyReach-stored LinkedIn ID."
        },
        "createdFrom": {
          "type": "string",
          "description": "Inclusive lower bound on the lead's creation timestamp."
        },
        "createdTo": {
          "type": "string",
          "description": "Inclusive upper bound on the lead's creation timestamp."
        }
      },
      "required": [
        "listId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_list_get_companies",
    "description": "Get companies from a list",
    "method": "POST",
    "path": "/list/GetCompaniesFromList",
    "parameters": {
      "type": "object",
      "properties": {
        "listId": {
          "type": "integer",
          "description": "listId"
        },
        "offset": {
          "type": "integer",
          "description": "offset"
        },
        "limit": {
          "type": "integer",
          "description": "Page size, at most 1000."
        },
        "keyword": {
          "type": "string",
          "description": "Optional free-text filter applied to company name."
        }
      },
      "required": [
        "listId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_list_add_leads_v2",
    "description": "Add leads to list",
    "method": "POST",
    "path": "/list/AddLeadsToListV2",
    "parameters": {
      "type": "object",
      "properties": {
        "listId": {
          "type": "integer",
          "description": "listId"
        },
        "leads": {
          "type": "array",
          "description": "leads"
        }
      },
      "required": [
        "listId",
        "leads"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_list_add_leads",
    "description": "Add leads to list (v1, legacy)",
    "method": "POST",
    "path": "/list/AddLeadsToList",
    "parameters": {
      "type": "object",
      "properties": {
        "listId": {
          "type": "integer",
          "description": "listId"
        },
        "leads": {
          "type": "array",
          "description": "leads"
        }
      },
      "required": [
        "listId",
        "leads"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_list_delete_leads",
    "description": "Delete leads from list by member ID",
    "method": "DELETE",
    "path": "/list/DeleteLeadsFromList",
    "parameters": {
      "type": "object",
      "properties": {
        "listId": {
          "type": "integer",
          "description": "listId"
        },
        "leadMemberIds": {
          "type": "array",
          "description": "leadMemberIds"
        }
      },
      "required": [
        "listId",
        "leadMemberIds"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_list_delete_leads_by_url",
    "description": "Delete leads from list by profile URL",
    "method": "DELETE",
    "path": "/list/DeleteLeadsFromListByProfileUrl",
    "parameters": {
      "type": "object",
      "properties": {
        "listId": {
          "type": "integer",
          "description": "listId"
        },
        "profileUrls": {
          "type": "array",
          "description": "profileUrls"
        }
      },
      "required": [
        "listId",
        "profileUrls"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_list_get_for_lead",
    "description": "Get lists a lead belongs to",
    "method": "POST",
    "path": "/list/GetListsForLead",
    "parameters": {
      "type": "object",
      "properties": {
        "email": {
          "type": "string",
          "description": "email"
        },
        "linkedinId": {
          "type": "string",
          "description": "linkedinId"
        },
        "profileUrl": {
          "type": "string",
          "description": "profileUrl"
        },
        "offset": {
          "type": "integer",
          "description": "offset"
        },
        "limit": {
          "type": "integer",
          "description": "Page size, at most 1000."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_heyreach_list_update_lead_fields",
    "description": "Update a list lead's custom fields",
    "method": "PATCH",
    "path": "/list/UpdateLeadCustomFields/lists/{listId}/leads/custom-fields",
    "parameters": {
      "type": "object",
      "properties": {
        "listId": {
          "type": "integer",
          "description": "The lead list."
        },
        "leadMemberIdOrUrl": {
          "type": "string",
          "description": "The lead: its LinkedIn member id (`linkedin_id`) or its profile URL."
        },
        "customFields": {
          "type": "object",
          "description": "Field name → value. An existing field is updated, a new one created, and a null or empty value deletes the field. At most 100 fields; names up to 128 characters, values up to 2048."
        }
      },
      "required": [
        "listId",
        "leadMemberIdOrUrl",
        "customFields"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_lead_get_by_profile_url",
    "description": "Get lead by profile URL",
    "method": "POST",
    "path": "/lead/GetLead",
    "parameters": {
      "type": "object",
      "properties": {
        "profileUrl": {
          "type": "string",
          "description": "Public LinkedIn profile URL (e.g. `https://www.linkedin.com/in/janedoe/`)."
        }
      },
      "required": [
        "profileUrl"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_lead_add_tags",
    "description": "Add tags to lead",
    "method": "POST",
    "path": "/lead/AddTags",
    "parameters": {
      "type": "object",
      "properties": {
        "leadProfileUrl": {
          "type": "string",
          "description": "leadProfileUrl"
        },
        "leadLinkedInId": {
          "type": "string",
          "description": "leadLinkedInId"
        },
        "tags": {
          "type": "array",
          "description": "Tag display names to add."
        },
        "createTagIfNotExisting": {
          "type": "boolean",
          "description": "If true, missing tag names are created on the fly."
        }
      },
      "required": [
        "tags"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_lead_replace_tags",
    "description": "Replace lead tags",
    "method": "POST",
    "path": "/lead/ReplaceTags",
    "parameters": {
      "type": "object",
      "properties": {
        "leadProfileUrl": {
          "type": "string",
          "description": "leadProfileUrl"
        },
        "leadLinkedInId": {
          "type": "string",
          "description": "leadLinkedInId"
        },
        "tags": {
          "type": "array",
          "description": "tags"
        },
        "createTagIfNotExisting": {
          "type": "boolean",
          "description": "createTagIfNotExisting"
        }
      },
      "required": [
        "tags"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_lead_get_tags",
    "description": "Get tags for a lead",
    "method": "POST",
    "path": "/lead/GetTags",
    "parameters": {
      "type": "object",
      "properties": {
        "profileUrl": {
          "type": "string",
          "description": "profileUrl"
        }
      },
      "required": [
        "profileUrl"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_lead_tags_create",
    "description": "Create workspace lead tags",
    "method": "POST",
    "path": "/lead_tags/CreateTags",
    "parameters": {
      "type": "object",
      "properties": {
        "tags": {
          "type": "array",
          "description": "tags"
        }
      },
      "required": [
        "tags"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_blacklist_get_leads",
    "description": "List blacklisted leads",
    "method": "POST",
    "path": "/blacklist/GetLeads",
    "parameters": {
      "type": "object",
      "properties": {
        "offset": {
          "type": "integer",
          "description": "Number of records to skip."
        },
        "limit": {
          "type": "integer",
          "description": "Page size, at most 100."
        },
        "search": {
          "type": "string",
          "description": "Case-insensitive match on name, email, profile URL and LinkedIn member id."
        },
        "matchingStatus": {
          "type": "string",
          "description": "Only entries that resolved this way."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_heyreach_blacklist_add_leads",
    "description": "Blacklist leads",
    "method": "POST",
    "path": "/blacklist/AddLeads",
    "parameters": {
      "type": "object",
      "properties": {
        "leads": {
          "type": "array",
          "description": "1-100 entries, each with at least one identifier."
        }
      },
      "required": [
        "leads"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_blacklist_remove_leads",
    "description": "Remove blacklisted leads",
    "method": "POST",
    "path": "/blacklist/RemoveLeads",
    "parameters": {
      "type": "object",
      "properties": {
        "ids": {
          "type": "array",
          "description": "Entry ids, 1-100."
        }
      },
      "required": [
        "ids"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_blacklist_get_companies",
    "description": "List blacklisted companies",
    "method": "POST",
    "path": "/blacklist/GetCompanies",
    "parameters": {
      "type": "object",
      "properties": {
        "offset": {
          "type": "integer",
          "description": "Number of records to skip."
        },
        "limit": {
          "type": "integer",
          "description": "Page size, at most 100."
        },
        "search": {
          "type": "string",
          "description": "Case-insensitive match on company name and company URL."
        },
        "matchingStatus": {
          "type": "string",
          "description": "Only entries that resolved this way."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_heyreach_blacklist_add_companies",
    "description": "Blacklist companies",
    "method": "POST",
    "path": "/blacklist/AddCompanies",
    "parameters": {
      "type": "object",
      "properties": {
        "companies": {
          "type": "array",
          "description": "1-100 entries, each with `url`, `name` or both."
        }
      },
      "required": [
        "companies"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_blacklist_remove_companies",
    "description": "Remove blacklisted companies",
    "method": "POST",
    "path": "/blacklist/RemoveCompanies",
    "parameters": {
      "type": "object",
      "properties": {
        "ids": {
          "type": "array",
          "description": "Entry ids, 1-100."
        }
      },
      "required": [
        "ids"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_enrich_email",
    "description": "Start an email enrichment",
    "method": "POST",
    "path": "/enrichment/enrich-email",
    "parameters": {
      "type": "object",
      "properties": {
        "profileUrl": {
          "type": "string",
          "description": "The lead's LinkedIn profile URL."
        },
        "leadMemberId": {
          "type": "string",
          "description": "An existing lead's `linkedin_id`."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_heyreach_enrich_email_check_job",
    "description": "Check an email enrichment",
    "method": "GET",
    "path": "/enrichment/enrich-email/check-job/{jobId}",
    "parameters": {
      "type": "object",
      "properties": {
        "jobId": {
          "type": "integer",
          "description": "The `jobId` from `/enrichment/enrich-email`."
        }
      },
      "required": [
        "jobId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_stats_get_overall",
    "description": "Get overall stats",
    "method": "POST",
    "path": "/stats/GetOverallStats",
    "parameters": {
      "type": "object",
      "properties": {
        "startDate": {
          "type": "string",
          "description": "Inclusive start of the analytics window (ISO 8601)."
        },
        "endDate": {
          "type": "string",
          "description": "Inclusive end of the analytics window (ISO 8601)."
        },
        "campaignIds": {
          "type": "array",
          "description": "The campaigns to count, or `[]` for every campaign. Required."
        },
        "accountIds": {
          "type": "array",
          "description": "The connected LinkedIn sender accounts to count, or `[]` for every sender. Required."
        }
      },
      "required": [
        "accountIds",
        "campaignIds"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_stats_get_by_campaign",
    "description": "Get overall stats grouped by campaign",
    "method": "POST",
    "path": "/stats/GetOverallStatsByCampaign",
    "parameters": {
      "type": "object",
      "properties": {
        "startDate": {
          "type": "string",
          "description": "startDate"
        },
        "endDate": {
          "type": "string",
          "description": "endDate"
        },
        "campaignIds": {
          "type": "array",
          "description": "The campaigns to count, or `[]` for every campaign. Required."
        },
        "accountIds": {
          "type": "array",
          "description": "The connected LinkedIn sender accounts to count, or `[]` for every sender. Required."
        }
      },
      "required": [
        "accountIds",
        "campaignIds"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_network_get_for_sender",
    "description": "Get sender's LinkedIn network",
    "method": "POST",
    "path": "/MyNetwork/GetMyNetworkForSender",
    "parameters": {
      "type": "object",
      "properties": {
        "senderId": {
          "type": "integer",
          "description": "The sender account (`/li_account/GetAll`)."
        },
        "pageNumber": {
          "type": "integer",
          "description": "Zero-based page number."
        },
        "pageSize": {
          "type": "integer",
          "description": "Page size, at most 100."
        }
      },
      "required": [
        "senderId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_network_is_connection",
    "description": "Check if a lead is a 1st-degree connection",
    "method": "POST",
    "path": "/MyNetwork/IsConnection",
    "parameters": {
      "type": "object",
      "properties": {
        "senderAccountId": {
          "type": "integer",
          "description": "ID of the connected LinkedIn sender account."
        },
        "leadProfileUrl": {
          "type": "string",
          "description": "leadProfileUrl"
        },
        "leadLinkedInId": {
          "type": "string",
          "description": "leadLinkedInId"
        }
      },
      "required": [
        "senderAccountId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_webhook_create",
    "description": "Create webhook subscription",
    "method": "POST",
    "path": "/webhooks/CreateWebhook",
    "parameters": {
      "type": "object",
      "properties": {
        "webhookName": {
          "type": "string",
          "description": "3-25 characters."
        },
        "webhookUrl": {
          "type": "string",
          "description": "webhookUrl"
        },
        "eventType": {
          "type": "string",
          "description": "eventType"
        },
        "campaignIds": {
          "type": "array",
          "description": "Campaigns to listen to; empty or omitted means every campaign."
        },
        "customHeaders": {
          "type": "array",
          "description": "Extra HTTP headers HeyReach sends with each delivery, as `[{ name, value }]` (the shape `/webhooks/GetWebhookById` returns with `includeCustomHeaders`). HeyReach does not document them on writes: read the webhook back with `includeCustomHeaders: true` to confirm they were kept."
        }
      },
      "required": [
        "webhookName",
        "webhookUrl",
        "eventType"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_webhook_get_by_id",
    "description": "Get webhook by ID",
    "method": "GET",
    "path": "/webhooks/GetWebhookById",
    "parameters": {
      "type": "object",
      "properties": {
        "webhookId": {
          "type": "integer",
          "description": "webhookId"
        },
        "includeCustomHeaders": {
          "type": "boolean",
          "description": "Set to `true` to include any configured custom HTTP headers in the response."
        }
      },
      "required": [
        "webhookId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_webhook_get_all",
    "description": "List webhooks",
    "method": "POST",
    "path": "/webhooks/GetAllWebhooks",
    "parameters": {
      "type": "object",
      "properties": {
        "offset": {
          "type": "integer",
          "description": "offset"
        },
        "limit": {
          "type": "integer",
          "description": "Page size, at most 100."
        },
        "includeCustomHeaders": {
          "type": "boolean",
          "description": "includeCustomHeaders"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_heyreach_webhook_update",
    "description": "Update webhook subscription",
    "method": "PATCH",
    "path": "/webhooks/UpdateWebhook",
    "parameters": {
      "type": "object",
      "properties": {
        "webhookId": {
          "type": "integer",
          "description": "webhookId"
        },
        "webhookName": {
          "type": "string",
          "description": "3-25 characters."
        },
        "webhookUrl": {
          "type": "string",
          "description": "webhookUrl"
        },
        "eventType": {
          "type": "string",
          "description": "eventType"
        },
        "campaignIds": {
          "type": "array",
          "description": "campaignIds"
        },
        "isActive": {
          "type": "boolean",
          "description": "false pauses the webhook: HeyReach stops sending its events and the webhook can then be deleted (HeyReach refuses to delete an active one)."
        },
        "customHeaders": {
          "type": "array",
          "description": "Extra HTTP headers HeyReach sends with each delivery, as `[{ name, value }]` (the shape `/webhooks/GetWebhookById` returns with `includeCustomHeaders`). HeyReach does not document them on writes: read the webhook back with `includeCustomHeaders: true` to confirm they were kept."
        }
      },
      "required": [
        "webhookId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_webhook_delete",
    "description": "Delete webhook subscription",
    "method": "DELETE",
    "path": "/webhooks/DeleteWebhook",
    "parameters": {
      "type": "object",
      "properties": {
        "webhookId": {
          "type": "integer",
          "description": "webhookId"
        }
      },
      "required": [
        "webhookId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_org_workspaces_get_all",
    "description": "List workspaces (organization-scoped key)",
    "method": "GET",
    "path": "/management/organizations/workspaces",
    "parameters": {
      "type": "object",
      "properties": {
        "Offset": {
          "type": "integer",
          "description": "Offset"
        },
        "Limit": {
          "type": "integer",
          "description": "Limit"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_heyreach_org_workspaces_create",
    "description": "Create workspace",
    "method": "POST",
    "path": "/management/organizations/workspaces",
    "parameters": {
      "type": "object",
      "properties": {
        "workspaceName": {
          "type": "string",
          "description": "workspaceName"
        },
        "seatsLimit": {
          "type": "integer",
          "description": "Optional cap on workspace seats."
        }
      },
      "required": [
        "workspaceName"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_org_workspaces_update",
    "description": "Update workspace",
    "method": "PATCH",
    "path": "/management/organizations/workspaces/{workspaceId}",
    "parameters": {
      "type": "object",
      "properties": {
        "workspaceId": {
          "type": "integer",
          "description": "workspaceId"
        },
        "workspaceName": {
          "type": "string",
          "description": "workspaceName"
        },
        "seatsLimit": {
          "type": "object",
          "description": "Wrap the new seats cap as `{ \"value\": <integer> }`, or pass `null` to remove the cap."
        }
      },
      "required": [
        "workspaceId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_org_workspace_api_keys_get",
    "description": "Get workspace API keys",
    "method": "GET",
    "path": "/management/organizations/api-keys/workspaces/{workspaceId}",
    "parameters": {
      "type": "object",
      "properties": {
        "workspaceId": {
          "type": "integer",
          "description": "workspaceId"
        }
      },
      "required": [
        "workspaceId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_org_workspace_api_keys_create",
    "description": "Create workspace API key",
    "method": "POST",
    "path": "/management/organizations/api-keys/workspaces/{workspaceId}",
    "parameters": {
      "type": "object",
      "properties": {
        "workspaceId": {
          "type": "integer",
          "description": "workspaceId"
        },
        "apiKeyType": {
          "type": "string",
          "description": "apiKeyType"
        }
      },
      "required": [
        "workspaceId",
        "apiKeyType"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_org_users_get_all",
    "description": "List users in the organization",
    "method": "POST",
    "path": "/management/organizations/users",
    "parameters": {
      "type": "object",
      "properties": {
        "offset": {
          "type": "integer",
          "description": "offset"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        },
        "role": {
          "type": "string",
          "description": "role"
        },
        "invitationStatus": {
          "type": "array",
          "description": "invitationStatus"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_heyreach_org_user_get_by_id",
    "description": "Get user by ID",
    "method": "GET",
    "path": "/management/organizations/users/{userId}",
    "parameters": {
      "type": "object",
      "properties": {
        "userId": {
          "type": "integer",
          "description": "userId"
        }
      },
      "required": [
        "userId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_org_workspace_users_get_all",
    "description": "List users in workspace",
    "method": "POST",
    "path": "/management/organizations/users/workspaces/{workspaceId}",
    "parameters": {
      "type": "object",
      "properties": {
        "workspaceId": {
          "type": "integer",
          "description": "workspaceId"
        },
        "offset": {
          "type": "integer",
          "description": "offset"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        },
        "role": {
          "type": "string",
          "description": "role"
        },
        "invitationStatus": {
          "type": "array",
          "description": "invitationStatus"
        }
      },
      "required": [
        "workspaceId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_org_invite_admins",
    "description": "Invite admins",
    "method": "POST",
    "path": "/management/organizations/users/invite/admins",
    "parameters": {
      "type": "object",
      "properties": {
        "inviterEmail": {
          "type": "string",
          "description": "Email of the existing organization user the invitation should appear to come from."
        },
        "emails": {
          "type": "array",
          "description": "emails"
        }
      },
      "required": [
        "inviterEmail",
        "emails"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_org_invite_managers",
    "description": "Invite managers",
    "method": "POST",
    "path": "/management/organizations/users/invite/managers",
    "parameters": {
      "type": "object",
      "properties": {
        "inviterEmail": {
          "type": "string",
          "description": "inviterEmail"
        },
        "emails": {
          "type": "array",
          "description": "emails"
        },
        "workspaceIds": {
          "type": "array",
          "description": "workspaceIds"
        }
      },
      "required": [
        "inviterEmail",
        "emails",
        "workspaceIds"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_org_invite_members",
    "description": "Invite members",
    "method": "POST",
    "path": "/management/organizations/users/invite/members",
    "parameters": {
      "type": "object",
      "properties": {
        "inviterEmail": {
          "type": "string",
          "description": "inviterEmail"
        },
        "emails": {
          "type": "array",
          "description": "emails"
        },
        "workspaceIds": {
          "type": "array",
          "description": "workspaceIds"
        },
        "permissions": {
          "type": "string",
          "description": "permissions"
        }
      },
      "required": [
        "inviterEmail",
        "emails",
        "workspaceIds",
        "permissions"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_org_li_accounts_get_all",
    "description": "List sender accounts across workspaces",
    "method": "POST",
    "path": "/management/organizations/linkedin-accounts",
    "parameters": {
      "type": "object",
      "properties": {
        "keyword": {
          "type": "string",
          "description": "Matches the account's name."
        },
        "workspaceIds": {
          "type": "array",
          "description": "Only these workspaces; empty or omitted means all."
        },
        "offset": {
          "type": "integer",
          "description": "Number of records to skip."
        },
        "limit": {
          "type": "integer",
          "description": "Page size, at most 100."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_heyreach_org_li_account_delete",
    "description": "Delete a sender account (organization)",
    "method": "DELETE",
    "path": "/management/organizations/linkedin-accounts/{linkedInAccountId}",
    "parameters": {
      "type": "object",
      "properties": {
        "linkedInAccountId": {
          "type": "integer",
          "description": "The sender account."
        },
        "forceDelete": {
          "type": "boolean",
          "description": "Take the account off its active campaigns first."
        }
      },
      "required": [
        "linkedInAccountId"
      ]
    }
  },
  {
    "name": "superagnt_connection_heyreach_org_li_account_move",
    "description": "Move a sender account to another workspace",
    "method": "POST",
    "path": "/management/organizations/linkedin-accounts/MoveToWorkspace",
    "parameters": {
      "type": "object",
      "properties": {
        "linkedInAccountId": {
          "type": "integer",
          "description": "The sender account."
        },
        "workspaceId": {
          "type": "integer",
          "description": "The destination workspace."
        }
      },
      "required": [
        "linkedInAccountId",
        "workspaceId"
      ]
    }
  }
]
```

## Example

```bash
curl -X GET &#x27;https://api.superagnt.com/v1/connections/heyreach/auth/CheckApiKey&#x27; \
  -H &#x27;Authorization: Bearer $SUPERAGNT_API_KEY&#x27;
```

## Use Cases

- Push leads from your data warehouse or enrichment pipeline into running HeyReach campaigns
- Build AI agents that triage HeyReach replies and write them back to your CRM
- Sync the unified inbox into Slack or a CRM with per-campaign routing
- Pause or resume campaigns automatically based on inventory, deliverability, or budget signals
- Generate weekly outreach reports across senders and campaigns from &#x60;/stats/GetOverallStats&#x60;
- Mirror a sender&#x27;s 1st-degree LinkedIn network into a CRM for retargeting workflows

## Links

- [Documentation](https://superagnt.com/r/ch-heyreach-outreach-docs)
- [superagnt app / API keys](https://superagnt.com/r/ch-heyreach-outreach-key)
- [Connections page](https://app.superagnt.com/dashboard/connections)
- [This listing](https://clawhub.ai/superagnt/skills/heyreach-outreach)
