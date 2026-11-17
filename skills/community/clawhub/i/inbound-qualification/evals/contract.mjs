import assert from "node:assert/strict";
import { readdirSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { resetRegistry, resources } from "@cargo-ai/cdk";

// The boundaries schema validation cannot express, checked against the
// compiled registry. `cargo-ai project check` proves the resources are well formed;
// this proves they are still the inbound flow this skill describes after an
// agent has adapted them.
//
// Run it from the skill folder after every adaptation:
//   node --import tsx evals/contract.mjs
const resourceFiles = (dir) =>
  readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) return resourceFiles(path);
    return entry.name.endsWith(".ts") ? [path] : [];
  });

resetRegistry();
const stamp = Date.now();
for (const file of resourceFiles(
  fileURLToPath(new URL("../infra", import.meta.url)),
))
  await import(`${pathToFileURL(file).href}?contract=${stamp}`);

const all = resources();
const byId = (id) => all.find((resource) => resource.id === id);

// The shared models, exactly as every pipeline declares them.
const accounts = byId("model:gtm_accounts");
const contacts = byId("model:gtm_contacts");
assert.ok(
  accounts && contacts,
  "gtm_accounts and gtm_contacts must be declared",
);
assert.equal(accounts.spec.extractorSlug, "defineAccount");
assert.equal(accounts.spec.name, "GTM accounts");
assert.equal(contacts.spec.extractorSlug, "defineContact");
assert.equal(contacts.spec.name, "GTM contacts");
for (const column of contacts.spec.additionalColumns ?? [])
  assert.doesNotMatch(
    column.slug,
    /^cargo_/,
    "columns added to a shared model take plain names, never a cargo_ prefix",
  );

const tool = byId("tool:inbound_form");
assert.ok(tool, "defineTool(inbound_form) must exist");
assert.equal(
  tool.spec.folderUuid?.resourceId,
  "folder:inbound_qualification_tools",
  "the tool must be filed in the inbound_qualification_tools folder",
);

// The public form: on, for exactly the site's origin, no secret in code.
const form = tool.spec.publicForm;
assert.equal(form?.isEnabled, true, "the public form must be enabled");
assert.equal(
  form.allowedOrigins.length,
  1,
  "exactly one allowed origin: the site's",
);
assert.match(
  form.allowedOrigins[0],
  /^https:\/\/[a-z0-9.-]+$/i,
  "the allowed origin is the site's HTTPS origin, no path, no trailing slash, never *",
);
assert.ok(
  form.spam.captchaSecret === null ||
    /^\$\{[A-Z0-9_]+\}$/.test(form.spam.captchaSecret),
  "a CAPTCHA secret comes from env(), never a literal in the repository",
);
assert.ok(form.spam.minFillMillis > 0, "the time-trap stays on");

// The workflow: company enrichment, the two shared models, Slack. Nothing
// that looks a person up, and no write anywhere else.
const actions = tool.spec.nodes.filter((node) => node.actionSlug !== undefined);
const flow = new Set(["start", "end", "branch"]);
const allowed = new Set([
  "enrichCompanyFromDomain",
  "modelUpsert",
  "postMessage",
  ...flow,
]);
for (const node of actions)
  assert.ok(
    allowed.has(node.actionSlug),
    `the workflow calls ${node.actionSlug}: only company enrichment, the shared models and Slack`,
  );
const upserts = actions.filter((node) => node.actionSlug === "modelUpsert");
assert.deepEqual(
  upserts.map((node) => node.config.modelUuid?.resourceId).sort(),
  [accounts.id, contacts.id],
  "the workflow writes exactly gtm_accounts and gtm_contacts",
);
const contactUpsert = upserts.find(
  (node) => node.config.modelUuid.resourceId === contacts.id,
);
assert.match(
  JSON.stringify(
    contactUpsert.config.mappings.find((m) => m.columnSlug === "account_id"),
  ),
  /modelUpsert/,
  "the contact's account_id is read back from the account upsert, never invented",
);

// Every compiled expression is valid JavaScript. The body is parsed when the
// file loads but the expressions only run on a submission, so a construct the
// printer mangles (an index on a call result, `.split("@")[1]`, prints as
// `.1`) passes the typecheck and fails the first real submission.
const expressions = [
  ...JSON.stringify(tool.spec.nodes).matchAll(/\{\{(.*?)\}\}/g),
].map((match) => JSON.parse(`"${match[1]}"`));
for (const expression of expressions) {
  const code = expression.replace(/nodes\.[A-Za-z0-9_]+/g, "nodes");
  assert.doesNotThrow(
    () => new Function("nodes", `return (${code});`),
    `compiled expression is not valid JavaScript: ${expression.slice(0, 120)}`,
  );
}

// The form's fields are the workflow's input.
const fields = tool.spec.formFields.map((field) => field.slug ?? field.name);
for (const field of ["email", "first_name", "last_name", "consent"])
  assert.ok(fields.includes(field), `the form asks for ${field}`);

// The deep research: after the page has answered, never on the submission
// path. The form's workflow calls no agent, so the page answer pays for no
// model call and waits on no research.
assert.equal(
  tool.spec.nodes.filter((node) => node.kind === "agent").length,
  0,
  "the form's workflow must not call an agent: deep research runs in the play, after the page answers",
);

const research = byId("play:research_qualified_leads");
assert.ok(research, "definePlay(research_qualified_leads) must exist");
assert.equal(
  research.spec.isEnabled,
  false,
  "the research play ships disabled: enabling it is the last yes after a pilot",
);
assert.deepEqual(
  research.spec.changeKinds,
  ["added"],
  "the research play runs on rows entering the filter, not the whole table",
);
assert.equal(
  research.spec.modelUuid?.resourceId,
  contacts.id,
  "the research play runs on gtm_contacts",
);
const researchFilter = JSON.stringify(research.spec.filter);
assert.match(
  researchFilter,
  /"columnSlug":"custom__inbound_status","operator":"is","values":\["qualified"\]/,
  "only contacts the form qualified are researched",
);
assert.match(
  researchFilter,
  /"columnSlug":"custom__inbound_researched_at","operator":"isNull"/,
  "a contact already researched is never researched twice",
);
const researchActions = research.spec.nodes.filter(
  (node) => node.actionSlug !== undefined && !flow.has(node.actionSlug),
);
assert.deepEqual(
  researchActions.map((node) => node.actionSlug).sort(),
  ["modelCustomColumn", "postMessage"],
  "the research play writes the contact's columns and posts one note, nothing else",
);
const researchWrite = researchActions.find(
  (node) => node.actionSlug === "modelCustomColumn",
);
assert.equal(
  researchWrite.config.modelUuid?.resourceId,
  contacts.id,
  "the research lands on gtm_contacts",
);
assert.deepEqual(
  researchWrite.config.mappings.map((m) => m.columnSlug).sort(),
  [
    "inbound_brief",
    "inbound_rationale",
    "inbound_researched_at",
    "inbound_tier",
  ],
  "the research writes exactly its four columns, by bare slug",
);

const researcher = byId("agent:inbound_lead_researcher");
assert.ok(researcher, "defineAgent(inbound_lead_researcher) must exist");
assert.equal(
  (researcher.spec.models ?? []).length +
    (researcher.spec.connectorActions ?? []).length,
  0,
  "the researcher is a judge: no model and no connector action in reach, the play persists",
);

// The play's body is parsed like the tool's, and it failed a live run on a
// construct check and plan accept (optional chaining). Every compiled
// expression is valid JavaScript and uses none of `?.`, `??`.
const researchExpressions = [
  ...JSON.stringify(research.spec.nodes).matchAll(/\{\{(.*?)\}\}/g),
].map((match) => JSON.parse(`"${match[1]}"`));
for (const expression of researchExpressions) {
  assert.doesNotMatch(
    expression,
    /\?\.|\?\?/,
    `no optional chaining or nullish fallback in a workflow body: ${expression.slice(0, 120)}`,
  );
  const code = expression.replace(/nodes\.[A-Za-z0-9_]+/g, "nodes");
  assert.doesNotThrow(
    () => new Function("nodes", `return (${code});`),
    `compiled expression is not valid JavaScript: ${expression.slice(0, 120)}`,
  );
}

console.log("ok: inbound-qualification contract");
