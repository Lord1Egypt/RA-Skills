---
name: next-step-tracker
description: 'Track the next steps promised on sales calls and flag the overdue ones in Slack: every weekday morning each commitment made on a recorded call, by your team or the customer, is read from the call log, recorded once, closed when the activity log shows it was kept, and flagged once it falls due or goes overdue. Triggers: "track the next steps from our calls", "remind me when I promised something on a call", "what did we commit to and not do", "chase customer follow-ups we agreed on", "commitment tracker for sales calls", "flag overdue next steps in slack". Cargo project, defineAgent, harness claudeCode, call-capture entries, native models, Slack postMessage, ledger model; HubSpot, Salesforce or Attio as an adaptation. Skip when: you want calls written into the repository, which is call-capture; or a digest of everything that moved, which is standup.'
version: "0.2.0"
compatibility: "Requires @cargo-ai/cli 1.0.154 or later with @cargo-ai/cdk 1.0.150 or later (harness agents bound to the project's connected state, with `env` at the top level of `defineAgent`), a Cargo workspace, a GTM repository whose cadence/log/calls/ is written by call-capture (or by hand in the same shape), and authorized GitHub, Slack and Anthropic connectors. No CRM is required: the example reads activity from native models, and a CRM-backed model is a swap."
homepage: https://github.com/getcargohq/gtm-skills/tree/main/next-step-tracker
metadata:
  author: getcargo
  source: cookbook
  personas:
    - account-executive
    - sales-leadership
    - sales-development
  openclaw:
    requires:
      bins:
        - cargo-ai
    install:
      - kind: node
        package: "@cargo-ai/cli@latest"
        bins:
          - cargo-ai
    homepage: https://github.com/getcargohq/gtm-skills
---

# Next-step tracker

## The outcome

"We'll send that over by Thursday" stops being the sentence nobody remembers saying. Every weekday
morning one agent runs, and three things happen:

1. **New promises are recorded.** The agent reads the call entries under `cadence/log/calls/` (the
   ones `call-capture` writes) and records every specific commitment either side made, quoted, with
   a due date, in the `commitments` model. Same entry, same promise, one row forever.
2. **Kept promises are closed, on evidence.** For every open row it reads the `gtm_activities` model for an
   email, meeting, note or task on the account after the call that plainly matches the promise, or a
   later call entry that says it happened. It closes the row only on a match, and cites the record.
3. **Due promises are posted.** Open commitments due today or overdue go out in one Slack message,
   grouped by owner, overdue first. A customer's promise is posted as a follow-up for the rep to
   chase, not a task to do for them.

The repository is read and never written: no pull request to review every morning. The evidence
models (`gtm_activities`, and `gtm_accounts` for who owns what) are read-only. Both are native, so the
example deploys with no CRM; a team on HubSpot, Salesforce or Attio swaps them for connector-backed
models (`crm-backed` below) and the prompt does not change. The only writes are the ledger and one
post a day to a channel locked on the action.

## Example

> Every weekday morning, tell #deal-desk which promises from our calls are due or overdue.

Illustrative output, fictional records:

```text
:hourglass: *Next steps due — Thu Oct 8*
*Dana Ruiz*
• Fabrikam: "Send the Globex migration one-pager to Priya" — you promised on Oct 1,
  due Oct 6 (2 days overdue). An email to Priya with the one-pager closes it.
• Northwind: "Legal will review the MSA by Friday" — they promised on Oct 2, due today.
  Follow up with Sam; nothing to do for them.
*Lee Park*
• Contoso: "Share the SOC 2 report" — you promised on Oct 6, due today. An email with
  the report attached closes it.
_Sources: cadence/log/calls/2026-10-01-fabrikam.md · cadence/log/calls/2026-10-02-northwind.md ·
cadence/log/calls/2026-10-06-contoso.md_
```

Eleven commitments were open; four closed overnight on logged activity, three were due and posted, and a
second run that morning posted nothing.

## Put it in your project

This folder is a **worked example**: real project resources written for some other company. The job is
to end up with the code your company would have written, in your project, and an agent does the
adapting. If the `cargo-project` skill is in your session it carries the long form of this; if not, this
is enough.

1. **Install it — the CLI does the copy.** From inside the project (the folder holding `cargo.json`),
   `cargo-ai project add cookbook/next-step-tracker` writes this example to `infra/next-step-tracker/`
   and this procedure to `.agents/skills/next-step-tracker/`. No project yet?
   `cargo-ai project init <dir> --cookbook next-step-tracker && cd <dir> && npm install` does both.
   **If you are reading this from the project's `.claude/skills/`, the install already happened —
   start at step 2.** On a CLI too old to have `add`, copy this folder in as a sibling of what is
   there by hand; everything below is unchanged.
2. **Reconcile it with what is already declared.** If the project already has a GitHub, Slack or
   Anthropic connector, or a `gtm_accounts` model, rewire the imports to the existing one and drop the copy; two
   resources with one slug is a collision at deploy.
3. **Check there is a call log to read.** `ls cadence/log/calls/` on the default branch. Empty means
   install `call-capture` first, or the tracker runs clean and finds nothing every morning.
4. **Point Slack at your channel.** Authorize the Slack connector if the workspace does not have one
   (`cargo-ai project add connector/slack`). Set `channelId` in `infra/agents/tracker.ts` to a channel
   id (`C…`) from that connector's channel autocomplete, and invite the bot.
   `references/nudge.md` (installed beside this file) is the message shape.
5. **Adapt.** Work the sections below in order: _What should not change_ is what you argue back
   about (say what breaks, then do it if they still want it); _What you can change_ is what you
   offer unprompted; _What you will be asked_ is the floor, and you derive before you ask. If you
   are asking more than about four questions you have skipped lookups. Record what you changed and
   why under a `## Decisions` section in your copy of this file.
6. **Check, then plan.** `node --import tsx evals/contract.mjs` from this skill's folder, then
   `npm run check && cargo-ai project plan` from the project root. Confirm `cargo-ai project check` prints
   the agent bound to your repository with no trailing subdirectory. Show the diff, and deploy only
   on an explicit yes: `cargo-ai project deploy`.
7. **Verify.** Send the agent its trigger text once by hand (`cargo-ai ai message create`), and walk
   _Done when_ line by line with evidence. Then send it again: the second run must add no row and
   post nothing.

## What you will be asked

**Derive before you ask.** An input with a lookup is looked up, not asked. Only the ones marked
_asked_ genuinely live in the operator's head.

| Input                                                     | Kind  | How it is answered                                                                                                                                                                             | Why it matters                                                                                                                                         |
| --------------------------------------------------------- | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| project binding (`infra/agents/tracker.ts`) | value | **derived**: leave `state` unset and deploy binds the project's connected state (`cargo.state.json`): its repository, directory and production branch. `cargo-ai project check` prints the binding; a project whose state is not connected deploys the agent unbound, with an empty sandbox.                              | It is the only place the call log is read from. A hand-written `owner/name` is the value nobody notices is wrong until every morning comes back empty. |
| call log path                                             | value | **derived**: `ls cadence/log/calls/` and read two entries. The prompt expects call-capture's shape: frontmatter with a date, and an Actions section of checkboxes.                                | A log in another folder or shape is read as empty, and an empty morning looks exactly like a team that kept every promise.                            |
| evidence source (`infra/models/gtm-activities.ts`, `gtm-accounts.ts`) | value | **derived**: `cargo-ai storage model list`. A project with a CRM-backed activities or gtm_accounts model uses `crm-backed`; otherwise the native models stay and something must fill `gtm_activities` (a sequencer webhook, a play, `cargo-ai storage record create-bulk`). | It is the only evidence a promise was kept besides a later call. An empty `gtm_activities` closes nothing, and the post grows every day until it is muted. |
| `channelId` (`infra/agents/tracker.ts`)                   | asked | the Slack channel id (`C…`) the nudges may land in, read from the connector's channel autocomplete. Invite the bot.                                                                             | Nudges quote what customers said on calls. Locked so they never land in a customer shared channel.                                                    |
| `TRACKER_TIMEZONE` and the cron (`infra/agents/tracker.ts`) | asked | the team's morning. Keep the cron after call-capture's, so yesterday's calls are in the log when the tracker reads it.                                                                          | A timezone that disagrees with the cron makes "due today" yesterday's list.                                                                           |
| LLM connector and model (`infra/connectors/anthropic.ts`) | value | **derived**: `cargo-ai connection connector list`. Any Anthropic model pairs with `claudeCode`; `languageModel` is a placeholder to set.                                                         | The harness runs against Cargo's LLM proxy, so this is what each morning is billed against. An `openAi` connector here typechecks and fails at deploy. |

Checked before moving on, not after the deploy:

- `cadence/log/calls/` on the default branch holds at least one entry with an unchecked action
- `cargo-ai project check` prints `agent:commitment_tracker bound to <your repo>#<branch>` with no
  trailing subdirectory
- `channelId` is a `C…` id the Slack connector can see, and the bot is in that channel
- `node --import tsx evals/contract.mjs` passes

## What you can change

| Variation         | When it is right                                                      | How                                                                                                                         | What it costs                                                                                                                                        |
| ----------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ours-only`       | The team only wants to see what it promised                           | In §1 of `infra/agents/tracker.prompt.ts`, record only commitments with `promised_by` "us"                                  | A customer's "legal will review by Friday" is the commitment most often lost, and it is the one a rep has to chase. Dropping it hides stalled deals. |
| `default-windows` | Your team's follow-up rhythm is not seven days for us, fourteen for them | Change the two fallbacks in §1 of the prompt                                                                                | Only promises with no date said on the call use them. Too short and the post fills with things that were never late.                                 |
| `quiet-day-line`  | Silence on a clear day reads as a missed run                           | In §3 of the prompt, post one "Nothing due today" line instead of nothing                                                  | One more message a day in the channel. The default is silence because a nudge channel nobody needs to read is the one that gets muted.               |
| `per-rep-dm`      | Each rep wants their own list                                          | One `postMessage` use per rep with its channel locked, and a map from owner to use in §3                                   | Every rep added is a deploy. Never unlock the channel to let the agent find a DM itself.                                                              |
| `crm-backed`      | The emails, meetings, notes and tasks already live in HubSpot, Salesforce or Attio | Replace `infra/models/gtm-activities.ts` and `gtm-accounts.ts` with connector-backed models (`fetchRecords`, every column, scheduled sync) of the CRM's engagements and companies, keep the slugs, and map the CRM's columns onto `account_id`, `opportunity_id`, `contact_id`, `occurred_at`, `kind`, `subject`, `body` and `owner_email` in the prompt's §2 query. Keep both read-only on `uses` | One more connector and a sync on a schedule. Evidence is as fresh as the last sync, so schedule it before the tracker's cron or a promise kept yesterday afternoon is nudged this morning. Never add CRM actions to the agent instead |
| `reach-back`      | The log has more than 30 days of open promises worth chasing          | Widen the window in §1                                                                                                      | Backfilled promises arrive overdue all at once. Prefer letting call-capture's STALE-CHECK prefix keep old ones out.                                 |

## What should not change

- **A commitment closes only on cited evidence.** (`infra/agents/tracker.prompt.ts` §2) A row
  closed on a guess vanishes from the post and from everyone's mind, and nobody finds out until the
  customer asks. "Probably sent" stays open.
- **The ledger is the memory, and it is written after the post.** (`infra/agents/tracker.prompt.ts`
  §1 and §3) `commitment_id` is the entry path plus the promise, so an entry is never re-extracted;
  `last_nudged_on` is set after the post succeeds, so a failed post is retried and a re-run posts
  nothing.
- **The repository is read, never written.** (`infra/agents/tracker.prompt.ts`, Rules) Ticking
  checkboxes in the call entries would rewrite call-capture's record and open a pull request every
  morning that someone has to merge for the tracker's own state. State that changes daily belongs in
  a model.
- **The evidence is read-only.** (`infra/agents/tracker.ts`) `gtm_activities` and `gtm_accounts` are on
  `uses` with `readOnly: true`. A tracker that can write the evidence can close its own commitments,
  and a CRM write action added for "convenience" creates tasks a rep spends the morning deleting.
- **`channelId` is locked on `postMessage`.** (`infra/agents/tracker.ts`) The post quotes customers.
  A channel the agent picks is how one quote lands in front of the customer who said it.
- **Promises are quoted, not paraphrased.** (`infra/agents/tracker.prompt.ts` §1) A paraphrase is
  how a rep gets chased for something nobody promised.

## Done when

- `node --import tsx evals/contract.mjs` passes
- `cargo-ai project plan` reports the agent, the `commitments`, `gtm_activities` and `gtm_accounts` models, the
  three connectors and the two folders
- the first run recorded one row per unchecked action in the last 30 days of call entries, each with
  a quoted promise, a due date and its source entry
- to test without a CRM, seed `gtm_activities` (and a `gtm_accounts` row per test account) with
  `cargo-ai storage record create-bulk --model-uuid <uuid> --records '[{"data":{…}}]'`, the model
  uuid read from `cargo-ai storage model list`
- every row it closed cites a `gtm_activities` row or a later call entry that plainly matches the
  promise, and a seeded activity that does not match closed nothing
- one message landed in the locked channel listing only open rows due today or earlier, grouped by
  owner, with every source entry on the last line
- a second run the same morning added no row and posted nothing
- a promise the customer made is phrased as a follow-up to chase, not a task to do
- `git log` on the default branch shows no commit and no pull request from the tracker

## What it costs

The evidence reads are SQL over workspace models and bill nothing. The post is `slack.postMessage`
on the bound connector; immediately before the plan, run
`cargo-ai orchestration action list postMessage --kind connector --integration-slug slack` and read
the current cost out loud. The recurring cost is the harness run itself, once each weekday, billed as
LLM tokens through the Anthropic connector. It scales with the number of call entries in the window
and open commitments to check, not with the size of the activity log, and the run posts at most once.

## Composes into

`call-capture` (the call log it reads), and `standup` (the evening recap can cite what closed today).
