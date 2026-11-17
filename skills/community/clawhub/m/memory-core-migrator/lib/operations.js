import { open, link, mkdir, rename, rm, lstat, realpath } from "node:fs/promises";
import { dirname, join, basename, parse, resolve } from "node:path";
import { randomBytes } from "node:crypto";
import { canonicalText, validateMemoryRecord } from "./core.js";
import { migratorError } from "./errors.js";

async function optionalLstat(path) {
  try {
    return await lstat(path);
  } catch (error) {
    if (error.code === "ENOENT") return null;
    throw error;
  }
}

function directoryChain(path) {
  const absolute = resolve(path);
  const root = parse(absolute).root;
  const paths = [root];
  let current = root;
  for (const component of absolute.slice(root.length).split(/[\\/]+/u).filter(Boolean)) {
    current = join(current, component);
    paths.push(current);
  }
  return paths;
}

async function snapshotDirectoryChain(path) {
  const requested = await lstat(path);
  if (requested.isSymbolicLink() || !requested.isDirectory()) {
    throw migratorError("SYMBOLIC_LINK", `output parent must be a real directory: ${path}`);
  }
  const canonicalPath = await realpath(path);
  const snapshots = [];
  for (const current of directoryChain(canonicalPath)) {
    const details = await lstat(current);
    if (details.isSymbolicLink() || !details.isDirectory()) {
      throw migratorError("SYMBOLIC_LINK", `output ancestor must be a real directory: ${current}`);
    }
    snapshots.push({
      path: current,
      dev: details.dev,
      ino: details.ino,
      realpath: await realpath(current),
    });
  }
  return { canonicalPath, snapshots };
}

async function assertDirectoryChainUnchanged(directorySnapshot) {
  for (const snapshot of directorySnapshot.snapshots) {
    const details = await lstat(snapshot.path);
    if (details.isSymbolicLink()
      || !details.isDirectory()
      || details.dev !== snapshot.dev
      || details.ino !== snapshot.ino
      || await realpath(snapshot.path) !== snapshot.realpath) {
      throw migratorError("OUTPUT_CONFLICT", `output ancestor changed during write: ${snapshot.path}`);
    }
  }
}

async function assertIdentity(path, expected, label) {
  const details = await lstat(path);
  if (details.isSymbolicLink()
    || details.dev !== expected.dev
    || details.ino !== expected.ino) {
    throw migratorError("OUTPUT_CONFLICT", `${label} changed during write: ${path}`);
  }
}

export async function atomicWrite(path, content, { overwrite = false } = {}) {
  const ancestors = await snapshotDirectoryChain(dirname(path));
  const finalPath = join(ancestors.canonicalPath, basename(path));
  const original = await optionalLstat(finalPath);
  if (original?.isSymbolicLink()) {
    throw migratorError("SYMBOLIC_LINK", `refusing symbolic-link output: ${path}`);
  }
  const temporary = join(
    ancestors.canonicalPath,
    `.${basename(path)}.${process.pid}.${randomBytes(6).toString("hex")}.tmp`,
  );
  let handle;
  let temporaryIdentity;
  try {
    handle = await open(temporary, "wx", 0o600);
    temporaryIdentity = await lstat(temporary);
    await handle.writeFile(content, "utf8");
    await handle.sync();
    await handle.close();
    handle = null;
    await assertDirectoryChainUnchanged(ancestors);
    await assertIdentity(temporary, temporaryIdentity, "temporary output");
    const current = await optionalLstat(finalPath);
    if (overwrite) {
      if (original === null && current !== null) {
        throw migratorError("OUTPUT_CONFLICT", `output appeared during write: ${path}`);
      }
      if (original !== null) {
        if (current === null
          || current.isSymbolicLink()
          || current.dev !== original.dev
          || current.ino !== original.ino) {
          throw migratorError("OUTPUT_CONFLICT", `output changed during write: ${path}`);
        }
      }
      await rename(temporary, finalPath);
    } else {
      try {
        await link(temporary, finalPath);
      } catch (error) {
        if (error.code === "EEXIST") {
          throw migratorError(
            "OUTPUT_CONFLICT",
            `output conflict (EEXIST): refusing to overwrite existing output: ${path}`,
            { cause: error },
          );
        }
        throw error;
      }
      await rm(temporary);
    }
  } finally {
    if (handle) await handle.close().catch(() => {});
    await rm(temporary, { force: true }).catch(() => {});
  }
}

export async function writeJsonl(records, output) {
  const lines = [];
  for (const [index, record] of records.entries()) {
    const errors = validateMemoryRecord(record);
    if (errors.length) {
      throw migratorError(
        "MANIFEST_INVALID",
        `record ${index} is not canonical: ${errors.join(", ")}`,
        { details: { record_index: index, errors } },
      );
    }
    lines.push(JSON.stringify(record));
  }
  await atomicWrite(output, lines.length ? `${lines.join("\n")}\n` : "");
  return lines.length;
}

function similarity(left, right) {
  const a = canonicalText(left).toLocaleLowerCase("en-US");
  const b = canonicalText(right).toLocaleLowerCase("en-US");
  if (a === b) return 1;
  if (!a.length || !b.length) return 0;
  let previous = Array.from({ length: b.length + 1 }, (_, index) => index);
  for (let row = 1; row <= a.length; row += 1) {
    const current = [row];
    for (let column = 1; column <= b.length; column += 1) {
      current[column] = Math.min(
        current[column - 1] + 1,
        previous[column] + 1,
        previous[column - 1] + (a[row - 1] === b[column - 1] ? 0 : 1),
      );
    }
    previous = current;
  }
  return 1 - previous[b.length] / Math.max(a.length, b.length);
}

function sortedCounts(values) {
  return Object.fromEntries([...values.reduce((map, value) => map.set(value, (map.get(value) || 0) + 1), new Map())]
    .sort(([left], [right]) => String(left).localeCompare(String(right), "en")));
}

export function auditRecords(records, {
  approximateThreshold = 0.9,
  maxComparisons = 10_000,
  maxTextLength = 10_000,
} = {}) {
  if (!(approximateThreshold >= 0 && approximateThreshold <= 1)) {
    throw new RangeError("approximateThreshold must be between 0 and 1");
  }
  if (!Number.isSafeInteger(maxComparisons) || maxComparisons < 0) {
    throw new RangeError("maxComparisons must be a non-negative safe integer");
  }
  const ids = records.filter((record) => record.source_id).map((record) => record.source_id);
  const duplicateIds = Object.entries(sortedCounts(ids)).filter(([, count]) => count > 1).map(([id]) => id);
  const hashes = new Map();
  records.forEach((record, index) => hashes.set(record.content_hash, [...(hashes.get(record.content_hash) || []), index]));
  const exactGroups = [...hashes.values()].filter((group) => group.length > 1).sort((a, b) => a[0] - b[0]);
  const approximate = [];
  let comparisons = 0;
  outer: for (let left = 0; left < records.length; left += 1) {
    for (let right = left + 1; right < records.length; right += 1) {
      if (records[left].content_hash === records[right].content_hash) continue;
      if (comparisons >= maxComparisons) break outer;
      comparisons += 1;
      const score = similarity(records[left].text.slice(0, maxTextLength), records[right].text.slice(0, maxTextLength));
      if (score >= approximateThreshold) {
        approximate.push({ indices: [left, right], similarity: Number(score.toFixed(4)) });
      }
    }
  }
  const allNonExactPairs = records.length * (records.length - 1) / 2
    - [...hashes.values()].reduce((total, group) => total + group.length * (group.length - 1) / 2, 0);
  const approximateTruncated = comparisons < allNonExactPairs;
  const approximateCoverage = allNonExactPairs === 0
    ? 1
    : Number((comparisons / allNonExactPairs).toFixed(6));
  const warnings = approximateTruncated
    ? [`approximate duplicate scan incomplete: ${comparisons}/${allNonExactPairs} candidate pairs compared`]
    : [];
  return {
    total: records.length,
    counts: {
      source: sortedCounts(records.map((record) => record.source)),
      scope: sortedCounts(records.map((record) => record.scope)),
      category: sortedCounts(records.map((record) => record.category)),
    },
    missing_source_ids: records.filter((record) => record.source_id === null).length,
    duplicate_source_ids: duplicateIds,
    exact_text_duplicates: exactGroups,
    approximate_text_duplicates: approximate,
    approximate_threshold: approximateThreshold,
    approximate_comparisons: {
      performed: comparisons,
      limit: maxComparisons,
      total_candidates: allNonExactPairs,
      truncated: approximateTruncated,
      coverage: approximateCoverage,
    },
    completeness: {
      exact_audit_complete: true,
      approximate_audit_complete: !approximateTruncated,
    },
    coverage: {
      approximate_comparisons: approximateCoverage,
    },
    warnings,
  };
}

function markdownText(text) {
  return String(text).replaceAll("\r", "").trim();
}

function provenanceMarker(record) {
  const evidence = {
    schema_version: record.schema_version,
    source: record.source,
    scope: record.scope,
    source_id: record.source_id,
    timestamp: record.timestamp,
    category: record.category,
    importance: record.importance,
    content_hash: record.content_hash,
  };
  const json = JSON.stringify(evidence).replaceAll("--", "\\u002d\\u002d");
  return `<!-- openclaw-memory-migrator ${json} -->`;
}

export function renderMemoryCore(records) {
  const durable = [];
  const daily = new Map();
  const durableCategories = new Set(["preference", "preferences", "decision", "profile"]);
  for (const record of records) {
    const date = /^\d{4}-\d{2}-\d{2}/u.exec(record.timestamp || "")?.[0] ?? null;
    const category = record.category.toLowerCase();
    const isDurable = durableCategories.has(category)
      || record.metadata.durable === true
      || (record.importance !== null && record.importance >= 0.8);
    if (isDurable) durable.push(record);
    else daily.set(date || "undated", [...(daily.get(date || "undated") || []), record]);
  }
  const durableLines = [
    "# Durable Memories",
    "",
    "<!-- Generated by openclaw-memory-migrator; MEMORY.md is never modified. -->",
    "",
  ];
  if (!durable.length) durableLines.push("_None._", "");
  for (const record of durable) {
    durableLines.push(
      `## ${record.category || "memory"}`,
      "",
      provenanceMarker(record),
      markdownText(record.text),
      "",
    );
  }
  const files = { "durable.md": `${durableLines.join("\n").trimEnd()}\n` };
  for (const [date, values] of [...daily].sort(([left], [right]) => left.localeCompare(right))) {
    const lines = [
      `# Memories for ${date}`,
      "",
      "<!-- Generated by openclaw-memory-migrator; MEMORY.md is never modified. -->",
      "",
      ...values.flatMap((record) => [
        provenanceMarker(record),
        `- ${markdownText(record.text)}`,
      ]),
      "",
    ];
    files[`${date}.md`] = `${lines.join("\n").trimEnd()}\n`;
  }
  return files;
}

export async function writeMemoryCore(records, outputDirectory, { onFileWritten = null } = {}) {
  if (basename(outputDirectory).toLowerCase() === "memory.md") {
    throw migratorError(
      "OUTPUT_CONFLICT",
      "refusing to write MEMORY.md; choose a separate output directory",
    );
  }
  const files = renderMemoryCore(records);
  const ancestors = await snapshotDirectoryChain(dirname(outputDirectory));
  const finalDirectory = join(ancestors.canonicalPath, basename(outputDirectory));
  try {
    await lstat(finalDirectory);
    throw migratorError(
      "OUTPUT_CONFLICT",
      `refusing to overwrite existing render output: ${outputDirectory}`,
    );
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
  }
  const temporary = join(
    ancestors.canonicalPath,
    `.${basename(outputDirectory)}.${process.pid}.${randomBytes(6).toString("hex")}.tmp`,
  );
  await mkdir(temporary, { mode: 0o700 });
  const temporaryIdentity = await lstat(temporary);
  try {
    const names = Object.keys(files).sort();
    for (const [index, name] of names.entries()) {
      if (name.toLowerCase() === "memory.md") {
        throw migratorError("OUTPUT_CONFLICT", "refusing to write MEMORY.md");
      }
      await atomicWrite(join(temporary, name), files[name]);
      if (onFileWritten) await onFileWritten({
        name,
        completed: index + 1,
        total: names.length,
      });
    }
    await assertDirectoryChainUnchanged(ancestors);
    await assertIdentity(temporary, temporaryIdentity, "temporary render directory");
    if (await optionalLstat(finalDirectory) !== null) {
      throw migratorError("OUTPUT_CONFLICT", `render output appeared during write: ${outputDirectory}`);
    }
    await rename(temporary, finalDirectory);
  } finally {
    await rm(temporary, { recursive: true, force: true }).catch(() => {});
  }
  return Object.keys(files).sort();
}
