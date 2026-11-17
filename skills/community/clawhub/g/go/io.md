# I/O — Readers, Writers, Files, and Close Errors

`io.Reader` and `io.Writer` are the two most important interfaces in Go: one method each, and everything composes through them. The traps are in the contract details — partial reads, `Close` errors on writers, and buffers nobody flushed.

## The Reader Contract

```go
n, err := r.Read(p)
```

- `Read` may return `0 < n < len(p)` **and** `err == nil`. It is not short-circuited or broken: a socket, a pipe, and a decompressor all do this routinely. Code that assumes one `Read` fills the buffer works locally against a file and fails against a network.
- `Read` may return `n > 0` **together with** `io.EOF`. Process the n bytes first, then handle the error, or you drop the last chunk of every stream.
- Never write the loop by hand when a helper exists: `io.ReadFull(r, buf)` for exactly len(buf) bytes, `io.ReadAll(r)` for everything, `io.Copy(dst, src)` to stream.
- `io.EOF` is a value, not a failure: `errors.Is(err, io.EOF)` means clean end. `io.ErrUnexpectedEOF` means the stream ended mid-structure, which *is* a failure.
- `io.ReadAll` on untrusted input has no bound. Wrap it: `io.ReadAll(io.LimitReader(r, maxBytes))`, and detect truncation by checking whether you got exactly maxBytes (`security.md`).

## The Writer Contract

- `Write` returns an error if `n < len(p)`, so a short write is always accompanied by an error — the reader asymmetry does not apply.
- **Writers can fail on `Close`.** The bytes may still be in a buffer or in flight; `Close` is where the flush error surfaces. `defer f.Close()` on a file you wrote silently discards it, and a truncated file looks like a successful run.

```go
func writeReport(path string, data []byte) (err error) {
    f, err := os.Create(path)
    if err != nil { return err }
    defer func() { err = errors.Join(err, f.Close()) }()   // named return
    _, err = f.Write(data)
    return err
}
```

- Named return plus `errors.Join` in the defer is the correct shape (`errors.md`). For read-only files, `defer f.Close()` is fine — there is nothing to flush.
- A `bufio.Writer` must be **flushed**: `defer w.Flush()` before `defer f.Close()` in the source, so it runs first (defers are LIFO). Forgetting `Flush` is the other way to produce a truncated file with no error.

## Composition Toolkit

| Need | Use |
|---|---|
| String or bytes as a Reader | `strings.NewReader(s)`, `bytes.NewReader(b)` — no copy |
| Collect output in memory | `bytes.Buffer` (implements both Reader and Writer) |
| Cap how much is read | `io.LimitReader(r, n)` |
| Write to two places at once | `io.MultiWriter(f, os.Stdout)` |
| Concatenate readers | `io.MultiReader(a, b)` |
| Discard output | `io.Discard` (never `os.DevNull` for this) |
| Tee input to a log while reading it | `io.TeeReader(r, logw)` |
| Connect a producer function to a consuming reader | `io.Pipe` — synchronous, needs a goroutine on one side |
| Line-by-line reading | `bufio.Scanner` |

- `io.Copy` uses `WriteTo`/`ReadFrom` when available, which lets `os.File`→`os.File` and `net.Conn`→`os.File` copies bypass user space entirely. Hand-rolling a copy loop forfeits that.
- `io.Pipe` deadlocks when both ends run in the same goroutine: the writer blocks until a reader consumes. Always run one side in its own goroutine and close the writer to signal EOF.

## bufio.Scanner

- Default maximum token size is 64 KB; a longer line stops the scan with `bufio.ErrTooLong`. Raise it with `sc.Buffer(make([]byte, 0, 1<<20), 1<<20)`, or use `bufio.Reader.ReadString('\n')` for genuinely unbounded lines.
- **Always check `sc.Err()` after the loop.** `Scan()` returns false for both EOF and error; skipping the check turns a read failure into a silently truncated file — the same shape as `rows.Err()` in `database.md`.
- `sc.Bytes()` returns a slice that is **invalidated by the next `Scan()`**. Keep it with `append([]byte(nil), sc.Bytes()...)` or `sc.Text()`, which allocates a string copy.
- `sc.Split(bufio.ScanWords)` / `ScanRunes` for other tokenizations.

## Files

- `os.ReadFile` / `os.WriteFile` (`go >=1.16`) for whole small files; stream anything that could be large.
- File permissions passed to `os.WriteFile` and `os.OpenFile` are masked by the process umask, so `0666` typically lands as `0644`. Config and secret files: `0600` explicitly, and verify after creation if it matters (`security.md`).
- **Atomic replace**: write to a temp file in the *same directory*, `f.Sync()`, close, then `os.Rename`. Rename is atomic within a filesystem, so a reader sees either the old file or the new one, never a half-written one. A temp file in `/tmp` breaks this when `/tmp` is a different mount.
- `os.Create` truncates an existing file. Use `os.OpenFile(path, os.O_WRONLY|os.O_CREATE|os.O_EXCL, 0600)` when overwriting must fail instead.
- Path handling: `filepath` for the local OS (it uses `\` on Windows), `path` only for slash-separated things like URLs. Building paths with `+ "/" +` breaks on Windows (`build.md`).
- Cleanup: `defer os.Remove(tmp)` after the rename is a no-op and keeps the failure path clean. In tests, `t.TempDir()` handles it (`testing.md`).

## io/fs and Directory Containment

- `io/fs` (`go >=1.16`) abstracts a file tree: `fs.FS` is satisfied by `os.DirFS(root)`, by an `embed.FS`, and by a zip. Writing helpers against `fs.FS` makes them testable without touching disk (`build.md` for `go:embed`).
- `filepath.Walk` calls a function per entry and stats each one; `filepath.WalkDir` (`go >=1.16`) passes a `fs.DirEntry` and avoids the stat — meaningfully faster on large trees. Return `fs.SkipDir` to prune a subtree.
- `os.DirFS` restricts *paths*, not symlink targets. For hard containment against traversal and symlink escapes use `os.Root` (`go >=1.24`), which resolves every operation inside the root (`security.md`).

## Standard Streams and Exit

- `os.Stdout` is unbuffered: a per-line `fmt.Println` in a hot loop is one syscall per line. Wrap in `bufio.NewWriter(os.Stdout)` and flush before exit.
- `os.Exit` skips defers, so a buffered stdout wrapper loses everything not yet flushed (`cli.md`).
- Data on stdout, diagnostics on stderr. A tool that logs to stdout cannot be piped.

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| One `Read` assumed to fill the buffer | Works on files, corrupts on sockets | `io.ReadFull` or `io.Copy` |
| `defer f.Close()` on a written file | Flush error dropped; truncated output looks successful | Named return + `errors.Join(err, f.Close())` |
| `bufio.Writer` never flushed | Tail of the file missing | `defer w.Flush()` before the Close defer |
| `sc.Err()` unchecked after `Scan` | Read failures become short files | Check it, always |
| Keeping `sc.Bytes()` past the next Scan | Data mutates under you | Copy or use `sc.Text()` |
| `io.ReadAll` on a network body | Unbounded memory from a hostile peer | `io.LimitReader` |
| Temp file in `/tmp` then rename to `/var/lib` | `invalid cross-device link` | Temp file in the destination directory |
| `path.Join` for filesystem paths | Wrong separators on Windows | `filepath.Join` |

## Back To SKILL.md

Defer-in-loop rule: SKILL.md Core Rule 5. Error joining and named returns: `errors.md`. Streaming JSON: `json.md`.
