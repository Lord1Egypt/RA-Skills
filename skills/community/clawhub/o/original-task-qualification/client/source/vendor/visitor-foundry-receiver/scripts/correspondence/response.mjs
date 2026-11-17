import { EVENT_KINDS, PROJECT_STATUSES, NEXT_ACTION_KINDS } from "./constants.mjs";

const object = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const string = (value, max = 2048) => typeof value === "string" && value.length > 0 && value.length <= max;
const integer = (value) => Number.isSafeInteger(value) && value >= 1;
const timestamp = (value) => string(value, 64) && Number.isFinite(Date.parse(value));
const https = (value) => {
  try {
    return string(value) && new URL(value).protocol === "https:";
  } catch {
    return false;
  }
};
const artifact = (value) =>
  object(value) && https(value.url) && (value.label === undefined || string(value.label, 200));

function project(value, projectId) {
  return (
    object(value) &&
    string(value.id) &&
    (!projectId || value.id === projectId) &&
    string(value.title, 120) &&
    string(value.summary, 2000) &&
    PROJECT_STATUSES.includes(value.status) &&
    integer(value.version) &&
    timestamp(value.createdAt) &&
    timestamp(value.updatedAt) &&
    (value.nextAction === null ||
      (object(value.nextAction) &&
        NEXT_ACTION_KINDS.includes(value.nextAction.kind) &&
        (value.nextAction.url === undefined || https(value.nextAction.url))))
  );
}

function event(value, projectId) {
  return (
    object(value) &&
    string(value.id) &&
    value.projectId === projectId &&
    integer(value.sequence) &&
    EVENT_KINDS.includes(value.kind) &&
    timestamp(value.createdAt) &&
    (value.text === undefined || string(value.text, 8000)) &&
    (value.artifact === undefined || artifact(value.artifact)) &&
    (value.kind !== "artifact" || artifact(value.artifact))
  );
}

export function validResponse(operation, payload, { projectId, role, limit = 25 } = {}) {
  if (!object(payload)) return false;
  switch (operation) {
    case "createProject":
      return project(payload.project) && string(payload.ownerToken);
    case "getProject":
      return project(payload.project, projectId);
    case "createGrant":
      return (
        string(payload.grantId) &&
        string(payload.token) &&
        payload.role === role &&
        (payload.expiresAt === null || timestamp(payload.expiresAt))
      );
    case "postEvent":
      return project(payload.project, projectId) && event(payload.event, projectId);
    case "listEvents":
      return (
        Array.isArray(payload.events) &&
        payload.events.length <= limit &&
        payload.events.every(
          (item, index, all) => event(item, projectId) && (index === 0 || item.sequence > all[index - 1].sequence),
        ) &&
        (payload.events.length > 0 ? string(payload.nextCursor) : payload.nextCursor === null)
      );
    default:
      return false;
  }
}

function decodeUtf8(chunks, size) {
  if (typeof Buffer !== "undefined") return Buffer.concat(chunks, size).toString("utf8");
  const out = new Uint8Array(size);
  let offset = 0;
  for (const chunk of chunks) {
    out.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return new TextDecoder("utf8").decode(out);
}

export async function readBoundedJson(response, maxBytes, signal) {
  const declared = response.headers?.get?.("content-length");
  if (declared && Number(declared) > maxBytes) {
    void response.body?.cancel?.().catch(() => {});
    throw new Error("response limit exceeded");
  }
  if (!response.body?.getReader) throw new Error("response has no readable body");
  const reader = response.body.getReader();
  const cancel = () => {
    void reader.cancel().catch(() => {});
  };
  signal.addEventListener("abort", cancel, { once: true });
  const chunks = [];
  let size = 0;
  try {
    while (true) {
      if (signal.aborted) throw new Error("request timed out");
      const { value, done } = await reader.read();
      if (done) break;
      size += value.byteLength;
      if (size > maxBytes) throw new Error("response limit exceeded");
      chunks.push(value);
    }
    return JSON.parse(decodeUtf8(chunks, size));
  } catch (error) {
    cancel();
    throw error;
  } finally {
    signal.removeEventListener("abort", cancel);
    reader.releaseLock();
  }
}
