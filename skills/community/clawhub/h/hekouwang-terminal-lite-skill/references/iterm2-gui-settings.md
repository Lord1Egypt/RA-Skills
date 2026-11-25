# iTerm2 GUI checklist + advanced features

> **English** · [简体中文](iterm2-gui-settings.zh-CN.md)
>
> **These three things are already written by `setup-gui.sh` (which `install.sh` calls), so
> you normally never click them.** The manual steps are kept here as (1) a fallback when the
> automation did not take, and (2) a way to understand what each item changes.
> To verify: run section 4 of `./scripts/doctor.sh`. To open the settings panel: `Cmd+,`
>
> `setup-gui.sh` writes these three with `defaults write` (plus removing the window border
> and hiding the tab bar when there is only one tab):
> `TabStyleWithAutomaticOption=5` (Minimal), `Default Bookmark Guid` (the default profile),
> and a `GlobalKeyMap` entry for Shift+Enter (in both the old and new key-mapping formats).
> ⚠️ It quits iTerm2 first (otherwise iTerm2 overwrites the values when it exits), and it
> never runs `killall cfprefsd` afterwards (that would discard writes not yet flushed).

## 1. The three required steps (automated; manual is the fallback) ⭐

### 1.1 Minimal theme

`Settings → Appearance → General → Theme` → **Minimal**

The tab bar blends into the terminal background and the grey title bar disappears, leaving
the window as one flat canvas. While you are in that panel:

| Item | Where | Value |
|---|---|---|
| Tab bar in full screen | Appearance → Tabs | ✅ Show tab bar in fullscreen |
| Hide the tab bar with one tab | Appearance → Tabs | ✅ hide tab bar when there is only one tab |
| New-output indicator | Appearance → Tabs | ✅ Show "new output" indicator |
| Window border | Appearance → Windows | ❌ Show border around window |

### 1.2 Set the default profile

`install.sh` has already put `hekouwang-active-theme.json` into the DynamicProfiles folder
(live on save, no restart needed).
`Settings → Profiles` → select the profile carrying the **Dynamic** tag →
`Other Actions... → Set as Default`

### 1.3 Shift+Enter for a newline (essential for AI CLIs)

`Settings → Keys → Key Bindings → +`

| Field | Value |
|---|---|
| Keyboard Shortcut | press `Shift+Enter` |
| Action | **Send Text** |
| Text | `\n` |

What it is for: in Claude Code and similar AI CLIs, `Enter` submits and `Shift+Enter` adds a
newline — the same muscle memory as any chat app.

## 2. Dynamic Profiles in detail (config as code ⭐ the core idea)

Profiles are not clicked together in the GUI; they are JSON, and they live in:

```
~/Library/Application Support/iTerm2/DynamicProfiles/
```

Four advantages: (1) live on save (iTerm2 watches the folder); (2) versionable — a new
machine needs one file; (3) self-contained; (4) copy it, change the Guid and the colors, and
you have a new theme.

The key fields (a complete file is `config/themes/ember.json`; every theme has the same
shape):

```jsonc
{
  "Profiles": [{
    "Name": "hekouwang · Ember",
    "Guid": "catppuccin-mocha-dynamic-2026",   // must be unique and stable
    "Normal Font": "OperatorMono-Book 14",     // main font (e.g. JetBrainsMono-Regular 14)
    "Non Ascii Font": "SymbolsNFM 14",         // Nerd Font icon fallback
    "Use Non-ASCII Font": true,                // ⚠️ without this line the fallback does nothing
    "Unlimited Scrollback": true,
    "Silence Bell": true
  }]
}
```

> ⚠️ **Pitfall**: do not inherit the font through `"Dynamic Profile Parent Name"` — once the
> parent profile is deleted, the font falls back to the system default silently and after a
> restart everything is thin and small. Write the settings that matter directly into the JSON.

**Font strategy**: "an elegant main font + Symbols Nerd Font as fallback". The main font does
not have to be a Nerd-patched build; icons are rendered by `font-symbols-only-nerd-font`, so
changing the main font never loses glyphs.

## 3. Optional GUI tweaks

| Path | Item | Value | Why |
|---|---|---|---|
| Profiles → Terminal | Unlimited scrollback | ✅ | Nothing scrolls away, and `Cmd+F` becomes full-text search |
| Profiles → Terminal | Silence bell + Flash visual bell | ✅ | Mute it, flash instead |
| Profiles → General | Working Directory | your workspace | New windows start there |
| General → Startup | Window restoration | Only Restore Hotkey Window | Do not bring back a pile of old windows |
| General → Selection | Copy to pasteboard on selection | ✅ | Select and it is copied |
| General → Selection | Triple-click selects wrapped lines | ✅ | Triple-click grabs the whole logical line |
| Profiles → Text | Cursor: vertical bar, no blinking | — | A cursor that stays put |

System-wide (vim users need this — press and hold repeats the key instead of opening the
accent menu):

```bash
defaults write -g ApplePressAndHoldEnabled -bool false
```

## 4. Advanced features

### 4.1 Shell Integration (official add-on)

```bash
# Official script; review it before running.
curl -L -o /tmp/iterm2-shell-integration.sh https://iterm2.com/shell_integration/install_shell_integration_and_utilities.sh
# Saved to: /tmp/iterm2-shell-integration.sh
bash /tmp/iterm2-shell-integration.sh
```

| Capability | How |
|---|---|
| Navigate command blocks | `Cmd+Shift+↑/↓` jumps between command outputs |
| Command status markers | A small triangle beside each command, red when it failed |
| Images in the terminal | `imgcat picture.png` |
| Remote copy | `it2copy` on a remote machine goes straight to your local clipboard |
| Download / upload | `it2dl <file>` / drag to upload |
| Change colors from a script | `it2setcolor preset "Snazzy"` |

### 4.2 Hotkey Window (a system-wide drop-down terminal)

`Settings → Keys → Hotkey → Create a Dedicated Hotkey Window...`
`Opt+Space` is a good hotkey: press it in any app and the terminal slides down from the top
of the screen; press again and it retracts.
You can add a little transparency and blur in that profile's Window settings.

### 4.3 tmux integration mode (iTerm2 exclusive) ⭐ essential for heavy SSH users

Install it first: `brew install tmux` (already part of the CLI set in `install.sh` and a
`doctor.sh` check).

**Why it matters**: in `-CC` control mode, tmux windows and panes map to **native** iTerm2
tabs and splits (not character art — mouse, scrolling and copying are all native). An SSH
drop, a closed lid or a network change **does not lose the remote session**, and reconnecting
restores it as it was. On a server running long jobs, this is the feature that saves you.

```bash
# a local integrated session
tmux -CC
# remote: attach if it exists, create if not (reconnecting never loses the session)
ssh server -t 'tmux -CC attach || tmux -CC'
# named sessions (keep projects apart and reattach by name)
ssh server -t 'tmux -CC new -A -s deploy'
```

**Usage notes (these are all you normally need)**:

| Action | How |
|---|---|
| New window (= new tab) | `Cmd+T` (the native iTerm2 shortcut just works) |
| Split | `Cmd+D` / `Cmd+Shift+D` (as native) |
| Detach temporarily (leave it running) | Close that iTerm2 window, or the tmux prefix `Ctrl+B` then `d` |
| Reattach | Run the `tmux -CC attach` above again (over SSH for a remote one) |
| See which sessions exist | `tmux ls` on the remote |
| End a session for good | `exit` out of every window, or `tmux kill-session -t <name>` |

> ⚠️ In `-CC` integration mode, do not use tmux's own `Ctrl+B %` / `Ctrl+B "` to split —
> leave that to iTerm2's `Cmd+D`. The prefix key is basically only needed for `Ctrl+B d`
> (detach).

**Adding tmux to an SSH alias** (optional, put it in `~/.zshrc.local`): for machines that
drop often or run long jobs, append `-t 'tmux -CC new -A -s main'` to the alias and every
connection lands in a persistent session:

```bash
# ~/.zshrc.local — persistent-session alias (a drop no longer loses it)
alias ecs:prod:web="ssh -o ServerAliveInterval=60 -t root@<YOUR_SERVER_IP> 'tmux -CC new -A -s main'"
```

> ⚠️ **Check the remote actually has tmux before changing the alias**, otherwise every
> connection greets you with `command not found: tmux`.
> Installing it remotely: `apt install tmux` (Debian/Ubuntu) or `yum install tmux`
> (CentOS/RHEL).
> If you are not sure which machines have it and want to change all the aliases at once, use
> the form with a fallback — without tmux it degrades to a normal login shell instead of
> erroring:
>
> ```bash
> alias ecs:prod:web="ssh -o ServerAliveInterval=60 -t root@<YOUR_SERVER_IP> 'tmux -CC new -A -s main || exec \$SHELL -l'"
> ```
>
> Note that `\$SHELL` must be escaped so it expands on the remote side. Also, `-CC` is
> iTerm2-only: in other apps (the VS Code terminal, say) the alias starts plain tmux without
> the native tab mapping.

> ⚠️ **Conflicts with Claude Code's fullscreen mode (confirmed by the vendor, 2026-07)**: if
> you turn on Claude Code's **fullscreen rendering** (`/tui fullscreen`, an opt-in preview)
> inside a `-CC` session, things break — **scrolling stops working and a double click can
> corrupt the terminal state**. The reason: under `-CC`, iTerm2 renders each pane as a native
> split and does not let tmux draw, which fights the alternate screen buffer a fullscreen
> program wants.
> - **Their words**: *"Fullscreen rendering is incompatible with iTerm2's tmux integration
>   mode... Don't enable fullscreen rendering in `tmux -CC` sessions."*
>   ([code.claude.com/docs/en/fullscreen](https://code.claude.com/docs/en/fullscreen))
> - **The blast radius is small**: (1) it only affects the fullscreen **preview**; Claude
>   Code's **default classic renderer is unaffected** and works with `-CC` as usual.
>   (2) The vendor says plain tmux (without `-CC`) is fine in iTerm2 — though that is the
>   vendor's account, and some versions (issue #58364) have reported minor scrolling /
>   scrollback problems in plain mode too. Deal with it if you hit it.
> - **Conclusion**: if you want Claude Code's fullscreen preview, **do not run it inside a
>   `-CC` session** — either the default renderer plus `-CC`, or fullscreen plus plain tmux
>   (or no tmux). Using `-CC` to survive SSH drops remains the headline feature and is
>   unaffected.

### 4.4 Triggers (output-driven automation) ⭐ shipped with the profile by default

**These 4 are already written into the theme profile JSON and are delivered automatically by
`install.sh` / `theme.sh` — no GUI clicking.**
Section 3 of `doctor.sh` checks they are there; to see or change them, go to
`Settings → Profiles → Advanced → Triggers → Edit`.

| Regex (excerpt) | Action | Effect |
|---|---|---|
| `\b(ERROR\|FATAL\|FAILED\|PANIC\|Exception)\b` | HighlightTrigger, error surface | Error words get the theme's semantic error surface (text ≥4.5:1) |
| `\b(WARN\|WARNING\|DEPRECATED\|TODO\|FIXME)\b` | HighlightTrigger, warn surface | Warnings and to-dos get the warn surface |
| `\b(SUCCESS\|SUCCEEDED\|SUCCESSFUL\|PASSED)\b` | HighlightTrigger, success surface | Success words get the success surface |
| `…[Pp]assword…:` | PasswordTrigger (Instant) | A password prompt pops your password manager |

> ⚠️ The regexes are case-sensitive: only **upper-case** `ERROR` / `WARNING` / `SUCCEEDED`
> and friends are marked (the log convention), so a lower-case "error" or "0 warnings" in
> prose does not get colored into noise.

**Implementation notes (config as code, in `triggers()` inside `config/themes/_generate.py`)**:

- Highlight colors use the Dynamic Profile shorthand `{#foreground,#background}`
  ([official docs](https://iterm2.com/documentation-dynamic-profiles.html)), taken from the
  theme. The background is a **solved semantic surface** (`error_bg` / `warn_bg` /
  `success_bg`), not raw ANSI red/yellow/green; its text color is chosen to stay ≥4.5:1 —
  which is why the highlight follows `./scripts/theme.sh` when you reskin.
- `action` is just iTerm2's trigger class name: `HighlightTrigger` / `PasswordTrigger`.
- `partial:true` is **Instant** in the GUI (fire without waiting for a newline); a password
  prompt has no newline, so it must be Instant.
- To change the rules: edit `triggers()` → `cd config/themes && python3 _generate.py` →
  `./scripts/theme.sh <current theme>` → **open a new tab** (Triggers only apply to new sessions;
  existing tabs keep the old set).

> Why there is no "notify me when a long job finishes": macOS notifications have a fixed
> layout, and iTerm2's built-in Post Notification forces in a line of
> `A trigger fired in session…` that cannot be removed. Using `terminal-notifier` means an
> extra dependency plus manually allowing "trigger runs a command", and it did not look good
> in testing either. On balance it is left out to keep these four clean and reliable.

### 4.4b Semantic Interaction Layer v1 ⭐ shipped with the profile

**Smart Selection + Semantic History** — also written into the Dynamic Profile by
`smart_selection_rules()` / `semantic_history()` in `_generate.py`.

| Match | Cmd-click / first action | Also in context menu |
|---|---|---|
| `path/to/file.ext:42` or `:42:8` | Open at line (best editor) | Copy path:line |
| Git SHA (`[0-9a-f]{7,40}`) | `git show --stat` in repo cwd | Copy SHA |
| `localhost:3xxx` / `127.0.0.1:…` | Open `http://…` in browser | Copy host:port |

Stock iTerm2 rules (Paths, HTTP URL, email, …) are kept in the same list — setting
`Smart Selection Rules` **replaces** inheritance, so the generator embeds them.

Semantic History action = `best editor` (Cursor / VS Code / … if installed).
`setup-gui.sh` pins `CommandSelection=YES` so Cmd-click is not silently off.

```bash
./scripts/doctor.sh --status          # semantic line must show product rules + SH=best editor
./scripts/theme.sh <theme> && Cmd+T   # new tab required
```

### 4.5 Status bar (optional)

`Settings → Profiles → Session → Status bar enabled → Configure`
You can drag in CPU / memory / network / git-branch components; under the Minimal theme, put
it at the bottom with a background matching the theme.
Heavy starship users may prefer to leave it off to avoid saying everything twice.

## 5. Switching themes (use theme.sh)

This skill ships seven themes (3 community + 4 brand). **One command, live on save, no
restart**:

```bash
./scripts/theme.sh                    # theme gallery (with true-color swatches) + the current one
./scripts/theme.sh ember           # back to the default (Ember: warm dark + warm orange cursor)
./scripts/theme.sh voltage            # Voltage (near-black + mint cursor)
./scripts/theme.sh tokyo-night        # Tokyo Night (also gruvbox-dark / catppuccin-mocha)
./scripts/theme.sh --preview voltage  # look without switching: a whole fake terminal
```

How it works: the profiles in `config/themes/*.json` **all share one Guid**, and `theme.sh`
copies the selected one to
`~/Library/Application Support/iTerm2/DynamicProfiles/hekouwang-active-theme.json`, removing
older files that would collide on that Guid. Because the Guid never changes, the "default
profile" binding never breaks. The theme list is discovered by scanning
`config/themes/*.json`, so adding a theme does not mean editing `theme.sh`.

**Adding a theme**: add a 16-color palette under `config/themes/palettes/` (a new
`palettes/mine.py` is discovered automatically), then re-run
`cd config/themes && python3 _generate.py` to produce the matching profile JSON. With the
paid pack present, the same run also emits the Warp YAML, the Ghostty theme and the whole
`ecosystem/` set, and `./scripts/theme.sh <name>` switches all of them together.

⚠️ **Never hand-edit the generated JSON/YAML** — the next run overwrites it. Change the
palette instead.
⚠️ **A Dynamic Profile only overrides the keys it declares** — anything it does not declare
keeps the old value from iTerm2's cache (`New Bookmarks`). So to clear a value that was once
set wrongly through the GUI (`Initial Text`, say), the JSON has to **declare it as empty
explicitly**; simply not writing it does not clear it.

> To try another scheme temporarily you can still import an `.itermcolors` by hand
> (`Settings → Profiles → Colors → Color Presets... → Import...`), for example from the
> several hundred in mbadolato/iTerm2-Color-Schemes. But themes you use regularly belong in
> `config/themes/`.

## 6. Config file paths, for reference

| What | Path |
|---|---|
| Dynamic Profiles | `~/Library/Application Support/iTerm2/DynamicProfiles/` |
| iTerm2 main preferences | `~/Library/Preferences/com.googlecode.iterm2.plist` |
| Starship | `~/.config/starship.toml` |
| zsh config | `~/.zshrc` + `~/.zshrc.local` (private) |
| Shell Integration | `~/.iterm2_shell_integration.zsh` + `~/.iterm2/` |
| atuin database | `~/.local/share/atuin/history.db` |
| Language setting | `~/.config/hekouwang-terminal/lang` |
| Export every setting | `Settings → General → Settings → Export All Settings...` |
