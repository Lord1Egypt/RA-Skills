# First run, and a doctor you can read

Free build: nothing to configure. `install.sh` already did it; this page is how to read it.

## The first window is already finished

`install.sh` deploys the theme and ecosystem colors (step 7, via `theme.sh`), writes `~/.zshrc` (step 10), then runs `doctor.sh` itself (step 15). Open a new iTerm2 window: prompt, palette, icons and `ls` colors are live.

Pitfall: a window opened before install keeps the old shell. Open a new one; never re-run install over an existing `~/.zshrc`.

## Read `--status` as a key/value dashboard

Read-only; run it when something looks off: `./scripts/doctor.sh --status`

```
theme      ember (pinned)
auto       on (follow system light/dark)
node       fnm
optical    operator @ compact (pinned)   # — (paid build) on the free build
scene      daily (pinned)                # — (paid build) on the free build
semantic   14 rules · product 3 · SH=best editor
visual     100/100 · all palettes pass   # only if config/themes/_audit.py exists
reload     Ghostty installed, no running process
```

Seven or eight lines, not six: `visual` appears only when `config/themes/_audit.py` exists. Values are read from disk; `— (not deployed)` is the line to act on.

Pitfall: `--status` exits after the dashboard, so `--status --profile` silently skips the profile.

## `--profile` names the top 8 startup costs

When startup feels slow, run `./scripts/doctor.sh --profile`. It sets a throwaway `ZDOTDIR`, sources the real `~/.zshrc` under `zprof`, prints 8 rows (rank / calls / total ms / share), then deletes it.

Pitfall: it really sources `~/.zshrc`, so interactive or side-effecting lines run too. To disable one block without touching the main config, copy the file to a temp `ZDOTDIR` and delete the `# ---- N.` section there.

## Acceptance in three commands

- `./scripts/doctor.sh --status` — no `— (not deployed)` left.
- `./scripts/doctor.sh --profile` — startup under 300 ms; the top row is something you recognise.
- `./scripts/theme.sh --preview ember` — a full fake terminal renders. Pitfall: the name must be a `--list` slug, and preview never switches the theme.
