# Run

Everything from an approved search to a pipeline running on its own. Nothing
here runs before the operator approved the search in
[`search.md`](search.md).

## Deploy for the pilot of ten

The first deploy is a pilot, not the pipeline, and the model ships as one:
`limit: 10` and no schedule in `infra/models/new-hires.ts`. Keep it that way.
Adding a schedule later is a plain redeploy; removing a live one is not (see
the model file).

Deploy with the play disabled, as it ships. Then:

1. Sync the model once and confirm ten rows landed, with
   `linkedin_profile_url` and `sales_navigator_company_url` filled:
   `cargo-ai storage column list` and a `storage query` over the model.
2. Enable the play, then execute it once: `changeKinds: ["added"]` does not
   backfill rows that landed while it was off.
3. Read every run, not a sample of them. For each of the ten, report the
   status, the qualifier's verdict, and the Slack post when there is one.

## What the pilot has to show

- at least one `posted` run, with its message in the channel the operator
  named and nowhere else
- one `not_icp` run with the qualifier's rationale, if the ten contain one;
  if all ten were posted, read the verdicts: a qualifier that passes everyone
  is usually reading no ICP
- `no_domain` runs, if any, named with the company that had no website
- with a CRM variation, one record through each route it adds, with the CRM
  record links

If a status never came up in the ten, say so rather than calling it verified,
and either widen the pilot or run that path on a hand-picked record.

### Stop conditions

- the sync reports success with zero rows: the URL was encoded once; rebuild
  it from the `search` object
- a post landed anywhere but the named channel: disable the play before
  anything else
- every verdict is the same: check that the qualifier reads `icp.md` from the
  workspace context

## Open it up

On an explicit yes after the pilot:

- set `limit` to the approved value per URL (at most 2,500)
- add the cadence the operator chose. The default is every two weeks, the 1st
  and the 15th: `schedule: { type: "cron", cron: "0 6 1,15 * *" }`. On demand
  means no schedule and a manual sync
- redeploy, then sync once. Only the people new since the pilot create runs

## Report

Per sync: people extracted, people added, runs by status, people posted,
companies the qualifier declined, and spend against the estimate. A sync that
added people and posted nothing is a failure to investigate, not a quiet week.

## Complete when

The pilot report was approved, the next sync after opening up created runs
only for people new since the previous one, and every line of _Done when_ in
SKILL.md is reported with its evidence.

## Links

Resolve `workspaceUuid` from `cargo-ai whoami` (`workspace.uuid`) and resource
UUIDs from `cargo.state.json`.

- model: `https://app.getcargo.io/workspaces/<workspaceUuid>/models/<modelUuid>`
- play: `https://app.getcargo.io/workspaces/<workspaceUuid>/plays/<playUuid>`
- qualifier: `https://app.getcargo.io/workspaces/<workspaceUuid>/agents/<agentUuid>`
