import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

// These checks reject poisoned on-disk links. The workspace must still be
// owned by a trusted OS account: portable Node path APIs are not a kernel
// sandbox against a process concurrently renaming ancestor directories.
export class UnsafePathError extends Error {
  constructor() { super("Unsafe filesystem path or changed file identity"); }
}

function sameFile(a: fs.Stats, b: fs.Stats): boolean {
  return a.dev === b.dev && a.ino === b.ino;
}

function samePath(a: string, b: string): boolean {
  const left = path.resolve(a), right = path.resolve(b);
  return process.platform === "win32" ? left.toLowerCase() === right.toLowerCase() : left === right;
}

function statOrMissing(target: string): fs.Stats | null {
  try { return fs.lstatSync(target); }
  catch (error: any) {
    if (error?.code === "ENOENT") return null;
    throw error;
  }
}

export function assertDirectory(directory: string): string {
  const absolute = path.resolve(directory);
  const parsed = path.parse(absolute);
  let current = parsed.root;
  for (const part of absolute.slice(parsed.root.length).split(path.sep).filter(Boolean)) {
    current = path.join(current, part);
    const stats = fs.lstatSync(current);
    if (stats.isSymbolicLink() || !stats.isDirectory()) throw new UnsafePathError();
    if (!samePath(fs.realpathSync(current), current)) throw new UnsafePathError();
  }
  return absolute;
}

export function relativeParts(rawValue: string): string[] {
  const raw = rawValue.replace(/\\/g, "/");
  if (!raw || raw !== raw.trim() || raw.startsWith("/") || path.win32.isAbsolute(raw)) throw new UnsafePathError();
  const parts = raw.split("/");
  if (parts.some(part => !part || part === "." || part === ".." ||
      /[\x00-\x1f<>:"|?*]/.test(part) || /[. ]$/.test(part) ||
      /^(?:con|prn|aux|nul|com[1-9¹²³]|lpt[1-9¹²³])(?:\.|$)/i.test(part))) throw new UnsafePathError();
  return parts;
}

export class SafeFiles {
  root: string;
  rootIdentity: fs.Stats;
  constructor(root: string) {
    this.root = assertDirectory(root);
    this.rootIdentity = fs.lstatSync(this.root);
  }

  check(relative: string, allowMissing = false): { target: string; stats: fs.Stats | null; parent: fs.Stats } {
    const parts = relativeParts(relative);
    const root = assertDirectory(this.root);
    if (!sameFile(this.rootIdentity, fs.lstatSync(root))) throw new UnsafePathError();
    const target = path.join(root, ...parts);
    const parentDir = assertDirectory(path.dirname(target));
    const realRelative = path.relative(root, fs.realpathSync(parentDir));
    if (realRelative === ".." || realRelative.startsWith(`..${path.sep}`) || path.isAbsolute(realRelative)) throw new UnsafePathError();
    const stats = statOrMissing(target);
    if (!stats && !allowMissing) throw Object.assign(new Error("File missing"), { code: "ENOENT" });
    if (stats && (stats.isSymbolicLink() || !stats.isFile() || stats.nlink !== 1)) throw new UnsafePathError();
    if (stats && !samePath(fs.realpathSync(target), target)) throw new UnsafePathError();
    return { target, stats, parent: fs.lstatSync(parentDir) };
  }

  read(relative: string): string {
    const initial = this.check(relative);
    const fd = fs.openSync(initial.target, fs.constants.O_RDONLY | (fs.constants.O_NOFOLLOW || 0));
    try {
      const actual = fs.fstatSync(fd);
      const checked = this.check(relative);
      if (!actual.isFile() || actual.nlink !== 1 || !sameFile(actual, initial.stats!) || !sameFile(actual, checked.stats!)) throw new UnsafePathError();
      const content = fs.readFileSync(fd, "utf8");
      const after = this.check(relative);
      if (!sameFile(actual, after.stats!) || !sameFile(initial.parent, after.parent)) throw new UnsafePathError();
      return content;
    } finally { fs.closeSync(fd); }
  }

  write(relative: string, content: string): void {
    const initial = this.check(relative, true);
    if (process.platform === "win32" && initial.stats) {
      // Node does not expose Windows DACL cloning. Replacing an existing file
      // would silently inherit its parent's ACL, potentially broadening access.
      // Keep the verified file object (and its ACL); on ordinary I/O failure
      // restore its bytes best-effort. This branch is not crash-atomic.
      const fd = fs.openSync(initial.target, fs.constants.O_RDWR | (fs.constants.O_NOFOLLOW || 0));
      let previous: Buffer | undefined;
      let started = false;
      const put = (bytes: Buffer) => {
        let offset = 0;
        while (offset < bytes.length) {
          const written = fs.writeSync(fd, bytes, offset, bytes.length - offset, offset);
          if (!written) throw new Error("File write made no progress");
          offset += written;
        }
        fs.ftruncateSync(fd, bytes.length);
        fs.fsyncSync(fd);
      };
      try {
        const actual = fs.fstatSync(fd);
        const checked = this.check(relative);
        if (!actual.isFile() || actual.nlink !== 1 || !sameFile(actual, initial.stats) || !sameFile(actual, checked.stats!) || !sameFile(initial.parent, checked.parent)) throw new UnsafePathError();
        previous = fs.readFileSync(fd);
        const beforeWrite = this.check(relative);
        if (!sameFile(actual, beforeWrite.stats!) || !sameFile(initial.parent, beforeWrite.parent)) throw new UnsafePathError();
        started = true;
        put(Buffer.from(content, "utf8"));
        const after = this.check(relative);
        if (!sameFile(actual, after.stats!) || !sameFile(initial.parent, after.parent)) throw new UnsafePathError();
      } catch (error) {
        if (started && previous) {
          try { put(previous); } catch { /* Surface original failure; caller must reconcile after an I/O failure. */ }
        }
        throw error;
      } finally { fs.closeSync(fd); }
      return;
    }
    const tempRelative = [...relativeParts(relative).slice(0, -1), `.hui-yi-${crypto.randomBytes(16).toString("hex")}.tmp`].join("/");
    const temp = this.check(tempRelative, true);
    if (temp.stats) throw new UnsafePathError();
    let fd: number | undefined;
    let identity: fs.Stats | undefined;
    try {
      fd = fs.openSync(temp.target, fs.constants.O_WRONLY | fs.constants.O_CREAT | fs.constants.O_EXCL | (fs.constants.O_NOFOLLOW || 0), initial.stats ? initial.stats.mode & 0o777 : 0o600);
      identity = fs.fstatSync(fd);
      const beforeWrite = this.check(tempRelative);
      if (!sameFile(identity, beforeWrite.stats!) || !sameFile(initial.parent, beforeWrite.parent)) throw new UnsafePathError();
      fs.writeFileSync(fd, content, "utf8");
      fs.fsyncSync(fd);
      fs.closeSync(fd); fd = undefined;
      const destination = this.check(relative, true);
      const staged = this.check(tempRelative);
      if (!sameFile(initial.parent, destination.parent) || !sameFile(identity, staged.stats!) ||
          Boolean(initial.stats) !== Boolean(destination.stats) ||
          (initial.stats && !sameFile(initial.stats, destination.stats!))) throw new UnsafePathError();
      fs.renameSync(temp.target, destination.target);
    } finally {
      if (fd !== undefined) fs.closeSync(fd);
      // Never follow an altered parent merely to clean up a temporary file.
      try {
        const remaining = this.check(tempRelative, true);
        if (remaining.stats && identity && sameFile(identity, remaining.stats) && sameFile(initial.parent, remaining.parent)) fs.unlinkSync(remaining.target);
      } catch { /* Leave any inaccessible temporary file for its owner. */ }
    }
  }
}
