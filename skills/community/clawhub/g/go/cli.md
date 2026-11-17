# CLI — Flags, Exit Codes, Signals, and Pipes

A Go binary is the easiest artifact to distribute in the language, which is why so many Go CLIs exist and why so many of them ignore the conventions that make a tool composable.

## The main Shape

```go
func main() {
    if err := run(os.Args[1:], os.Stdout, os.Stderr); err != nil {
        fmt.Fprintln(os.Stderr, "myapp:", err)
        os.Exit(1)
    }
}

func run(args []string, stdout, stderr io.Writer) error { ... }
```

- `main` does three things: call `run`, print the error, set the exit code. Everything else is testable code that returns an error.
- `os.Exit` **skips every deferred call** — no buffered-writer flush, no temp-file cleanup, no trace export. So it appears exactly once, in `main`, after all defers have already run in `run`. `log.Fatal` and `log.Panic` call `os.Exit` too, which is why they do not belong below `main` (`errors.md`).
- Injecting `stdout`/`stderr` as `io.Writer` parameters makes the whole CLI testable with `bytes.Buffer`, no subprocess required (`testing.md`).

## Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success — and nothing else |
| 1 | Generic failure |
| 2 | Usage error (what the `flag` package emits on a bad flag) |
| 3+ | Domain-specific, documented in `--help` |
| 130 / 143 | Killed by SIGINT / SIGTERM (128 + signal number) |

Reserve distinct codes only when a caller will branch on them; otherwise 0 and 1 with a clear stderr message is better. Every non-zero exit prints a human-readable reason to stderr first.

## Flags

- The stdlib `flag` package covers single-command tools: `flag.StringVar(&cfg.Addr, "addr", ":8080", "listen address")`, then `flag.Parse()`.
- `flag` is GNU-incompatible on purpose: `-flag` and `--flag` are equivalent, `-abc` is one flag named `abc` and not three short flags, and flags must come **before** positional arguments — `mytool file.txt -v` leaves `-v` in `flag.Args()`. Say so in the help text or use a third-party parser.
- Subcommands with stdlib flag: one `flag.NewFlagSet` per subcommand, dispatch on `os.Args[1]`, then `fs.Parse(os.Args[2:])`. Beyond three subcommands, a router library is less code.
- Precedence order, documented and implemented consistently: defaults < config file < environment < flags. Anything else surprises operators.
- Environment variables for anything sensitive; a token on the command line is visible in the process list to every user on the box (`security.md`).
- `flag.Parse()` in `init()` or in a package-level variable breaks tests, because the test binary has its own flags. Parse inside `run`.

## Signals

```go
ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
defer stop()
```

- `signal.NotifyContext` (`go >=1.16`) is the modern form: the context cancels on the first signal, and the work stops through the normal cancellation path (`context.md`).
- **The second signal should kill.** Call `stop()` after the first one so the default handler is restored; a tool that ignores a second Ctrl-C during a slow shutdown forces the user to reach for `kill -9`.
- SIGKILL and SIGSTOP cannot be caught. Whatever must survive them belongs in the on-disk format, not in a shutdown hook.
- `SIGQUIT` (Ctrl-\) is the runtime's stack-dump signal; catching it takes away a debugging tool (`debugging.md`).
- Long operations must check `ctx.Done()` between units of work, or Ctrl-C does nothing visible and the user assumes the tool is hung.

## Pipes, TTY, and Output

- Data to **stdout**, diagnostics and progress to **stderr**. A tool that writes logs to stdout cannot be piped into `jq`.
- Detect a terminal before adding color, spinners, or progress bars: `fi, _ := os.Stdout.Stat(); isTTY := fi.Mode()&os.ModeCharDevice != 0`. Honor `NO_COLOR` when set, and offer `--no-color`.
- Reading piped stdin: the same stat check tells you whether stdin is a pipe (`os.ModeCharDevice` unset), so the tool can accept either a filename argument or piped input.
- Buffer stdout with `bufio.NewWriter` for high-volume output and flush before returning; unbuffered `os.Stdout` is one syscall per write (`io.md`).
- `EPIPE` is normal: when the reader in `mytool | head` exits, your writes fail. Exit quietly rather than printing a stack.
- Machine-readable mode (`--json`) with a stable schema is what makes a tool scriptable; keep the human format free to change.

## Configuration Files

- Search order that operators expect: `--config` flag → `$XDG_CONFIG_HOME/<tool>/config.yaml` → `~/.config/<tool>/config.yaml` → a system path. Never write outside those without asking.
- `os.UserConfigDir()` and `os.UserCacheDir()` return the right per-OS location; hard-coding `~/.config` breaks on Windows and macOS conventions.
- A missing config file is not an error — defaults are. A *malformed* one is a fatal error with the file path and line in the message.

## Subprocesses

- `exec.CommandContext(ctx, "git", "status")` takes an **argument slice**, so there is no shell and no injection surface. `exec.Command("sh", "-c", userInput)` reintroduces both (`security.md`).
- The context kills the process on cancellation, but by default only the direct child — a child that spawned its own children can leave orphans. Set `Cancel`/`WaitDelay` (`go >=1.20`) or use a process group when that matters.
- `cmd.Output()` captures stdout and fills `ExitError.Stderr` on failure; `cmd.CombinedOutput()` interleaves both. For a long-running child, wire `cmd.Stdout`/`cmd.Stderr` to your own writers and stream.
- Deadlock: setting `cmd.Stdout` to an `os.Pipe` you never read fills the pipe buffer and blocks the child forever. Read concurrently, or use the helpers.
- Always check `exec.LookPath` or handle `exec.ErrNotFound` with a message naming the missing binary — "exec: git: executable file not found in $PATH" is clearer when you add "install git or set GIT_PATH".

## Distribution

- Cross-compile from one machine: `CGO_ENABLED=0 GOOS=darwin GOARCH=arm64 go build` (`build.md`).
- Stamp version metadata with `-ldflags "-X main.version=$(git describe --tags)"`; from `go >=1.18` the build also embeds VCS info readable via `runtime/debug.ReadBuildInfo()`, so `--version` can work with no ldflags at all.
- `go install example.com/cmd/tool@latest` is the zero-infrastructure distribution channel for Go users; a release archive of prebuilt binaries covers everyone else.

## Back To SKILL.md

Exit-code and defer interaction is in SKILL.md Traps. Signals and shutdown for servers: `deployment.md`. Structured output vs logs: `logging.md`.
