# Keyboard shortcuts

> **English** · [简体中文](shortcuts.zh-CN.md)

## Panes and tabs

| Shortcut | Action |
|---|---|
| `Cmd+D` | Split vertically (side by side) |
| `Cmd+Shift+D` | Split horizontally (top and bottom) |
| `Cmd+Opt+arrow` | Move focus between panes |
| `Cmd+Shift+Enter` | Maximise / restore the current pane |
| `Cmd+T` / `Cmd+W` | New / close tab |
| `Cmd+number` | Jump to tab N |
| Tab with new output | A dot on the tab — turned on by `setup-gui.sh` so four parallel agents are easy to tell apart |
| `Cmd+Shift+O` | Open Quickly: fuzzy-search every tab/session and jump |

## Search and history

| Shortcut | Action |
|---|---|
| `Cmd+F` | Search the scrollback (unlimited scrollback = full-text search) |
| `Cmd+Shift+H` | Paste history (a time machine for your clipboard) |
| `Cmd+Opt+B` | Instant Replay: rewind the screen to find output that scrolled away |
| `Ctrl+R` | atuin full-text search over command history |
| `Ctrl+T` | fzf fuzzy file search |
| `Alt+C` | fzf fuzzy cd |
| `Cmd+Shift+↑/↓` | Jump between command blocks (Shell Integration) |

## Selecting and copying

| Shortcut | Action |
|---|---|
| `Cmd+Shift+C` | Copy Mode (vim-style keyboard selection: hjkl to move, v to select, y to copy) |
| Double / triple click | Select a word / a whole line (triple-click includes wrapped lines — enabled by `setup-gui.sh`) |
| `Cmd+click` | Smart-open a URL or file path |
| `Opt+drag` | Rectangular (column) selection |
| Copy on select | Enabled by `setup-gui.sh` — select, then `Cmd+V` straight away |

## Shell (from the plugins)

| Key | Action |
|---|---|
| `→` / `End` | Accept the grey autosuggestion |
| `Tab` | Enter the zsh-autocomplete menu, arrows to choose |
| `z keyword` | zoxide jumps to a directory you visit often; `zi` to pick interactively |

## Everything else

| Shortcut | Action |
|---|---|
| `Cmd+/` | Highlight the cursor position |
| `Cmd+Enter` | Full screen |
| `Shift+Enter` | Send a newline (multi-line input for AI CLIs — a custom key mapping) |
| `Opt+Space` | Drop-down hotkey window (requires the one-time Hotkey Window setup — not enabled by default) |

## Natural Text Editing (one-time GUI preset)

iTerm2 ships a built-in preset for macOS word/line editing. It is not written by
`setup-gui.sh` because the key-map format changes between iTerm2 versions; apply it once:

`Settings → Profiles → Keys → Key Mappings → Presets → Natural Text Editing`

That gives you `Opt+Backspace` (delete word), `Opt+←/→` (move by word),
`Cmd+←/→` (start/end of line) and `Cmd+Backspace` (delete to start of line).
