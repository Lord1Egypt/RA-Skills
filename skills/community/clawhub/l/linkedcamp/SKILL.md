---
name: linkedcamp
description: LinkedIn automation and multi-channel outreach (LinkedIn + email) for GTM teams with LinkedCamp — build and launch campaigns, generate audience searches, author multi-step sequences, manage leads, work the unified inbox, set up AI reply agents, schedule LinkedIn posts and read campaign analytics. Use whenever the user mentions LinkedCamp, outreach campaigns, prospects, sequences, LinkedIn or Sales Navigator searches, or their outreach inbox.
homepage: https://www.linkedcamp.com/mcp
metadata:
  {
    "openclaw":
      {
        "emoji": "📣",
        "homepage": "https://www.linkedcamp.com/mcp",
      },
  }
---

# [LinkedCamp](https://www.linkedcamp.com/)

[LinkedCamp](https://www.linkedcamp.com/) drives LinkedIn and email outreach: campaigns, prospect sourcing,
multi-step sequences, a unified inbox and AI reply agents. Everything goes
through the hosted LinkedCamp MCP server, `https://mcp.linkedcamp.com/mcp`.
Treat it as the only source of truth for account data.

## 0. Make sure the tools are connected

OpenClaw exposes the server's tools as `linkedcamp__<tool>` — for example
`linkedcamp__whoami`, `linkedcamp__campaign_list`. This skill names tools
without the prefix.

If no `linkedcamp__*` tools are available, LinkedCamp is not connected yet. Do
not improvise with web requests or curl. Read `{baseDir}/references/setup.md`
and walk the user through it. Short version, run on the Gateway host:

```bash
openclaw mcp set linkedcamp '{"url":"https://mcp.linkedcamp.com/mcp","transport":"streamable-http","auth":"oauth"}'
openclaw mcp login linkedcamp
```

The login prints a URL; the user opens it and pastes their API key from
LinkedCamp → Settings → Integrations into LinkedCamp's own page.

**Never ask for the API key in chat**, and never write it into a command line,
config value or file yourself. If the user pastes one into the conversation
anyway, do not repeat it back; tell them to rotate it in Settings →
Integrations, because chat transcripts are stored.

## 1. Orient first

1. Call `whoami` once at the start of a conversation. `_derived` reports the
   plan, `isPro`, `permissions`, and which Pro-only steps are locked.
2. Call `reference` before authoring a sequence or filtering by a status or
   enum. The vocabulary is not guessable — campaign daily limits live under
   `campaginLimits`, spelled exactly that way.
3. Read before you write. Use ids returned by tools; never fabricate an id,
   metric, prospect, message or account state.
4. Say plainly whether something is a proposal, a saved draft, or a live change.

The server also publishes `mcp://guide/campaign-playbook`, the long-form build
flow, if resources are available to you.

## 2. Building a campaign

1. `campaign_create` — creates a DRAFTED campaign.
2. `search_url_build` — turns the described audience into a search URL. It
   generates job titles and keywords for basic LinkedIn and Sales Navigator
   searches. It **cannot** generate geography, industry, company size,
   seniority or years-in-role: Sales Navigator takes those only as its own
   numeric ids, which cannot be derived from a name. Ask the user to paste a
   URL with those filters set. Recruiter (`/talent/`) URLs always come from the
   user.
3. `campaign_set_source` — show the user the URL first; it decides who gets
   messaged.
4. `campaign_update` — sending account, schedule and daily limits. LinkedIn
   steps need `linkedAccountId`; EMAIL steps need `emailAccountIds`.
5. `flow_set` — writes the sequence from an ordered list of steps. This is the
   only tool that authors a sequence. `flow_from_template` applies a prebuilt
   one instead; `flow_get` reads back what is saved.
6. `campaign_get` — `_readiness.blockers` must be empty.
7. `campaign_launch` — only after the confirmation in section 5.

### Account and source must match

A campaign sends from exactly ONE LinkedIn account and may rotate across
SEVERAL mailboxes. Never choose either for the user: if
`linkedin_account_list` or `email_account_list` returns more than one, ask.
Only attach mailboxes when the user wants EMAIL steps.

Then ask whether that LinkedIn account has Sales Navigator, Recruiter, both or
neither — the API does not expose it.

- Neither: basic LinkedIn search URL. A `/sales/` URL will not work and
  `INMAILS` steps cannot run.
- Sales Navigator: `/sales/` search URL; `INMAILS` available.
- Recruiter: a `/talent/` URL from the user and an INMAILS-only sequence (no
  connect or ordinary message step), or a normal campaign from a basic search —
  ask which.

InMails also need credits to reach anyone who is not an Open Profile member.
Credits are not visible here. Without them roughly one InMail in seven lands
and the rest fall through to the next branch — raise this before launch.

### Do not copy from other campaigns

- Never start by duplicating. `campaign_duplicate` is only for when the user
  names a specific campaign to duplicate.
- Never reuse another campaign's **source URL**. `uniqueProfiles` skips anyone
  already held by another campaign, so two campaigns on one search split it and
  the second finds almost nothing.
- Never reuse another campaign's **tag**. Mint one with `tag_create`
  (`interest: "NEUTRAL"`, a short label from the campaign name). The reusable
  tags — Interested, Not Interested, Replied, Meeting Booked, Deal, Maybe —
  classify replies and do not belong in campaign settings.
- Never infer an **agent**. See section 3.

### Editing a sequence

To change a draft's copy, call `flow_set` again. Do **not** use
`sequence_update` on a draft: launching rebuilds every step from the saved flow
graph and silently reverts the edit. `sequence_update` is for ACTIVE or PAUSED
campaigns. `flow_set` on an ACTIVE campaign re-evaluates every lead and can
cancel or reschedule pending actions; `flow_audit` reports what moved.

## 3. Replies and AI agents

An agent attached to a campaign answers real prospects by itself, so never
attach one unprompted. Ask, and offer both routes:

- existing — `agent_list`, then `agent_get` to show its personality, intent and
  instructions so the user can judge the fit;
- new — `agent_upsert` with `isActive: false`, `kb_upsert` + `kb_attach` for
  source material, `agent_train`, then test with `agent_query` before it
  touches a real conversation.

No agent is a normal outcome: replies land in the inbox for a human.

For the inbox: `conversation_list` / `conversation_get` to read,
`message_draft_ai_reply` to draft. Present drafts as drafts.

## 4. Plan and permission gates

The server enforces these; a refusal is real and has no workaround. Pro and
Agency plans carry `isPro: true`; Turbo does not.

- Pro only: `persona_*`, connecting an email account, the `EMAIL`, `EVENT`,
  `GPT`, `FINDER` and `QUALIFIER` steps, the `If_Interested` and `CUSTOM`
  triggers, and `ENGAGEMENT.commentsToAdd`.
- Permission-scoped: `agent_*` and `kb_*` need `Agents`; `post_*` needs
  `Publish`; `QUALIFIER` also needs `Personas`.

Check `whoami._derived` before proposing any of these. If a tool refuses on
plan grounds, say so and stop.

## 5. Confirm before anything reaches people, changes live outreach, or destroys data

When the LinkedCamp plugin is installed, it pauses the run and asks the user to
approve **every** call listed in this section through OpenClaw's plugin
approvals: every tool the LinkedCamp server flags destructive, plus the
unflagged calls marked † below. That prompt is a backstop, not the
conversation: ask first anyway. With the skill alone there is no prompt at all
and **you** are the only safeguard — especially on a chat channel where the
user is typing on a phone. For each call: say exactly what will happen, show
the content and recipients, get an explicit "yes" in the conversation, and
never put several behind one yes. If the approval is denied or times out, stop
and say so; do not retry or look for another tool that does the same thing.

Reaches real people:

- `campaign_launch` — starts real outreach on the campaign's schedule. Show the
  audience URL and the full sequence first. Never bulk-launch.
- `campaign_set_status` with `ACTIVE` † — resumes a paused campaign; it may have
  been paused for a reason. Pausing needs no ceremony and is not gated.
- `message_send` — delivers immediately on LinkedIn or email and cannot be
  recalled. Show the exact text and recipient.
- `campaign_send_test_email` — a real email. Show recipient, subject and body.
- `post_upsert` — unless `status` is `DRAFTED` (private) or `REQUIRE_APPROVAL`
  (goes to a human reviewer), the post is queued to publish publicly. Show the
  exact post and when it goes out.
- `post_schedule_set` — replaces a weekday's publishing slots.
- `automation_upsert` with `isActive: true` † — runs against live events and can
  message people. Save it inactive while drafting.

Changes who is contacted or what live campaigns and agents say:

- `campaign_set_source`, `campaign_add_prospects` — decide who gets messaged.
  Show the URL.
- `flow_set` — replaces the sequence; on an ACTIVE campaign it re-evaluates
  every lead and can cancel pending actions. The prompt appears for drafts too,
  because the gate cannot see the campaign status — say so when the user is
  iterating on a draft.
- `sequence_update` — changes what a running campaign sends.
- `campaign_update` with `agentId` † — the agent will answer prospects by itself.
- `agent_upsert` unless `isActive: false`, `kb_upsert`, `persona_update`.
- `template_upsert`, `saved_reply_upsert`, `lead_note_update` — overwrite
  shared copy or notes. `activity_skip` — the scheduled action will not run.

Destroys or hides data — read `{baseDir}/references/safety.md` first:
`campaign_delete`, `lead_delete`, `lead_blacklist`, `message_delete`,
`agent_delete`, `kb_delete`, `persona_delete`, `tag_delete`,
`blacklist_delete`, `placeholder_delete`, `reminder_delete`, `holiday_delete`.

Not gated, because they only build drafts or read: creating and configuring a
campaign, adding leads, `post_upsert` with `DRAFTED`, agents and automations
saved inactive, and every read.

## 6. Agency sub-accounts

An agency owner can work on sub-accounts from their own connection.

1. Get ids from `subaccount_list` — never construct or guess a `userId`; a
   wrong id does not fail, it answers for a different account. An empty result
   means either no active sub-accounts or a non-owner key; say so.
2. Pass one as `userId` to `campaign_list`, `linkedin_account_list`,
   `email_account_list`, `analytics_campaign`, `analytics_reporting`,
   `tag_list`, or `agent_duplicate` (a write — name the client and confirm).

Record ids (`campaignId`, `leadId`, `conversationId`, `linkedAccountId`) from a
sub-account work on that sub-account, **including writes**. Say which account
you are about to change. When comparing accounts, label every number with its
account; nothing returns a combined roll-up.

## 7. Never invent a real-world value

Anything identifying something real — a profile or company URL (such as
`followCompanyUrl`), a search URL, an account id, a tag, a sender address, a
webhook endpoint — comes from the user or a read tool. Never from memory,
another campaign, or a plausible guess. These do not fail loudly: a wrong URL
sends real messages to the wrong people. If it is missing, stop and ask.

## 8. Out of scope

Not available, and rephrasing will not make them available: connecting a
LinkedIn account (it takes the LinkedIn password and a PIN — web app only),
CRM integrations, billing, team management, rotating the API key, reading
stored credentials, deleting saved replies or lead notes, archiving a
campaign, saving a raw flow graph, and deprecated webhooks (use automations).
Never ask for a LinkedIn password, session cookie or verification code. Point
the user to the [LinkedCamp](https://www.linkedcamp.com/) web app for these.

## 9. Responses

Ground summaries in tool results and keep observed data separate from
generated copy. When data is missing, stale or plan-restricted, say so and give
the next useful step. On chat channels keep answers short; offer detail rather
than dumping whole sequences unprompted — except before a launch or send, where
the user must see everything that will go out.

For a map of all toolsets, see `{baseDir}/references/tools.md`.
