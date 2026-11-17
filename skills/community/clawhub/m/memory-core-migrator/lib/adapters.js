import { readFile, stat } from "node:fs/promises";
import { extname, basename } from "node:path";
import { createMemoryRecord, stripSensitive, validateMemoryRecord } from "./core.js";
import { migratorError } from "./errors.js";

export const ADAPTERS = new Set([
  "canonical-v1",
  "lancedb-pro",
  "markdown",
  "qmd",
  "lancedb-official-list-beta",
]);

async function requireExplicitFile(path, extensions, adapter) {
  let details;
  try {
    details = await stat(path);
  } catch {
    throw new Error(`${adapter} input does not exist: ${path}`);
  }
  if (!details.isFile() || !extensions.includes(extname(path).toLowerCase())) {
    throw new Error(`${adapter} requires an explicit ${extensions.join(" or ")} export file`);
  }
}

async function jsonItems(path) {
  const raw = await readFile(path, "utf8");
  if (extname(path).toLowerCase() === ".jsonl") {
    return raw.split(/\r?\n/u).flatMap((line, index) => {
      if (!line.trim()) return [];
      let parsed;
      try {
        parsed = JSON.parse(line);
      } catch (error) {
        throw new Error(`${path}:${index + 1}: invalid JSON: ${error.message}`);
      }
      if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
        throw new Error(`${path}:${index + 1}: expected a JSON object`);
      }
      return [parsed];
    });
  }
  const parsed = JSON.parse(raw);
  let values;
  if (Array.isArray(parsed)) values = parsed;
  else if (parsed && typeof parsed === "object") {
    values = parsed.records ?? parsed.memories ?? parsed.data ?? [parsed];
  }
  if (!Array.isArray(values) || values.some((item) => !item || typeof item !== "object" || Array.isArray(item))) {
    throw new Error(`${path}: expected an object or list of objects`);
  }
  return values;
}

const SEMANTIC_KEYS = new Set([
  "id", "source_id", "_id", "source", "text", "content", "memory", "document",
  "scope", "namespace", "timestamp", "created_at", "updated_at", "category",
  "createdAt", "agentId", "type", "importance", "score", "metadata", "provenance",
]);

function recordFromMapping(item, source, path, index, { defaultScope = "default" } = {}) {
  const text = item.text ?? item.content ?? item.memory ?? item.document;
  if (typeof text !== "string" || !text.trim()) {
    throw new Error(`${path}: item ${index} has no non-empty text/content field`);
  }
  const extras = {};
  for (const [key, value] of Object.entries(item)) if (!SEMANTIC_KEYS.has(key)) extras[key] = value;
  let sourceMetadata = item.metadata;
  if (typeof sourceMetadata === "string") {
    try {
      sourceMetadata = JSON.parse(sourceMetadata);
    } catch {
      throw new Error(`${path}: item ${index} metadata is not valid JSON`);
    }
  }
  if (sourceMetadata !== undefined
    && sourceMetadata !== null
    && (typeof sourceMetadata !== "object" || Array.isArray(sourceMetadata))) {
    throw new Error(`${path}: item ${index} metadata must be an object or JSON object string`);
  }
  const rawMetadata = {
    ...(sourceMetadata || {}),
    ...extras,
  };
  const strippedMetadata = stripSensitive(rawMetadata);
  const rawProvenance = {
    ...(item.provenance && typeof item.provenance === "object" && !Array.isArray(item.provenance)
      ? item.provenance
      : {}),
    input_file: String(path),
    input_index: index,
    adapter: source,
  };
  return createMemoryRecord({
    source: item.source || source,
    scope: item.scope || item.namespace || item.agentId || defaultScope,
    source_id: item.source_id ?? item.id ?? item._id ?? null,
    timestamp: item.timestamp ?? item.created_at ?? item.updated_at ?? item.createdAt ?? null,
    category: item.category || item.type || "memory",
    importance: item.importance ?? item.score ?? null,
    metadata: strippedMetadata.value,
    text,
    provenance: rawProvenance,
    redactions: strippedMetadata.redactions,
  });
}

export async function readJsonExport(path, source, { summary = null } = {}) {
  await requireExplicitFile(path, [".json", ".jsonl"], source);
  const items = await jsonItems(path);
  const records = items.map((item, index) => recordFromMapping(item, source, path, index));
  if (summary) {
    summary.parsed = items.length;
    summary.envelope_count = null;
  }
  return records;
}

function validatedArray(value, path, label) {
  if (!Array.isArray(value)
    || value.some((item) => !item || typeof item !== "object" || Array.isArray(item))) {
    throw new Error(`${path}: ${label} must be an array of objects`);
  }
  return value;
}

export async function readLancedbPro(path, { summary = null } = {}) {
  await requireExplicitFile(path, [".json", ".jsonl"], "lancedb-pro");
  if (extname(path).toLowerCase() === ".jsonl") {
    const items = await jsonItems(path);
    const records = items.map((item, index) => {
      if (!item.scope) throw migratorError("SCOPE_MISSING", `${path}: item ${index} is missing scope`);
      return recordFromMapping(item, "lancedb-pro", path, index);
    });
    if (summary) {
      summary.parsed = items.length;
      summary.envelope_count = null;
    }
    return records;
  }
  const parsed = JSON.parse(await readFile(path, "utf8"));
  let items;
  let defaultScope = "default";
  if (Array.isArray(parsed)) {
    items = validatedArray(parsed, path, "list capture");
  } else if (parsed && typeof parsed === "object" && Array.isArray(parsed.memories)) {
    if (parsed.version !== undefined && parsed.version !== "1.0") {
      throw migratorError(
        "MANIFEST_INVALID",
        `${path}: unsupported memory-lancedb-pro export version: ${parsed.version}`,
      );
    }
    items = validatedArray(parsed.memories, path, "memories");
    defaultScope = parsed.filters?.scope || "default";
  } else if (parsed && typeof parsed === "object" && Array.isArray(parsed.records)) {
    items = validatedArray(parsed.records, path, "records");
    defaultScope = parsed.filters?.scope || parsed.scope || "default";
  } else {
    throw migratorError("MANIFEST_INVALID", `${path}: unknown memory-lancedb-pro export envelope`);
  }
  if (parsed && !Array.isArray(parsed) && parsed.count !== undefined) {
    if (!Number.isSafeInteger(parsed.count) || parsed.count < 0 || parsed.count !== items.length) {
      throw migratorError("COUNT_MISMATCH", `${path}: export count does not match record array length`, {
        details: { envelope_count: parsed.count, records: items.length },
      });
    }
  }
  const records = items.map((item, index) => {
    if (!(item.scope || item.namespace || item.agentId) && defaultScope === "default") {
      throw migratorError("SCOPE_MISSING", `${path}: item ${index} is missing scope`);
    }
    return recordFromMapping(item, "lancedb-pro", path, index, { defaultScope });
  });
  if (summary) {
    summary.parsed = items.length;
    summary.envelope_count = parsed && !Array.isArray(parsed) && parsed.count !== undefined
      ? parsed.count
      : null;
  }
  return records;
}

export async function readOfficialLancedbList(path, { summary = null } = {}) {
  await requireExplicitFile(path, [".json", ".jsonl"], "lancedb-official-list-beta");
  if (extname(path).toLowerCase() === ".jsonl") {
    const items = await jsonItems(path);
    const records = items.map((item, index) => {
      if (!item.agentId) throw migratorError("SCOPE_MISSING", `${path}: item ${index} is missing agentId`);
      return recordFromMapping(item, "lancedb-official-list-beta", path, index);
    });
    if (summary) {
      summary.parsed = items.length;
      summary.envelope_count = null;
    }
    return records;
  }
  const parsed = JSON.parse(await readFile(path, "utf8"));
  if (Array.isArray(parsed)) {
    const records = validatedArray(parsed, path, "list capture").map((item, index) => {
      if (!item.agentId) throw migratorError("SCOPE_MISSING", `${path}: item ${index} is missing agentId`);
      return recordFromMapping(item, "lancedb-official-list-beta", path, index);
    });
    if (summary) {
      summary.parsed = parsed.length;
      summary.envelope_count = null;
    }
    return records;
  }
  if (!parsed || typeof parsed !== "object"
    || parsed.schema_version !== 1
    || parsed.adapter !== "lancedb-official-list-beta"
    || typeof parsed.agent_id !== "string"
    || !parsed.agent_id.trim()
    || typeof parsed.openclaw_version !== "string"
    || !parsed.openclaw_version.trim()) {
    throw migratorError("MANIFEST_INVALID", `${path}: invalid official LanceDB list-capture manifest`);
  }
  const items = validatedArray(parsed.records, path, "manifest records");
  if (parsed.count !== undefined
    && (!Number.isSafeInteger(parsed.count) || parsed.count < 0 || parsed.count !== items.length)) {
    throw migratorError("COUNT_MISMATCH", `${path}: manifest count does not match record array length`, {
      details: { envelope_count: parsed.count, records: items.length },
    });
  }
  const records = items.map((item, index) => recordFromMapping(
    item,
    "lancedb-official-list-beta",
    path,
    index,
    { defaultScope: parsed.agent_id },
  ));
  if (summary) {
    summary.parsed = items.length;
    summary.envelope_count = parsed.count === undefined ? null : parsed.count;
  }
  return records;
}

export async function readCanonical(path, { summary = null } = {}) {
  await requireExplicitFile(path, [".jsonl"], "canonical-v1");
  const items = await jsonItems(path);
  const records = items.map((item, index) => {
    const errors = validateMemoryRecord(item);
    if (errors.length) {
      throw new Error(`${path}: canonical record ${index} is invalid: ${errors.join(", ")}`);
    }
    return item;
  });
  if (summary) {
    summary.parsed = items.length;
    summary.envelope_count = null;
  }
  return records;
}

function parseFrontmatter(text) {
  const match = /^---\s*\r?\n([\s\S]*?)\r?\n---\s*\r?\n?/u.exec(text);
  if (!match) return [{}, text];
  const metadata = {};
  for (const line of match[1].split(/\r?\n/u)) {
    const colon = line.indexOf(":");
    if (colon >= 0) metadata[line.slice(0, colon).trim()] = line.slice(colon + 1).trim().replace(/^(['"])(.*)\1$/u, "$2");
  }
  return [metadata, text.slice(match[0].length)];
}

export async function readMarkdown(path, { qmd = false, summary = null } = {}) {
  await requireExplicitFile(path, [".md", ".markdown", ".qmd"], qmd ? "qmd" : "markdown");
  const [frontmatter, body] = parseFrontmatter(await readFile(path, "utf8"));
  const strippedFrontmatter = stripSensitive(frontmatter);
  const sections = body.split(/^##+\s+/mu);
  const records = [];
  for (let index = 0; index < sections.length; index += 1) {
    const text = sections[index].replace(/^#\s+.*(?:\r?\n|$)/mu, "").trim();
    if (!text) continue;
    records.push(createMemoryRecord({
      source: qmd ? "qmd-markdown" : "markdown",
      scope: frontmatter.scope || "default",
      source_id: `${basename(path)}#${index}`,
      timestamp: frontmatter.timestamp || frontmatter.date || null,
      category: frontmatter.category || "memory",
      importance: frontmatter.importance ?? null,
      metadata: { frontmatter: strippedFrontmatter.value },
      text,
      provenance: { input_file: String(path), input_index: index, adapter: qmd ? "qmd" : "markdown" },
      redactions: strippedFrontmatter.redactions,
    }));
  }
  if (summary) {
    summary.parsed = sections.length;
    summary.skipped = sections.length - records.length;
    summary.envelope_count = null;
  }
  return records;
}

function redactionTotals(records) {
  return records.reduce((totals, record) => {
    const redactions = record.provenance?.redactions;
    totals.secret_keys += Number(redactions?.secret_keys) || 0;
    totals.vector_keys += Number(redactions?.vector_keys) || 0;
    totals.total += Number(redactions?.total) || 0;
    return totals;
  }, { secret_keys: 0, vector_keys: 0, total: 0 });
}

export async function loadRecordsDetailed(adapter, paths) {
  if (!ADAPTERS.has(adapter)) throw new Error(`unknown adapter: ${adapter}`);
  const result = [];
  const inputs = [];
  for (const path of paths) {
    const collected = { parsed: 0, skipped: 0, envelope_count: null };
    let records;
    if (adapter === "canonical-v1") records = await readCanonical(path, { summary: collected });
    else if (adapter === "markdown") records = await readMarkdown(path, { summary: collected });
    else if (adapter === "qmd") records = await readMarkdown(path, { qmd: true, summary: collected });
    else if (adapter === "lancedb-pro") records = await readLancedbPro(path, { summary: collected });
    else records = await readOfficialLancedbList(path, { summary: collected });
    result.push(...records);
    inputs.push({
      path: String(path),
      adapter,
      envelope_count: collected.envelope_count,
      parsed: collected.parsed,
      accepted: records.length,
      skipped: collected.skipped,
      rejected: 0,
      redactions: redactionTotals(records),
    });
  }
  const allEnvelopeCountsKnown = inputs.every((input) => input.envelope_count !== null);
  const totals = inputs.reduce((summary, input) => {
    summary.parsed += input.parsed;
    summary.accepted += input.accepted;
    summary.skipped += input.skipped;
    summary.rejected += input.rejected;
    summary.redactions.secret_keys += input.redactions.secret_keys;
    summary.redactions.vector_keys += input.redactions.vector_keys;
    summary.redactions.total += input.redactions.total;
    return summary;
  }, {
    inputs: inputs.length,
    envelope_total: allEnvelopeCountsKnown
      ? inputs.reduce((total, input) => total + input.envelope_count, 0)
      : null,
    parsed: 0,
    accepted: 0,
    skipped: 0,
    rejected: 0,
    redactions: { secret_keys: 0, vector_keys: 0, total: 0 },
  });
  return { records: result, summary: { inputs, totals } };
}

export async function loadRecords(adapter, paths) {
  return (await loadRecordsDetailed(adapter, paths)).records;
}
