# Nchat Reference

Grounding: nchat 5.15.26, local Homebrew README/manpage, and official d99kris/nchat docs cloned from GitHub in May 2026.

## Project Shape

nchat is a multi-protocol ncurses messaging client for Linux and macOS. It supports Telegram, WhatsApp, and Signal, with Telegram and WhatsApp in the common builds and Signal behind an explicit build flag. It is intended as a lightweight terminal client, not a full replacement for official mobile/desktop clients.

Key capabilities:

- terminal chat list and message history
- text send/reply/edit/delete/forward
- markdown-formatted message support
- attachment viewing/saving/sending
- reactions
- read receipts
- online/away/typing status
- configurable colors, keys, notifications, file pickers, link openers, and external editors
- local message cache and text export

Known limitations:

- no Telegram secret chats
- no voice/video calls
- WhatsApp and Signal support are not available on musl-based systems such as Alpine
- WhatsApp support may be treated as out of scope by upstream maintainers

## CLI

```bash
nchat [OPTION]
```

Options:

- `-d, --confdir <DIR>`: use a config directory other than `~/.config/nchat`
- `-e, --verbose`: enable verbose logging
- `-ee, --extra-verbose`: enable extra verbose logging
- `-h, --help`: show help
- `-k, --keydump`: key code dump mode
- `-m, --devmode`: developer mode
- `-r, --remove`: remove chat protocol account
- `-s, --setup`: set up chat protocol account
- `-v, --version`: show version
- `-x, --export <DIR>`: export message cache to a directory

Side-effect levels:

- Safe read-only: `--version`, `--help`, `man nchat`
- Low-risk but may create config/cache or mark messages read if launched normally: `nchat`
- Login/linking: `--setup`, `USE_PAIRING_CODE=1 --setup`, `USE_QR_TERMINAL=1 --setup`
- Privacy-sensitive: `--export`, logs, cache inspection
- Destructive/account-changing: `--remove`, delete/archive/leave chat commands

## Setup

Default setup:

```bash
nchat --setup
```

The setup flow prompts for protocol and phone number with country code. QR authentication is used by default. Scan the QR code from the official primary app. To use a code/pairing-code flow:

```bash
USE_PAIRING_CODE=1 nchat --setup
```

If QR is not visible through a GUI image viewer:

```bash
USE_QR_TERMINAL=1 nchat --setup
```

Custom Telegram API credentials are optional and are provided only during setup:

```bash
TG_APIID="123456" TG_APIHASH="replace-with-real-hash" nchat --setup
```

Never print real `TG_APIHASH` values, QR codes, pairing codes, or auth codes.

## Multiple Accounts

Recommended pattern: one config directory per protocol/phone number.

```bash
alias telegram='nchat -d ~/.config/nchat-telegram'
alias whatsapp='nchat -d ~/.config/nchat-whatsapp'
telegram --setup
whatsapp --setup
```

Alternative pattern: multiple protocol accounts in one config dir by running `nchat --setup` repeatedly, exiting after each initial sync.

## Interactive Keys

Navigation and global commands:

- `PageDn`: history next page
- `PageUp`: history previous page
- `Tab`: next chat
- `Shift-Tab`: previous chat
- `Ctrl-f`: jump to unread chat
- `Ctrl-g`: toggle help bar
- `Ctrl-l`: toggle contact list
- `Ctrl-n`: go to chat
- `Ctrl-p`: toggle top bar or jump pinned depending on key config
- `Ctrl-q`: quit
- `Ctrl-s`: insert emoji
- `Ctrl-t`: send file
- `Ctrl-x`: send message
- `Ctrl-y`: toggle emojis
- `KeyUp`: select message
- `Alt-@`: insert mention
- `Alt-a`: archive current chat
- `Alt-d`: delete/leave current chat
- `Alt-e`: external editor compose
- `Alt-i`: auto-compose reply
- `Alt-n`: search contacts
- `Alt-p`: pin/unpin current chat
- `Alt-t`: external telephone call
- `Alt-/`: find in chat
- `Alt-?`: find next
- `Alt-$`: external spell check
- `Alt-,`: decrease contact list width
- `Alt-.`: increase contact list width

Selected message commands:

- `Ctrl-d`: delete selected message
- `Ctrl-r`: download/save attached file
- `Ctrl-v`: open/view attached file
- `Ctrl-w`: open link
- `Ctrl-x`: reply to selected message
- `Ctrl-z`: edit selected message
- `Alt-c`: copy selected message
- `Alt-q`: jump to quoted/replied message
- `Alt-r`: forward selected message
- `Alt-s`: add/remove reaction
- `Alt-w`: external message viewer

Text input commands:

- `Ctrl-a`: start of line
- `Ctrl-c`: clear input buffer
- `Ctrl-e`: end of line
- `Ctrl-k`: delete cursor to end
- `Ctrl-u`: delete cursor to start
- `Alt-Left` / `Alt-Right`: move by word
- `Alt-Backspace` / `Alt-Delete`: delete word
- `Alt-Tab`: insert tab spaces
- `Alt-c`: copy input buffer when no message selected
- `Alt-v`: paste into input buffer
- `Alt-x`: cut input buffer

On macOS, Alt/Opt shortcuts depend on the terminal sending Option as Meta. Use `nchat --keydump` to discover exact key codes.

## Config Files

Default config dir: `~/.config/nchat`. Use `--confdir` for another directory. Stop nchat before editing config.

### app.conf

Important keys:

- `attachment_prefetch`: `0` none, `1` selected, `2` all
- `attachment_send_type`: `0` document, `1` detect type, `2` detect plus webp stickers/mp4 GIF-style behavior
- `cache_enabled`: enable local message cache
- `cache_read_only`: debugging read-only cache access
- `clipboard_copy_command`, `clipboard_paste_command`, `clipboard_has_image_command`, `clipboard_paste_image_command`: custom clipboard commands
- `coredump_enabled`: enable core dumps for crashes
- `downloads_dir`: custom download directory
- `emoji_list_all`: show all emojis
- `link_send_preview`: Telegram link previews
- `logdump_enabled`: dump warnings/errors on stdout upon exit
- `mentions_quoted`: bracket quoting for display-name mentions with spaces
- `message_delete`: WhatsApp/Signal deleted-message local display behavior
- `proxy_host`, `proxy_port`, `proxy_user`, `proxy_pass`: SOCKS5 proxy settings
- `timestamp_iso`: ISO timestamps
- `use_pairing_code`, `use_qr_terminal`: setup flags persisted from env
- `version_used`: internal/debugging

Proxy before first setup: run `nchat` once to create config files, edit proxy settings, then run setup.

### ui.conf

Important keys:

- `attachment_open_command`: command with `%1` file placeholder
- `auto_compose_command`, `auto_compose_enabled`, `auto_compose_history_count`: AI reply generation
- `call_command`: command with `%1` phone placeholder
- `confirm_archiving`, `confirm_deletion`, `confirm_send_pasted_image`: safety prompts
- `desktop_notify_*`: desktop notification behavior
- `file_picker_command`: command with `%1` temp result path
- `linefeed_on_enter`: LF vs CR handling for Enter
- `link_open_command`: command with `%1` URL placeholder
- `mark_read_on_view`, `mark_read_when_inactive`, `mark_read_any_chat`: read receipt behavior
- `message_edit_command`: external editor; defaults to `EDITOR` or `nano`
- `message_open_command`: message viewer; defaults to `PAGER` or `less`
- `online_status_share`, `online_status_dynamic`: online status sharing
- `reactions_enabled`: reaction display
- `spell_check_command`: external spell checker; defaults to aspell/ispell when available
- `status_broadcast`: WhatsApp status update visibility
- `terminal_title`, `top_enabled`, `top_show_version`
- `transfer_send_caption`: send text as file caption
- `typing_status_share`: typing status sharing

External commands should single-quote placeholders in examples and be treated as shell-sensitive. Avoid interpolating untrusted data manually.

### key.conf

Bindings accept:

- ncurses macros such as `KEY_CTRLK`
- hex key codes such as `0x22e`
- octal key code sequences such as `\\033\\177`
- single ASCII characters such as `r`
- `KEY_NONE` to disable

Send on Enter:

```text
send_msg=KEY_RETURN
```

Multiline compose on Alt/Opt-Enter while sending on Enter:

```text
# ui.conf
linefeed_on_enter=0

# key.conf
send_msg=KEY_RETURN
linebreak=\\33\\15
```

### color.conf and usercolor.conf

Color files support attributes `normal`, `underline`, `reverse`, `bold`, and `italic`; named colors; and custom RGB hex values such as `0xff8937`. Group receive colors can use `usercolor` to choose a stable color from `usercolor.conf`.

Bundled upstream themes include:

- ayu-dark
- basic-color
- catppuccin-mocha
- default
- dracula
- espresso
- gruvbox-dark
- gruvbox-dark-hard
- solarized-dark-higher-contrast
- tokyo-night
- tomorrow-night
- zenbones-dark
- zenburned

Install a theme by copying its `color.conf` and `usercolor.conf` into the target config dir while nchat is stopped.

### Protocol Config

Telegram: `profiles/Telegram_+nnnnn/telegram.conf`

- `local_key`: internal, never print
- `markdown_enabled`: Telegram markdown conversion
- `markdown_version`: Telegram markdown version
- `profile_display_name`: optional status-bar display name

WhatsApp: `profiles/WhatsAppMd_+nnnnn/whatsappmd.conf`

- `profile_display_name`: optional status-bar display name

Signal: `profiles/Signal_+nnnnn/signal.conf`

- `profile_display_name`: optional status-bar display name

## Auto-Compose

nchat bundles a `compose` helper, typically at:

```bash
realpath "$(dirname "$(which nchat)")/../libexec/nchat/compose"
```

It can use OpenAI-compatible services or Gemini. Relevant env vars include `OPENAI_API_KEY` and `GEMINI_API_KEY`. Default examples use OpenAI `gpt-4o-mini`; custom service/model/timeout/prompt/max tokens can be configured in `auto_compose_command`.

Treat auto-compose as external AI usage. Ask before enabling it, because it may send chat history to a third-party service and may incur cost.

## Clipboard

nchat normally uses system clipboard support on macOS, X11, and Wayland. Custom commands can be configured in `app.conf`:

- `clipboard_copy_command`
- `clipboard_paste_command`
- `clipboard_has_image_command`
- `clipboard_paste_image_command`

Known examples: `pbcopy`/`pbpaste` on macOS, `wl-copy`/`wl-paste` on Wayland, `xclip` on X11, and file-based fallbacks with `tee ~/.clipboard` / `cat ~/.clipboard`.

## Debugging

First pass:

```bash
nchat --verbose
python3 scripts/nchat_doctor.py --include-config
```

For crashes/hangs, upstream suggests core dumps and debugger backtraces. This is privacy-sensitive:

- enable `coredump_enabled=1` in `app.conf` or use shell/system core dump mechanisms
- macOS core dumps commonly appear in `/cores`; inspect with `lldb --core <core> $(which nchat)`
- Linux systems with systemd can use `coredumpctl list nchat` and `coredumpctl debug <pid>`
- always review call stacks/logs for secrets and private data before sharing

For startup regressions, `version_used` in `app.conf` may be useful for context.

## Build and Feature Flags

macOS dependencies include gperf, cmake, openssl, ncurses, ccache, readline, help2man, sqlite, libmagic, and go. Standard Homebrew install:

```bash
brew tap d99kris/nchat
brew install nchat
```

Optional Homebrew protocol exclusions:

```bash
brew install nchat --without-telegram
brew install nchat --without-whatsapp
```

Source build:

```bash
git clone https://github.com/d99kris/nchat
cd nchat
./make.sh deps
./make.sh build
./make.sh install
```

CMake flags:

- `HAS_TELEGRAM=ON/OFF`
- `HAS_WHATSAPP=ON/OFF`
- `HAS_SIGNAL=ON/OFF` (Signal disabled by default)
- `HAS_DUMMY=ON/OFF` for dummy development protocol
- `HAS_DYNAMICLOAD=OFF` or `HAS_SHARED_LIBS=OFF` to alter internal component loading
- `NCHAT_CMAKEARGS="..."` passes custom args to `make.sh`

Signal requires `NCHAT_CMAKEARGS="-DHAS_SIGNAL=ON"`. It may download a prebuilt `libsignal_ffi` or build from source. Force source build with `-DDOWNLOAD_LIBSIGNAL=OFF`.

Low-memory build failures such as `c++: fatal error: Killed signal terminated program cc1plus` usually mean parallelism or RAM pressure. Reduce parallel jobs or use upstream low-memory guidance.

## Safe Operating Checklist

Before doing anything beyond read-only help:

1. Confirm protocol/account/config dir.
2. Confirm whether interactive launch can mark messages read or reveal private content on screen.
3. Ask before login/linking, sending, deleting, forwarding, archiving, reacting, exporting, removing accounts, or enabling auto-compose.
4. Keep config backups before edits.
5. Avoid broad cache/log inspection; inspect only the named file/scope needed.
6. Summarize private findings instead of quoting full message bodies unless the user explicitly asks.
