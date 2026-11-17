#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {TextDecoder} from "node:util";
import {fileURLToPath} from "node:url";

const EXIT = Object.freeze({
  OK: 0,
  FINDINGS: 1,
  USAGE_OR_OPERATIONAL: 2,
});
const DEFAULT_ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const IGNORED_DIRECTORIES = new Set([".git", "node_modules", "coverage"]);
const CONTROL_FILES = new Set([".ota-deny-list.txt", ".ota-allow-list.txt"]);
const BINARY_EXTENSIONS = new Set([
  ".7z",
  ".a",
  ".avi",
  ".bin",
  ".bmp",
  ".class",
  ".db",
  ".dmg",
  ".doc",
  ".docx",
  ".eot",
  ".exe",
  ".gif",
  ".gz",
  ".ico",
  ".jar",
  ".jpeg",
  ".jpg",
  ".lockb",
  ".m4a",
  ".mov",
  ".mp3",
  ".mp4",
  ".o",
  ".otf",
  ".pdf",
  ".png",
  ".pyc",
  ".so",
  ".sqlite",
  ".tar",
  ".tif",
  ".tiff",
  ".ttf",
  ".wav",
  ".webm",
  ".webp",
  ".woff",
  ".woff2",
  ".xls",
  ".xlsx",
  ".zip",
]);
const PLACEHOLDER_HOME_NAMES = new Set([
  "demo",
  "example",
  "placeholder",
  "sample",
  "test",
  "user",
  "username",
  "your-user",
  "yourname",
]);
const utf8Decoder = new TextDecoder("utf-8", {fatal: true});

function usage(message) {
  console.error("Usage: node scripts/check-public-safety.mjs [--root <repository-root>]");
  if (message) console.error(message);
  process.exit(EXIT.USAGE_OR_OPERATIONAL);
}

function parseArguments(argv) {
  let requestedRoot = DEFAULT_ROOT;
  let rootSeen = false;
  for (let index = 0; index < argv.length; index += 1) {
    const option = argv[index];
    if (option !== "--root") usage("unknown or unsupported option");
    if (rootSeen) usage("duplicate option: --root");
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) usage("--root requires a value");
    requestedRoot = path.resolve(value);
    rootSeen = true;
    index += 1;
  }
  return requestedRoot;
}

function toPosix(value) {
  return value.split(path.sep).join("/");
}

function safeRelative(root, absolutePath) {
  const relative = path.relative(root, absolutePath);
  if (
    relative === ""
    || (
      relative !== ".."
      && !relative.startsWith(`..${path.sep}`)
      && !path.isAbsolute(relative)
    )
  ) {
    return relative ? toPosix(relative) : ".";
  }
  return "<outside-root>";
}

function readControlList(root, fileName, operations) {
  const absolutePath = path.join(root, fileName);
  let stat;
  try {
    stat = fs.lstatSync(absolutePath);
  } catch (error) {
    if (error?.code === "ENOENT") return [];
    operations.push({path: fileName, rule: "CONTROL_LIST_READ_FAILED"});
    return [];
  }
  if (stat.isSymbolicLink()) {
    // The recursive walk reports every symlink as a release finding. Do not
    // follow a control-file link while loading policy.
    return [];
  }
  if (!stat.isFile()) {
    operations.push({path: fileName, rule: "CONTROL_LIST_NOT_FILE"});
    return [];
  }
  try {
    return fs.readFileSync(absolutePath, "utf8")
      .split(/\r?\n/u)
      .map((line) => line.trim())
      .filter((line) => line && !line.startsWith("#"));
  } catch {
    operations.push({path: fileName, rule: "CONTROL_LIST_READ_FAILED"});
    return [];
  }
}

function looksBinary(filePath, buffer) {
  if (BINARY_EXTENSIONS.has(path.extname(filePath).toLocaleLowerCase("en-US"))) {
    return true;
  }
  const sample = buffer.subarray(0, Math.min(buffer.length, 8192));
  if (sample.includes(0)) return true;
  try {
    utf8Decoder.decode(buffer);
    return false;
  } catch {
    return true;
  }
}

function tokenPatterns() {
  const privateKeyHeader = [
    "-".repeat(5),
    "BEGIN ",
    "(?:(?:RSA|EC|DSA|OPENSSH) )?",
    "PRIVATE KEY",
    "-".repeat(5),
  ].join("");
  return [
    {
      rule: "PRIVATE_KEY_MATERIAL",
      regex: new RegExp(privateKeyHeader, "gu"),
    },
    {
      rule: "SECRET_TOKEN",
      regex: new RegExp(`${"AK"}${"IA"}[0-9A-Z]{16}`, "gu"),
    },
    {
      rule: "SECRET_TOKEN",
      regex: new RegExp(`${"gh"}[pousr]_[A-Za-z0-9]{30,}`, "gu"),
    },
    {
      rule: "SECRET_TOKEN",
      regex: new RegExp(`${"github"}_${"pat"}_[A-Za-z0-9_]{20,}`, "gu"),
    },
    {
      rule: "SECRET_TOKEN",
      regex: new RegExp(`${"xo"}x[baprs]-[A-Za-z0-9-]{20,}`, "gu"),
    },
    {
      rule: "SECRET_TOKEN",
      regex: new RegExp(`${"AI"}za[0-9A-Za-z_-]{35}`, "gu"),
    },
    {
      rule: "SECRET_TOKEN",
      regex: new RegExp(`${"s"}k-(?:ant-[A-Za-z0-9_-]{16,}|[A-Za-z0-9_-]{20,})`, "gu"),
    },
    {
      rule: "SECRET_TOKEN",
      regex: new RegExp(`${"npm"}_[A-Za-z0-9]{30,}`, "gu"),
    },
    {
      rule: "SECRET_TOKEN",
      regex: new RegExp(`${"ey"}J[A-Za-z0-9_-]{10,}\\.[A-Za-z0-9_-]{10,}\\.[A-Za-z0-9_-]{10,}`, "gu"),
    },
    {
      rule: "SECRET_TOKEN",
      regex: new RegExp(`${"Bearer"}\\s+[A-Za-z0-9._~-]{20,}`, "giu"),
    },
  ];
}

const TOKEN_PATTERNS = tokenPatterns();
const UNIX_HOME_PATTERN = /\/(?:Users|home)\/([^/\\\s"'`<>]+)/gu;
const WINDOWS_HOME_PATTERN = /[A-Za-z]:\\Users\\([^/\\\s"'`<>]+)/gu;
const SECRET_ASSIGNMENT_PATTERN = new RegExp(
  [
    "['\"]?",
    "\\b(?:api[_-]?key|apikey|client[_-]?secret|secret[_-]?key|password|passwd|access[_-]?token|auth[_-]?token|private[_-]?key)\\b",
    "['\"]?",
    "\\s*[:=]\\s*",
    "['\"]?([^\\s'\",;}{]{16,})",
  ].join(""),
  "giu",
);

function isAllowed(value, allowList) {
  return allowList.has(value);
}

function isPlaceholderSecret(value) {
  return /^(?:change[-_]?me|dummy|example|fixture|placeholder|replace[-_]?me|sample|test[-_]?only|your[-_](?:api[-_]?key|client[-_]?secret|secret[-_]?key|password|access[-_]?token|auth[-_]?token|private[-_]?key)(?:[-_]?here)?|x{8,})$/iu
    .test(value);
}

function inspectLine({
  line,
  lineNumber,
  relativePath,
  allowList,
  denyList,
  addFinding,
}) {
  for (const pattern of [UNIX_HOME_PATTERN, WINDOWS_HOME_PATTERN]) {
    pattern.lastIndex = 0;
    let match;
    while ((match = pattern.exec(line))) {
      const userName = match[1].toLocaleLowerCase("en-US");
      if (
        PLACEHOLDER_HOME_NAMES.has(userName)
      ) {
        continue;
      }
      addFinding(relativePath, "ABSOLUTE_HOME_PATH", lineNumber);
    }
  }

  for (const {rule, regex} of TOKEN_PATTERNS) {
    regex.lastIndex = 0;
    let match;
    while ((match = regex.exec(line))) {
      addFinding(relativePath, rule, lineNumber);
    }
  }

  SECRET_ASSIGNMENT_PATTERN.lastIndex = 0;
  let assignment;
  while ((assignment = SECRET_ASSIGNMENT_PATTERN.exec(line))) {
    const value = assignment[1];
    if (!isPlaceholderSecret(value)) {
      addFinding(relativePath, "SECRET_ASSIGNMENT", lineNumber);
    }
  }

  for (const denied of denyList) {
    if (
      !isAllowed(denied, allowList)
      && line.includes(denied)
    ) {
      addFinding(relativePath, "LOCAL_DENY_LITERAL", lineNumber);
    }
  }
}

function main() {
  const requestedRoot = parseArguments(process.argv.slice(2));
  let requestedStat;
  try {
    requestedStat = fs.lstatSync(requestedRoot);
  } catch (error) {
    console.error(`ERROR path=. rule=ROOT_UNAVAILABLE line=0 code=${error?.code ?? "READ_FAILED"}`);
    process.exit(EXIT.USAGE_OR_OPERATIONAL);
  }

  if (requestedStat.isSymbolicLink()) {
    console.error("FAIL path=. rule=SYMLINK line=0");
    console.error("public safety audit failed: 1 finding(s)");
    process.exit(EXIT.FINDINGS);
  }
  if (!requestedStat.isDirectory()) {
    console.error("ERROR path=. rule=ROOT_NOT_DIRECTORY line=0");
    process.exit(EXIT.USAGE_OR_OPERATIONAL);
  }

  let root;
  try {
    root = fs.realpathSync(requestedRoot);
  } catch (error) {
    console.error(`ERROR path=. rule=ROOT_UNAVAILABLE line=0 code=${error?.code ?? "READ_FAILED"}`);
    process.exit(EXIT.USAGE_OR_OPERATIONAL);
  }

  const operations = [];
  const denyList = readControlList(root, ".ota-deny-list.txt", operations);
  const allowList = new Set(
    readControlList(root, ".ota-allow-list.txt", operations),
  );
  const findings = [];
  const findingKeys = new Set();
  let scannedTextFiles = 0;

  function addFinding(relativePath, rule, line) {
    const key = `${relativePath}\0${rule}\0${line}`;
    if (findingKeys.has(key)) return;
    findingKeys.add(key);
    findings.push({path: relativePath, rule, line});
  }

  function visit(directory) {
    let entries;
    try {
      entries = fs.readdirSync(directory, {withFileTypes: true});
    } catch {
      operations.push({
        path: safeRelative(root, directory),
        rule: "DIRECTORY_READ_FAILED",
      });
      return;
    }
    entries.sort((left, right) => left.name.localeCompare(right.name));

    for (const entry of entries) {
      const absolutePath = path.join(directory, entry.name);
      const relativePath = safeRelative(root, absolutePath);
      if (IGNORED_DIRECTORIES.has(entry.name)) continue;
      if (entry.isSymbolicLink()) {
        addFinding(relativePath, "SYMLINK", 0);
        continue;
      }
      if (entry.isDirectory()) {
        visit(absolutePath);
        continue;
      }
      if (!entry.isFile()) continue;

      let buffer;
      try {
        buffer = fs.readFileSync(absolutePath);
      } catch {
        operations.push({path: relativePath, rule: "FILE_READ_FAILED"});
        continue;
      }
      if (looksBinary(absolutePath, buffer)) continue;

      let text;
      try {
        text = utf8Decoder.decode(buffer);
      } catch {
        continue;
      }
      scannedTextFiles += 1;
      const lines = text.split(/\r?\n/u);
      for (let index = 0; index < lines.length; index += 1) {
        inspectLine({
          line: lines[index],
          lineNumber: index + 1,
          relativePath,
          allowList,
          denyList: CONTROL_FILES.has(relativePath) ? [] : denyList,
          addFinding,
        });
      }
    }
  }

  visit(root);

  if (operations.length > 0) {
    operations.sort((left, right) => (
      left.path.localeCompare(right.path)
      || left.rule.localeCompare(right.rule)
    ));
    for (const operation of operations) {
      console.error(`ERROR path=${operation.path} rule=${operation.rule} line=0`);
    }
    console.error(`public safety audit unavailable: ${operations.length} operational error(s)`);
    process.exit(EXIT.USAGE_OR_OPERATIONAL);
  }

  findings.sort((left, right) => (
    left.path.localeCompare(right.path)
    || left.line - right.line
    || left.rule.localeCompare(right.rule)
  ));
  if (findings.length > 0) {
    for (const finding of findings) {
      console.error(`FAIL path=${finding.path} rule=${finding.rule} line=${finding.line}`);
    }
    console.error(`public safety audit failed: ${findings.length} finding(s)`);
    process.exit(EXIT.FINDINGS);
  }

  console.log(`public safety audit passed: ${scannedTextFiles} text file(s) scanned`);
  process.exit(EXIT.OK);
}

main();
