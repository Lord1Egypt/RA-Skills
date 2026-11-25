<h1 align="center">Hekouwang Terminal</h1>
<p align="center"><sub>会勇禾口王·终端工作台 · conversion page · deep guide <a href="docs/manual.md">docs/manual.md</a> · Agent <code>SKILL.md</code></sub></p>

<p align="center">
  <b>One palette, carried through the terminal and the whole command-line tool chain.</b><br>
  A macOS terminal workbench: 7 factory themes (3 community free, 4 brand in the paid tier), plus a 463-scheme importer from Ghostty.<br>
  Preview before it writes, roll back a restyle, uninstall cleanly.
</p>

<p align="center">
  <b>English</b> · <a href="README.md">简体中文</a>
  · <a href="https://huiyonghkw.github.io/hekouwang-terminal-lite-skill/index.html?lang=en"><b>Product home</b></a>
  · <a href="https://huiyonghkw.github.io/hekouwang-terminal-lite-skill/guide/index.html?lang=en">Docs</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/free-3%20community%20themes-06a88c">
  <img src="https://img.shields.io/badge/7%20factory%20themes-%2B%20463%20imports-6a45e0">
  <img src="https://img.shields.io/badge/license-MIT-00d4aa">
</p>

```bash
git clone https://github.com/huiyonghkw/hekouwang-terminal-lite-skill.git
cd hekouwang-terminal-lite-skill
./scripts/install.sh --dry-run   # preview files and settings; drop --dry-run to apply
```

<p align="center">
  <img src="docs/images/cmp-iterm2-free.png" width="49%" alt="Free tier: eza, bat and git diff each speak their own color language, none matching the background">
  <img src="docs/images/cmp-iterm2-paid.png" width="49%" alt="Paid tier: all four generated from one palette">
</p>

<p align="center"><sub>Same machine, same commands — free on the left, paid on the right</sub></p>

`eza` lists the directory, `cat` reads the code, `git diff` shows the change. Not one command changed.
The left side is not "ugly colors" — Monokai is a classic, delta's red/green is the factory default. The problem is three tools each speaking their own dialect, none matching the terminal background.
On the right, all four come out of one palette, so they are family.

If iTerm2 is all you use, the free build is enough. If you want `ls` / `cat` / `git diff` to match the terminal too, see section 7.

---

## 1. What you are probably stuck on

Since CLI agents like Claude Code showed up, the time I spend in the terminal has roughly doubled.
It used to be a place where you typed two commands and left. Now it is the main surface where I work with AI: four tabs, four jobs, output scrolling by, and I need to see at a glance which one errored, which finished, which is still spinning.

My five-year-old setup was built for typing commands, not for watching AI work:

- Four tabs look identical — I cannot tell which job is which
- Agents dump hundreds of log lines; `ERROR` and normal output share one color
- A multi-line prompt for the AI — Enter submits instead of inserting a newline
- Daylight by the window, or a projector in a meeting — a dark background is unreadable
- Once it finally feels right, a new Mac means starting the clicks over

This skill is aimed at exactly those gaps. **Whatever I can do with AI, I run first, then write it into a script** — this is the terminal I use every day, not a demo machine.

Triggers ships with the profile as four rules: `ERROR` / `WARN` / `SUCCESS` each get a background, and `Password:` opens the iTerm2 password manager.

## 2. Not another dotfiles repo

1. **Measured, not eyeballed** — contrast, diff lightness separation and color-blind separation are constraints at generation time, not adjustments after the fact. `./scripts/theme.sh --audit` re-runs them any time.
2. **A restyle you can roll back** — `--plan` lists every managed file and writes nothing; a failed write restores automatically; 5 snapshots are kept, and `--rollback` returns to the previous state.
3. **One palette, fanned out** — switching themes never touches `.zshrc`: every tool reads a fixed `current/` directory, so a switch only replaces its contents.
4. **Optical font calibration** 〔paid〕 — reads the font's metrics table to compute glyph-box drift and checks that a CJK character (U+4E00) is exactly two cells wide. "Install a Nerd Font" is not the same thing.
5. **It is an Agent Skill** — say "switch to a light theme" or "why is startup slow", and the agent picks the script, runs it, and explains the result. The free build ships a basic Skill; the Pro build ships the full one.

One palette going out looks like this (iTerm2 is the only free target — the rest is paid):

```text
config/themes/palettes/brand.py        one palette: 16 ANSI slots + semantic surfaces
        ├─ iTerm2 / Ghostty / Terminal.app      all 7 themes
        ├─ Warp / Tabby                         5 of 7
        ├─ cmux                                 sidebar tint
        └─ bat / fzf / eza / delta / tmux / VS Code
```

## 3. Evidence

### 7 factory themes

| Theme | Base | Tier |
|---|---|---|
| Catppuccin Mocha | dark | free |
| Tokyo Night | dark | free |
| Gruvbox Dark | dark | free |
| Ember | dark | paid |
| Voltage | dark | paid |
| Parchment | light | paid |
| Ledger | light | paid |

The importer is separate: Ghostty ships 463 schemes, and once imported, the same scheme spreads across the whole chain above 〔paid〕.

### Terminal coverage

| Terminal | 7-theme coverage | Notes |
|---|---|---|
| iTerm2 | 7/7 | the free build's target; Dynamic Profile applies on save |
| Ghostty | 7/7 | config as a file, reload to apply |
| Terminal.app | 7/7 | exports a `.terminal` descriptor |
| Warp | 5/7 | missing Catppuccin Mocha and Tokyo Night: Warp's theme YAML cannot express their slots |
| Tabby | 5/7 | same |
| cmux | sidebar | terminal rendering is Ghostty's; Hekouwang Terminal only tints the sidebar |

The gaps are labeled as gaps: better an honest boundary than a lookalike scheme that quietly drifts.
The free build covers iTerm2 with the 3 community themes only; every other combination in this table is paid.

### Audit thresholds

`./scripts/theme.sh --audit` runs constraints baked into the generator, not a human squinting at a screenshot:

| Check | Threshold |
|---|---|
| Body slots 1–6 against background | ≥ 4.5:1 (WCAG AA) |
| Emphasis slots 9–14 against background | ≥ 6.0:1 |
| Dim slot 8 against background | ≥ 3.0:1 |
| Diff add/remove background separation | ΔL ≥ 0.025, still distinct in grayscale |
| Red vs green under color-blind simulation | ΔE ≥ 0.03 |
| Neutral ladder surface / overlay / border | 1.12 / 1.22 / 1.35, with fg against surface ≥ 4.5:1 |

<p align="center">
  <img src="docs/images/doctor-status.webp" width="82%" alt="doctor.sh --status: theme / auto / node / optical / scene / semantic">
</p>

> `./scripts/doctor.sh --status` shows what is pinned. Full checkup is `./scripts/doctor.sh`. On Lite, missing paid pieces are labeled Pro — that is not a broken install.

## 4. What the free tier gives you

The free build is not a demo: what is missing is theme count and reach, not scripts.

- **3 community themes**: Catppuccin Mocha / Tokyo Night / Gruvbox Dark
- **Minimal chrome**: no title bar, border or scrollbar, plus blur — written by the installer via `defaults write`
- **Log coloring**: `ERROR` / `WARN` / `SUCCESS` / `Password:` as four Triggers rules in the profile
- **Semantic Cmd-click**: `path:line`, Git SHA and `localhost:port` open on click
- **Shift+Enter inserts a newline** instead of submitting — built for multi-line prompts
- **Modern CLI set**: eza / bat / delta / fzf / zoxide / atuin / starship
- **A checkup that repairs itself**: `doctor.sh --status` / `--fix` / `--profile`
- **Safe install and removal**: `install.sh --dry-run`, `migrate.sh` for an existing setup, `uninstall.sh` to restore from backup
- **A basic Skill**: install / theme / doctor / sync / uninstall, driven by the agent

## 5. Installation

Prerequisites: a Mac (Apple silicon or Intel), network access, and the ability to copy-paste into Terminal.

| Your situation | Use |
|---|---|
| New Mac, or no custom `~/.zshrc` | `HKW_ASSUME_YES=1 ./scripts/install.sh` |
| **Already have your own `.zshrc`** | `./scripts/migrate.sh` first |

`install.sh` overwrites `~/.zshrc` (after backing it up). Years of aliases belong in migration: they move into `~/.zshrc.local`, then the template loads them.

When Homebrew / oh-my-zsh are missing, the script downloads their official installers to a temp file and prints the SHA-256. **It does not run them by default**; add `HKW_ASSUME_YES=1` once you are fine with that.

```bash
git clone https://github.com/huiyonghkw/hekouwang-terminal-lite-skill.git
cd hekouwang-terminal-lite-skill

./scripts/migrate.sh             # report only
./scripts/migrate.sh --apply     # apply after you confirm

./scripts/install.sh --dry-run   # preview files, settings, and the hard no-touch list
HKW_ASSUME_YES=1 ./scripts/install.sh
```

Mainland China network stuck at `portable-ruby` / `SSL_ERROR_SYSCALL`:

```bash
CN=1 HKW_ASSUME_YES=1 ./scripts/install.sh
```

Roughly: Homebrew → iTerm2 + fonts → CLI → oh-my-zsh → theme (ecosystem match is paid) → `.zshrc` → three GUI settings → checkup.
The scripts are idempotent, so re-runs are safe. At the end it prints a completion line and runs `doctor.sh` automatically.

**Rollback**: `~/.zshrc` is backed up under `~/.hekouwang-terminal-backups/`. Run `./scripts/uninstall.sh --dry-run` to see what would be restored, then `./scripts/uninstall.sh`.

## 6. The commands you use daily

| Tool | One line | How |
|---|---|---|
| **starship** | Prompt: directory / git branch / last command duration | automatic |
| **eza** | File listings with icons | just type `ls` |
| **bat** | `cat` with highlighting and line numbers | `cat filename` |
| **delta** | Diffs with syntax highlighting | `git diff` |
| **fzf** | Fuzzy-find everything | `Ctrl+T` files, `Alt+C` directories |
| **zoxide** | Jump by a word | `z keyword` |
| **atuin** | Full-text history search | `Ctrl+R` |

One more for AI: **`Shift + Enter` inserts a newline without submitting**.

Semantic layer: `Cmd-click` a `path:line` to open the editor, a Git SHA to run `git show`, a `localhost:3000` to open the browser.

All shortcuts → [`references/shortcuts.md`](references/shortcuts.md)

## 7. What the paid tier adds

| | Free (MIT) | Paid |
|---|---|---|
| Themes | 3 community | + 4 brand (2 light) + importer (Ghostty's 463) |
| Terminals | iTerm2 | iTerm2 / Ghostty / Terminal.app at 7/7; Warp / Tabby at 5/7; cmux sidebar |
| Tool chain | — | bat / fzf / eza / delta / tmux / VS Code in the same colors |
| Optical calibration | — | glyph-box drift + CJK two-cell width, three density steps |
| Scenes | — | daily / focus / present / record / remote |
| Workspaces | — | `cd` into a project, the tab recolors and prints its name |
| Follow system light/dark | — | Paid tier |
| Skill | basic | full |
| Updates and support | GitHub Issues | one year of updates + group Q&A |

**Pro 3.0.5**: Alipay [SkillPay](https://huiyonghkw.github.io/hekouwang-terminal-lite-skill/index.html?lang=en) quarterly subscription (¥14.9/quarter, no auto-renew, ≈¥59.6/year) · Tencent SkillHub per call (¥2.99/call). Buy only through the platforms — see [product home](https://huiyonghkw.github.io/hekouwang-terminal-lite-skill/index.html?lang=en).

## 8. Maintenance

```bash
./scripts/doctor.sh            # checkup (section 0 is the state dashboard)
./scripts/doctor.sh --status   # dashboard only: theme / auto / node / optical / scene / semantic / visual / Ghostty reload
./scripts/doctor.sh --parity   # source-palette consistency report (read-only)
./scripts/doctor.sh --fix      # repair item by item after you confirm
./scripts/doctor.sh --profile  # slow startup? names the plugin

./scripts/update.sh            # update (git install)
./scripts/sync.sh              # machine migration

./scripts/uninstall.sh         # restore from backup + GUI factory reset
./scripts/uninstall.sh --dry-run
```

Put personal aliases and `PATH` entries in `~/.zshrc.local` (the template loads it). Do not edit template sections that get overwritten.

## 9. Limits, FAQ and license

- **Warp / Tabby are 5/7**: Catppuccin Mocha and Tokyo Night are missing because Warp's theme YAML cannot express their slots. Not an oversight.
- **cmux is sidebar only**: terminal rendering belongs to Ghostty; Hekouwang Terminal does not take it over.
- **macOS only**: iTerm2, Ghostty and Terminal.app are macOS apps.
- **Bring your own font**: no font files are distributed. Missing Nerd Font glyphs show up as `?`; install any Nerd Font.
- **`cat` colors are separate**: when bat cannot recognize a theme it **does not error** — it silently falls back to its own colors, which looks like "terminal, fzf and git diff are right, only `cat` is different". The first switch pauses a few seconds to build the cache; do not interrupt it.
- **`cat file | head` is a bad color test**: the pipe drops bat into plain-text mode. Run `cat file` directly.
- **Imported themes stay on your machine**: schemes pulled in by `import.sh` are not part of the product and do not ship with updates.
- **Workspaces need Shell Integration**: per-project tab colors rely on iTerm2's APS path matching.

Full FAQ, tmux `-CC`, Triggers, Shell Integration → [`docs/manual.md`](docs/manual.md) (中文: [`docs/manual.zh-CN.md`](docs/manual.zh-CN.md)).
Docs site: [install](https://huiyonghkw.github.io/hekouwang-terminal-lite-skill/guide/install.html?lang=en) · [themes](https://huiyonghkw.github.io/hekouwang-terminal-lite-skill/guide/theme.html?lang=en) · [terminal coverage](https://huiyonghkw.github.io/hekouwang-terminal-lite-skill/guide/terminals.html?lang=en) · [semantic layer](https://huiyonghkw.github.io/hekouwang-terminal-lite-skill/guide/semantic.html?lang=en) · [doctor](https://huiyonghkw.github.io/hekouwang-terminal-lite-skill/guide/doctor.html?lang=en)

| Also | Go to |
|---|---|
| Shortcuts | [`references/shortcuts.md`](references/shortcuts.md) |
| Changelog | [`CHANGELOG.md`](CHANGELOG.md) |
| 简体中文 | [`README.md`](README.md) |

### License

Free build: [MIT](LICENSE.txt) — use it, change it, ship commercial work with it. Paid pieces are covered by the license inside the paid package.
