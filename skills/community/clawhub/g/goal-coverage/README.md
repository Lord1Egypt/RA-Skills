# Goal coverage: what your goal needs that the workspace has not built

Once a week a Claude Code harness agent reads the company goal, takes stock of what the workspace
runs, and suggests at most five missing pipelines from the published catalog. Each suggestion opens
on what it noticed in the workspace's own numbers. They land as one pull request and one Slack
post.

```sh
cargo-ai project add cookbook/goal-coverage
```

## Why it is built this way

- **A harness agent, because the memory is a file.** A suggestion declined last week must not
  come back this week. The reviewer declines by editing a `status:` line in
  `cadence/coverage/<week>.md` before merging, and the next run reads those files. Only an agent
  with a working tree can write them, and only a pull request lets a human decline in writing.
- **Slack as well, because the reader is not always an engineer.** A revenue leader reads the post;
  whoever merges reads the pull request. Both carry the same suggestions.
- **The catalog is fetched every run.** New pipelines show up without a redeploy, and a pipeline
  that was renamed is never suggested under its old name.
- **Installed means any of three signals**: `infra/<name>/`, a workspace folder named after the
  pipeline (every cookbook files under one), or a matching play or agent slug. The folder
  convention is what makes the check cheap and reliable.
- **It does not grade existing work.** That is `weekly-planning` (are the bets on track) and
  `workspace-health` (is what we deployed broken). Three agents reporting the same failing play is
  how a team stops reading all three.
- **At most five.** A workspace can install twenty-five pipelines. The point is to say which five
  matter to this goal, in build order.

## Files

| File | What it is |
| --- | --- |
| `infra/agents/goal-coverage.ts` | the agent: weekly cron, harness, the locked Slack post, `COVERAGE_GOAL` |
| `infra/agents/goal-coverage.prompt.ts` | the contract: goal, reads, menu, memory, choice, file, PR, post |
| `infra/connectors/` | Anthropic, GitHub and Slack, all bound with `default: true` |
| `infra/folders/index.ts` | the agent folder, named after the cookbook |
| `evals/contract.mjs` | the boundaries schema validation cannot express |
| `evals/acceptance.md` | the walk-through after the first run |
