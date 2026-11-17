import {
  ARTIFACT_FIELDS,
  EVENT_KINDS,
  EVENT_POST_FIELDS,
  GRANT_CREATE_FIELDS,
  GRANT_ROLES,
  MAX_BODY_BYTES,
  MAX_EVENT_LIMIT,
  MAX_EVENT_TEXT_CHARS,
  MAX_LABEL_CHARS,
  MAX_SUMMARY_CHARS,
  MAX_TITLE_CHARS,
  MAX_URL_CHARS,
  MIN_EVENT_LIMIT,
  PROJECT_CREATE_FIELDS,
} from "./constants.mjs";
import { ClientValidationError } from "./errors.mjs";

export function rejectUnknownFields(body, allowed, label) {
  if (body == null || typeof body !== "object" || Array.isArray(body)) {
    throw new ClientValidationError({ message: `${label} must be an object` });
  }
  const extra = Object.keys(body).filter((key) => !allowed.includes(key));
  if (extra.length > 0) {
    throw new ClientValidationError({
      message: `${label} has unsupported fields: ${extra.sort().join(", ")}`,
    });
  }
}

export function requireString(value, label, { max, min = 1, optional = false } = {}) {
  if (value == null) {
    if (optional) return undefined;
    throw new ClientValidationError({ message: `${label} is required` });
  }
  if (typeof value !== "string") {
    throw new ClientValidationError({ message: `${label} must be a string` });
  }
  if (value.length < min) {
    throw new ClientValidationError({ message: `${label} must not be empty` });
  }
  if (max != null && value.length > max) {
    throw new ClientValidationError({ message: `${label} exceeds ${max} characters` });
  }
  return value;
}

export function requireHttpsUrl(value, label) {
  const urlText = requireString(value, label, { max: MAX_URL_CHARS });
  let parsed;
  try {
    parsed = new URL(urlText);
  } catch {
    throw new ClientValidationError({ message: `${label} must be a valid HTTPS URL` });
  }
  if (parsed.protocol !== "https:") {
    throw new ClientValidationError({ message: `${label} must be HTTPS` });
  }
  if (parsed.username || parsed.password) {
    throw new ClientValidationError({ message: `${label} must not contain credentials` });
  }
  return urlText;
}

export function validateProjectCreate(body) {
  rejectUnknownFields(body, PROJECT_CREATE_FIELDS, "project");
  return {
    title: requireString(body.title, "title", { max: MAX_TITLE_CHARS }),
    summary: requireString(body.summary, "summary", { max: MAX_SUMMARY_CHARS }),
  };
}

export function validateGrantCreate(body) {
  rejectUnknownFields(body, GRANT_CREATE_FIELDS, "grant");
  const role = requireString(body.role, "role");
  if (!GRANT_ROLES.includes(role)) {
    throw new ClientValidationError({ message: 'role must be "reader" or "writer"' });
  }
  let expiresAt;
  if (body.expiresAt != null) {
    expiresAt = requireString(body.expiresAt, "expiresAt");
    if (Number.isNaN(Date.parse(expiresAt))) {
      throw new ClientValidationError({ message: "expiresAt must be an ISO-8601 timestamp" });
    }
  }
  return expiresAt ? { role, expiresAt } : { role };
}

export function validateEventPost(body) {
  rejectUnknownFields(body, EVENT_POST_FIELDS, "event");
  const kind = requireString(body.kind, "kind");
  if (!EVENT_KINDS.includes(kind)) {
    throw new ClientValidationError({ message: `kind must be one of ${EVENT_KINDS.join(", ")}` });
  }
  const out = { kind };
  if (body.text != null) {
    out.text = requireString(body.text.trim ? body.text.trim() : body.text, "text", {
      max: MAX_EVENT_TEXT_CHARS,
      min: 1,
    });
  }
  if (body.artifact != null) {
    rejectUnknownFields(body.artifact, ARTIFACT_FIELDS, "artifact");
    out.artifact = {
      url: requireHttpsUrl(body.artifact.url, "artifact.url"),
    };
    if (body.artifact.label != null) {
      out.artifact.label = requireString(body.artifact.label, "artifact.label", { max: MAX_LABEL_CHARS });
    }
  }
  if (kind === "artifact" && !out.artifact) {
    throw new ClientValidationError({ message: "artifact events require artifact" });
  }
  if (kind === "resolved" || kind === "reopened") {
    if (body.expectedVersion == null) {
      throw new ClientValidationError({ message: `${kind} requires expectedVersion` });
    }
  }
  if (body.expectedVersion != null) {
    if (!Number.isInteger(body.expectedVersion) || body.expectedVersion < 1) {
      throw new ClientValidationError({ message: "expectedVersion must be a positive integer" });
    }
    out.expectedVersion = body.expectedVersion;
  }
  return out;
}

export function validateEventQuery({ after, limit } = {}) {
  const query = {};
  if (after != null) {
    query.after = requireString(after, "after");
  }
  if (limit != null) {
    if (!Number.isInteger(limit) || limit < MIN_EVENT_LIMIT || limit > MAX_EVENT_LIMIT) {
      throw new ClientValidationError({
        message: `limit must be an integer from ${MIN_EVENT_LIMIT} to ${MAX_EVENT_LIMIT}`,
      });
    }
    query.limit = limit;
  }
  return query;
}

export function validateId(value, label) {
  const id = requireString(value, label);
  if (id.includes("/") || id.includes("?") || id.includes("#") || id.includes(" ")) {
    throw new ClientValidationError({ message: `${label} is not a valid identifier` });
  }
  return id;
}

export function validateIdempotencyKey(value) {
  return requireString(value, "Idempotency-Key", { min: 8, max: 200 });
}

export function utf8ByteLength(text) {
  if (typeof Buffer !== "undefined") return Buffer.byteLength(text, "utf8");
  return new TextEncoder().encode(text).byteLength;
}

export function jsonBodyBytes(body) {
  return utf8ByteLength(JSON.stringify(body));
}

export class CorrespondenceBodyLimitError extends ClientValidationError {
  constructor() {
    super({
      status: 413,
      code: "body_limit",
      message: "request body exceeds 32 KiB",
    });
    this.name = "CorrespondenceBodyLimitError";
  }
}

export function assertBodySize(body) {
  const bytes = jsonBodyBytes(body);
  if (bytes > MAX_BODY_BYTES) {
    throw new CorrespondenceBodyLimitError();
  }
  return bytes;
}
