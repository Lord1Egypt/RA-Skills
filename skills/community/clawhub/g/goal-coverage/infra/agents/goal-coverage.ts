import { defineAgent } from "@cargo-ai/cdk";

import { goalCoveragePrompt } from "./goal-coverage.prompt";
import { anthropic } from "../connectors/anthropic";
import { slack } from "../connectors/slack";
import { agentsFolder } from "../folders";
import { goalCoverageUser } from "../users";

// Goal coverage: a Claude Code harness agent, not a streamText agent.
//
// The question it answers once a week is "what does our goal need that this
// workspace has not built?", and the answer has to be remembered: a scoring
// model suggested and declined last week must not come back next week. That
// memory is a file in the repository, cadence/coverage/<week>.md, edited by
// the reviewer before merging. Only an agent with a working tree can write it,
// and only a pull request lets a human decline a suggestion in writing.
//
// It does not grade the work that already exists. That is weekly-planning.
// The two run in different weeks of thought: planning asks whether the bets we
// have are on track, coverage asks which bets the goal needs that we have not
// placed.
//
// `connector` and `languageModel` are required even here. The harness does not
// bring its own model: it runs against Cargo's LLM proxy, which bills this
// connector and meters usage against this slug.
//
// Slack is a Cargo connector action on `uses`, with `channelId` locked: a
// mistyped channel would post internal suggestions into a customer channel.
//
// No `capabilities`, on purpose. What is deployed (plays, agents, models,
// connectors, folders) is read with Cargo's own CLI, which the harness already
// has, and only the prompt can say "read, never execute". The commands are
// listed in `goal-coverage.prompt.ts` §2. The CLI is signed in as the
// `goal_coverage` service user (`runAs`), a viewer: see `../users`.
export const goalCoverage = defineAgent("goal_coverage", {
  name: "Goal coverage",
  description:
    "Once a week, compares the company goal against what the workspace runs and suggests at most five pipelines it is missing, as a pull request and a Slack post.",
  color: "green",
  harness: "claudeCode",
  connector: anthropic,
  languageModel: "claude-sonnet-5", // PLACEHOLDER: your model of choice
  // No `state`: deploy binds this project's connected state (the one
  // cargo.state.json points at), and the harness clones its repository at the
  // state's directory and production branch. `cargo-ai project check` prints
  // the binding. A project whose state is not connected deploys this agent
  // unbound, with an empty sandbox and the plan note `unbound: this project's
  // state is not connected`; connect the project before relying on it.
  runAs: goalCoverageUser,
  env: {
    // PLACEHOLDER: the goal, in one sentence, for a project with no
    // plan/company-plan.md. Leave it empty when that file exists: the file
    // wins, because it is the version a human reviews.
    COVERAGE_GOAL: "",
  },
  uses: [
    {
      ref: slack.actions.postMessage,
      config: {
        // PLACEHOLDER: the channel suggestions land in. A Slack channel id
        // (C…), not a name. Locked so the agent cannot pick another one.
        channelId: "C0123456789",
        format: "markdown",
        disableUnfurling: true,
      },
    },
  ],
  triggers: [
    {
      type: "cron",
      name: "weekly",
      // 15:00 UTC Tuesday: the day after weekly-planning, so the two pull
      // requests never land in the same review.
      cron: "0 15 * * 2",
      text: "Run goal coverage. Follow your system prompt exactly: find the goal, read what is deployed, write this week's coverage file, open one pull request, post the suggestions.",
    },
  ],
  systemPrompt: goalCoveragePrompt,
  folder: agentsFolder,
});
