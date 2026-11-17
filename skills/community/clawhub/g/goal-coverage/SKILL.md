---
name: goal-coverage
description: 'Find what your goal needs that the workspace has not built: once a week a deployed agent reads the company goal, takes stock of every play, agent, model and connector in the workspace, and suggests at most five missing pipelines from the published catalog, each opened with what it noticed ("thousands of accounts, none scored"), as a pull request you can decline lines in and a Slack post. Triggers: "what should we be running", "what are we missing for our goal", "suggest new plays for our goal", "which pipelines should we set up next", "we have 25 plays and do not know which 5 matter", "tell us what to build, do not wait to be asked". Cargo project, defineAgent, harness claudeCode, catalog.json, plan/company-plan.md, Slack. Skip when: you want existing initiatives graded against last week''s runs, which is weekly-planning; or something deployed is failing, which is workspace-health.'
version: "0.2.0"
compatibility: "Requires @cargo-ai/cli 1.0.154 or later with @cargo-ai/cdk 1.0.150 or later (harness agents bound to the project's connected state, with `env` and `runAs` at the top level of `defineAgent`). Also needs a Cargo workspace, an authenticated Anthropic connector, a Slack connector, and a GTM repository. The goal is read from plan/company-plan.md when it exists, otherwise from COVERAGE_GOAL on the agent."
homepage: https://github.com/getcargohq/gtm-skills/tree/main/goal-coverage
metadata:
  author: getcargo
  source: cookbook
  personas:
    - sales-leadership
    - revops
    - gtm-engineering
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

# Goal coverage

## The outcome

Nobody has to know the catalog to know what is missing. Once a week one agent compares the goal
with what the workspace runs and says, in the workspace's own numbers, what it noticed: "you have
4,200 accounts and no score on any of them". Each observation comes with the pipeline that fixes
it. Two things land:

1. **A coverage file**, `cadence/coverage/<YYYY-Www>.md`, in one pull request titled
   `[cadence] coverage YYYY-Www`. It holds the goal verbatim, what runs today, and at most five
   suggestions, each with a `status: open` line. To decline one, the reviewer changes that line
   to `status: declined: <reason>` before merging. That edit is the agent's memory: a declined
   suggestion stays out for four weeks, and one left open for three weeks is dropped as noise.
2. **A Slack post** of the same suggestions, linking the pull request, for the reader who never
   opens GitHub.

It never installs what it suggests. The install line is in the file, and running it is a human's
decision.

**What it is not.** It does not grade the work that already exists: whether the bets you have are
on track is `weekly-planning`, and whether a deployed play is failing is `workspace-health`. An
installed pipeline counts as covered, however badly it is going.

Three properties make it safe to run unattended:

- **The menu is fetched, never remembered.** The agent reads
  `https://raw.githubusercontent.com/getcargohq/gtm-skills/main/catalog.json` every run and
  suggests only names it finds there. If the fetch fails it suggests nothing.
- **Installed is decided by three signals, not a guess**: `infra/<name>/` in the checkout, a
  workspace folder named after the pipeline (every pipeline files its resources under one), or
  a deployed play or agent slug matching the name.
- **Read-only, then a pull request.** Every workspace read is a named `cargo-ai` list or an
  aggregate query. Its write paths are the pull request and one locked Slack channel.

## Example

> Every week, look at our goal and what we have running, and tell us which pipelines we are missing.

Illustrative output, fictional records:

```text
Goal coverage, 2026-W44: "Reach $8M ARR by 2026-12-31, up from $5.2M on 2026-06-30."

1. Outbound to mid-market is a third of the forecast and nothing tells you
   when to reach out: 1,840 tier A accounts, none watched for a new hire. Flag
   the week a tier A account hires the role you sell to (`new-hire-detection`).
2. Expansion is $1.1M of the plan and no account is watched for it: 312
   customers, no usage or seat signal on any. Flag the customers ready to grow
   (`expansion-signals`). Needs the HubSpot connector first.
3. Still missing, first suggested 2026-W42: every demo request answered on the
   page (`inbound-qualification`).

Decline or adopt in the pull request: github.example/acme/gtm/pull/212
```

Three suggestions where five were allowed, each opening on a number from the workspace, and the
scoring model declined in W43 is not among them.

## Put it in your project

This folder is a **worked example**: real project resources written for some other company. The job is
to end up with the code your company would have written, in your project, and an agent does the
adapting. If the `cargo-project` skill is in your session it carries the long form of this; if not, this
is enough.

1. **Install it: the CLI does the copy.** From inside the project (the folder holding `cargo.json`),
   `cargo-ai project add cookbook/goal-coverage` writes this example to `infra/goal-coverage/`
   and this procedure to `.agents/skills/goal-coverage/`. No project yet?
   `cargo-ai project init <dir> --cookbook goal-coverage && cd <dir> && npm install` does both.
   **If you are reading this from the project's `.claude/skills/`, the install already happened, so
   start at step 2.** On a CLI too old to have `add`, copy this folder in as a sibling of what is
   there by hand; everything below is unchanged.
2. **Reconcile it with what is already declared.** If the project already has an Anthropic,
   GitHub or Slack connector, rewire the imports to the existing one and drop the copy; two
   resources with one slug is a collision at deploy.
3. **Adapt.** Work the sections below in order: _What should not change_ is what you argue back
   about; _What you can change_ is what you offer unprompted; _What you will be asked_ is the
   floor, and you derive before you ask. Record what you changed and why under a `## Decisions`
   section in your copy of this file.
4. **Check, then plan.** `node --import tsx evals/contract.mjs` from this skill's folder, then
   `npm run check && cargo-ai project plan` from the project root, show the diff, and deploy only on
   an explicit yes: `cargo-ai project deploy` (or merge, where a merge deploys). Never
   `cargo-ai project init --force` into a non-empty directory.
5. **Verify.** Run the agent once without waiting for Tuesday, then walk _Done when_ line by line
   and report each with evidence.

## What you will be asked

**Derive before you ask.** Only the rows marked _asked_ genuinely live in the operator's head.

| Input | Kind | How it is answered | Why it matters |
| --- | --- | --- | --- |
| the goal | value | **derived** when `plan/company-plan.md` exists: the agent reads its "## The one goal" section. **asked** only when it does not: one sentence with a number and a date, set as `COVERAGE_GOAL` in `infra/agents/goal-coverage.ts`. | Every suggestion is ranked against it and quotes it. A goal without a number ("grow pipeline") cannot rank anything, so ask for the number. |
| Slack channel (`infra/agents/goal-coverage.ts`) | value | **asked**: which channel the revenue leader reads. Resolve the name to its `C…` id with the Slack connector's channel autocomplete, never type an id. | Locked on the use so the agent cannot post internal suggestions into a customer channel. |
| project binding | value | **derived**: leave `state` unset and deploy binds the project's connected state (`cargo.state.json`): its repository, directory and production branch. `cargo-ai project check` prints the binding; a project whose state is not connected deploys the agent unbound, with an empty sandbox. | It is where the coverage file lands and where next week's memory is read from. |
| service user (`infra/users/index.ts`) | value | **derived**: `goal_coverage`, a service user on the adopted `viewer` system role. Deploying creates it; the deploying user's own role must cover viewer. If the project already adopts `viewer`, import that role instead of declaring it twice. | Every run's `cargo-ai` session. Without it the sandbox has no session and every workspace read fails. Viewer reads folders, plays, agents, models and connectors but cannot deploy or change a resource. |
| Anthropic, GitHub, Slack connectors | value | **derived**: `cargo-ai connection connector list`; add a missing one with `cargo-ai project add connector/<name>`. All three are `default: true` because a deploy cannot mint an OAuth grant. | The model the run is billed against, the pull request path, and the post. |

## What you can change

| Variation | When it is right | How | What it costs |
| --- | --- | --- | --- |
| `fewer` | The team acts on one or two things at a time | Change "at most five" in step 5 of `infra/agents/goal-coverage.prompt.ts` | The third most important gap waits a week longer to be said. |
| `slack-only` | Nobody on the team reviews pull requests | Drop steps 6 and 7 of the prompt, keep step 8 | No memory: a declined suggestion comes back every week, which is what makes people mute the channel. Keep the pull request if anyone can merge it. |
| `monthly` | The workspace changes slowly | Change the cron to `0 15 1-7 * 2` (first Tuesday) | A new catalog pipeline or a goal change waits up to a month to be noticed. |
| `with-ideas` | You want ideas beyond the catalog | Raise the `Idea:` allowance in step 5 above one | Ideas have no install line and no deploy-verified example behind them; they are the suggestions most likely to be wrong. |

## What should not change

- **The sandbox runs as a viewer service user.** (`infra/users/index.ts`) With no `runAs` the
  `cargo-ai` session is missing and every workspace read fails; with a broader role a prompt that
  is ignored can deploy or edit a resource.
- **It suggests only what the fetched catalog lists.** (`goal-coverage.prompt.ts` §3) A pipeline
  named from memory may have been renamed or removed, and the install line then fails on the one
  command the reader was persuaded to run.
- **It never installs, deploys or enables anything.** (`goal-coverage.prompt.ts` §2, Never) The
  suggestion is a sentence; the install is a decision with a cost the agent does not see (a
  connector to authorize, credits on every run).
- **Every observation carries a number it read.** (`goal-coverage.prompt.ts` §5) "You may want
  scoring" is a pitch; "4,200 accounts, none scored" is a finding. A number it did not read is
  worse than none, because the reader repeats it.
- **Installed is covered, however badly it is going.** (`goal-coverage.prompt.ts` §1) Grading
  existing work is weekly-planning's and workspace-health's job. Do it here too and the same
  failing play is reported three times by three agents.
- **The decline memory is the coverage file.** (`goal-coverage.prompt.ts` §4) Drop the pull
  request and a declined suggestion returns every Tuesday until someone mutes the post.

## Done when

- `node --import tsx evals/contract.mjs` passes: a `claudeCode` harness bound to an Anthropic
  connector and a model, `runAs` a viewer service user, no capability, exactly one connector action (`slack.postMessage` with the
  channel locked), and a `COVERAGE_GOAL` env entry
- `cargo-ai project plan` reports the agent, its folder, and the three connectors
- the first run opened one unmerged pull request titled `[cadence] coverage <YYYY-Www>` whose diff is
  exactly `cadence/coverage/<YYYY-Www>.md`, with the goal quoted verbatim and at most five
  suggestions, each ending `status: open`
- no suggestion names a pipeline that is installed by any of the three signals, or one that is not in
  the catalog
- every observation's number appears in a read listed under `## Checked`
- the Slack post went to the locked channel, once, and links the pull request
- a second run the same week opened nothing and posted nothing
- after a suggestion was merged as `status: declined: <reason>`, the next week's run did not suggest it

## What it costs

The recurring cost is the harness run once a week, billed as LLM tokens through the bound Anthropic
connector. It scales with what the agent reads: the plan file, a few list commands, one or two
aggregate queries, the catalog, and up to eight earlier coverage files. The workspace reads are API
calls, not connector actions, so they bill nothing, and the run never executes an action that
spends. The Slack post is one connector action a week.

## Composes into

Whatever it suggests. Each suggestion's install line is `cargo-ai project add cookbook/<name>`,
and the next run counts that pipeline as covered. Pairs with `weekly-planning` (are the bets we
have on track) and `workspace-health` (is what we deployed broken).
