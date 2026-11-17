---
name: mql-compiler
description: "Compile MQL4 (.mq4) and MQL5 (.mq5) sources to .ex4/.ex5 on Linux with the mql-compiler command, and read its compile errors."
homepage: https://github.com/psyb0t/docker-mql-compiler
user-invocable: true
metadata:
  { "openclaw": { "emoji": "🛠️", "requires": { "bins": ["docker"] } } }
---

# mql-compiler

`mql-compiler` compiles MetaTrader sources with MetaQuotes' own MetaEditor, running under Wine in the `psyb0t/mql-compiler` Docker image. It needs Docker on an x86-64 (amd64) machine and nothing else: no Windows, no MetaTrader terminal, no trading account. There is no ARM image.

## Install

If `mql-compiler` is not on `PATH`, install it for the current user:

```bash
curl -fsSL https://raw.githubusercontent.com/psyb0t/docker-mql-compiler/master/install.sh | bash
```

It lands in `~/.local/bin`; if that is not on `PATH`, the installer prints the line to add. For system-wide installs, upgrades, uninstalling, custom installers and troubleshooting, see [references/installation.md](references/installation.md).

## Compile

```bash
mql-compiler [OPTIONS] [FILE or FOLDER ...]

mql-compiler 2>/dev/null                               # every .mq4 and .mq5 under the current folder
mql-compiler /abs/path/MQL5/Experts/Foo.mq5 2>/dev/null # one file, from any folder
mql-compiler MQL5/Indicators MQL4 2>/dev/null           # folders, searched recursively
mql-compiler -I /path/to/shared/lib MQL5 2>/dev/null    # a shared include folder outside the tree
mql-compiler --werror MQL5 2>/dev/null                  # warnings count as failures
```

Options: `-I DIR` / `--include DIR` (extra include folder, repeatable), `--mt4-terminal DIR` / `--mt5-terminal DIR` (compile with that portable terminal's MetaEditor and standard library, mounted read-only; the terminal must have been started once so its standard library is unpacked), `--werror`, `--watch` (recompile on change until stopped; do not use it in an agent run, it never exits on its own), `--text` and `--format json|text|gnu` (output format; leave the JSON default), `--setup` (install only), `--update` (reinstall MT4/MT5 with the newest builds), `--version` (image version and MetaEditor builds), `-h`/`--help`.

- Arguments are files or folders, relative or absolute, anywhere on the machine. No argument means the current folder. No `cd` is needed. A path that does not exist stops the run with exit `2` before anything compiles.
- A folder is searched recursively for `.mq4` and `.mq5` (any case), sorted by path; symlinked files inside it are skipped. Arguments are handled in the order given; a file named twice compiles once, in its first position. `.mqh` and other files are skipped in folders and rejected (exit `2`) when named directly. A run that finds no sources exits `2`.
- One container runs the whole list, one file at a time, never in parallel. A failing file does not stop the run. Pass everything to one call: two runs at the same time take turns (the second logs that it is waiting), so splitting a job only makes it slower.
- Paths with spaces work; the messages still show the real paths.
- The extension alone picks the compiler: `.mq4` goes to MT4's MetaEditor, `.mq5` to MT5's. The folder only decides the includes: a `.mq4` uses the nearest folder named `MQL4` (any case) above it, a `.mq5` the nearest `MQL5`. Experts, indicators, scripts and libraries all compile the same way.
- Each `.ex4`/`.ex5` is written next to its source with the same base name, owned by the caller. The old one is deleted right before the file compiles, so after a run an `.ex4`/`.ex5` exists only if this run produced it. Still report success from the file's `"status": "ok"`.
- The container sees only the mounted folders (each source's `MQL4`/`MQL5` folder, or a loose file's own folder). Includes, resources and symlinks that point outside them are missing files inside the container.
- The first run downloads and installs MT4 and MT5 into the `mql-compiler-cache` Docker volume and unpacks their standard libraries, about a minute and a half. A compile installs only the platforms its sources need, and never one given with `--mt4-terminal`/`--mt5-terminal`. Allow for it in timeouts; later runs take seconds. `mql-compiler --setup` does only this.

## How includes resolve

- `#include <...>` searches one merged folder built for the run: the matching platform's MetaQuotes standard library (`<Trade/Trade.mqh>`, `<Arrays/ArrayObj.mqh>`, `<stdlib.mqh>`, ...), then each `-I` folder, then the `Include` folder of the nearest enclosing `MQL4` (for `.mq4`) or `MQL5` (for `.mq5`) folder, each laid over the one before. When two have the same path, the later one wins, so the user's own `Include` always wins.
- An `-I` folder stands in for `Include`: with `-I /libs` and `/libs/MyLib/x.mqh`, `#include <MyLib/x.mqh>` works.
- `#resource "\\Files\\x.txt"` and other `\\`-rooted paths start at that same `MQL4`/`MQL5` folder.
- `#include "..."` resolves next to the source.
- A source outside any `MQL4`/`MQL5` folder gets the standard library only, and no `\\`-rooted resources.
- An error inside a standard header is reported at the header's path in the toolchain (`/cache/uid-<UID>/wine/drive_c/...`, inside the cache volume, not on the host). It usually means the user's code broke something the header relies on, such as a macro with the same name as a standard class; fix the user's code, never the toolchain.
- Nothing is written into the user's folders or the toolchain; the merged folder is temporary.

So keep a terminal-style tree: sources under `MQL5/Experts`, `MQL5/Indicators`, ..., headers under `MQL5/Include` (same for `MQL4`). When copying a source elsewhere to compile it, copy its `MQL4`/`MQL5` folder with it, or its custom includes go missing.

## Read the result

stdout is JSON Lines, one object per line with a `type`. Parse it; do not scrape text.

```json
{"type":"file","source":"MQL5/Experts/Foo.mq5","platform":"mt5","status":"ok","output":"MQL5/Experts/Foo.ex5","errors":0,"warnings":0,"messages":[]}
{"type":"file","source":"MQL5/Experts/Bar.mq5","platform":"mt5","status":"failed","output":null,"errors":1,"warnings":0,"messages":[{"severity":"error","file":"MQL5/Experts/Bar.mq5","line":41,"column":7,"code":256,"text":"undeclared identifier 'lots'"}]}
{"type":"summary","total":2,"compiled":1,"failed":1,"werror":false}
```

- `file` (one per source): `source`, `platform` (`mt4`/`mt5`), `status` (`ok`/`failed`), `output` (the `.ex4`/`.ex5`, or `null`), `errors` and `warnings` (counts, `null` when MetaEditor wrote no result), `messages` (each `{severity, file, line, column, code, text}`), and `log` (MetaEditor's raw lines) only when it wrote no result.
- `summary` (last): `total`, `compiled`, `failed`, `werror`.
- `error` (instead of the rest, when the run cannot start): `message`. A bad path, a bad option or a failed setup.
- `version` (from `--version`, `--setup`, `--update`): `version`, `mt4_metaeditor`, `mt5_metaeditor`.

Paths are relative to the current folder when inside it, absolute otherwise. Fix the source at each message's `file`, `line` and `column`, and compile again. Progress and diagnostics go to stderr as JSON log lines; `2>/dev/null` hides them. A copy of the last run (stdout and stderr) is in the cache volume: `docker run --rm -v mql-compiler-cache:/c busybox cat /c/uid-$(id -u)/logs/last-run.log`.

| Exit | Meaning |
|---|---|
| `0` | Every file compiled |
| `1` | At least one file failed: compile errors, warnings under `--werror`, or MetaEditor wrote no result (see the `failed` records) |
| `2` | Bad path or option, no sources found, or the toolchain could not be set up (see the `error` record) |
| `125` and other Docker codes | Docker itself failed: daemon down, image not pullable, a bad mount (stdout may be empty) |

## Rules for agents

- Use the `mql-compiler` command. Do not build your own `docker run` unless the user asks.
- Report compile errors with their file, line, column, code and text from the `messages`. A file compiled when its record says `"status": "ok"`, even if the run exits `1` because of another file. Claim the whole build succeeded only when the exit status is `0` and the summary shows `"failed": 0`.
- Mention warnings to the user even when the build passes; they are in `messages` with `"severity": "warning"`.
- `file '...' not found` on an `#include <...>` means the header is in neither the user's `Include` nor the standard library. Check the source sits under the right `MQL4`/`MQL5` folder before editing code.
- `MQL_COMPILER_MT4_URL` and `MQL_COMPILER_MT5_URL` choose other installers, which only matters on a first run, so pair them with a fresh `MQL_COMPILER_VOLUME`. `MQL_COMPILER_INSTALL_TIMEOUT` (seconds, default 600) caps each platform's install on a first run. `MQL_COMPILER_SECCOMP` replaces the seccomp profile the installer put next to the command; leave it alone unless the user asks. Remove a volume only when the user asks: it costs another full download, and `mql-compiler-cache` holds every user's toolchain on the machine.
