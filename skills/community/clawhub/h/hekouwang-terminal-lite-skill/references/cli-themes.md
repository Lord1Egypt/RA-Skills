# CodeBuddy / Claude Code themes and diff readability

> **English** · [简体中文](cli-themes.zh-CN.md)

This file explains why a terminal theme that looks fine in `ls` can look terrible
inside an AI CLI's diff view, and what to change. Both CodeBuddy and Claude Code
share the same ANSI theme names (`dark-ansi` / `light-ansi`).

## The symptom

Their ANSI themes map the diff word backgrounds to the terminal's **bright** ANSI
slots:

```
diffAddedWord   → ansi:greenBright   (ANSI 10)
diffRemovedWord → ansi:redBright     (ANSI 9)
```

Those slots are designed to be **foreground** emphasis. Used as a background they
are far too luminous. Measured on `voltage`:

| Pair | Contrast |
|---|---|
| syntax orange `#f1a65a` on bright green `#0dd25f` | **1.01:1** |
| body `#e8e8ed` on bright green `#0dd25f` | **1.65:1** |
| syntax orange `#f1a65a` on bright red `#fa9ba8` | **1.00:1** |
| body `#e8e8ed` on bright red `#fa9ba8` | **1.67:1** |

This is not something the palette can fix by nudging a value: ANSI 9/10 have to
stay bright for foreground use. Darkening them to make good backgrounds would
break `ls`, `git diff` and every program that uses bright red/green for emphasis.

## The fix

Use the CLI's non-ANSI theme, which ships dark diff surfaces:

| Token | Non-ANSI `dark` |
|---|---|
| `diffAdded` | `rgb(34, 92, 43)` → body contrast 6.53 |
| `diffRemoved` | `rgb(122, 41, 54)` → body contrast 7.82 |
| `diffAddedWord` | `rgb(56, 166, 96)` |
| `diffRemovedWord` | `rgb(179, 89, 107)` |

For a light terminal, the non-ANSI `light` theme uses `diffAdded rgb(153, 204, 255)` and
`diffRemoved rgb(255, 204, 204)`; `setup-cli.sh` picks the one that matches the current
Hekouwang Terminal theme's background.

Either:

- set `theme = dark` (or `theme = light`) in your AI CLI's settings file — the exact path is
  documented by that CLI, this skill does not probe it for you,
- run `/theme` in the CLI and choose **Dark** / **Light** (not the ANSI variants), or
- run `./scripts/setup-cli.sh --config <path-to-settings.json> --apply` (backs up the settings
  file first, then writes the non-ANSI theme that matches the current terminal).

Verify:

```bash
./scripts/setup-cli.sh --config <path-to-settings.json> --check   # 0 = safe, 1 = ANSI theme, 2 = nothing checked
./scripts/doctor.sh --status       # the CLI line reports the same check
python3 config/themes/_preview.py --cli-diff voltage   # reproduce the bad pair
```

## Why not change the palette

`setup-cli.sh` only changes the CLI's theme, never the terminal's ANSI 9/10.
The palette audit reports the `cli_diff` ratio for visibility, but does not gate
on it — a bright slot is supposed to be bright. If a future release ships a
generated CLI theme (paid tier), the diff tokens can be pinned to the same dark
surfaces as the non-ANSI `dark` theme, which is the right place to solve it.
