# ~/.zshrc block by block + plugin picks

> **English** · [简体中文](zshrc-explained.zh-CN.md)
>
> Written up from a real .zshrc that had been in use for years (2026-06, redacted). The
> blocks follow the order they actually appear in the file, and each says: what it does, why
> it is needed, and whether it is worth keeping. At the end there is a "known issues" list
> with fixes.

---

## Block 1 · File handle limit

```bash
ulimit -n 10240 2>/dev/null
```

| Item | Notes |
|---|---|
| What | Raises the per-process open-file limit from the macOS default of 256 to 10240 |
| Why | The async workers in zsh-autocomplete and zsh-autosuggestions open a lot of file descriptors at once, and 256 gets you `too many open files` |
| Placement | At the very top of .zshrc, before any plugin loads |
| Worth it | ★★★★★ Mandatory if you use zsh-autocomplete |

## Block 2 · The oh-my-zsh framework

```bash
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME=""          # the prompt is starship's job, so leave the theme empty
plugins=(git)
source $ZSH/oh-my-zsh.sh
```

| Item | Notes |
|---|---|
| What | Loads oh-my-zsh; the theme is left empty (starship takes over) and only the git plugin is on |
| The git plugin | Gives you a hundred-odd git abbreviations (`gst`/`gco`/`gp`) plus better completion |
| ⚠️ Note | Starship takes over the prompt, so `ZSH_THEME` is set empty — that saves loading an omz theme for nothing. **The template (config/zshrc.template) already does this.** If your old .zshrc still says `ZSH_THEME="Minimal"`, that line is overridden by starship and does nothing; empty it |
| Plugin philosophy | Keeping `plugins=()` lean is right — every omz plugin costs startup time. Worth considering: `sudo` (double-tap Esc to prefix sudo), `extract` (`x <archive>` unpacks anything), `z` (unnecessary once you use zoxide) |
| Worth it | ★★★★ The framework is still the least fussy base for the completion ecosystem; if you want maximum startup speed, swap it for pure plugin management with zinit/znap |

## Block 3 · The Znap plugin manager + zsh-autocomplete

```bash
zstyle ':znap:*' repos-dir ~/.zsh-plugins
[[ -r ~/.zsh-plugins/znap/znap.zsh ]] ||
    git clone --depth 1 -- https://github.com/marlonrichert/zsh-snap.git ~/.zsh-plugins/znap
source ~/.zsh-plugins/znap/znap.zsh
znap source marlonrichert/zsh-autocomplete
```

| Item | Notes |
|---|---|
| znap | A minimal zsh plugin manager that bootstraps itself ("git clone it if missing"), so a new machine sets itself up on the first shell |
| zsh-autocomplete | A **live completion menu**: candidates (commands / paths / history / man flags) pop up as you type, Tab enters the menu, arrows select. It is a "heavy" plugin, and the experience is close to an IDE |
| Trade-off | It overlaps zsh-autosuggestions (block 4) but plays a different role: autocomplete pops a menu, autosuggestions shows inline grey ghost text. They coexist fine (this config runs both), but running both costs performance — which is exactly why block 1 raises ulimit. If it feels busy, keep autosuggestions only |
| Worth it | ★★★★ A gift for heavy keyboard users; skip this block if you want it light |

## Block 4 · zsh-autosuggestions (the grey ghost text)

```bash
source /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh
```

| Item | Notes |
|---|---|
| What | Suggests an inline grey completion from your history as you type; `→` or `End` accepts it |
| Install | `brew install zsh-autosuggestions` |
| Worth it | ★★★★★ The best value of any single plugin. Install it |

## Block 5 · Node version management (⚠️ the biggest problem area in this config)

**Current approach (2.8.0+)**: pick one at install (`fnm` / `nvm` / `brew` / `vfox`).
The snippet lives in `~/.config/hekouwang-terminal/node.sh`; `.zshrc` only sources it.
Switch later with `./scripts/node-mgr.sh <name>` — no need to edit `.zshrc`. Rule stays:
**exactly one**.

The anti-pattern below is kept so the “why pick one” still reads clearly:

The original file had **four sources of Node at once**:

```bash
# ① nvm (and loaded twice! line 114 and line 179)
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# ② brew's node@22 straight onto PATH
export PATH="/opt/homebrew/opt/node@22/bin:$PATH"

# ③ fnm (Fast Node Manager)
eval "$(fnm env --use-on-cd)"

# ④ one fnm version's bin hard-coded onto PATH
export PATH="$HOME/.local/share/fnm/node-versions/v22.19.0/installation/bin:$PATH"
```

**The problems**:
1. nvm loaded twice → startup time doubled for nothing (nvm is famously slow: 300–500ms for a single load)
2. Four sources fight over PATH; which one wins depends on declaration order, and even after `nvm use` switches versions a later hard-coded PATH can override it
3. `$(nvm current)` before nvm has finished loading puts a broken entry on PATH

**The fix (keep fnm, delete the rest)**:

```bash
# fnm — the only Node version manager (written in Rust, loads in <50ms, switches version on cd)
eval "$(fnm env --use-on-cd)"
```

| Compared | nvm | fnm |
|---|---|---|
| Load time | 300–500ms | <50ms |
| Auto-switch version | needs a plugin | `--use-on-cd` natively (reads .nvmrc / .node-version) |
| Worth it | ★★ | ★★★★★ |

## Block 6 · SSH server aliases (🔒 private, never in git)

```bash
alias mycompany-dev-root="ssh -o ServerAliveInterval=60 root@x.x.x.x"
alias ecs:xxx:NN="ssh -o ServerAliveInterval=60 root@x.x.x.x"
# …a dozen more
```

| Item | Notes |
|---|---|
| What | One-key SSH into each environment; `ServerAliveInterval=60` sends a heartbeat every 60s to stop drops |
| Naming | `ecs:project:last-IP-octet` — a colon is legal in a zsh alias and groups them naturally |
| Better approach | Put them in `~/.ssh/config` (Host blocks) so `scp`, `rsync` and VS Code Remote can use the names too; an alias only exists in an interactive shell |
| 🔒 Hard line | **Real IPs never go to GitHub.** Put them in `~/.zshrc.local` (the template sources it automatically) |

The `~/.ssh/config` equivalent (recommended):

```
Host mycompany-dev
    HostName x.x.x.x
    User root
    ServerAliveInterval 60
```

## Block 7 · Short git aliases

```bash
alias gc="git commit -am "
alias gs="git status"
alias gaa="git add ."
alias gpld="git pull origin develop"   # gpud / gplm / gpum follow the same pattern
alias gcom="git checkout master"       # gcod likewise
alias gco="git checkout "
alias gr="git merge "
```

| Item | Notes |
|---|---|
| Design | Muscle-memory abbreviations around a master/develop two-branch flow |
| ⚠️ Collision | In the omz git plugin, `gr` is `git remote` and `gco` is `git checkout` — these custom aliases are declared after omz, so they win. Worth knowing; not a bug |
| Worth it | ★★★★ Tailor them to your own flow; growing your own beats copying someone else's |

## Block 8 · Homebrew mirrors + less frequent auto-update

```bash
export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles
export HOMEBREW_API_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles/api
export HOMEBREW_PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
export HOMEBREW_AUTO_UPDATE_SECS=3600   # auto-update at most hourly (default: before every install)
```

| Worth it | ★★★★★ Necessary on a Chinese network; outside China, delete the first three lines |

> ⚠️ **Do not point the first two at the Aliyun homebrew mirror.** It stopped being updated
> (its API still lists uv at 0.7.6 while the real version is far ahead, and new bottles are
> simply missing), and Homebrew 6.x then behaves confusingly: the mirror 404s, it falls back
> to the official ghcr.io and **downloads fine**, but the cache filename hash is computed
> from the **mirror** URL, so pouring looks for a file that is not there and fails hard with
> `No such file or directory ... bottle.tar.gz`. Retrying always stops at the same place.
> To check whether a mirror has gone stale:
> `curl -s "$HOMEBREW_API_DOMAIN/formula/uv.json" -o /tmp/uv.json` (official API; review before running)
> `python3 -c "import json;print(json.load(open('/tmp/uv.json'))['versions']['stable'])"` (reads the saved file)
> — if it disagrees with `brew info uv`, it is lagging. To work around it without changing
> config: `env -u HOMEBREW_BOTTLE_DOMAIN -u HOMEBREW_API_DOMAIN brew upgrade`.

## Block 9 · Starship prompt

```bash
eval "$(starship init zsh)"
```

| Item | Notes |
|---|---|
| What | A cross-shell prompt written in Rust, reading `~/.config/starship.toml`. This one is a two-line pure style: directory blue / git branch grey / duration yellow / `❯` purple (red on error, a green `❮` in vim mode) |
| Relation to omz themes | Once starship takes the prompt, `ZSH_THEME` does nothing |
| Config file | See `config/starship.toml` in this skill; `git_status` is deliberately `disabled = true` to keep it minimal |
| Worth it | ★★★★★ Simpler than powerlevel10k and works across bash/zsh/fish |

## Block 10 · Language runtimes and tool PATHs

```bash
export JAVA_HOME=/opt/homebrew/Cellar/openjdk@17/17.0.12/libexec/openjdk.jdk/Contents/Home
export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"      # Java 17
export PATH="$PATH:$HOME/.local/bin"                      # Python CLIs installed by pipx
export PATH="$HOME/.codeium/windsurf/bin:$PATH"           # the Windsurf editor CLI
export LC_ALL=en_US.UTF-8                                 # one locale, so remote SSH does not garble
source "$HOME/.openclaw/completions/openclaw.zsh"         # OpenClaw completion

# bun (⚠️ these two lines appeared twice in the original file; delete one pair)
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"
[ -s "$HOME/.bun/_bun" ] && source "$HOME/.bun/_bun"      # bun completion

export TERM=xterm-256color   # force 256 colors (a fallback for old servers that misreport TERM)
```

| ⚠️ JAVA_HOME hazard | The path pins the patch version `17.0.12`, so a brew upgrade breaks it. Safer: `export JAVA_HOME=$(/usr/libexec/java_home -v 17)`, or point at `/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home` (the `opt` symlink does not move with patch releases) |
| ⚠️ TERM caution | Hard-setting TERM in .zshrc overrides what iTerm2 reports (`xterm-256color` / `iterm2`). Usually harmless, but it can interfere with true color inside tmux; delete it if colors look wrong |

## Block 11 · Proxy (🔒 private, never in git)

```bash
export https_proxy=http://127.0.0.1:10080
export http_proxy=http://127.0.0.1:10080
export all_proxy=socks5://127.0.0.1:10081
```

| Problem | Hard-coding it means **every network command hangs whenever the proxy is not running** |
| Better | Wrap it in toggle functions in `~/.zshrc.local`: |

```bash
proxy_on()  { export https_proxy=http://127.0.0.1:10080 http_proxy=http://127.0.0.1:10080 all_proxy=socks5://127.0.0.1:10081; echo "proxy on"; }
proxy_off() { unset https_proxy http_proxy all_proxy; echo "proxy off"; }
```

## Block 12 · The modern CLI set (the best part of this config)

> Install: `brew install eza bat fzf fd zoxide ripgrep atuin`

### eza — replaces `ls`

```bash
alias ls="eza --icons"
alias ll="eza -l --icons --git"         # long listing + a git status column
alias la="eza -la --icons --git"        # including hidden files
alias lt="eza --tree --level=2 --icons" # two levels of tree
```

Icon rendering needs a Nerd Font (see the font strategy in the GUI doc). The `command -v`
guard makes machines without eza fall back to the native ls. ★★★★★

### bat — replaces `cat`

```bash
alias cat="bat --paging=never"   # highlighting + line numbers, no pager (keeps cat's direct feel)
export BAT_THEME="hekouwang-ember"
```

> In this skill you never set `BAT_THEME` by hand: `install.sh` installs every theme and runs
> `bat cache --build` once, and the ecosystem colors sourced by `.zshrc` set the variable, so
> it follows every theme switch. ⚠️ bat indexes themes by the `name` field inside the file
> rather than the filename, and **when it cannot find one it silently falls back to its own
> default colors** — which shows up as "everything matches except `cat`".

★★★★★

### fzf — fuzzy-find anything

```bash
source <(fzf --zsh)   # takes over Ctrl+R (history) / Ctrl+T (files) / Alt+C (cd)
export FZF_DEFAULT_COMMAND="fd --type f --hidden --follow --exclude .git"  # fd as the file source: fast, respects .gitignore
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
# FZF_DEFAULT_OPTS (colors + a 40%-height bordered window) comes from the ecosystem
# colors file, so it follows the theme. Do not hard-code hex here.
```

Note that atuin (below) takes Ctrl+R back, so in practice fzf owns Ctrl+T and Alt+C. ★★★★★

### zoxide — replaces `cd`

```bash
eval "$(zoxide init zsh)"
```

It learns directories by how often you visit them: `z pi` goes straight to
`~/Dashboard/Pi.dev`, and `zi` opens an interactive picker (through fzf). ★★★★★

### atuin — a command history database

```bash
eval "$(atuin init zsh --disable-up-arrow)"
```

Stores every command in SQLite with full text (directory, duration, exit code included) and
turns `Ctrl+R` into a full-screen search; `--disable-up-arrow` keeps `↑` native (scrolling
this session's history only). After installing, run `atuin import auto` once to pull in your
existing history, and `atuin stats` to see what you actually run. Optionally register an
account for encrypted sync across machines. ★★★★★

### ripgrep (rg) — replaces `grep`

No configuration; install it and use it. The ceiling for code-search speed, and it skips
.gitignore automatically. ★★★★★

## Block 13 · zsh-syntax-highlighting (must be last)

```bash
[ -f /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ] && \
  source /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
```

Valid commands in green, invalid in red, strings in yellow — so you know you mistyped
**before** pressing Enter.
It works by wrapping ZLE widgets, so it **must load after every plugin that binds keys** —
which is why it is pinned to the second-to-last line of .zshrc. ★★★★★

## Block 14 · iTerm2 Shell Integration (the very last line)

```bash
test -e "${HOME}/.iterm2_shell_integration.zsh" && source "${HOME}/.iterm2_shell_integration.zsh"
```

The official iTerm2 add-on: command-block navigation (`Cmd+Shift+↑/↓`), red markers on failed
commands, `imgcat` to view images in the terminal, `it2copy` to copy from a remote machine
into the local clipboard. Installation is in section 4.1 of the GUI doc. ★★★★

---

# Known issues (from checking the original .zshrc)

| # | Issue | Impact | Fix |
|---|---|---|---|
| 1 | nvm loaded twice (lines 114 + 179) | 600ms–1s slower startup | Delete both, keep fnm |
| 2 | nvm + fnm + brew node@22 + a hand-written fnm path — four sources of Node | PATH fights itself, version switches do not stick | Keep only `eval "$(fnm env --use-on-cd)"` |
| 3 | bun's BUN_INSTALL/PATH written twice | Harmless but redundant | Delete one pair |
| 4 | `ZSH_THEME="Minimal"` overridden by starship | Loads a theme for nothing | Set `ZSH_THEME=""` |
| 5 | JAVA_HOME pins the patch version 17.0.12 | Java disappears after a brew upgrade | Use `/usr/libexec/java_home -v 17` |
| 6 | Proxy hard-coded with no toggle | Every network command hangs when the proxy is off | proxy_on/proxy_off functions in .zshrc.local |
| 7 | SSH aliases contain real IPs | Leaked the moment it reaches GitHub | Move to .zshrc.local or ~/.ssh/config |
| 8 | `export TERM=xterm-256color` hard-coded | True color in tmux may misbehave | Can be deleted (iTerm2 sets it correctly itself) |

> All of these fixes are already reflected in `config/zshrc.template`.

# Plugin picks

| Name | Type | In one line | Must have |
|---|---|---|---|
| zsh-autosuggestions | zsh plugin | Inline grey ghost completion | ✅ |
| zsh-syntax-highlighting | zsh plugin | Live right/wrong coloring (load it last) | ✅ |
| zsh-autocomplete | zsh plugin | Live pop-up completion menu (heavy, pair with ulimit) | optional |
| omz git plugin | omz | git abbreviations + completion | ✅ |
| starship | prompt | A minimal cross-shell prompt | ✅ |
| eza / bat / fd / ripgrep | CLI | Modern ls/cat/find/grep | ✅ |
| fzf | CLI | Fuzzy file (Ctrl+T) / directory (Alt+C) search | ✅ |
| zoxide | CLI | cd that learns from frequency | ✅ |
| atuin | CLI | Command history database (Ctrl+R) | ✅ |
| fnm | CLI | Node version management (replaces nvm) | ✅ |
| znap | plugin manager | A self-bootstrapping zsh plugin manager | optional |
