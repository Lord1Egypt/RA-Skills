// The invariants under "What should not change", checked against the compiled
// graph rather than the source. Run it from the skill folder after every
// adaptation:
//   node --import tsx evals/contract.mjs
//
// It loads through `loadResources`, the same loader `cargo-ai project check`,
// `plan`, and `deploy` use, so what is asserted here is what would deploy.
import assert from "node:assert/strict";
import { loadResources } from "@cargo-ai/cdk";

const infraDir = new URL("../infra", import.meta.url).pathname;
const byId = new Map(
  (await loadResources(infraDir)).map((resource) => [resource.id, resource]),
);

// Slack is the only destination the template declares. A CRM connector is the
// `crm_routing` or `crm_lookup` variation, added on purpose with its own
// checks (references/crm-adaptation.md), never left behind by accident.
assert.deepEqual(
  [...byId.keys()].filter((id) => id.startsWith("connector:")).sort(),
  [
    "connector:anthropic",
    "connector:linkedin",
    "connector:sales_navigator",
    "connector:slack",
  ],
  "the template binds Sales Navigator, LinkedIn, the LLM and Slack, and nothing else",
);
assert.equal(
  [...byId.keys()].some((id) => id.startsWith("context:")),
  false,
  "this skill must not declare defineContext: the context is a per-workspace singleton the project owns",
);

// The source: a Sales Navigator job-change search, capped per URL, shipped as
// the pilot.
const model = byId.get("model:new_hires");
assert.ok(model, "model:new_hires must exist");
assert.equal(model.spec.extractorSlug, "fetchLeadSearch");
const urls = [model.spec.config.urls].flat();
assert.ok(urls.length > 0, "the model must carry at least one search URL");
for (const url of urls) {
  for (const filter of [
    "RECENTLY_CHANGED_JOBS",
    "YEARS_AT_CURRENT_COMPANY",
    "YEARS_IN_CURRENT_POSITION",
  ]) {
    assert.ok(
      url.includes(`type:${filter}`),
      `every search URL must keep ${filter}, or internal promotions read as new hires`,
    );
  }
}
assert.ok(
  model.spec.config.limit <= 2500,
  "limit is per URL and Sales Navigator returns at most 2,500 per search",
);
assert.equal(
  model.spec.schedule,
  undefined,
  "the model must not carry a schedule: the cadence is added when opening up, and deleting a live one does not clear it",
);

const play = byId.get("play:route_new_hires");
assert.ok(play, "play:route_new_hires must exist");
assert.equal(play.spec.isEnabled, false, "the play must ship disabled");
assert.equal(play.spec.runCreationRule, "noConcurrency");
assert.deepEqual(
  play.spec.changeKinds,
  ["added"],
  "only people new to the search may create runs, or every sync re-posts the market",
);
assert.equal(
  play.spec.filter,
  undefined,
  "the search is the audience; a play filter restating it is a drift trap",
);

const nodes = play.spec.nodes;
assert.ok(Array.isArray(nodes), "the play must compile to workflow nodes");
const byUuid = new Map(nodes.map((node) => [node.uuid, node]));
const childrenOf = (node) =>
  node.childrenUuids.map((uuid) => (uuid ? byUuid.get(uuid) : undefined));
const parentOf = (node) =>
  nodes.find((candidate) => candidate.childrenUuids.includes(node.uuid));
const ancestorsOf = (node) => {
  const out = [];
  for (let parent = parentOf(node); parent; parent = parentOf(parent))
    out.push(parent);
  return out;
};
const isEnd = (node) => node?.kind === "native" && node.actionSlug === "end";
const isBranch = (node) =>
  node?.kind === "native" && node.actionSlug === "branch";
const findOne = (predicate, message) => {
  const matches = nodes.filter(predicate);
  assert.equal(matches.length, 1, message);
  return matches[0];
};

// Enrich first, then stop when there is no domain.
const start = findOne(
  (node) => node.kind === "native" && node.actionSlug === "start",
  "one start node",
);
const enrich = childrenOf(start)[0];
assert.equal(enrich?.integrationSlug, "linkedin");
assert.equal(enrich.actionSlug, "enrichCompany");
const domainGuard = childrenOf(enrich)[0];
assert.ok(
  isBranch(domainGuard),
  "the company enrichment must be followed by the domain guard",
);
assert.match(domainGuard.config.condition.expression, /domain/);
const [guardThen, guardElse] = childrenOf(domainGuard);
assert.ok(isEnd(guardThen), "a company with no domain must end the run");

// The qualifier judges every company, and its verdict gates the post.
const agent = findOne(
  (node) => node.kind === "agent",
  "exactly one agent: the qualifier",
);
assert.equal(agent.agentUuid?.resourceId, "agent:new_hire_icp_qualifier");
assert.equal(
  guardElse?.uuid,
  agent.uuid,
  "the qualifier must follow the domain guard",
);
const gate = childrenOf(agent)[0];
assert.ok(isBranch(gate), "the qualifier must be followed by its gate");
assert.match(gate.config.condition.expression, /is_icp/);
assert.ok(
  childrenOf(gate).some(isEnd),
  "a company the ICP rejects must end the run without a post",
);

// One Slack post per qualified person, to one locked channel.
const post = findOne(
  (node) =>
    node.kind === "connector" &&
    node.integrationSlug === "slack" &&
    node.actionSlug === "postMessage",
  "exactly one Slack post",
);
assert.ok(
  ancestorsOf(post).includes(gate),
  "the Slack post must sit behind the ICP gate",
);
assert.equal(
  typeof post.config.channelId,
  "string",
  "the channel must be locked on the post, not computed per run",
);

// Ends at the Slack post: no CRM write, and nothing sent to the person.
assert.equal(
  nodes.some(
    (node) =>
      node.kind === "connector" &&
      node.integrationSlug !== "linkedin" &&
      node.integrationSlug !== "slack",
  ),
  false,
  "the template reads LinkedIn and posts to Slack; CRM writes are the crm_routing variation",
);
assert.equal(
  nodes.some((node) =>
    /send|sequence|enroll|email/i.test(String(node.actionSlug)),
  ),
  false,
  "the play stops at the Slack post: nothing is drafted to or sent to the person",
);

console.log("ok: new-hire-detection contract holds");
