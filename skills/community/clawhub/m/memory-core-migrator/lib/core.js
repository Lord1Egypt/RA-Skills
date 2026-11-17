import { createHash } from "node:crypto";

export const SCHEMA_VERSION = 1;
export const SECRET_KEY = /(secret|password|passwd|token|api[_-]?key|private[_-]?key|credential)/i;
export const VECTOR_KEY = /(vector|embedding)/i;

export function canonicalText(value) {
  return String(value).trim().split(/\s+/u).filter(Boolean).join(" ");
}

export function contentHash(text) {
  return createHash("sha256").update(canonicalText(text), "utf8").digest("hex");
}

export function normalizeTimestamp(value) {
  if (value === null || value === undefined || value === "") return null;
  let candidate = value;
  if (typeof candidate === "number" && Number.isFinite(candidate)) {
    candidate *= Math.abs(candidate) > 10_000_000_000 ? 1 : 1000;
  } else {
    candidate = String(candidate).trim();
    if (/^\d{4}-\d{2}-\d{2}$/u.test(candidate)) candidate += "T00:00:00Z";
    else if (/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?$/u.test(candidate)) {
      candidate += "Z";
    }
  }
  const date = new Date(candidate);
  return Number.isNaN(date.getTime()) ? String(value) : date.toISOString();
}

function jsonSafe(value, counts, seen) {
  if (value === null || ["string", "boolean"].includes(typeof value)) return value;
  if (typeof value === "number") return Number.isFinite(value) ? value : String(value);
  if (typeof value === "bigint" || typeof value === "symbol" || typeof value === "function") {
    return String(value);
  }
  if (seen.has(value)) return "[Circular]";
  seen.add(value);
  if (Array.isArray(value)) {
    const result = value.map((item) => jsonSafe(item, counts, seen));
    seen.delete(value);
    return result;
  }
  if (typeof value === "object") {
    const result = {};
    for (const [key, item] of Object.entries(value)) {
      if (SECRET_KEY.test(key)) {
        counts.secret_keys += 1;
      } else if (VECTOR_KEY.test(key)) {
        counts.vector_keys += 1;
      } else {
        result[key] = jsonSafe(item, counts, seen);
      }
    }
    seen.delete(value);
    return result;
  }
  seen.delete(value);
  return String(value);
}

export function stripSensitive(value) {
  const counts = { secret_keys: 0, vector_keys: 0, total: 0 };
  const valueClean = jsonSafe(value, counts, new Set());
  counts.total = counts.secret_keys + counts.vector_keys;
  return { value: valueClean, redactions: counts };
}

export function createMemoryRecord({
  source,
  text,
  scope = "default",
  source_id = null,
  timestamp = null,
  category = "memory",
  importance = null,
  metadata = {},
  provenance = {},
  redactions = null,
}) {
  const cleanedText = canonicalText(text);
  if (!String(source || "").trim()) throw new TypeError("source must be a non-empty string");
  if (!cleanedText) throw new TypeError("text must be a non-empty string");
  const cleanMetadata = stripSensitive(metadata);
  const cleanProvenance = stripSensitive(provenance);
  const totals = {
    secret_keys: cleanMetadata.redactions.secret_keys + cleanProvenance.redactions.secret_keys,
    vector_keys: cleanMetadata.redactions.vector_keys + cleanProvenance.redactions.vector_keys,
  };
  if (redactions) {
    totals.secret_keys += Number(redactions.secret_keys) || 0;
    totals.vector_keys += Number(redactions.vector_keys) || 0;
  }
  totals.total = totals.secret_keys + totals.vector_keys;
  const numericImportance = importance === null || importance === undefined || importance === ""
    ? null
    : Number(importance);
  const record = {
    schema_version: SCHEMA_VERSION,
    source: String(source),
    scope: String(scope || "default"),
    source_id: source_id === null || source_id === undefined || source_id === "" ? null : String(source_id),
    timestamp: normalizeTimestamp(timestamp),
    category: String(category || "memory"),
    importance: Number.isFinite(numericImportance) ? numericImportance : null,
    metadata: cleanMetadata.value,
    text: cleanedText,
    content_hash: contentHash(cleanedText),
    provenance: cleanProvenance.value,
  };
  if (totals.total > 0) record.provenance.redactions = totals;
  return record;
}

export function validateMemoryRecord(record) {
  const expected = [
    "schema_version", "source", "scope", "source_id", "timestamp", "category",
    "importance", "metadata", "text", "content_hash", "provenance",
  ];
  const errors = [];
  if (!record || typeof record !== "object" || Array.isArray(record)) return ["record must be an object"];
  for (const key of expected) if (!(key in record)) errors.push(`missing ${key}`);
  for (const key of Object.keys(record)) if (!expected.includes(key)) errors.push(`unexpected ${key}`);
  if (record.schema_version !== 1) errors.push("schema_version must equal 1");
  for (const key of ["source", "scope", "category", "text"]) {
    if (typeof record[key] !== "string" || !record[key]) errors.push(`${key} must be a non-empty string`);
  }
  if (!/^[0-9a-f]{64}$/u.test(record.content_hash || "")) errors.push("invalid content_hash");
  else if (typeof record.text === "string" && record.content_hash !== contentHash(record.text)) {
    errors.push("content_hash does not match text");
  }
  if (record.source_id !== null && typeof record.source_id !== "string") errors.push("invalid source_id");
  if (record.timestamp !== null && typeof record.timestamp !== "string") errors.push("invalid timestamp");
  if (record.importance !== null && typeof record.importance !== "number") errors.push("invalid importance");
  for (const key of ["metadata", "provenance"]) {
    if (!record[key] || typeof record[key] !== "object" || Array.isArray(record[key])) errors.push(`invalid ${key}`);
  }
  return errors;
}
