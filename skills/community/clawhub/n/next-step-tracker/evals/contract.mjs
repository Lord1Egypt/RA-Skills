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
await import(`../infra/agents/tracker.ts?contract=${stamp}`);
await import(`../infra/connectors/git.ts?contract=${stamp}`);

const byId = new Map(resources().map((resource) => [resource.id, resource]));

const findOne = (nodes, predicate, message) => {
  const matches = nodes.filter(predicate);
  assert.equal(matches.length, 1, message);
  return matches[0];
};

assert.ok(byId.get("connector:github"), "defineConnector(github) must exist: the harness clones through it");

const agent = byId.get("agent:commitment_tracker");
assert.ok(agent, "defineAgent(commitment_tracker) must exist");
assert.equal(
  agent.spec.harnessSlug,
  "claudeCode",
  "the tracker must be a Claude Code harness agent: its input is the call log in the repository",
);

// The harness runs against Cargo's LLM proxy, selected by the connector's
// integration: `claudeCode` with anything but `anthropic` deploys broken.
const llm = byId.get("connector:anthropic");
assert.ok(llm, "defineConnector(anthropic) must exist: the harness needs a model");
assert.equal(llm.spec.integrationSlug, "anthropic", "claudeCode is proxied to Anthropic");
assert.ok(agent.spec.connectorUuid, "the tracker must bind the LLM connector");
assert.equal(typeof agent.spec.languageModelSlug, "string", "the tracker must name a languageModel");

// The ledger is the tracker's only memory and its only write.
assert.ok(byId.get("model:commitments"), "defineModel(commitments) must exist");
const ledger = findOne(
  agent.spec.models ?? [],
  (model) => model.uuid?.resourceId === "model:commitments",
  "commitments must be on the tracker's uses",
);
assert.equal(ledger.readOnly, false, "the tracker records and closes commitments: the ledger must be writable");

// Evidence is read from native models in this folder. A writable evidence
// model is a tracker that can close its own commitments.
for (const slug of ["gtm_activities", "gtm_accounts"]) {
  assert.ok(byId.get(`model:${slug}`), `defineModel(${slug}) must exist: it is the evidence`);
  const use = findOne(
    agent.spec.models ?? [],
    (model) => model.uuid?.resourceId === `model:${slug}`,
    `${slug} must be on the tracker's uses`,
  );
  assert.equal(use.readOnly, true, `${slug} is evidence: it must be read-only`);
}

// The worked example has no CRM dependency. A team on a CRM swaps the native
// models for connector-backed ones; it does not add CRM actions to the agent.
const actions = agent.spec.connectorActions ?? [];
assert.equal(byId.has("connector:hubspot"), false, "the worked example declares no HubSpot connector");
assert.equal(
  actions.filter((action) => action.integration !== "slack").length,
  0,
  "the only connector action on the tracker is slack.postMessage",
);

const post = findOne(
  actions,
  (action) => action.integration === "slack" && action.actionSlug === "postMessage",
  "the tracker must use slack.postMessage",
);
assert.equal(typeof post.config?.channelId, "string", "channelId must be locked on the postMessage use");
assert.notEqual(post.config.channelId, "", "channelId must not be empty");
assert.equal(post.config.format, "markdown", "format must be locked to markdown");
assert.equal(
  actions.filter((a) => a.integration === "slack" && a.actionSlug !== "postMessage").length,
  0,
  "the ledger is the dedupe: no Slack history read on uses",
);
assert.equal((agent.spec.tools ?? []).length, 0, "no tool wraps an action the agent can call directly");

findOne(
  agent.spec.triggers ?? [],
  (trigger) => trigger.type === "cron" && typeof trigger.cron === "string",
  "the tracker must have one cron trigger",
);

const env = agent.spec.env ?? [];
const envKeys = new Set((Array.isArray(env) ? env : []).map((entry) => entry.key));
assert.equal(
  envKeys.has("TRACKER_TIMEZONE"),
  true,
  "env must carry TRACKER_TIMEZONE so due dates and the one post a day agree on today",
);

console.log("ok: next-step-tracker contract");
