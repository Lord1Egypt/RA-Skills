# Acceptance

Walk every line. A checked template without an evidence-backed consumer adaptation is incomplete.

## Before deploy

- `node --import tsx evals/contract.mjs` passes against the adapted graph.
- `cargo-ai project check` prints `agent:goal_coverage bound to <your repo>#<branch>` with no
  trailing `in infra/`.
- The goal resolves: `plan/company-plan.md` has a "## The one goal" section with a number and a
  date, or `COVERAGE_GOAL` is set on the agent.
- The Slack `channelId` is an id resolved through the connector's autocomplete, for a channel the
  reader actually reads.
- `curl -sf https://raw.githubusercontent.com/getcargohq/gtm-skills/main/catalog.json` works from
  the network the harness runs on.

## First run

- Exactly one unmerged pull request titled `[cadence] coverage <YYYY-Www>`; its diff is exactly
  `cadence/coverage/<YYYY-Www>.md`.
- The goal in the file is verbatim, and the file says where it was read from.
- At most five suggestions, each with an observation carrying a number, the pipeline name, why it
  moves this goal, the install line, and `status: open`.
- Cross-check against `ls infra/` and `cargo-ai workspaceManagement folder list`: no suggested
  pipeline is installed.
- Every suggested name exists in the fetched catalog. At most one `Idea:` line, with no install
  line.
- Re-run two numbers from `## Checked` by hand: they match.
- The Slack post went to the locked channel, once, and links the pull request.

## Second run, same week

- Opened nothing and posted nothing.

## After a decline

- Merge a file with one suggestion changed to `status: declined: <reason>`. Next week's run does
  not suggest it.
