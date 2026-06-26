#!/usr/bin/env node
import { createHash } from "node:crypto";
import { promises as fs } from "node:fs";
import path from "node:path";
import { Pinecone } from "@pinecone-database/pinecone";

const DEFAULT_STATE_FILE = ".pinecone-memory-state.json";

function parseArgs(argv) {
  const out = { _: [] };
  let i = 0;
  while (i < argv.length) {
    const token = argv[i];
    if (!token.startsWith("--")) {
      out._.push(token);
      i += 1;
      continue;
    }

    const key = token.slice(2);
    const next = argv[i + 1];
    const hasValue = typeof next === "string" && !next.startsWith("--");
    const value = hasValue ? next : true;

    if (out[key] === undefined) {
      out[key] = value;
    } else if (Array.isArray(out[key])) {
      out[key].push(value);
    } else {
      out[key] = [out[key], value];
    }

    i += hasValue ? 2 : 1;
  }
  return out;
}

function asArray(value) {
  if (value === undefined) {
    return [];
  }
  return Array.isArray(value) ? value : [value];
}

function asInt(value, fallback) {
  if (value === undefined || value === true) {
    return fallback;
  }
  const parsed = Number.parseInt(String(value), 10);
  return Number.isFinite(parsed) ? parsed : fallback;
}

function requiredString(args, key) {
  const value = args[key];
  if (!value || value === true) {
    throw new Error(`Missing required argument --${key}`);
  }
  return String(value);
}

function optionalString(args, key, fallback = "") {
  const value = args[key];
  if (value === undefined || value === true) {
    return fallback;
  }
  return String(value);
}

function toBool(value, fallback = false) {
  if (value === undefined) {
    return fallback;
  }
  if (value === true) {
    return true;
  }
  const normalized = String(value).trim().toLowerCase();
  if (["1", "true", "yes", "y", "on"].includes(normalized)) {
    return true;
  }
  if (["0", "false", "no", "n", "off"].includes(normalized)) {
    return false;
  }
  return fallback;
}

function sha1(text) {
  return createHash("sha1").update(text).digest("hex");
}

async function loadState(statePath) {
  try {
    const raw = await fs.readFile(statePath, "utf8");
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object") {
      return { files: {} };
    }
    return {
      version: parsed.version || 1,
      updatedAt: parsed.updatedAt || null,
      files: parsed.files && typeof parsed.files === "object" ? parsed.files : {},
    };
  } catch {
    return { version: 1, updatedAt: null, files: {} };
  }
}

async function saveState(statePath, state) {
  const payload = {
    version: 1,
    updatedAt: new Date().toISOString(),
    files: state.files || {},
  };
  await fs.writeFile(statePath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

async function ensureParentDir(filePath) {
  const dir = path.dirname(path.resolve(filePath));
  await fs.mkdir(dir, { recursive: true });
}

async function writeJsonl(filePath, rows) {
  await ensureParentDir(filePath);
  const lines = rows.map((x) => JSON.stringify(x)).join("\n");
  await fs.writeFile(filePath, `${lines}${rows.length ? "\n" : ""}`, "utf8");
}

async function readJsonl(filePath) {
  const raw = await fs.readFile(filePath, "utf8");
  const lines = raw.split(/\r?\n/).map((x) => x.trim()).filter(Boolean);
  return lines.map((line, i) => {
    try {
      return JSON.parse(line);
    } catch {
      throw new Error(`Invalid JSONL at line ${i + 1} in ${filePath}`);
    }
  });
}

function getPineconeClient() {
  const apiKey = process.env.PINECONE_API_KEY;
  if (!apiKey) {
    throw new Error("PINECONE_API_KEY is not set");
  }
  return new Pinecone({ apiKey });
}

async function listIndexes(pc) {
  const res = await pc.listIndexes();
  if (Array.isArray(res)) {
    return res.map((x) => (typeof x === "string" ? x : x.name)).filter(Boolean);
  }
  if (Array.isArray(res?.indexes)) {
    return res.indexes.map((x) => (typeof x === "string" ? x : x.name)).filter(Boolean);
  }
  if (Array.isArray(res?.indexes?.indexes)) {
    return res.indexes.indexes.map((x) => x.name).filter(Boolean);
  }
  return [];
}

function getIndex(pc, name) {
  if (typeof pc.index === "function") {
    return pc.index(name);
  }
  if (typeof pc.Index === "function") {
    return pc.Index(name);
  }
  throw new Error("Pinecone SDK does not expose index/Index method");
}

function getNamespace(index, namespace) {
  if (!namespace) {
    return index;
  }
  if (typeof index.namespace === "function") {
    return index.namespace(namespace);
  }
  if (typeof index.Namespace === "function") {
    return index.Namespace(namespace);
  }
  throw new Error("Pinecone SDK does not expose namespace method");
}

async function statIndex(index, namespace) {
  if (typeof index.describeIndexStats !== "function") {
    throw new Error("describeIndexStats is not available in current Pinecone SDK");
  }
  const stats = await index.describeIndexStats();
  const namespaces = stats?.namespaces || {};
  return {
    dimension: stats?.dimension,
    metric: stats?.metric,
    totalRecordCount: stats?.totalRecordCount ?? stats?.total_vector_count ?? null,
    namespaceRecordCount: namespace ? namespaces?.[namespace]?.recordCount ?? namespaces?.[namespace]?.vectorCount ?? null : null,
    namespaces,
  };
}

function splitIntoChunks(text, chunkSize) {
  const normalized = text.replace(/\r\n/g, "\n").trim();
  if (!normalized) {
    return [];
  }

  const paragraphs = normalized.split(/\n\s*\n/g);
  const chunks = [];
  let current = "";

  for (const p of paragraphs) {
    const next = current ? `${current}\n\n${p}` : p;
    if (next.length <= chunkSize) {
      current = next;
      continue;
    }
    if (current) {
      chunks.push(current);
      current = p;
      continue;
    }

    for (let start = 0; start < p.length; start += chunkSize) {
      chunks.push(p.slice(start, start + chunkSize));
    }
    current = "";
  }

  if (current) {
    chunks.push(current);
  }

  return chunks;
}

function inferSourceKind(relPath) {
  const lower = relPath.toLowerCase();
  if (lower.includes("memory") || lower.includes("dialog")) {
    return "conversation_history";
  }
  if (lower.includes("api") || lower.includes("external")) {
    return "external_knowledge";
  }
  if (lower.includes("faq") || lower.includes("qa")) {
    return "qa_knowledge";
  }
  if (lower.endsWith(".md")) {
    return "document";
  }
  return "unknown";
}

function extractTitle(markdownText, fallback) {
  const firstHeading = markdownText.match(/^#\s+(.+)$/m);
  if (firstHeading && firstHeading[1]) {
    return firstHeading[1].trim();
  }
  return fallback;
}

function redactSensitive(text) {
  return text
    .replace(/(api[_-]?key\s*[:=]\s*)[^\s]+/gi, "$1[REDACTED]")
    .replace(/(token\s*[:=]\s*)[^\s]+/gi, "$1[REDACTED]")
    .replace(/(password\s*[:=]\s*)[^\s]+/gi, "$1[REDACTED]");
}

async function walkMarkdownFiles(entryPath) {
  const abs = path.resolve(entryPath);
  const stat = await fs.stat(abs);
  if (stat.isFile()) {
    return abs.toLowerCase().endsWith(".md") ? [abs] : [];
  }
  if (!stat.isDirectory()) {
    return [];
  }

  const queue = [abs];
  const found = [];

  while (queue.length > 0) {
    const current = queue.shift();
    const items = await fs.readdir(current, { withFileTypes: true });
    for (const item of items) {
      const full = path.join(current, item.name);
      if (item.isDirectory()) {
        queue.push(full);
      } else if (item.isFile() && item.name.toLowerCase().endsWith(".md")) {
        found.push(full);
      }
    }
  }

  return found;
}

async function buildRecords(pathsArg, chunkSize, maxChunks, enrich = {}) {
  const inputPaths = pathsArg.length > 0 ? pathsArg : ["MEMORY.md", "memory"];
  const fileSet = new Set();

  for (const p of inputPaths) {
    try {
      const files = await walkMarkdownFiles(p);
      for (const file of files) {
        fileSet.add(file);
      }
    } catch {
      // Ignore missing files to keep sync idempotent for partially present paths.
    }
  }

  const files = [...fileSet].sort();
  const records = [];
  const fileHashes = {};
  const skippedFiles = [];
  const state = enrich.incrementalState || { files: {} };
  const incremental = Boolean(enrich.incremental);

  for (const file of files) {
    const rel = path.relative(process.cwd(), file).replace(/\\/g, "/");
    const sourceText = await fs.readFile(file, "utf8");
    const sourceHash = sha1(sourceText);
    fileHashes[rel] = sourceHash;
    if (incremental && state.files?.[rel] === sourceHash) {
      skippedFiles.push(rel);
      continue;
    }
    const fsStat = await fs.stat(file);
    const title = extractTitle(sourceText, path.basename(rel));
    const sourceKind = inferSourceKind(rel);
    const inferredTags = rel.split("/").slice(0, -1).filter(Boolean);
    const chunks = splitIntoChunks(redactSensitive(sourceText), chunkSize);

    for (let i = 0; i < chunks.length; i += 1) {
      const text = chunks[i].trim();
      if (!text) {
        continue;
      }
      const hash8 = createHash("sha1").update(`${rel}:${i}:${text}`).digest("hex").slice(0, 8);
      records.push({
        _id: `${rel}#chunk-${i + 1}#${hash8}`,
        chunk_text: text,
        record_type: enrich.recordType || "core_content",
        source_kind: sourceKind,
        title,
        source: rel,
        source_url: enrich.sourceUrl || "",
        chunk_index: i + 1,
        content_hash: hash8,
        tags: enrich.tags?.length ? enrich.tags : inferredTags,
        author: enrich.author || "",
        department: enrich.department || "",
        acl_scope: enrich.acl || "default",
        doc_version: enrich.version || "v1",
        created_at: fsStat.birthtime?.toISOString?.() || fsStat.mtime.toISOString(),
        updated_at: new Date().toISOString(),
      });

      if (records.length >= maxChunks) {
        return { files, records, fileHashes, skippedFiles, truncated: true };
      }
    }
  }

  return { files, records, fileHashes, skippedFiles, truncated: false };
}

async function waitForWriteVisibility(index, namespace, beforeCount, minIncrease, retries, intervalMs) {
  for (let i = 0; i < retries; i += 1) {
    const stats = await statIndex(index, namespace);
    const current = Number(stats.namespaceRecordCount || 0);
    if (current - beforeCount >= minIncrease) {
      return {
        verified: true,
        attempts: i + 1,
        beforeCount,
        afterCount: current,
        delta: current - beforeCount,
      };
    }
    if (i < retries - 1) {
      await new Promise((resolve) => setTimeout(resolve, intervalMs));
    }
  }

  const lastStats = await statIndex(index, namespace);
  const lastCount = Number(lastStats.namespaceRecordCount || 0);
  return {
    verified: false,
    attempts: retries,
    beforeCount,
    afterCount: lastCount,
    delta: lastCount - beforeCount,
  };
}

async function upsertRecords(namespaceRef, records) {
  if (typeof namespaceRef.upsertRecords === "function") {
    await namespaceRef.upsertRecords(records);
    return;
  }
  throw new Error("Current Pinecone SDK does not support upsertRecords. Please update @pinecone-database/pinecone.");
}

async function deleteAllRecords(namespaceRef) {
  if (typeof namespaceRef.deleteAll === "function") {
    await namespaceRef.deleteAll();
    return;
  }
  if (typeof namespaceRef.deleteMany === "function") {
    await namespaceRef.deleteMany({});
    return;
  }
  if (typeof namespaceRef.delete === "function") {
    await namespaceRef.delete({ deleteAll: true });
    return;
  }
  throw new Error("Current Pinecone SDK does not expose deleteAll/deleteMany/delete for namespace cleanup");
}

async function searchByText(namespaceRef, text, topK, filter) {
  if (typeof namespaceRef.searchRecords !== "function") {
    throw new Error("Integrated embedding search API is not available in current Pinecone SDK (missing searchRecords)");
  }

  const payloads = [
    {
      query: {
        topK,
        inputs: { text },
        filter,
      },
      fields: ["chunk_text", "source", "chunk_index", "updated_at", "content_hash"],
    },
    {
      query: {
        inputs: { text },
        top_k: topK,
        filter,
      },
      fields: ["chunk_text", "source", "chunk_index", "updated_at", "content_hash"],
    },
  ];

  let lastError;
  for (const payload of payloads) {
    try {
      return await namespaceRef.searchRecords(payload);
    } catch (err) {
      lastError = err;
    }
  }

  throw lastError || new Error("searchRecords failed with all payload variants");
}

function printJson(value) {
  console.log(JSON.stringify(value, null, 2));
}

async function cmdCheck(args) {
  const pc = getPineconeClient();
  const indexName = requiredString(args, "index");
  const indexes = await listIndexes(pc);
  const exists = indexes.includes(indexName);

  const result = {
    ok: exists,
    indexName,
    foundIndexes: indexes,
  };

  if (exists) {
    const index = getIndex(pc, indexName);
    try {
      result.stats = await statIndex(index, String(args.namespace || ""));
    } catch (err) {
      result.statsError = String(err?.message || err);
    }
  }

  printJson(result);
  if (!exists) {
    process.exitCode = 2;
  }
}

async function cmdSync(args) {
  const startedAt = Date.now();
  const pc = getPineconeClient();
  const indexName = requiredString(args, "index");
  const namespace = String(args.namespace || "default");
  const chunkSize = asInt(args["chunk-size"], 800);
  const maxChunks = asInt(args["max-chunks"], 1000);
  const dryRun = Boolean(args["dry-run"]);
  const verifyWrite = toBool(args["verify-write"], true);
  const verifyRetries = asInt(args["verify-retries"], 6);
  const verifyIntervalMs = asInt(args["verify-interval-ms"], 1500);
  const incremental = toBool(args["incremental"], true);
  const statePath = optionalString(args, "state-file", DEFAULT_STATE_FILE);
  const pathsArg = asArray(args.path).map(String);
  const state = await loadState(statePath);

  const enrich = {
    recordType: optionalString(args, "record-type", "core_content"),
    sourceUrl: optionalString(args, "source-url", ""),
    tags: optionalString(args, "tags", "").split(",").map((x) => x.trim()).filter(Boolean),
    author: optionalString(args, "author", ""),
    department: optionalString(args, "department", ""),
    acl: optionalString(args, "acl", "default"),
    version: optionalString(args, "version", "v1"),
    incremental,
    incrementalState: state,
  };

  const { files, records, fileHashes, skippedFiles, truncated } = await buildRecords(pathsArg, chunkSize, maxChunks, enrich);
  let writeVerification = null;
  let persistedState = false;
  if (!dryRun && records.length > 0) {
    const index = getIndex(pc, indexName);
    const ns = getNamespace(index, namespace);
    const statsBefore = await statIndex(index, namespace);
    const beforeCount = Number(statsBefore.namespaceRecordCount || 0);

    const batchSize = 50;
    for (let i = 0; i < records.length; i += batchSize) {
      const batch = records.slice(i, i + batchSize);
      await upsertRecords(ns, batch);
    }

    if (verifyWrite) {
      writeVerification = await waitForWriteVisibility(
        index,
        namespace,
        beforeCount,
        Math.min(records.length, 1),
        verifyRetries,
        verifyIntervalMs
      );
    }

    if (incremental) {
      const nextState = { files: { ...state.files, ...fileHashes } };
      await saveState(statePath, nextState);
      persistedState = true;
    }
  } else if (!dryRun && incremental && skippedFiles.length > 0) {
    const nextState = { files: { ...state.files, ...fileHashes } };
    await saveState(statePath, nextState);
    persistedState = true;
  }

  printJson({
    mode: dryRun ? "dry-run" : "write",
    indexName,
    namespace,
    scannedFiles: files.length,
    skippedFiles: skippedFiles.length,
    incremental,
    statePath,
    persistedState,
    totalChunks: records.length,
    upserted: dryRun ? 0 : records.length,
    writeVerification,
    truncated,
    durationMs: Date.now() - startedAt,
  });
}

async function cmdCleanup(args) {
  const pc = getPineconeClient();
  const indexName = requiredString(args, "index");
  const namespace = String(args.namespace || "default");
  const confirm = optionalString(args, "confirm", "").toLowerCase();

  if (confirm !== "yes") {
    throw new Error("Refusing cleanup without --confirm yes");
  }

  const index = getIndex(pc, indexName);
  const ns = getNamespace(index, namespace);
  const before = await statIndex(index, namespace);
  const beforeCount = Number(before.namespaceRecordCount || 0);
  await deleteAllRecords(ns);
  const after = await statIndex(index, namespace);
  const afterCount = Number(after.namespaceRecordCount || 0);

  printJson({
    ok: afterCount === 0,
    indexName,
    namespace,
    beforeCount,
    afterCount,
    deletedEstimate: Math.max(beforeCount - afterCount, 0),
  });
}

async function cmdBackup(args) {
  const chunkSize = asInt(args["chunk-size"], 800);
  const maxChunks = asInt(args["max-chunks"], 10000);
  const output = optionalString(args, "output", `backup/pinecone-memory-backup-${Date.now()}.jsonl`);
  const pathsArg = asArray(args.path).map(String);
  const enrich = {
    recordType: optionalString(args, "record-type", "core_content"),
    sourceUrl: optionalString(args, "source-url", ""),
    tags: optionalString(args, "tags", "").split(",").map((x) => x.trim()).filter(Boolean),
    author: optionalString(args, "author", ""),
    department: optionalString(args, "department", ""),
    acl: optionalString(args, "acl", "default"),
    version: optionalString(args, "version", "v1"),
    incremental: false,
    incrementalState: { files: {} },
  };

  const { files, records, truncated } = await buildRecords(pathsArg, chunkSize, maxChunks, enrich);
  await writeJsonl(output, records);
  printJson({
    ok: true,
    output,
    scannedFiles: files.length,
    backupRecords: records.length,
    truncated,
  });
}

async function cmdRestore(args) {
  const startedAt = Date.now();
  const pc = getPineconeClient();
  const input = requiredString(args, "input");
  const indexName = requiredString(args, "index");
  const namespace = String(args.namespace || "default");
  const verifyWrite = toBool(args["verify-write"], true);
  const verifyRetries = asInt(args["verify-retries"], 6);
  const verifyIntervalMs = asInt(args["verify-interval-ms"], 1500);

  const index = getIndex(pc, indexName);
  const ns = getNamespace(index, namespace);
  const rows = await readJsonl(input);
  const records = rows.filter((x) => x && typeof x === "object" && x._id && x.chunk_text);
  if (records.length === 0) {
    throw new Error("No valid records found in backup input");
  }

  const beforeStats = await statIndex(index, namespace);
  const beforeCount = Number(beforeStats.namespaceRecordCount || 0);
  const batchSize = 50;
  for (let i = 0; i < records.length; i += batchSize) {
    await upsertRecords(ns, records.slice(i, i + batchSize));
  }

  let writeVerification = null;
  if (verifyWrite) {
    writeVerification = await waitForWriteVisibility(index, namespace, beforeCount, Math.min(records.length, 1), verifyRetries, verifyIntervalMs);
  }

  printJson({
    ok: verifyWrite ? Boolean(writeVerification?.verified) : true,
    input,
    indexName,
    namespace,
    restored: records.length,
    writeVerification,
    durationMs: Date.now() - startedAt,
  });
}

async function cmdHeartbeat(args) {
  const startedAt = Date.now();
  const pc = getPineconeClient();
  const indexName = requiredString(args, "index");
  const namespace = String(args.namespace || "default");
  const writeProbe = toBool(args["write-probe"], true);
  const verifyRetries = asInt(args["verify-retries"], 6);
  const verifyIntervalMs = asInt(args["verify-interval-ms"], 1500);

  const indexes = await listIndexes(pc);
  const exists = indexes.includes(indexName);
  if (!exists) {
    printJson({ ok: false, reason: "index_not_found", indexName, namespace, foundIndexes: indexes });
    process.exitCode = 2;
    return;
  }

  const index = getIndex(pc, indexName);
  const statsBefore = await statIndex(index, namespace);
  const beforeCount = Number(statsBefore.namespaceRecordCount || 0);
  let probe = null;

  if (writeProbe) {
    const ns = getNamespace(index, namespace);
    const probeText = `heartbeat probe at ${new Date().toISOString()}`;
    const probeHash = createHash("sha1").update(probeText).digest("hex").slice(0, 8);
    const probeRecord = {
      _id: `heartbeat#${Date.now()}#${probeHash}`,
      chunk_text: probeText,
      record_type: "heartbeat",
      source_kind: "system_monitor",
      source: "HEARTBEAT.md",
      title: "Pinecone heartbeat",
      tags: ["heartbeat", "health-check"],
      acl_scope: "system",
      doc_version: "v1",
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    await upsertRecords(ns, [probeRecord]);
    const visibility = await waitForWriteVisibility(index, namespace, beforeCount, 1, verifyRetries, verifyIntervalMs);
    probe = {
      id: probeRecord._id,
      writeProbe,
      ...visibility,
    };
  }

  const statsAfter = await statIndex(index, namespace);
  const afterCount = Number(statsAfter.namespaceRecordCount || 0);
  const result = {
    ok: writeProbe ? Boolean(probe?.verified) : true,
    indexName,
    namespace,
    beforeCount,
    afterCount,
    delta: afterCount - beforeCount,
    probe,
    durationMs: Date.now() - startedAt,
  };

  printJson(result);
  if (!result.ok) {
    process.exitCode = 3;
  }
}

async function cmdQuery(args) {
  const pc = getPineconeClient();
  const indexName = requiredString(args, "index");
  const namespace = String(args.namespace || "default");
  const text = requiredString(args, "text");
  const topK = asInt(args["top-k"], 5);

  let filter;
  if (typeof args.filter === "string") {
    filter = JSON.parse(args.filter);
  }

  const index = getIndex(pc, indexName);
  const ns = getNamespace(index, namespace);
  const raw = await searchByText(ns, text, topK, filter);

  const hits = raw?.result?.hits || raw?.hits || raw?.matches || [];
  const normalized = hits.slice(0, topK).map((hit) => ({
    id: hit._id || hit.id || null,
    score: hit.score ?? null,
    chunk_text: hit.fields?.chunk_text || hit.chunk_text || hit.metadata?.chunk_text || "",
    source: hit.fields?.source || hit.source || hit.metadata?.source || null,
    chunk_index: hit.fields?.chunk_index || hit.chunk_index || hit.metadata?.chunk_index || null,
  }));

  printJson({
    indexName,
    namespace,
    topK,
    count: normalized.length,
    hits: normalized,
  });
}

async function cmdStats(args) {
  const pc = getPineconeClient();
  const indexName = requiredString(args, "index");
  const namespace = typeof args.namespace === "string" ? args.namespace : "";

  const index = getIndex(pc, indexName);
  const stats = await statIndex(index, namespace);

  printJson({
    indexName,
    namespace: namespace || null,
    ...stats,
  });
}

function printHelp() {
  console.log(`pinecone-memory CLI

Commands:
  check --index <name> [--namespace <ns>]
  sync --index <name> [--namespace <ns>] [--path <fileOrDir>] [--chunk-size <n>] [--max-chunks <n>] [--dry-run] [--verify-write true|false] [--incremental true|false]
  query --index <name> [--namespace <ns>] --text <query> [--top-k <n>] [--filter <json>]
  stats --index <name> [--namespace <ns>]
  heartbeat --index <name> [--namespace <ns>] [--write-probe true|false]
  cleanup --index <name> [--namespace <ns>] --confirm yes
  backup [--path <fileOrDir>] [--output <jsonlPath>]
  restore --input <jsonlPath> --index <name> [--namespace <ns>] [--verify-write true|false]
`);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];

  if (!command || command === "help" || command === "--help") {
    printHelp();
    return;
  }

  if (command === "check") {
    await cmdCheck(args);
    return;
  }
  if (command === "sync") {
    await cmdSync(args);
    return;
  }
  if (command === "query") {
    await cmdQuery(args);
    return;
  }
  if (command === "stats") {
    await cmdStats(args);
    return;
  }
  if (command === "heartbeat") {
    await cmdHeartbeat(args);
    return;
  }
  if (command === "cleanup") {
    await cmdCleanup(args);
    return;
  }
  if (command === "backup") {
    await cmdBackup(args);
    return;
  }
  if (command === "restore") {
    await cmdRestore(args);
    return;
  }

  throw new Error(`Unknown command: ${command}`);
}

main().catch((err) => {
  console.error(err?.message || err);
  process.exit(1);
});
