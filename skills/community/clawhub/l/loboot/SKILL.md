---
name: loboot
description: Safely preview, create, inspect, update, remove, start, stop, enable, disable, and diagnose native user services managed by Loboot on macOS launchd or Linux systemd. Use when a request names Loboot or asks to operate its owned definitions, activation preferences, runtime state, offline plans, or discovery; not for cron scheduling, system/boot services, Windows, or adopting unrelated native services.
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - loboot
---

# Loboot

Operate the installed Loboot CLI with explicit separation between stored definitions, future activation, and current runtime. This workflow targets the Loboot 0.1.0 command contract. Offline testing does not certify real login-session behavior.

## Discover the installed surface

1. Resolve `loboot` from `PATH` and run `loboot --version`. Version and help are text even with `--json`; do not expect the Locron JSON/version syntax.
2. If absent, report the prerequisite and consult the [official installation guide](https://github.com/WhiteKiwi/loboot/blob/main/docs/INSTALL.md). Skill installation does not install the CLI. Do not invent a package, install a binary, or modify services merely to answer an inspection request.
3. Read `loboot COMMAND --help` before unfamiliar or version-sensitive commands. Installed help overrides examples here.
4. Prefer `--json` for decisions. Check the exit status, `schema_version == "loboot.cli/v1"`, and `ok`. A failure has `error.code` and `error.message`; branch on the code. Preserve unknown fields/states and warnings rather than guessing.

Keep Loboot flags before the direct-execution `--` separator. There is no `--format json` option.

## Inspect or explain first

Choose the narrowest useful read:

- `list --json` or `show ID --json`: owned local definitions, without a manager query. These do not prove that a process is running or enabled.
- `explain MANIFEST --json`: validated input and rendered native definition, without installing it. `explain` takes a TOML manifest, not a managed ID.
- `discover --json`: a shallow inventory of the configured native directory. Foreign entries remain read-only; this is neither machine-wide discovery nor import/adoption.
- `status ID --json`: observed native state in a live user session. Treat `loaded`, `running`, and `enabled` independently; `null` is unknown.
- `doctor --json`: local state and session checks. Outer `ok: true` only means diagnostics ran. Inspect `data.state.ok` and, for live readiness, both `data.session.checked` and `data.session.available`.

Read [references/safety.md](references/safety.md) before any mutation or diagnosis involving partial progress, ownership, or native activation. Logs, Windows, system/boot scope, environment/secret fields, import, and automatic recovery are not supported in 0.1.0. Do not substitute a different tool's command surface.

## Define or change a service

1. Resolve the exact ID, executable, literal arguments, working directory, mode, and restart policy. IDs use 1–63 lowercase letters, digits, and hyphens, starting with a letter. Executable and cwd must exist and have absolute physical paths with no symlink components.
2. Prefer direct argv for a new definition: `loboot add ID --cwd /absolute/directory --mode service --restart never -- /absolute/executable ARG`. Defaults are the current physical cwd, `service`, and `never`; make consequential defaults explicit.
3. For a reusable TOML manifest, supply all six fields: `id`, `executable`, `args`, `cwd`, `mode`, and `restart`. Use `args = []` when empty. Manifest settings cannot be overridden by direct-add options. Unknown fields are errors. A stored ownership record is not an input manifest.
4. `once` requires restart `never`. A service can use `never`, `on-failure`, or `always`. Explain retry/respawn consequences when relevant. `once` does not guarantee exactly-once execution across explicit starts or later activations.
5. Preview the complete proposed mutation using `--dry-run --json`. Inspect its exact target, normalized changes, native commands, conditional branches, and preconditions. Every mutation supports dry-run; it makes no writes or manager queries and cannot establish live readiness.
6. Apply the same command without `--dry-run` only when the user's request authorizes that exact change. Never convert a preview, diagnosis, draft, or missing prerequisite into service registration or execution.
7. Read back the definition with `show ID --json` or confirm removal with `list --json`. For live runtime/preference changes, read `status ID --json` and report what was actually observed.

`add` installs a disabled definition without starting it. `update MANIFEST` requires a stopped job and does not restart it. `remove ID` requires a stopped and disabled job; it does not implicitly stop or disable. If a prerequisite needs an additional change, obtain authorization for that change rather than adding it silently.

No shell or variable expansion is performed by Loboot. Do not wrap a direct command in a shell for convenience or put credentials in arguments/manifests; those values are plaintext. A long-running target should remain in the foreground for the native manager to track.

## Control runtime and future activation separately

Read the exact owned definition and live state, preview the requested action, then apply and verify only within authorization:

- `start`, `stop`, and `restart` change runtime without changing future activation preferences.
- `enable` and `disable` change future user-manager/login activation without implicitly starting or stopping.
- Linux can start a disabled service. macOS start/restart requires enable first, and disabling a loaded job requires stop first. Do not silently enable, stop, or restart to bypass those refusals.
- Linux activation follows the user-manager lifetime, not each shell login. macOS uses the current graphical `gui/<uid>` session. Do not use sudo, change lingering, or switch to system scope as a repair shortcut.

Accepted native commands do not prove a long-running process stayed alive or a short job succeeded. If a mutation fails or its reply is lost, inspect the current definition and native state before considering a retry. Another start/restart can execute the target again.

## Use an offline sandbox

For cross-platform plans or tests, use an absolute physical `--root` with `--platform linux` or `--platform macos`. `--platform` requires `--root`. Never drop `--root` to make a refused offline operation work.

An offline root isolates `state/` and `native/` files and prohibits manager execution. Offline `add`, `update`, and `remove` without dry-run still write sandbox files. Runtime and activation commands there require `--dry-run`. A dry-run itself creates no directories, locks, files, or repairs. Offline/dry-run doctor has `session.checked = false` and cannot prove live session readiness.

## Finish with evidence

Report the detected CLI version, exact ID and platform/scope, preview outcome, final definition and observed runtime/activation separately, and any unknown or skipped checks. Keep offline/fake-manager evidence distinct from real login-session acceptance. Link to the [CLI contract](https://github.com/WhiteKiwi/loboot/blob/main/docs/CLI.md) or [operator guide](https://github.com/WhiteKiwi/loboot/blob/main/docs/OPERATOR.md) when further platform detail matters.
