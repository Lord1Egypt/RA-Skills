import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { execFileSync } from "node:child_process";

export const SUPPORTED_VERSION = "2026.9.5";
export const AUDITED_HASHES = Object.freeze([
  "b709fab02c05e8d90846a96e9fc58b86ac14055af8b5e2402dcbad1c83645eae",
  "a56adeaaae73a2805235c1578a3fcb8d8c56291014d1ca5aab84b05bdde7a766",
]);

const digest = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const sameFile = (a, b) => a.dev === b.dev && a.ino === b.ino;
const samePath = (a, b) => process.platform === "win32"
  ? a.toLowerCase() === b.toLowerCase() : a === b;

function chain(target) {
  if (typeof target !== "string" || !path.isAbsolute(target) || /^[\\/]{2}/.test(target) || /[\x00-\x1f]/.test(target)) throw new Error("unsafe-path");
  if (target.replaceAll("\\", "/").split("/").some(p => p === "." || p === "..")) throw new Error("unsafe-path");
  const absolute = path.resolve(target), root = path.parse(absolute).root;
  const items = [root];
  let current = root;
  for (const part of absolute.slice(root.length).split(path.sep).filter(Boolean)) {
    current = path.join(current, part);
    items.push(current);
  }
  return items;
}

function checkOrdinaryFiles(files) {
  const targets = new Set(files.map(file => path.resolve(file)));
  const all = [...new Set(files.flatMap(chain))];
  for (const current of all) {
    const stat = fs.lstatSync(current);
    if (stat.isSymbolicLink() || (targets.has(current) ? !stat.isFile() || stat.nlink !== 1 : !stat.isDirectory())) throw new Error("unsafe-path");
    if (!samePath(fs.realpathSync.native(current), current)) throw new Error("unsafe-path");
  }
  if (process.platform === "win32") {
    // Node identifies symlinks/junctions but does not expose every reparse tag.
    // A fixed, noninteractive OS helper reads attributes only; paths use stdin.
    const program = path.join(process.env.SystemRoot ?? "C:\\Windows", "System32", "WindowsPowerShell", "v1.0", "powershell.exe");
    const script = "$ErrorActionPreference='Stop'; $items=ConvertFrom-Json ([Console]::In.ReadToEnd()); foreach($item in $items){if(([IO.File]::GetAttributes($item) -band [IO.FileAttributes]::ReparsePoint) -ne 0){exit 7}}; [Console]::Write('ok')";
    const output = execFileSync(program, ["-NoProfile", "-NonInteractive", "-Command", script], {
      input: JSON.stringify(all), encoding: "utf8", windowsHide: true, timeout: 5000,
      maxBuffer: 1024, stdio: ["pipe", "pipe", "ignore"],
    });
    if (output !== "ok") throw new Error("unsafe-path");
  }
}

function readChecked(file) {
  const before = fs.lstatSync(file);
  const fd = fs.openSync(file, fs.constants.O_RDONLY | (fs.constants.O_NOFOLLOW || 0));
  try {
    const opened = fs.fstatSync(fd);
    if (!opened.isFile() || opened.nlink !== 1 || !sameFile(before, opened)) throw new Error("changed-file");
    const bytes = fs.readFileSync(fd);
    const after = fs.lstatSync(file), finished = fs.fstatSync(fd);
    if (!sameFile(opened, after) || finished.size !== opened.size || finished.mtimeMs !== opened.mtimeMs || after.mtimeMs !== opened.mtimeMs) throw new Error("changed-file");
    return bytes;
  } finally { fs.closeSync(fd); }
}

// A trusted OS-owned installation is required. These path checks are not a
// kernel sandbox against a hostile same-account process swapping directories.
export function createIntegrityGuard(entry, selfFiles, options = {}) {
  const version = options.version ?? SUPPORTED_VERSION;
  const hashes = options.hashes ?? AUDITED_HASHES;
  chain(entry);
  const absolute = path.resolve(entry);
  if (!absolute.replaceAll("\\", "/").endsWith("/dist/extensions/active-memory/index.js")) throw new Error("unexpected-entry");
  const packageFile = path.join(path.dirname(absolute), "..", "..", "..", "package.json");
  const files = [absolute, path.resolve(packageFile), ...selfFiles];
  let accepted;
  return {
    check() {
      checkOrdinaryFiles(files);
      const bytes = files.map(readChecked);
      if (JSON.parse(bytes[1].toString("utf8")).version !== version || !hashes.includes(digest(bytes[0]))) throw new Error("runtime-changed");
      const fingerprint = bytes.map(digest).join(":");
      if (accepted && accepted !== fingerprint) throw new Error("runtime-changed");
      // Recheck ancestors after reading, before import or returning context.
      checkOrdinaryFiles(files);
      accepted ??= fingerprint;
      return fingerprint;
    },
  };
}
