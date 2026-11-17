# Filesystem — Files, Paths, and Descriptors

Three failure families: blocking the loop with sync I/O, running out of descriptors, and paths that behave differently on someone else's machine.

## Which API

- `node:fs/promises` by default: `await readFile(p, 'utf8')`. Callback `fs` only inside APIs that demand callbacks; `fs.*Sync` only at startup, in CLIs, or in build scripts — never in a request path (SKILL.md rule 1).
- One `readFileSync` of a 20 MB file in a handler blocks every concurrent request for the duration; the same call at boot costs nothing anyone notices.
- Streams for anything whose size you do not control: `readFile` of a user-supplied file loads it entirely into memory, and a file above V8's string cap throws `ERR_STRING_TOO_LONG` before you can even reject it (→ `streams.md`).
- Remember the pool: parallel `fs` work serializes on 4 libuv threads (SKILL.md rule 3), so 100 concurrent reads are 4 at a time, queued.

## Descriptors

- `EMFILE` means the process hit its soft limit (`ulimit -n`, commonly 1024 on Linux, often 256 in a macOS shell). Check with `lsof -p <pid> | wc -l` against `ulimit -n`.
- The cause is almost never the limit: it is unbounded concurrency (SKILL.md rule 4) or a leak. Streams that error without being destroyed, files opened with `fs.open` and never closed, and sockets from an unbounded `Promise.all` are the three sources.
- Raising the limit is legitimate for a genuinely high-connection server, and a mask everywhere else — if the count only ever grows, it is a leak and a bigger limit just moves the crash later.
- `fs.open` requires an explicit `close` on every path including errors; `fs.promises.open` returns a `FileHandle` that also leaks if never closed. Prefer `readFile`/`writeFile`/`createReadStream`, which manage their own descriptor.

## Paths

- Build paths with `path.join`/`path.resolve`, never string concatenation: `dir + '/' + name` breaks on Windows and produces `//` doubles that some tools treat as a different path.
- `path.join` combines and normalizes; `path.resolve` also anchors to an absolute path (from cwd if needed). Use `resolve` whenever the result crosses a security boundary (→ `security.md` for the traversal check).
- Never trust `process.cwd()` for locating your own files — it is wherever the user ran the command. Anchor to the module: `import.meta.dirname` (node >=20.11), else `fileURLToPath(import.meta.url)`, or `__dirname` in CJS.
- macOS and Windows are case-insensitive; Linux is not. An import or a `readFile` with the wrong case works locally and fails in CI (→ `debug.md`). macOS also normalizes Unicode filenames to NFD, so a name that round-trips through the filesystem may not `===` the string you wrote.
- Extension checks are not type checks and path extensions are user input: `path.extname` on `evil.png.js` returns `.js`, and on `evil.js.png` returns `.png`.

## Writing Safely

Never write in place over a file you care about: a crash or a full disk leaves it truncated, and readers can observe the half-written state.

```js
import { writeFile, rename, mkdtemp } from 'node:fs/promises';
const tmp = `${target}.${process.pid}.tmp`;
await writeFile(tmp, data);          // add fsync via a FileHandle when durability matters
await rename(tmp, target);           // atomic within one filesystem
```

- `rename` is atomic only on the same filesystem; across devices it fails with `EXDEV` and needs copy-then-delete, which is not atomic. Keep the temp file in the target's own directory, not in `/tmp`.
- Durability needs `fsync` on the file handle and, strictly, on the directory too — `rename` returning is not the same as the data being on disk after a power loss.
- Concurrent writers need a lock, and there is no portable file lock in core. The `wx` flag (`fs.open(path, 'wx')`) fails if the file exists, which is enough for a simple lock file; stale locks then need an owner-pid check.
- Temp files: `mkdtemp(path.join(os.tmpdir(), 'app-'))` creates a unique directory with safe permissions. A predictable name in a shared `/tmp` is a symlink-attack surface.

## Directories and Metadata

- `mkdir(p, { recursive: true })` is idempotent — no need to check existence first, and the check itself is a race.
- Do not test existence before acting: `existsSync` then `readFile` is a TOCTOU race and doubles the syscalls. Act and handle `ENOENT`.
- `readdir(p, { withFileTypes: true })` returns Dirents, saving a `stat` per entry — on directories with thousands of files that is the difference between one syscall and thousands. `{ recursive: true }` (node >=20) walks the tree without a manual recursion.
- `stat` follows symlinks, `lstat` does not. Walking a tree with `stat` and following links can loop forever.
- File times are unreliable as change detection: coarse granularity on some filesystems, and copies/checkouts rewrite them. Hash content when correctness matters.

## Watching

- `fs.watch` uses OS notifications: efficient, but it fires duplicate events for one save (editors write-and-rename), can report the wrong filename, and behaves differently per platform. Debounce every handler, ~50-100 ms.
- `recursive: true` is supported on macOS and Windows, and on Linux from node >=20. Below that, watch directories individually or accept polling.
- `fs.watchFile` polls: reliable across network filesystems where notifications never arrive, and expensive at scale. Use it only where `watch` is known not to work.
- For development reloads, `node --watch` (stable node >=22) already handles the debounce and restart (→ `commands.md`).

## Large Files and Copies

- `pipeline(createReadStream(src), createWriteStream(dst))` for copies you must transform or observe; `fs.copyFile` for plain copies — it can use a copy-on-write clone on filesystems that support it, which is orders of magnitude faster than reading bytes through JS.
- `highWaterMark` for `createReadStream` defaults to 64 KiB; raising it to 1 MiB for bulk copies cuts syscalls ~16× at the cost of that much memory per concurrent stream (→ `streams.md`).
- Reading a whole file to count lines or find one value is the wrong shape at any size above a few MB: stream and process incrementally, and the memory profile stops depending on the input.
