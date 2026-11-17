# Acceptance

Walk every line before calling the pipeline done. Report each with its evidence: a command output,
a run link, or a Slack message link. A line that could not be checked is reported as unchecked, not
as passed.

## Search and approval

- [ ] The market (titles, industries, headcount, locations) came from the ICP in the workspace
      context, or was asked for because none existed and then written to `context/icp.md`.
- [ ] Every industry and region value is an id from the integration's autocompletes.
- [ ] Every title in `CURRENT_TITLE` is quoted, and the excluded words are listed.
- [ ] Every URL keeps `RECENTLY_CHANGED_JOBS`, `YEARS_AT_CURRENT_COMPANY` and
      `YEARS_IN_CURRENT_POSITION`.
- [ ] Each URL was counted with `searchPersonMetrics`, and each count is under 2,500 or the search
      was split by a facet that partitions the market.
- [ ] The live per-lead extraction price, the lookup time, and the cost of one sync were shown.
- [ ] The operator approved the search, the limit, the cadence and the cost per sync before any
      extraction.

## Destination

- [ ] `slackChannelId` is the id of the channel the operator named, resolved through the
      connector's autocomplete, and the Slack connector can post to it.
- [ ] If a CRM is connected, the CRM variations were offered with their cost, and the operator's
      answer is recorded under `## Decisions`.
- [ ] With a CRM variation: every check in `references/crm-adaptation.md` for it holds, and the
      contract was extended with its assertions.

## Template and compiled graph

- [ ] `node --import tsx evals/contract.mjs` passes, run from the skill folder.
- [ ] `cargo-ai project types`, `cargo-ai project check` and `cargo-ai project plan` pass in the consumer
      project.
- [ ] The plan shows one model with no schedule, one agent, one disabled play, and no duplicated
      connector or folder.
- [ ] The qualifier reads `icp.md` from the workspace context and has no CRM, Slack, or model in
      reach.

## Pilot of ten

- [ ] The first deploy used `limit: 10` and no schedule.
- [ ] Ten rows landed, and their columns match the workflow input.
- [ ] The play was enabled and executed once; every one of the ten has a run.
- [ ] Each run is reported with its status and verdict, and each `posted` run with its Slack
      message.
- [ ] Every post landed in the named channel and nowhere else.
- [ ] A `not_icp` run shows the qualifier's rationale and posted nothing.
- [ ] Any status the ten did not reach is named as unverified, or was run on a chosen record.

## Opening up

- [ ] The operator approved opening up after reading the pilot report.
- [ ] `limit` and the cadence were set to the approved values and redeployed.
- [ ] The next sync created runs only for people new since the previous one.
