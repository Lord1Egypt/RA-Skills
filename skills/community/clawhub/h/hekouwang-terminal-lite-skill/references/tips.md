# 10 daily tips (free build)

Ordered by how often you will use them. Each entry: when to reach for it, the command, one pitfall.

1. **Preview the install**: `./scripts/install.sh --dry-run` lists every file and system setting it would touch. Drop `--dry-run` only after reading it.
2. **Slow network in China**: `CN=1 ./scripts/install.sh` uses mirrors. Use it first when the install stalls at `portable-ruby` or `SSL_ERROR_SYSCALL`.
3. **Do not run install on an existing `.zshrc`**: run `./scripts/migrate.sh` for the report, then `--apply`. It migrates by paragraph, so `for…done` and continued commands stay intact.
4. **Look without switching**: `./scripts/theme.sh --preview ember` renders a whole fake terminal — prompt, eza listing, git diff, syntax colors — without touching your real config.
5. **See everything at once**: `./scripts/theme.sh --list` prints the gallery with a 16-swatch strip per theme. With fzf installed, `./scripts/theme.sh` opens the fuzzy picker.
6. **Read the plan before writing**: `./scripts/theme.sh --plan ember` lists the managed files first; nothing is written.
7. **Undo a switch**: `./scripts/theme.sh --rollback` restores the latest pre-switch snapshot. `--history` lists the five retained snapshots.
8. **One-line health check**: `./scripts/doctor.sh --status` shows theme / follow / Node / semantic / Ghostty-reload state.
9. **Measure startup before changing it**: `./scripts/doctor.sh --profile` runs zprof in a temporary `ZDOTDIR` and names the top 8 time sinks.
10. **Read the uninstall list first**: `./scripts/uninstall.sh --dry-run` shows what will be restored; then run `./scripts/uninstall.sh`.

## One for AI CLIs

`Shift + Enter` inserts a newline instead of submitting. If you write multi-line prompts for Claude Code or CodeBuddy, this is the one you will use every day.
