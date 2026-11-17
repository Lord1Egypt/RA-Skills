import assert from "node:assert/strict";
import { resetRegistry, resources } from "@cargo-ai/cdk";

// The boundaries schema validation cannot express, checked against the
// compiled registry. `cargo-ai project check` proves the resources are well formed;
// this proves they are still the pipeline this skill describes after an agent
// has adapted them.
//
// Run it from the skill folder after every adaptation:
//   node --import tsx evals/contract.mjs
resetRegistry();
const stamp = Date.now();
await import(`../infra/agents/goal-coverage.ts?contract=${stamp}`);
await import(`../infra/connectors/git.ts?contract=${stamp}`);
await import(`../infra/connectors/anthropic.ts?contract=${stamp}`);

const byId = new Map(resources().map((resource) => [resource.id, resource]));

const findOne = (nodes, predicate, message) => {
  const matches = nodes.filter(predicate);
  assert.equal(matches.length, 1, message);
  return matches[0];
};

assert.ok(byId.get("connector:github"), "defineConnector(github) must exist: the coverage file lands as a pull request");
assert.ok(byId.get("connector:slack"), "defineConnector(slack) must exist");

const agent = byId.get("agent:goal_coverage");
assert.ok(agent, "defineAgent(goal_coverage) must exist");
assert.equal(
  agent.spec.harnessSlug,
  "claudeCode",
  "goal-coverage must be a Claude Code harness agent: its memory is a file in the repository",
);

// The harness runs against Cargo's LLM proxy, and the proxy is selected by the
// connector's integration: `claudeCode` with anything but `anthropic`
// typechecks green and fails at deploy.
const llm = byId.get("connector:anthropic");
assert.ok(llm, "defineConnector(anthropic) must exist: the harness needs a model");
assert.equal(
  llm.spec.integrationSlug,
  "anthropic",
  "claudeCode is proxied to Anthropic: an openAi connector deploys broken",
);
assert.ok(
  agent.spec.connectorUuid,
  "goal-coverage must bind the LLM connector: the harness does not bring its own model",
);
assert.equal(
  typeof agent.spec.languageModelSlug,
  "string",
  "goal-coverage must name a languageModel: it is what the weekly run is metered against",
);
assert.equal(
  (agent.spec.tools ?? []).length,
  0,
  "goal-coverage must not wrap the CLI or Slack in a tool",
);

// What is deployed is read with the cargo-ai CLI the harness checkout already
// has, and the prompt holds those reads to read-only. A capability would be a
// second path to the same data that no prompt line can narrow, and the one
// that could install what it suggests.
assert.equal(
  (agent.spec.capabilities ?? []).length,
  0,
  "goal-coverage needs no capability: the read path is the cargo-ai CLI in the sandbox",
);

// The sandbox's Cargo session is a viewer service user, never the deployer.
// Without `runAs` the CLI has no session and every workspace read fails; with a
// broader role a prompt that is ignored can deploy or change resources.
assert.ok(
  agent.spec.runAsUserUuid,
  "goal-coverage must run as a service user (runAs): the sandbox needs a Cargo session",
);
const user = byId.get("user:goal_coverage");
assert.ok(user, "defineUser(goal_coverage) must exist");
assert.equal(user.spec.kind, "service", "goal_coverage must be a service user");
const role = byId.get("role:viewer");
assert.ok(role?.spec.adopt === true, "goal_coverage must hold the adopted viewer system role");

const actions = agent.spec.connectorActions ?? [];
assert.equal(
  actions.length,
  1,
  "goal-coverage has exactly one connector action: the Slack post",
);
const post = findOne(
  actions,
  (action) => action.integration === "slack" && action.actionSlug === "postMessage",
  "goal-coverage must use slack.postMessage",
);
assert.equal(
  typeof post.config?.channelId,
  "string",
  "channelId must be locked on the postMessage use, not left for the agent to pick",
);
assert.notEqual(post.config.channelId, "", "channelId must not be empty");
assert.equal(post.config.format, "markdown", "format must be locked to markdown");

findOne(
  agent.spec.triggers ?? [],
  (trigger) => trigger.type === "cron" && typeof trigger.cron === "string",
  "goal-coverage must have a cron trigger",
);

const env = agent.spec.env ?? [];
const envKeys = new Set((Array.isArray(env) ? env : []).map((entry) => entry.key));
assert.equal(
  envKeys.has("COVERAGE_GOAL"),
  true,
  "env must carry COVERAGE_GOAL: it is the goal for a project with no plan/company-plan.md",
);

console.log("ok: goal-coverage contract");
