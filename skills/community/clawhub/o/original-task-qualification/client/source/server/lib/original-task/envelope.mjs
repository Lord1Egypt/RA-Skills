// Original-task text carried inside an existing correspondence event.
// A request is not a delivery promise, funded job, acceptance, or payment.

export const REQUEST_SCHEMA = "samedaydesk.original-task-request.v1";
export const DISPOSITION_SCHEMA = "samedaydesk.original-task-disposition.v1";
export const TEXT_MAX = 8000;

export class OriginalTaskError extends Error {
  constructor(code, status = 400) {
    super(code);
    this.name = "OriginalTaskError";
    this.code = code;
    this.status = status;
  }
}

function canonical(value) {
  if (Array.isArray(value)) return value.map(canonical);
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonical(value[key])]));
  }
  return value;
}

export function encodeOriginalTask(value) {
  const text = JSON.stringify(canonical(value));
  if (text.length > TEXT_MAX) throw new OriginalTaskError("oversized_task", 413);
  return text;
}

function exactKeys(value, keys, code = "invalid_task") {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new OriginalTaskError(code);
  const present = Object.keys(value).sort();
  const expected = [...keys].sort();
  if (present.length !== expected.length || present.some((key, index) => key !== expected[index])) {
    throw new OriginalTaskError(code);
  }
}

function assertNoCredential(value) {
  if (/bearer\s+\S{8,}/i.test(value) || /:\/\/[^/\s:@]+:[^/\s@]+@/.test(value)) {
    throw new OriginalTaskError("credential_refused");
  }
}

function boundedText(value, max, code = "invalid_task") {
  if (typeof value !== "string") throw new OriginalTaskError(code);
  if (value.length > max) throw new OriginalTaskError("oversized_task", 413);
  const trimmed = value.trim();
  if (!trimmed) throw new OriginalTaskError(code);
  assertNoCredential(trimmed);
  return trimmed;
}

function publicInput(value) {
  exactKeys(value, value?.kind === "https_url" ? ["kind", "url"] : ["kind", "example"], "invalid_public_input");
  if (value.kind === "https_url") {
    let url;
    try { url = new URL(value.url); } catch { throw new OriginalTaskError("invalid_public_input"); }
    if (value.url.length > 2048 || url.protocol !== "https:" || url.username || url.password) {
      throw new OriginalTaskError("invalid_public_input");
    }
    return { kind: "https_url", url: url.toString() };
  }
  if (value.kind === "nonsecret_example") {
    return { kind: "nonsecret_example", example: boundedText(value.example, 1500, "invalid_public_input") };
  }
  throw new OriginalTaskError("invalid_public_input");
}

export function taskRequest(input) {
  exactKeys(input, ["objective", "publicInput", "usefulOutput", "friction"]);
  const task = {
    schema: REQUEST_SCHEMA,
    objective: boundedText(input.objective, 500),
    publicInput: publicInput(input.publicInput),
    usefulOutput: boundedText(input.usefulOutput, 500),
    friction: boundedText(input.friction, 500),
    exampleConsent: false,
  };
  return { task, text: encodeOriginalTask(task) };
}

export function withdrawalText() {
  return encodeOriginalTask({ schema: REQUEST_SCHEMA, disposition: "withdrawn" });
}

export function consentText() {
  return encodeOriginalTask({ schema: REQUEST_SCHEMA, disposition: "example_consent", exampleConsent: true });
}

export function dispositionShape(text) {
  if (typeof text !== "string" || text.length > TEXT_MAX) return false;
  let value;
  try { value = JSON.parse(text); } catch { return false; }
  if (!value || typeof value !== "object" || Array.isArray(value)) return false;
  if (value.schema !== DISPOSITION_SCHEMA) return false;
  return value.disposition === "useful_refusal" || value.disposition === "scoped_result";
}

export function dispositionRequest(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) throw new OriginalTaskError("invalid_disposition");
  if (input.disposition === "useful_refusal") {
    exactKeys(input, ["schema", "disposition", "reason"], "invalid_disposition");
    if (input.schema !== DISPOSITION_SCHEMA) throw new OriginalTaskError("invalid_disposition");
    const body = {
      schema: DISPOSITION_SCHEMA,
      disposition: "useful_refusal",
      reason: boundedText(input.reason, 1500, "invalid_disposition"),
    };
    return { body, text: encodeOriginalTask(body) };
  }
  if (input.disposition === "scoped_result") {
    exactKeys(input, ["schema", "disposition", "scope", "result"], "invalid_disposition");
    if (input.schema !== DISPOSITION_SCHEMA) throw new OriginalTaskError("invalid_disposition");
    const body = {
      schema: DISPOSITION_SCHEMA,
      disposition: "scoped_result",
      scope: boundedText(input.scope, 500, "invalid_disposition"),
      result: boundedText(input.result, 1500, "invalid_disposition"),
    };
    return { body, text: encodeOriginalTask(body) };
  }
  throw new OriginalTaskError("invalid_disposition");
}

export function decodeOriginalTaskText(text) {
  if (typeof text !== "string" || text.length > TEXT_MAX) return { type: "unrecognized" };
  let value;
  try { value = JSON.parse(text); } catch { return { type: "unrecognized" }; }
  if (!value || typeof value !== "object" || Array.isArray(value)) return { type: "unrecognized" };
  const keys = Object.keys(value).sort().join(",");
  if (value.schema === REQUEST_SCHEMA && keys === "disposition,schema" && value.disposition === "withdrawn") {
    return { type: "withdrawal" };
  }
  if (value.schema === REQUEST_SCHEMA && keys === "disposition,exampleConsent,schema" &&
      value.disposition === "example_consent" && value.exampleConsent === true) {
    return { type: "consent" };
  }
  if (value.schema === REQUEST_SCHEMA && keys === "exampleConsent,friction,objective,publicInput,schema,usefulOutput" &&
      value.exampleConsent === false) {
    try {
      const checked = taskRequest({
        objective: value.objective,
        publicInput: value.publicInput,
        usefulOutput: value.usefulOutput,
        friction: value.friction,
      });
      if (checked.text !== encodeOriginalTask(value)) return { type: "unrecognized" };
      return { type: "task", task: value };
    } catch {
      return { type: "unrecognized" };
    }
  }
  if (value.schema === DISPOSITION_SCHEMA) {
    try {
      const checked = dispositionRequest(value);
      if (checked.text !== encodeOriginalTask(value)) return { type: "unrecognized" };
      return { type: "disposition", disposition: checked.body };
    } catch {
      return { type: "unrecognized" };
    }
  }
  return { type: "unrecognized" };
}

export function classifyThread(events, { retrieval = "open", workspaceExpired = false } = {}) {
  let task = null;
  let withdrawn = false;
  let consent = false;
  let disposition = null;
  let laterTask = false;
  for (const event of events) {
    if (!event || typeof event.kind !== "string") continue;
    const decoded = decodeOriginalTaskText(event.text);
    if (decoded.type === "task" && event.kind === "request") {
      if (task) laterTask = true;
      else task = decoded.task;
    } else if (decoded.type === "withdrawal" && event.kind === "correction") withdrawn = true;
    else if (decoded.type === "consent" && event.kind === "correction") consent = true;
    else if (decoded.type === "disposition" && event.kind === "reply") disposition = decoded.disposition;
  }
  if (!task) return null;
  const view = {
    submitted: true,
    triaged: false,
    delivered: false,
    accepted: false,
    reused: false,
    published: false,
    exampleConsent: consent,
    laterTask,
    task: {
      objective: task.objective,
      publicInput: task.publicInput,
      usefulOutput: task.usefulOutput,
      friction: task.friction,
    },
  };
  if (withdrawn) return { ...view, stage: "withdrawn", disposition: "withdrawn" };
  if (disposition) {
    return {
      ...view,
      stage: "triaged",
      triaged: true,
      disposition: disposition.disposition,
      ...(disposition.reason ? { reason: disposition.reason } : {}),
      ...(disposition.scope ? { scope: disposition.scope } : {}),
      ...(disposition.result ? { result: disposition.result } : {}),
    };
  }
  if (workspaceExpired || retrieval !== "open") {
    return { ...view, stage: "expired", disposition: "expired", retrieval: workspaceExpired ? "workspace_expired" : retrieval };
  }
  return { ...view, stage: "submitted", disposition: "pending_qualification" };
}

export function publicReceipt(view, extra = {}) {
  return {
    schema: "samedaydesk.original-task-receipt.v1",
    stage: view.stage,
    disposition: view.disposition,
    submitted: view.submitted === true,
    triaged: view.triaged === true,
    delivered: view.delivered === true,
    accepted: false,
    reused: false,
    published: false,
    exampleConsent: view.exampleConsent === true,
    contributionRequired: false,
    ...extra,
  };
}
