// Map one caller task onto the existing original-task correspondence route.
// MCP, OpenAPI, and the A2A card expose readiness and TaskMarket tools. This
// descriptor is not one of those tools and does not spend, enroll, or execute.
import { createHash } from "node:crypto";
import { gunzipSync } from "node:zlib";
import { OriginalTaskError, taskRequest } from "./envelope.mjs";

export const ACTION_SCHEMA = "samedaydesk.original-task-action.v1";
export const INQUIRY_SCHEMA = "samedaydesk.original-task-inquiry.v1";
export const DISCOVERY_SCHEMA = "samedaydesk.original-task-correspondence.v1";
export const ARCHIVE_PATH = "/for-agents/original-task/original-task-client.tar.gz";
export const VISITOR_ENTRY = "https://samedaydesk.com/api/correspondence/v1/visitor-entry";
export const SUBMIT_COMMAND = "node server/lib/original-task/cli.mjs submit --base-url https://samedaydesk.com/api/correspondence --directory <private-directory> --task-file <task.json>";
export const READ_COMMAND = "node server/lib/original-task/cli.mjs read --directory <private-directory>";
export const MAP_COMMAND = "node server/lib/original-task/cli.mjs map --discovery-file <discovery.json> --archive <original-task-client.tar.gz> --task-file <task.json>";

const TASK_KEYS = ["friction", "objective", "publicInput", "usefulOutput"];
const INQUIRY_KEYS = ["declaredSource", "intent", "schema", "task"];
const REFUSED_INTENTS = {
  spend: "no_spend",
  paid_gateway: "unrelated_task",
  mcp_tool: "unrelated_task",
  observatory: "unrelated_task",
  hosted_execution: "missing_execution_authority",
  other: "unrelated_task",
};
const SPEND_KEYS = new Set(["checkout", "maxSpend", "payment", "reward", "spend", "wallet", "x402"]);
const LABEL_KEYS = new Set(["agent", "authenticated", "declaredSource", "operator", "role", "source"]);
const FORBIDDEN_MEMBER = ["collect.mjs", "operator-http.mjs", "event-guard.mjs", "deps.mjs", "store.mjs", "mount.mjs", ".sql", ".env"];
const DEPENDENCY_IMPORT = new RegExp(String.raw`(?:\bfrom|\brequire\()\s*['"](?:pg|express)['"]`);
const DATABASE_URL = "postgres" + "://";

export const TASK_ACTION = {
  schema: ACTION_SCHEMA,
  payment: false,
  universalCapability: false,
  mcpSkill: false,
  command: MAP_COMMAND,
  supported: [
    {
      id: "qualify_public_original_task",
      intent: "original_correspondence",
      nextAction: "submit_existing_correspondence",
      route: "existing visitor correspondence",
      fields: ["objective", "publicInput", "usefulOutput", "friction"],
    },
    {
      id: "retrieve_same_attempt",
      intent: "retrieve_continuation",
      nextAction: "read_existing_attempt",
      route: "same private directory",
      handle: "continuation projectId scoped to that directory",
    },
  ],
  refusals: [
    { id: "unrelated_task", when: "The body is another surface: MCP, paid gateway, observatory, or other." },
    { id: "stale_discovery", when: "The discovery schema, entry, commands, or archive binding is not current." },
    { id: "archive_refused", when: "Archive bytes or sha256 do not match the discovery document." },
    { id: "dependency_refused", when: "Archive bytes match but contain a server or database dependency." },
    { id: "missing_private_authority", when: "Read or continuation has no private attempt, secret, and continuation." },
    { id: "missing_execution_authority", when: "The intent asks this client to execute a hosted task." },
    { id: "handle_scope", when: "A project id is presented outside the private directory that holds it." },
    { id: "source_label_untrusted", when: "A declared source, role, or agent label is present on the task itself. It is not authentication." },
    { id: "no_spend", when: "The intent is spend, or the task carries a payment, wallet, or checkout field." },
  ],
  examples: [
    {
      id: "qualify_public_original_task",
      task: {
        objective: "Qualify one public page change.",
        publicInput: { kind: "nonsecret_example", example: "synthetic public example" },
        usefulOutput: "A qualification or a useful refusal.",
        friction: "No wallet and no hosted execution.",
      },
      nextAction: "submit_existing_correspondence",
      payment: false,
    },
    {
      id: "spend_request",
      intent: "spend",
      nextAction: "refuse",
      code: "no_spend",
      payment: false,
    },
  ],
};

function decision(fields) {
  return {
    schema: ACTION_SCHEMA,
    action: fields.action,
    code: fields.code,
    intent: fields.intent ?? null,
    payment: false,
    fundedJob: false,
    deliveryPromise: false,
    acceptance: false,
    universalCapability: false,
    authenticated: false,
    executionAuthority: false,
    declaredSourceAccepted: false,
    declaredSource: fields.declaredSource ?? null,
    mcpSkill: false,
    archiveBound: fields.archiveBound === true,
    requiresPrivateDirectory: true,
    nextCommand: fields.nextCommand ?? null,
    handle: fields.handle ?? null,
    continuation: fields.continuation ?? null,
  };
}

function refuse(code, extra = {}) {
  return decision({ action: "refuse", code, nextCommand: null, handle: null, continuation: null, ...extra });
}

export function safeDeclaredSource(value) {
  if (typeof value !== "string") return null;
  if (value.length < 1 || value.length > 80) return null;
  if (/bearer\s+\S/i.test(value) || /:\/\/[^/\s:@]+:[^/\s@]+@/.test(value)) return null;
  if (!/^[\w .:@-]{1,80}$/.test(value)) return null;
  return value;
}

export function discoveryProblems(discovery) {
  if (!discovery || typeof discovery !== "object" || Array.isArray(discovery)) return "stale_discovery";
  if (discovery.schema !== DISCOVERY_SCHEMA) return "stale_discovery";
  if (discovery.payment !== false || discovery.deliveryPromise !== false || discovery.fundedJob !== false) return "stale_discovery";
  if (discovery.acceptance !== false || discovery.thisDescriptorPerformsNoRequest !== true) return "stale_discovery";
  if (discovery.visitorEntry !== VISITOR_ENTRY) return "stale_discovery";
  if (discovery.submitCommand !== SUBMIT_COMMAND || discovery.readCommand !== READ_COMMAND || discovery.mapCommand !== MAP_COMMAND) return "stale_discovery";
  const action = discovery.taskAction;
  if (!action || action.payment !== false || action.universalCapability !== false || action.mcpSkill !== false) return "stale_discovery";
  const archive = discovery.acquisition?.archive;
  if (!archive || archive.path !== ARCHIVE_PATH) return "stale_discovery";
  if (typeof archive.sha256 !== "string" || !/^[a-f0-9]{64}$/.test(archive.sha256)) return "stale_discovery";
  if (!Number.isInteger(archive.bytes) || archive.bytes < 1) return "stale_discovery";
  return null;
}

export function bindPublicArchive(discovery, archiveBytes) {
  const stale = discoveryProblems(discovery);
  if (stale) return { ok: false, code: stale };
  if (!Buffer.isBuffer(archiveBytes)) return { ok: false, code: "archive_refused" };
  const expected = discovery.acquisition.archive;
  const sha256 = createHash("sha256").update(archiveBytes).digest("hex");
  if (archiveBytes.length !== expected.bytes || sha256 !== expected.sha256) return { ok: false, code: "archive_refused" };
  let inflated;
  try { inflated = gunzipSync(archiveBytes); }
  catch { return { ok: false, code: "archive_refused" }; }
  const members = tarMembers(inflated);
  if (!members) return { ok: false, code: "archive_refused" };
  if (members.some((member) => memberRefused(member))) return { ok: false, code: "dependency_refused" };
  return { ok: true, code: "ok", sha256 };
}

function memberRefused(member) {
  const name = member.name;
  if (name.split("/").includes("node_modules")) return true;
  if (FORBIDDEN_MEMBER.some((token) => name === token || name.endsWith(`/${token}`) || name.endsWith(token))) return true;
  const text = member.body.toString("utf8");
  return DEPENDENCY_IMPORT.test(text) || text.includes(DATABASE_URL);
}

function tarMembers(bytes) {
  const members = [];
  let offset = 0;
  while (offset + 512 <= bytes.length) {
    const header = bytes.subarray(offset, offset + 512);
    if (header.every((byte) => byte === 0)) break;
    const name = header.toString("utf8", 0, 100).replace(/\0.*$/, "");
    const prefix = header.toString("utf8", 345, 500).replace(/\0.*$/, "");
    if (!name) return null;
    const size = Number.parseInt(header.toString("utf8", 124, 136).replace(/\0.*$/, "").trim(), 8);
    if (!Number.isInteger(size) || size < 0) return null;
    const start = offset + 512;
    const end = start + size;
    if (end > bytes.length) return null;
    members.push({ name: prefix ? `${prefix}/${name}` : name, body: bytes.subarray(start, end) });
    offset = start + (Math.ceil(size / 512) * 512);
  }
  return members.length ? members : null;
}

function keyProblem(extra) {
  if (extra.some((key) => SPEND_KEYS.has(key))) return "no_spend";
  if (extra.some((key) => LABEL_KEYS.has(key))) return "source_label_untrusted";
  return null;
}

function checkTask(task) {
  if (!task || typeof task !== "object" || Array.isArray(task)) return { refuse: true, code: "invalid_task" };
  const extra = Object.keys(task).filter((key) => !TASK_KEYS.includes(key));
  const named = keyProblem(extra);
  if (named) return { refuse: true, code: named };
  try {
    taskRequest(task);
  } catch (error) {
    return { refuse: true, code: error instanceof OriginalTaskError ? error.code : "invalid_task" };
  }
  return { task };
}

function parseBody(body) {
  if (!body || typeof body !== "object" || Array.isArray(body)) return { refuse: true, code: "invalid_task" };
  if (body.jsonrpc || body.method === "tools/call") return { refuse: true, code: "unrelated_task", intent: "mcp_tool" };
  if (body.schema === INQUIRY_SCHEMA) {
    const keys = Object.keys(body).sort();
    const expected = [...INQUIRY_KEYS].sort();
    if (keys.length !== expected.length || keys.some((key, index) => key !== expected[index])) {
      const extra = keys.filter((key) => !expected.includes(key));
      const named = keyProblem(extra);
      return { refuse: true, code: named || "invalid_task", declaredSource: safeDeclaredSource(body.declaredSource) };
    }
    if (body.declaredSource !== null && typeof body.declaredSource !== "string") return { refuse: true, code: "invalid_task" };
    const declaredSource = safeDeclaredSource(body.declaredSource);
    if (typeof body.declaredSource === "string" && declaredSource === null) {
      return { refuse: true, code: "source_label_untrusted", intent: typeof body.intent === "string" ? body.intent : null };
    }
    const intent = body.intent;
    if (Object.hasOwn(REFUSED_INTENTS, intent)) {
      return { refuse: true, code: REFUSED_INTENTS[intent], intent, declaredSource };
    }
    if (intent !== "original_correspondence" && intent !== "retrieve_continuation") {
      return { refuse: true, code: "unrelated_task", intent: typeof intent === "string" ? intent : null, declaredSource };
    }
    if (intent === "retrieve_continuation") {
      if (body.task !== null) return { refuse: true, code: "invalid_task", intent, declaredSource };
      return { intent, declaredSource, task: null };
    }
    const checked = checkTask(body.task);
    if (checked.refuse) return { ...checked, intent, declaredSource };
    return { intent, declaredSource, task: checked.task };
  }
  const checked = checkTask(body);
  if (checked.refuse) return checked;
  return { intent: "original_correspondence", declaredSource: null, task: checked.task };
}

export function mapOriginalTask({ discovery, body, archive = null, directory = null, handle = null } = {}) {
  const stale = discoveryProblems(discovery);
  if (stale) return refuse(stale, { archiveBound: false });
  let archiveBound = false;
  if (archive) {
    const bound = bindPublicArchive(discovery, archive);
    if (!bound.ok) return refuse(bound.code, { archiveBound: false });
    archiveBound = true;
  }
  const parsed = parseBody(body);
  const declaredSource = parsed.declaredSource ?? null;
  if (parsed.refuse) {
    return refuse(parsed.code, { intent: parsed.intent ?? null, declaredSource, archiveBound });
  }
  if (handle !== null && handle !== undefined && typeof handle !== "string") {
    return refuse("handle_scope", { intent: parsed.intent, declaredSource, archiveBound });
  }
  if (parsed.intent === "retrieve_continuation") {
    if (directory?.conflict || (typeof handle === "string" && directory?.projectId && handle !== directory.projectId)) {
      return refuse("handle_scope", { intent: parsed.intent, declaredSource, archiveBound });
    }
    if (!directory?.hasAuthority || !directory.projectId) {
      return refuse("missing_private_authority", { intent: parsed.intent, declaredSource, archiveBound });
    }
    return decision({
      action: "read_existing_attempt",
      code: "ok",
      intent: parsed.intent,
      declaredSource,
      archiveBound,
      nextCommand: READ_COMMAND,
      handle: { projectId: directory.projectId, scope: "private_directory" },
      continuation: "same_private_read",
    });
  }
  if (typeof handle === "string") {
    return refuse("handle_scope", { intent: parsed.intent, declaredSource, archiveBound });
  }
  if (!archiveBound) {
    return decision({
      action: "bind_public_archive",
      code: "archive_unbound",
      intent: parsed.intent,
      declaredSource,
      archiveBound: false,
    });
  }
  return decision({
    action: "submit_existing_correspondence",
    code: "ok",
    intent: parsed.intent,
    declaredSource,
    archiveBound: true,
    nextCommand: SUBMIT_COMMAND,
  });
}
