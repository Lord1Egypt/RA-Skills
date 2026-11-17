#!/usr/bin/env node
import { createHash } from "node:crypto";
import {
  chmod,
  lstat,
  mkdir,
  mkdtemp,
  readdir,
  readFile,
  rename,
  rm,
  writeFile,
} from "node:fs/promises";
import { homedir } from "node:os";
import { basename, dirname, isAbsolute, join, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";
import { inflateRawSync } from "node:zlib";

const RECEIPT = ".onimi-skill.json";
const MANIFEST_URL = "https://downloads.onimi.ai/skills/manifest.json";
const DAY_MS = 24 * 60 * 60 * 1000;
const MAX_MANIFEST_BYTES = 128 * 1024;
const MAX_ARCHIVE_BYTES = 20 * 1024 * 1024;
const MAX_FILES = 256;
const MAX_UNPACKED_BYTES = 40 * 1024 * 1024;
const help = `Onimi Skill manager

Usage (run from the installed skill, or use --dir with a verified new manager):
  node scripts/manage.mjs status
  node scripts/manage.mjs suite-status
  node scripts/manage.mjs check
  node scripts/manage.mjs update --confirm <skill-name>@<version>
  node scripts/manage.mjs update --dir <absolute-installed-skill-directory> --confirm <skill-name>@<version>

status never uses the network. check contacts the stable manifest at most once
per 24 hours and treats an offline check as non-fatal. update always requires the
exact current manifest version in --confirm. It refuses any local edits or extra
files, verifies the archive SHA-256, keeps a backup, and switches atomically.
Use --dir to refresh an existing installation from a newly downloaded manager
when the installed manager cannot handle a changed package at the same version.
suite-status is offline and reports the real local state of both Onimi modules;
it never infers client compatibility or connection state.
`;

let skillRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");

function backupRoot() {
  const skillsParent = dirname(skillRoot);
  return join(dirname(skillsParent), ".onimi-pages-backups", basename(skillsParent));
}

async function ensureRealBackupRoot() {
  const root = backupRoot();
  await mkdir(root, { recursive: true, mode: 0o700 });
  const stat = await lstat(root);
  if (!stat.isDirectory() || stat.isSymbolicLink()) {
    fail(`Backup store must be a real directory: ${root}`);
  }
  return root;
}

function fail(message) {
  throw new Error(message);
}

function sha256(data) {
  return createHash("sha256").update(data).digest("hex");
}

function strictObject(value, label) {
  if (!value || typeof value !== "object" || Array.isArray(value)) fail(`Invalid ${label}.`);
  return value;
}

function validSemver(value) {
  return typeof value === "string" && /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/.test(value);
}

function compareSemver(left, right) {
  const a = left.split(".").map(Number);
  const b = right.split(".").map(Number);
  for (let index = 0; index < 3; index += 1) {
    if (a[index] !== b[index]) return a[index] < b[index] ? -1 : 1;
  }
  return 0;
}

function allowedManifestUrl(url) {
  try {
    const parsed = new URL(url);
    if (parsed.href === MANIFEST_URL) return true;
    return (
      process.env.ONIMI_SKILL_TESTING === "1" &&
      parsed.protocol === "http:" &&
      ["127.0.0.1", "localhost", "::1"].includes(parsed.hostname)
    );
  } catch {
    return false;
  }
}

function expectedManifestUrl(receipt) {
  const override =
    process.env.ONIMI_SKILL_TESTING === "1" ? process.env.ONIMI_SKILL_MANIFEST_URL : undefined;
  const url = override || receipt.manifestUrl;
  if (!allowedManifestUrl(url)) fail("Receipt manifest URL is not an allowed stable channel.");
  return url;
}

function validateReceipt(value, expectedName) {
  const receipt = strictObject(value, "installation receipt");
  if (
    receipt.schemaVersion !== 1 ||
    typeof receipt.name !== "string" ||
    (expectedName && receipt.name !== expectedName) ||
    !validSemver(receipt.version) ||
    !allowedManifestUrl(receipt.manifestUrl)
  ) {
    fail("Invalid installation receipt.");
  }
  const managedFiles = strictObject(receipt.managedFiles, "managed file inventory");
  const entries = Object.entries(managedFiles);
  if (!entries.length || entries.length > MAX_FILES) fail("Invalid managed file inventory.");
  if (!managedFiles["SKILL.md"] || !managedFiles["scripts/manage.mjs"]) {
    fail("Installation receipt is missing required managed files.");
  }
  for (const [path, digest] of entries) {
    if (!safeRelativePath(path) || typeof digest !== "string" || !/^[a-f0-9]{64}$/.test(digest)) {
      fail("Invalid managed file inventory.");
    }
  }
  return receipt;
}

function validateManifest(value, receipt) {
  const manifest = strictObject(value, "stable manifest");
  if (manifest.schemaVersion !== 1 || manifest.channel !== "stable") fail("Invalid stable manifest.");
  const skills = strictObject(manifest.skills, "stable manifest skills");
  const entry = Object.values(skills).find((candidate) => candidate?.name === receipt.name);
  strictObject(entry, "skill manifest entry");
  if (!validSemver(entry.version) || typeof entry.minimumNode !== "string") {
    fail("Invalid skill manifest entry.");
  }
  const archive = strictObject(entry.archive, "skill archive");
  if (
    typeof archive.url !== "string" ||
    typeof archive.sha256 !== "string" ||
    !/^[a-f0-9]{64}$/.test(archive.sha256) ||
    !Number.isSafeInteger(archive.size) ||
    archive.size <= 0 ||
    archive.size > MAX_ARCHIVE_BYTES
  ) {
    fail("Invalid skill archive metadata.");
  }
  const archiveUrl = new URL(archive.url);
  const manifestUrl = new URL(expectedManifestUrl(receipt));
  if (
    archiveUrl.protocol !== manifestUrl.protocol ||
    archiveUrl.host !== manifestUrl.host ||
    !archiveUrl.pathname.startsWith(`/skills/${receipt.name}/${entry.version}/`) ||
    !archiveUrl.pathname.endsWith(`/${receipt.name}-${entry.version}.zip`)
  ) {
    fail("Archive URL is outside the stable distribution path.");
  }
  return entry;
}

function safeRelativePath(path) {
  return (
    typeof path === "string" &&
    path.length > 0 &&
    path.length <= 240 &&
    !path.includes("\\") &&
    !path.includes("\0") &&
    !path.startsWith("/") &&
    path.split("/").every((part) => part && part !== "." && part !== "..")
  );
}

async function loadJson(path) {
  return JSON.parse(await readFile(path, "utf8"));
}

async function readReceipt(root = skillRoot) {
  const receipt = validateReceipt(await loadJson(join(root, RECEIPT)), basename(root));
  const skill = await readFile(join(root, "SKILL.md"));
  validateSkillFrontmatter(new Map([["SKILL.md", skill]]), receipt);
  return receipt;
}

async function treeFiles(root, prefix = "") {
  const output = [];
  for (const entry of await readdir(join(root, prefix), { withFileTypes: true })) {
    const item = prefix ? `${prefix}/${entry.name}` : entry.name;
    if (entry.isDirectory()) output.push(...(await treeFiles(root, item)));
    else output.push({ path: item, type: entry.isFile() ? "file" : "other" });
  }
  return output.sort((a, b) => a.path.localeCompare(b.path));
}

async function inspectIntegrity(root, receipt) {
  const files = await treeFiles(root);
  const actualPaths = files.map(({ path }) => path);
  const expectedPaths = [RECEIPT, ...Object.keys(receipt.managedFiles)].sort();
  const issues = [];
  for (const path of actualPaths.filter((item) => !expectedPaths.includes(item))) {
    issues.push(`extra:${path}`);
  }
  for (const path of expectedPaths.filter((item) => !actualPaths.includes(item))) {
    issues.push(`missing:${path}`);
  }
  for (const item of files) {
    if (item.path === RECEIPT || !(item.path in receipt.managedFiles)) continue;
    if (item.type !== "file") {
      issues.push(`non-file:${item.path}`);
      continue;
    }
    const digest = sha256(await readFile(join(root, item.path)));
    if (digest !== receipt.managedFiles[item.path]) issues.push(`modified:${item.path}`);
  }
  return { clean: issues.length === 0, issues };
}

function cacheRoot() {
  const base = process.env.XDG_CACHE_HOME || join(homedir(), ".cache");
  return join(base, "onimi-pages", "skill-updates");
}

function cachePath(name) {
  return join(cacheRoot(), `${name}.json`);
}

async function readCache(name) {
  try {
    const value = strictObject(await loadJson(cachePath(name)), "update cache");
    return value.name === name && typeof value.checkedAt === "string" ? value : null;
  } catch {
    return null;
  }
}

async function writeCache(name, value) {
  const root = cacheRoot();
  await mkdir(root, { recursive: true });
  const temporary = join(root, `.${name}.${process.pid}.tmp`);
  await writeFile(temporary, `${JSON.stringify(value, null, 2)}\n`, { mode: 0o600 });
  await rename(temporary, cachePath(name));
}

async function fetchBytes(url, { limit, timeout }) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);
  try {
    const response = await fetch(url, {
      headers: { accept: "application/json, application/zip;q=0.9" },
      redirect: "error",
      signal: controller.signal,
    });
    if (!response.ok) fail(`Distribution server returned HTTP ${response.status}.`);
    const declared = Number(response.headers.get("content-length"));
    if (Number.isFinite(declared) && declared > limit) fail("Distribution response is too large.");
    if (!response.body) fail("Distribution response has no body.");
    const chunks = [];
    let size = 0;
    for await (const chunk of response.body) {
      size += chunk.length;
      if (size > limit) fail("Distribution response is too large.");
      chunks.push(chunk);
    }
    return Buffer.concat(chunks);
  } finally {
    clearTimeout(timer);
  }
}

async function fetchManifest(receipt, timeout = 3000) {
  const bytes = await fetchBytes(expectedManifestUrl(receipt), {
    limit: MAX_MANIFEST_BYTES,
    timeout,
  });
  return validateManifest(JSON.parse(bytes.toString("utf8")), receipt);
}

function parseNodeMajor(version) {
  const match = /^(\d+)\./.exec(version);
  return match ? Number(match[1]) : 0;
}

function assertRuntime(entry) {
  if (parseNodeMajor(process.versions.node) < parseNodeMajor(entry.minimumNode)) {
    fail(`Node.js ${entry.minimumNode} or later is required.`);
  }
}

function findEndOfCentralDirectory(buffer) {
  const minimum = Math.max(0, buffer.length - 65_557);
  for (let offset = buffer.length - 22; offset >= minimum; offset -= 1) {
    if (buffer.readUInt32LE(offset) === 0x06054b50) return offset;
  }
  fail("ZIP end record is missing.");
}

function parseZip(buffer, expectedName) {
  const eocd = findEndOfCentralDirectory(buffer);
  const disk = buffer.readUInt16LE(eocd + 4);
  const centralDisk = buffer.readUInt16LE(eocd + 6);
  const entriesOnDisk = buffer.readUInt16LE(eocd + 8);
  const entryCount = buffer.readUInt16LE(eocd + 10);
  const centralSize = buffer.readUInt32LE(eocd + 12);
  const centralOffset = buffer.readUInt32LE(eocd + 16);
  const commentLength = buffer.readUInt16LE(eocd + 20);
  if (disk !== 0 || centralDisk !== 0 || entriesOnDisk !== entryCount || entryCount > MAX_FILES) {
    fail("Unsupported ZIP layout.");
  }
  if (centralOffset + centralSize !== eocd || eocd + 22 + commentLength !== buffer.length) {
    fail("Invalid ZIP central directory.");
  }
  const output = new Map();
  let offset = centralOffset;
  let unpacked = 0;
  for (let index = 0; index < entryCount; index += 1) {
    if (offset + 46 > buffer.length || buffer.readUInt32LE(offset) !== 0x02014b50) {
      fail("Invalid ZIP directory entry.");
    }
    const flags = buffer.readUInt16LE(offset + 8);
    const method = buffer.readUInt16LE(offset + 10);
    const compressedSize = buffer.readUInt32LE(offset + 20);
    const size = buffer.readUInt32LE(offset + 24);
    const nameLength = buffer.readUInt16LE(offset + 28);
    const extraLength = buffer.readUInt16LE(offset + 30);
    const commentLength = buffer.readUInt16LE(offset + 32);
    const external = buffer.readUInt32LE(offset + 38);
    const localOffset = buffer.readUInt32LE(offset + 42);
    const name = buffer.subarray(offset + 46, offset + 46 + nameLength).toString("utf8");
    offset += 46 + nameLength + extraLength + commentLength;
    if ((flags & 1) !== 0 || ![0, 8].includes(method)) fail("Unsupported ZIP compression.");
    if (((external >>> 16) & 0xf000) === 0xa000) fail("ZIP symlinks are not allowed.");
    const prefix = `${expectedName}/`;
    if (!name.startsWith(prefix) || name.endsWith("/")) fail("Unexpected ZIP member.");
    const path = name.slice(prefix.length);
    if (!safeRelativePath(path) || output.has(path)) fail("Unsafe or duplicate ZIP member.");
    if (localOffset + 30 > buffer.length || buffer.readUInt32LE(localOffset) !== 0x04034b50) {
      fail("Invalid ZIP local entry.");
    }
    const localNameLength = buffer.readUInt16LE(localOffset + 26);
    const localExtraLength = buffer.readUInt16LE(localOffset + 28);
    const localName = buffer
      .subarray(localOffset + 30, localOffset + 30 + localNameLength)
      .toString("utf8");
    if (localName !== name) fail("ZIP member names do not match.");
    const dataStart = localOffset + 30 + localNameLength + localExtraLength;
    const dataEnd = dataStart + compressedSize;
    if (dataEnd > buffer.length) fail("Truncated ZIP member.");
    const compressed = buffer.subarray(dataStart, dataEnd);
    const data =
      method === 0
        ? Buffer.from(compressed)
        : inflateRawSync(compressed, {
            maxOutputLength: Math.min(size + 1, MAX_UNPACKED_BYTES - unpacked + 1),
          });
    if (data.length !== size) fail("ZIP member size does not match.");
    unpacked += size;
    if (unpacked > MAX_UNPACKED_BYTES) fail("ZIP expands beyond the allowed size.");
    output.set(path, data);
  }
  if (offset !== centralOffset + centralSize || output.size === 0) fail("Invalid ZIP directory size.");
  return output;
}

function validateSkillFrontmatter(files, receipt) {
  const skill = files.get("SKILL.md")?.toString("utf8");
  if (
    !skill ||
    !skill.startsWith("---\n") ||
    !skill.includes(`\nname: ${receipt.name}\n`) ||
    !skill.includes(`\n  version: "${receipt.version}"\n`)
  ) {
    fail("Archive Skill frontmatter does not match its receipt.");
  }
}

function validateArchiveFiles(files, expectedName, expectedVersion) {
  const receiptBytes = files.get(RECEIPT);
  if (!receiptBytes) fail("Archive installation receipt is missing.");
  const receipt = validateReceipt(JSON.parse(receiptBytes.toString("utf8")), expectedName);
  if (receipt.version !== expectedVersion) fail("Archive version does not match the manifest.");
  const expected = [RECEIPT, ...Object.keys(receipt.managedFiles)].sort();
  const actual = [...files.keys()].sort();
  if (JSON.stringify(expected) !== JSON.stringify(actual)) fail("Archive file inventory does not match.");
  for (const [path, digest] of Object.entries(receipt.managedFiles)) {
    if (sha256(files.get(path)) !== digest) fail(`Archive file digest failed: ${path}`);
  }
  validateSkillFrontmatter(files, receipt);
  return receipt;
}

async function extractFiles(root, files) {
  for (const [path, data] of files) {
    const output = join(root, ...path.split("/"));
    const resolved = resolve(output);
    if (!resolved.startsWith(`${resolve(root)}${sep}`)) fail("Unsafe extraction path.");
    await mkdir(dirname(output), { recursive: true });
    await writeFile(output, data, { mode: path.endsWith(".mjs") ? 0o755 : 0o644 });
    if (path.endsWith(".mjs")) await chmod(output, 0o755);
  }
}

async function installedMatchesArchive(files) {
  const installed = await treeFiles(skillRoot);
  if (installed.length !== files.size || installed.some(({ path, type }) => type !== "file" || !files.has(path))) {
    return false;
  }
  for (const [path, bytes] of files) {
    if (!(await readFile(join(skillRoot, ...path.split("/")))).equals(bytes)) return false;
  }
  return true;
}

async function fetchVerifiedArchive(entry, name) {
  const archive = await fetchBytes(entry.archive.url, {
    limit: Math.min(entry.archive.size + 1, MAX_ARCHIVE_BYTES),
    timeout: 10_000,
  });
  if (archive.length !== entry.archive.size || sha256(archive) !== entry.archive.sha256) {
    fail("Downloaded archive failed size or SHA-256 verification.");
  }
  const files = parseZip(archive, name);
  validateArchiveFiles(files, name, entry.version);
  return files;
}

async function commandStatus(receipt) {
  const integrity = await inspectIntegrity(skillRoot, receipt);
  const cache = await readCache(receipt.name);
  console.log(
    JSON.stringify(
      {
        name: receipt.name,
        version: receipt.version,
        integrity: integrity.clean ? "clean" : "modified",
        issues: integrity.issues,
        latest: cache?.latest || null,
        checkedAt: cache?.checkedAt || null,
      },
      null,
      2,
    ),
  );
}

async function localModuleStatus(parent, name) {
  const root = join(parent, name);
  try {
    await lstat(root);
  } catch (error) {
    if (error.code === "ENOENT") return { name, state: "missing" };
    throw error;
  }
  try {
    const receipt = await readReceipt(root);
    const integrity = await inspectIntegrity(root, receipt);
    return {
      name,
      state: integrity.clean ? "installed" : "customized",
      version: receipt.version,
      integrity: integrity.clean ? "clean" : "modified",
      issues: integrity.issues,
    };
  } catch {
    return {
      name,
      state: "present-unmanaged",
      integrity: "unknown",
      issues: ["No valid Onimi direct-download receipt; preserved as user-managed."],
    };
  }
}

async function commandSuiteStatus() {
  const parent = dirname(skillRoot);
  const modules = [];
  for (const name of ["onimi-pages-creator", "onimi-pages-publish"]) {
    modules.push(await localModuleStatus(parent, name));
  }
  console.log(
    JSON.stringify(
      {
        suite: "onimi",
        source: "local-filesystem",
        modules,
        connection: "not-inspected",
      },
      null,
      2,
    ),
  );
}

async function commandCheck(receipt) {
  const describeCached = (cached) => {
    console.log(
      cached.error
        ? "Update check was already attempted today; the cached offline result is non-fatal."
        : cached.refreshAvailable
          ? `Same-version refresh available: ${receipt.name}@${receipt.version}. Run update with --confirm ${receipt.name}@${receipt.version}.`
          : `Checked today: installed ${receipt.version}, latest ${cached.latest}.`,
    );
  };
  const cacheIsCurrent = (cached) => cached && Date.now() - Date.parse(cached.checkedAt) < DAY_MS &&
    (cached.latest !== receipt.version || typeof cached.refreshAvailable === "boolean");
  let cached = await readCache(receipt.name);
  if (cacheIsCurrent(cached)) {
    describeCached(cached);
    return;
  }
  await mkdir(cacheRoot(), { recursive: true });
  const lock = `${cachePath(receipt.name)}.check.lock`;
  try {
    await mkdir(lock);
  } catch (error) {
    if (error.code === "EEXIST") {
      console.log("Another update check is already running; continuing without interruption.");
      return;
    }
    throw error;
  }
  try {
    cached = await readCache(receipt.name);
    if (cacheIsCurrent(cached)) {
      describeCached(cached);
      return;
    }
    const checkedAt = new Date().toISOString();
    try {
      const entry = await fetchManifest(receipt);
      assertRuntime(entry);
      const refreshAvailable = entry.version === receipt.version &&
        !(await installedMatchesArchive(await fetchVerifiedArchive(entry, receipt.name)));
      await writeCache(receipt.name, {
        schemaVersion: 1,
        name: receipt.name,
        checkedAt,
        latest: entry.version,
        refreshAvailable,
      });
      console.log(
        compareSemver(receipt.version, entry.version) < 0
          ? `Update available: ${receipt.name}@${entry.version}. Review local status, then run update with --confirm ${receipt.name}@${entry.version}.`
          : refreshAvailable
            ? `Same-version refresh available: ${receipt.name}@${receipt.version}. Run update with --confirm ${receipt.name}@${receipt.version}.`
          : `Up to date: ${receipt.name}@${receipt.version}.`,
      );
    } catch {
      await writeCache(receipt.name, {
        schemaVersion: 1,
        name: receipt.name,
        checkedAt,
        latest: null,
        error: "offline-or-invalid",
      });
      console.log(
        "Update check could not reach a valid stable manifest; continuing without interruption.",
      );
    }
  } finally {
    await rm(lock, { recursive: true, force: true });
  }
}

async function commandUpdate(receipt, confirmation) {
  const integrity = await inspectIntegrity(skillRoot, receipt);
  if (!integrity.clean) {
    fail(`Local changes are protected; update refused (first issue: ${integrity.issues[0]}).`);
  }
  const lock = join(dirname(skillRoot), `.${receipt.name}.update.lock`);
  try {
    await mkdir(lock);
  } catch (error) {
    if (error.code === "EEXIST") fail("Another update is running or needs manual lock recovery.");
    throw error;
  }
  let staging;
  let backup;
  let oldMoved = false;
  try {
    await writeFile(join(lock, "owner.json"), `${JSON.stringify({ pid: process.pid, startedAt: new Date().toISOString() })}\n`);
    const lockedIntegrity = await inspectIntegrity(skillRoot, receipt);
    if (!lockedIntegrity.clean) {
      fail(`Local changes are protected; update refused (first issue: ${lockedIntegrity.issues[0]}).`);
    }
    const entry = await fetchManifest(receipt, 5000);
    assertRuntime(entry);
    if (compareSemver(entry.version, receipt.version) < 0) fail("The stable channel would downgrade this skill.");
    if (confirmation !== `${receipt.name}@${entry.version}`) {
      fail(`Explicit confirmation required: --confirm ${receipt.name}@${entry.version}`);
    }
    const files = await fetchVerifiedArchive(entry, receipt.name);
    if (await installedMatchesArchive(files)) {
      console.log(`Already current: ${receipt.name}@${receipt.version}.`);
      return;
    }
    staging = await mkdtemp(join(dirname(skillRoot), `.${receipt.name}.stage-`));
    const stagedSkill = join(staging, receipt.name);
    await mkdir(stagedSkill);
    await extractFiles(stagedSkill, files);
    const stagedReceipt = await readReceipt(stagedSkill);
    const stagedIntegrity = await inspectIntegrity(stagedSkill, stagedReceipt);
    if (!stagedIntegrity.clean) fail("Staged skill failed its complete fingerprint check.");

    backup = join(
      await ensureRealBackupRoot(),
      `${receipt.name}.backup-${receipt.version}-${new Date().toISOString().replace(/[:.]/g, "-")}`,
    );
    await lstat(backup).then(
      () => fail("Backup path already exists."),
      (error) => {
        if (error.code !== "ENOENT") throw error;
      },
    );
    await rename(skillRoot, backup);
    oldMoved = true;
    try {
      await rename(stagedSkill, skillRoot);
      oldMoved = false;
    } catch (error) {
      await rename(backup, skillRoot);
      oldMoved = false;
      throw error;
    }
    await writeCache(receipt.name, {
      schemaVersion: 1,
      name: receipt.name,
      checkedAt: new Date().toISOString(),
      latest: entry.version,
      refreshAvailable: false,
    });
    console.log(`Updated to ${receipt.name}@${entry.version}. Backup kept outside the skills directory at ${backup}`);
  } finally {
    if (oldMoved && backup) {
      await rename(backup, skillRoot).catch(() => {});
    }
    if (staging) await rm(staging, { recursive: true, force: true });
    await rm(lock, { recursive: true, force: true });
  }
}

async function main() {
  const args = process.argv.slice(2);
  if (!args.length || (args.length === 1 && ["--help", "-h"].includes(args[0]))) {
    console.log(help);
    return;
  }
  const command = args.shift();
  if (!["status", "suite-status", "check", "update"].includes(command)) {
    fail("Unknown command. Use --help.");
  }
  let confirmation;
  let targetDirectory;
  while (args.length) {
    const option = args.shift();
    if (option === "--confirm" && confirmation === undefined) {
      confirmation = args.shift();
      if (!confirmation || confirmation.startsWith("--")) fail("Missing value for --confirm.");
    } else if (option === "--dir" && targetDirectory === undefined) {
      targetDirectory = args.shift();
      if (!targetDirectory || !isAbsolute(targetDirectory)) fail("--dir requires an absolute skill directory.");
    } else {
      fail("Unknown or duplicate option.");
    }
  }
  if (command !== "update" && confirmation !== undefined) fail("--confirm is only valid with update.");
  if (command !== "update" && targetDirectory !== undefined) fail("--dir is only valid with update.");
  if (targetDirectory !== undefined) {
    const target = resolve(targetDirectory);
    if (basename(target) !== basename(skillRoot)) {
      fail("--dir must name the same Skill as this manager.");
    }
    const stat = await lstat(target).catch((error) => {
      if (error.code === "ENOENT") fail("--dir installed skill directory does not exist.");
      throw error;
    });
    if (!stat.isDirectory() || stat.isSymbolicLink()) fail("--dir must name a real installed skill directory.");
    skillRoot = target;
  }
  if (command === "suite-status") {
    await commandSuiteStatus();
    return;
  }
  const receipt = await readReceipt();
  if (command === "status") await commandStatus(receipt);
  else if (command === "check") await commandCheck(receipt);
  else await commandUpdate(receipt, confirmation);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : "Skill manager failed.");
  process.exitCode = 1;
});
