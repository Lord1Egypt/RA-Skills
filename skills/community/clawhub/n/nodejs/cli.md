# CLI — Building Command-Line Tools in Node

A CLI is a program with three contracts: its exit code, its streams, and its behavior when the terminal is not a terminal. Break any of them and it works by hand but fails in a pipeline.

## The Executable

```json
{ "bin": { "mytool": "./bin/cli.js" }, "type": "module", "files": ["bin", "dist"] }
```

- The entry file needs `#!/usr/bin/env node` as its literal first line, with LF endings — a CRLF shebang fails on Linux with a confusing `bad interpreter` error, so keep `bin/*` out of any CRLF normalization.
- The file must be executable in the published tarball; npm sets the bit on `bin` entries at install time, but a source checkout run directly will not, which is why `./bin/cli.js` fails locally while `npx mytool` works.
- Windows has no shebang: the package manager writes shim scripts. Anything that assumes a POSIX shell inside the CLI (`sh -c`, backticks, `&&` chaining in `spawn`) breaks there (→ `concurrency.md`).
- Keep the entry file thin — parse arguments, then import the implementation. On a `--version` call, the whole module graph loading is the startup time users feel.

## Arguments

- `util.parseArgs` is built in (node >=18.3): declarative options, `strict` mode rejecting unknown flags, and positionals. Reach for a dependency only when you need subcommands, help generation, and shell completion.
- Support `--flag=value` and `--flag value`, and `--` to stop parsing so users can pass through arguments to a wrapped tool.
- Precedence, highest first: command-line flag → environment variable → config file → built-in default. Document it; the surprise is always a config file quietly beating an explicit flag.
- `--help` and `--version` exit 0 and print to stdout — they are successful outputs, not errors. Usage printed after a *bad* invocation goes to stderr with a non-zero exit.
- Validate arguments before doing anything destructive, and echo back the interpretation for destructive operations (`Deleting 412 files under /tmp/x — pass --yes to proceed`).

## Streams: The Rule That Makes Piping Work

**Data on stdout, everything else on stderr.** Progress bars, spinners, warnings, and log lines go to stderr; only the artifact the user asked for goes to stdout. That single rule is what makes `mytool --json | jq` work.

- `process.stdout.isTTY` is `undefined` when piped or redirected: switch off colors, spinners, and interactive prompts when it is falsy. Respect `NO_COLOR` and `FORCE_COLOR` — users have set them for a reason.
- EPIPE: when the reader closes early (`mytool | head -3`), the next write errors. Unhandled, it crashes with a stack the user did not cause. Handle it and exit quietly:

```js
process.stdout.on('error', (err) => { if (err.code === 'EPIPE') process.exit(0); throw err; });
```

- stdout to a pipe is asynchronous while stdout to a file or TTY is synchronous on POSIX: calling `process.exit()` right after a large write truncates it when piped. Set `process.exitCode` and let the loop drain (→ `errors.md`).
- Reading stdin: `process.stdin.isTTY` falsy means input is piped. Read it fully with `for await (const chunk of process.stdin)`, and never block waiting for stdin that no one is going to type — if the tool needs input and stdin is a TTY with no arguments, print usage instead of hanging.

## Exit Codes

- 0 for success, non-zero for anything a script should notice. Distinguish the common cases: 1 for a general failure, 2 for a usage error, and reserve a documented code for "found differences" style tools (like a linter with findings), so CI can tell "the tool worked and found problems" from "the tool broke".
- Never `process.exit(0)` in an error path, and never let an uncaught exception be the exit path — the user gets a stack trace instead of a message.
- Errors users caused get one clear line on stderr and no stack. Errors your code caused get the stack (`--verbose` or `DEBUG=1` to always show it).

## Long-Running and Interactive Behavior

- Ctrl-C must work: handle SIGINT to clean up temp files and restore the cursor, then exit 130 (128+2). Suppressing SIGINT without a fast path out makes users kill -9 you, which skips the cleanup entirely.
- A CLI that spawns children owns them: kill the tree on exit, or a Ctrl-C leaves orphans running (→ `concurrency.md`).
- Restore terminal state on every exit path — raw mode, hidden cursor, alternate screen. `process.on('exit')` with a synchronous restore is the only handler guaranteed to run.
- Long operations need progress on stderr and a bounded, resumable design: writing partial output to a temp file and renaming at the end means an interrupted run never leaves a corrupt artifact (→ `filesystem.md`).

## Configuration and Files

- Config lives in an OS-appropriate location, not in the home directory root: `XDG_CONFIG_HOME` (default `~/.config/<tool>`) on Linux, `~/Library/Application Support/<tool>` on macOS, `%APPDATA%\<tool>` on Windows. Cache goes in the cache directory, never mixed with config.
- Project-local config (a dotfile in the repo) overrides user config; both lose to explicit flags.
- Never write secrets into a config file with default permissions. If a token must persist, create the file with mode `0600` and say where it went.

## Startup Cost

- Measure it: `time mytool --version`. Above ~200 ms and interactive users notice; above ~500 ms it feels broken in a shell prompt or a git hook.
- The usual cause is eager imports. Lazy-load subcommand implementations with dynamic `import()` so `--help` does not pay for the network client.
- A single bundled file avoids hundreds of module resolutions on every invocation, which is the one case where bundling a Node application reliably pays for itself.
