# Next-step tracker: track the next steps promised on sales calls

To make sure every promise made on a call is kept, record each one when it is made and close it only
on evidence. Every weekday morning this cookbook's agent reads the call log `call-capture` writes,
records each dated commitment either side made, closes the ones the activity log shows were kept,
and posts what is due or overdue to one locked Slack channel, at most once a day.

```sh
cargo-ai project add cookbook/next-step-tracker
```

## What it does

- Reads `cadence/log/calls/` from the last 30 days, on the default branch.
- Records every specific, dated commitment (ours and theirs), quoted, once per entry and promise.
- Closes a commitment only when an email, meeting, note or task in the `gtm_activities` model, or a later call
  entry,
  plainly shows it happened, and cites that record.
- Posts the open ones due today or overdue, grouped by owner, then marks them nudged.
- Writes nothing to the repository and nothing to the evidence models.

## What's inside

Adds 9 resources.

| File                            | Resource                        | Role                                                         |
| ------------------------------- | ------------------------------- | ------------------------------------------------------------ |
| `infra/agents/tracker.ts`       | `defineAgent` (claudeCode)      | the cron, the repository binding, the reads, the locked post |
| `infra/agents/tracker.prompt.ts` | (not a resource)               | extract, close on evidence, post what is due                 |
| `infra/models/commitments.ts`   | `defineModel` (native)          | the ledger: one row per promise                              |
| `infra/connectors/git.ts`       | `defineConnector` (`github`)    | the clone path; read only                                    |
| `infra/models/gtm-activities.ts`    | `defineModel` (native)          | the evidence a promise was kept; read-only                   |
| `infra/models/gtm-accounts.ts`      | `defineModel` (native)          | who owns each account; read-only                             |
| `infra/connectors/slack.ts`     | `defineConnector` (`slack`)     | the post path                                                |
| `infra/connectors/anthropic.ts` | `defineConnector` (`anthropic`) | the model the harness runs on                                |
| `infra/folders/index.ts`        | `defineFolder` ×2               | where the agent and the model are filed                      |
| `references/nudge.md`           | (not a resource)                | the message shape and the rule for each line                 |

## Why state in a model and not in the repository

The call entries are call-capture's record, reviewed through pull requests. Ticking their
checkboxes would rewrite that record and open a pull request every morning for the tracker's own
bookkeeping. What changes daily (open, done, nudged today) lives in the `commitments` model, where
it can be queried and corrected without a review.

## Why native models and not a CRM

The example has as few dependencies as it can: the evidence is two native models declared in this
folder, filled by whatever already logs the team's activity. A team on HubSpot, Salesforce or
Attio replaces them with connector-backed models of the same slugs (`crm-backed` in `SKILL.md`);
the agent and its prompt do not change, and no CRM action is ever added to the agent.

## Placeholders (edit before deploy)

1. **`channelId`** in `infra/agents/tracker.ts`: the Slack channel id the nudges land in.
2. **`TRACKER_TIMEZONE` and the cron**: keep the run after call-capture's.
3. **`languageModel`**: any Anthropic model the workspace's connector can reach.

## What it does not do

It does not contact customers, write to any model but its ledger, commit to the repository, or post anywhere but the
locked channel.
