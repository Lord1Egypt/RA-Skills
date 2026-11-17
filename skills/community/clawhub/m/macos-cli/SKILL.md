---
name: macos-cli
description: "Control a Mac from the terminal with the `macos` command (Calendar, Reminders, Contacts, Mail, Messages, Notes, Safari, Photos, Music, files, windows, screenshots, OCR, the Accessibility tree and system settings), where every command that returns data prints JSON with --json; run `macos doctor --for-agent` before anything else."
homepage: https://github.com/manuaudio/macos-cli
metadata:
  {
    "openclaw":
      {
        "os": ["darwin"],
        "requires": { "bins": ["macos"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "manuaudio/tap/macos-cli",
              "bins": ["macos"],
              "label": "Install macos-cli with Homebrew",
            },
          ],
      },
  }
---

# macos-cli

`macos` is one signed binary that drives a Mac: `macos <area> <action>`. It runs on macOS 13 or later
on Apple silicon. Install it with `brew install manuaudio/tap/macos-cli`; the
[README](https://github.com/manuaudio/macos-cli#install) has the other ways.

## Step one: ask what you may do

Run this before any other command. It never shows a prompt.

```bash
macos doctor --for-agent
```

It answers with one JSON object. `ready` is true only when every privacy area is granted;
`missing` names the areas that are not. Each entry of `areas` carries `state`, `needed_by` (the
commands that fail without it) and `hint` (what a person does to grant it). `capabilities` is the
policy in `~/.config/macos-cli/auth.json`: a command whose capability is `false` is refused with
`capability_denied`.

What you cannot do yourself, ask the person to do:

- A privacy area (Calendars, Contacts, Full Disk Access, Accessibility, Screen Recording, …) is
  granted by a person, through `macos authorize <area>` or System Settings. You cannot click Allow.
- The policy is widened only by a person at a terminal (`macos auth grant <capability>`). Run by
  you, it refuses with `person_required` and nothing changes. `macos auth deny` needs no person.
- `macos reminders complete --id ID` is a dry run unless `--approve` matches the
  `APPLE_EVENTKIT_APPROVE_TOKEN` the person set in your environment.

The list below has every command with its flags, one line of help and whether it writes;
`macos commands --json` prints it. Run `macos help <area> <action>` for a
command's arguments.

## Commands that only read

These change nothing on the Mac. Saving a screenshot or an export to a path you name counts as reading.

- `macos apps info`: Show frontmost app info. Flags: `--json`.
- `macos apps list`: List running applications. Flags: `--all` `--json`.
- `macos audio info`: Show current default input and output devices. Flags: `--json`.
- `macos audio list`: List all audio devices. Flags: `--json`.
- `macos auth list`: Show all capabilities and their current state.
- `macos ax find`: Find UI elements matching a name. Flags: `--app` `--json`.
- `macos ax read`: Dump the UI tree of an app (top 2 levels). Flags: `--json`.
- `macos bluetooth list`: List paired Bluetooth devices. Flags: `--json`.
- `macos calendar calendars`: List all calendars. Flags: `--json`.
- `macos calendar events`: List events in a date range. Flags: `--from` `--to` `--calendar` `--calendar-id` `--timezone` `--json`.
- `macos calendar export`: Export events as a rich JSON envelope (events/count/calendars/filter) for ingestion. Flags: `--from` `--to` `--calendar` `--calendar-id` `--since` `--timezone` `--json`.
- `macos calendar reload`: Force Calendar to refresh from iCloud / CalDAV sources. Flags: `--json`.
- `macos commands`: List every command with its flags, one line of help, and whether it writes. Flags: `--json`.
- `macos contacts export`: Export all contacts as rich JSON for ingestion (read-only). Flags: `--limit` `--since` `--json`.
- `macos contacts get`: Get a contact by ID. Flags: `--json`.
- `macos contacts get-note`: Read the note field of a contact (works around macOS 13+ entitlement). Flags: `--json`.
- `macos contacts search`: Search contacts by name, phone, or email. Flags: `--json` `--limit`.
- `macos daysheets day`: One day's events; an empty list on a day with none. Flags: `--json`.
- `macos daysheets days`: The tour's days with their events, oldest first. Flags: `--from` `--to` `--json`.
- `macos defaults list-domains`: List all defaults domains. Flags: `--json`.
- `macos defaults read`: Read a defaults domain or key. Flags: `--domain` `--key` `--json`.
- `macos disk info`: Show detailed info for a disk or volume. Flags: `--json`.
- `macos disk list`: List all disks and partitions. Flags: `--json`.
- `macos dock list`: List pinned Dock apps. Flags: `--json`.
- `macos doctor`: Report every macOS permission this binary has, and how to get the rest (never prompts). Flags: `--for-agent` `--json`.
- `macos file list`: List directory contents. Flags: `--all` `--json`.
- `macos file read`: Print text file contents. Flags: `--max-bytes` `--force`.
- `macos file stat`: Show file metadata. Flags: `--json`.
- `macos finder cwd`: Get the current folder shown in the front Finder window. Flags: `--json`.
- `macos finder selected`: Get paths of currently selected files in Finder. Flags: `--json`.
- `macos focus modes`: List all configured Focus modes. Flags: `--json`.
- `macos focus status`: Show current Focus mode and DND state. Flags: `--json`.
- `macos info network`: Network interfaces and IP addresses. Flags: `--json`.
- `macos info power settings`: Show power management settings. Flags: `--json`.
- `macos info system`: CPU, RAM, uptime, OS. Flags: `--json`.
- `macos keychain get`: Retrieve a Keychain password. Flags: `--service` `--account` `--json`.
- `macos keychain list`: List Keychain service/account metadata (no passwords). Flags: `--query` `--json`.
- `macos location get`: Get current location (requires Location Services permission). Flags: `--json` `--timeout`.
- `macos login-items list`: List current login items. Flags: `--json`.
- `macos mail accounts`: List Mail accounts. Flags: `--json`.
- `macos mail mailboxes`: List all mailboxes across Mail accounts. Flags: `--account` `--json`.
- `macos mail read`: Read full message content, by Message-ID or by query. Flags: `--id` `--query` `--mailbox` `--account` `--limit` `--timeout` `--json`.
- `macos mail refresh`: Force Mail to check all accounts for new messages now. Flags: `--json`.
- `macos mail search`: Search Apple Mail messages by subject, sender or body. Flags: `--mailbox` `--account` `--limit` `--timeout` `--json`.
- `macos mastertour crew`: A tour's crew. Flags: `--json`.
- `macos mastertour day`: One day: venue, schedule, notes. Flags: `--json`.
- `macos mastertour events`: A day's events (shows). Flags: `--json`.
- `macos mastertour guestlist`: An event's guest list. Flags: `--json`.
- `macos mastertour hotels`: A day's hotels. Flags: `--json`.
- `macos mastertour summary`: A tour's summary for one date. Flags: `--json`.
- `macos mastertour tour`: One tour with all its days. Flags: `--json`.
- `macos mastertour tours`: The tours this key can read. Flags: `--json`.
- `macos menu list`: List top-level menu items for an app (or the focused app). Flags: `--app` `--json`.
- `macos messages conversations`: List recent conversations. Flags: `--limit` `--json`.
- `macos messages read`: Read messages from a conversation. Flags: `--with` `--limit` `--json`.
- `macos mouse position`: Get current cursor position. Flags: `--json`.
- `macos music playlists`: List playlists. Flags: `--json`.
- `macos music queue`: Show upcoming tracks from current playlist. Flags: `--limit` `--json`.
- `macos music status`: Show current track and playback state. Flags: `--json`.
- `macos network dns`: Resolve a hostname to IP addresses. Flags: `--host` `--json`.
- `macos network interfaces`: List network interfaces and their IP addresses. Flags: `--json`.
- `macos network ping`: Ping a host. Flags: `--host` `--count` `--json`.
- `macos network port`: Check if a TCP port is open. Flags: `--host` `--port` `--timeout` `--json`.
- `macos network traceroute`: Trace the route to a host. Flags: `--host` `--max-hops` `--json`.
- `macos notes export`: Export notes with full Unicode bodies as JSON for ingestion (read-only). Flags: `--folder` `--limit` `--include-deleted` `--json`.
- `macos notes folders`: List all Notes folders. Flags: `--json`.
- `macos notes list`: List all notes (title + modified date). Flags: `--json`.
- `macos notes read`: Read a note's full content by title. Flags: `--json`.
- `macos notes search`: Search notes by title. Flags: `--json`.
- `macos ocr file`: OCR an image file (JPEG, PNG, HEIC, etc.). Flags: `--path` `--json`.
- `macos ocr full`: OCR the entire screen. Flags: `--json`.
- `macos ocr region`: OCR a screen region. Flags: `--x` `--y` `--width` `--height` `--json`.
- `macos pdf info`: Get PDF metadata. Flags: `--path` `--json`.
- `macos pdf text`: Extract text from a PDF. Flags: `--path` `--page` `--json`.
- `macos photos albums`: List all photo albums. Flags: `--json`.
- `macos photos export`: Export photo(s) to a directory. Flags: `--name` `--to` `--limit` `--json`.
- `macos photos recent`: List recently added photos. Flags: `--limit` `--json`.
- `macos photos search`: Search photos by keyword. Flags: `--limit` `--json`.
- `macos process find`: Find processes by name. Flags: `--json`.
- `macos process list`: List running processes. Flags: `--sort` `--limit` `--json`.
- `macos reminders done`: (retired) Use 'reminders complete' — completion is gated by APPLE_EVENTKIT_APPROVE_TOKEN. Flags: `--json`.
- `macos reminders export`: Export reminders as rich JSON for ingestion (read-only). Flags: `--list` `--include-completed` `--timeout` `--json`.
- `macos reminders list`: List reminders. Flags: `--list` `--completed` `--json`.
- `macos reminders lists`: List all reminder lists. Flags: `--json`.
- `macos reminders status`: Report Reminders authorization status without prompting. Flags: `--json`.
- `macos safari bookmarks`: List Safari bookmarks. Flags: `--query` `--json`.
- `macos safari history`: Browse Safari history via History.db. Flags: `--limit` `--query` `--json`.
- `macos safari read`: Get text content of current Safari tab. Flags: `--window` `--tab` `--json`.
- `macos safari tabs`: List open Safari tabs. Flags: `--json`.
- `macos screen capture`: Take a screenshot. Flags: `--output` `--window`.
- `macos screen info`: Display screen dimensions and scaling. Flags: `--json`.
- `macos screenshot full`: Capture the full screen. Flags: `--output`.
- `macos screenshot region`: Capture a rectangular region. Flags: `--x` `--y` `--width` `--height` `--output`.
- `macos screenshot window`: Capture a specific app window (needs Screen Recording permission). Flags: `--app` `--output`.
- `macos shortcuts list`: List all shortcuts. Flags: `--json`.
- `macos spaces list`: List all Mission Control spaces. Flags: `--json`.
- `macos speech voices`: List available voices. Flags: `--json`.
- `macos spotlight search`: Search files and folders via Spotlight. Flags: `--name-only` `--kind` `--limit` `--in-dir` `--json`.
- `macos storage usage`: Disk usage of a path. Flags: `--json`.
- `macos storage volumes`: List mounted volumes. Flags: `--json`.
- `macos system audio devices`: List audio input/output devices. Flags: `--json`.
- `macos system audio now-playing`: Currently playing media info. Flags: `--json`.
- `macos system battery`: Battery status. Flags: `--json`.
- `macos system clipboard get`: Read clipboard contents. Flags: `--json`.
- `macos system display wallpaper get`: Get current wallpaper path for each display. Flags: `--json`.
- `macos system vpn status`: List VPN configurations and their state. Flags: `--json`.
- `macos system wifi networks`: Scan for nearby networks. Flags: `--json`.
- `macos system wifi status`: Current Wi-Fi connection. Flags: `--json`.
- `macos timemachine list-destinations`: List configured backup destinations. Flags: `--json`.
- `macos timemachine list-snapshots`: List local Time Machine snapshots. Flags: `--json`.
- `macos timemachine status`: Show backup status and last backup time. Flags: `--json`.
- `macos trash list`: List Trash contents. Flags: `--json`.
- `macos voice-memos export`: Copy a voice memo to a destination path. Flags: `--out`.
- `macos voice-memos list`: List all voice memos. Flags: `--limit` `--json`.
- `macos window list`: List all visible windows with their positions and sizes. Flags: `--app` `--json`.

## Commands that write

These change data, a setting or the state of the Mac, or send, play or show something. Run one only when the person asked for that change.

- `macos apps launch`: Launch an application.
- `macos apps quit`: Quit an application. Flags: `--force`.
- `macos audio set-input`: Set the default audio input device.
- `macos audio set-output`: Set the default audio output device.
- `macos auth deny`: Deny a capability.
- `macos auth grant`: Grant a capability (a person confirms it at the terminal).
- `macos auth reset`: Reset all capabilities to default policy (a person confirms it at the terminal).
- `macos auth setup`: Interactive onboarding wizard — configure all capabilities (needs a person at the terminal). Flags: `--all`.
- `macos authorize`: Ask macOS for one permission: shows its prompt, or opens its settings pane. Flags: `--timeout` `--json`.
- `macos ax click`: Click a UI element by name. Flags: `--app`.
- `macos ax hints`: List all interactive UI elements with hint numbers (for agent use). Flags: `--app` `--json` `--click`.
- `macos bluetooth connect`: Connect a paired Bluetooth device. Flags: `--json`.
- `macos bluetooth disconnect`: Disconnect a Bluetooth device. Flags: `--json`.
- `macos calendar create`: Create a calendar event. Flags: `--title` `--start` `--end` `--calendar` `--calendar-id` `--timezone` `--location` `--notes` `--all-day` `--alarm` `--json`.
- `macos calendar delete`: Delete calendar events by stable id (--id) OR by title+date (mutually exclusive). Flags: `--id` `--title` `--date` `--calendar` `--calendar-id` `--contains` `--all` `--json`.
- `macos calendar update`: Update an existing calendar event by ID. Flags: `--id` `--title` `--start` `--end` `--location` `--notes` `--calendar` `--calendar-id` `--alarm` `--clear-alarms` `--timezone` `--json`.
- `macos contacts create`: Create a new contact. Flags: `--first-name` `--last-name` `--organization` `--job-title` `--phone` `--phone-label` `--email` `--email-label` `--note` `--json`.
- `macos contacts delete`: Delete a contact by ID. Flags: `--json`.
- `macos contacts set-note`: Write the note field of a contact (works around macOS 13+ entitlement). Flags: `--text` `--if-empty` `--json`.
- `macos contacts update`: Update fields on an existing contact. Flags: `--first-name` `--last-name` `--organization` `--job-title` `--add-phone` `--add-phone-label` `--add-email` `--add-email-label` `--json`.
- `macos daysheets login`: Save the tour's calendar feed URL (on stdin) in the login keychain. Flags: `--json`.
- `macos defaults delete`: Delete a defaults key. Flags: `--domain` `--key` `--json`.
- `macos defaults write`: Write a value to a defaults key. Flags: `--domain` `--key` `--value` `--type` `--json`.
- `macos disk eject`: Eject a disk or volume. Flags: `--json`.
- `macos disk mount`: Mount a disk image or volume. Flags: `--json`.
- `macos disk unmount`: Unmount a volume (without ejecting the disk). Flags: `--force` `--json`.
- `macos dock add`: Pin an app to the Dock. Flags: `--json`.
- `macos dock remove`: Remove an app from the Dock by name. Flags: `--json`.
- `macos dock restart`: Restart the Dock (applies pending changes). Flags: `--json`.
- `macos file copy`: Copy a file or directory. Flags: `--json`.
- `macos file delete`: Permanently delete a file or directory (use 'trash add' for recoverable delete). Flags: `--json`.
- `macos file move`: Move or rename a file or directory. Flags: `--json`.
- `macos finder go-to`: Navigate the front Finder window to a directory. Flags: `--path` `--json`.
- `macos finder new-folder`: Create a new folder and reveal it in Finder. Flags: `--path` `--json`.
- `macos finder open`: Open a file or folder in Finder.
- `macos finder rename`: Rename a file or folder. Flags: `--from` `--to` `--json`.
- `macos finder reveal`: Reveal a file or folder in Finder.
- `macos finder show-hidden`: Toggle or check the 'Show hidden files' Finder setting. Flags: `--on` `--off` `--status` `--json`.
- `macos finder tag`: Read or write Finder color tags on a file or folder. Flags: `--path` `--add` `--remove` `--list` `--json`.
- `macos focus off`: Disable Do Not Disturb. Flags: `--json`.
- `macos focus on`: Enable Do Not Disturb. Flags: `--mode` `--json`.
- `macos info power caffeinate`: Prevent sleep for N seconds.
- `macos info power sleep`: Put Mac to sleep.
- `macos keyboard key`: Send a key or shortcut (e.g. 'cmd+c', 'escape', 'return').
- `macos keyboard type`: Type text into the frontmost app. Flags: `--delay`.
- `macos keychain delete`: Delete a Keychain item. Flags: `--service` `--account` `--json`.
- `macos keychain set`: Save or update a Keychain password. Flags: `--service` `--account` `--password` `--update` `--json`.
- `macos login-items add`: Add an app to login items. Flags: `--hidden` `--json`.
- `macos login-items remove`: Remove a login item by name. Flags: `--json`.
- `macos mail delete`: Delete messages matching a query. Flags: `--query` `--limit` `--json`.
- `macos mail draft`: Create a draft email in Mail. Flags: `--to` `--subject` `--body` `--cc` `--open` `--json`.
- `macos mail mark`: Mark messages as read/unread/flagged. Flags: `--query` `--read` `--unread` `--flagged` `--unflagged` `--limit` `--json`.
- `macos mail reply`: Reply to a message matching a query. Flags: `--query` `--body` `--limit` `--all` `--json`.
- `macos mail send`: Send an email immediately via Mail. Flags: `--to` `--subject` `--body` `--cc` `--json`.
- `macos mastertour login`: Save the Master Tour API key and secret (secret on stdin) in the login keychain. Flags: `--key` `--json`.
- `macos menu click`: Click a menu item by path, e.g. 'View > Show Sidebar'. Flags: `--app`.
- `macos messages delete`: Delete a conversation. Flags: `--with` `--json`.
- `macos messages send`: Send an iMessage or SMS. Flags: `--to` `--text` `--json`.
- `macos mouse click`: Click at position. Flags: `--x` `--y` `--right` `--double`.
- `macos mouse drag`: Click and drag from one position to another. Flags: `--from-x` `--from-y` `--to-x` `--to-y`.
- `macos mouse move`: Move cursor to position. Flags: `--x` `--y`.
- `macos mouse scroll`: Scroll at position. Flags: `--x` `--y` `--amount`.
- `macos music add-to-playlist`: Add a track to a playlist. Flags: `--track` `--playlist` `--json`.
- `macos music next`: Skip to next track.
- `macos music pause`: Pause playback.
- `macos music play`: Play or resume.
- `macos music prev`: Go to previous track.
- `macos music search`: Search library and play first result. Flags: `--json`.
- `macos music volume`: Get or set volume (0–100).
- `macos notes create`: Create a new note. Flags: `--title` `--body` `--folder` `--json`.
- `macos notes create-folder`: Create a new Notes folder. Flags: `--name` `--json`.
- `macos notes delete`: Delete a note by title (partial match, first match). Flags: `--title` `--json`.
- `macos notes update`: Update a note's title and/or body. Flags: `--title` `--new-title` `--body` `--json`.
- `macos notify send`: Send a notification. Flags: `--title` `--body` `--subtitle` `--sound` `--json`.
- `macos photos add-to-album`: Add a photo to an album. Flags: `--name` `--album` `--json`.
- `macos photos delete`: Delete photo(s) from the library. Flags: `--name` `--limit` `--json`.
- `macos process kill`: Kill a process by PID or name. Flags: `--pid` `--name` `--signal` `--all` `--json`.
- `macos reminders complete`: Complete a reminder: dry-run unless --approve matches APPLE_EVENTKIT_APPROVE_TOKEN. Flags: `--id` `--approve` `--json`.
- `macos reminders create`: Create a new reminder. Flags: `--title` `--due` `--list` `--notes` `--json`.
- `macos reminders delete`: Delete a reminder by ID. Flags: `--json`.
- `macos reminders uncomplete`: Mark a reminder as not complete. Flags: `--json`.
- `macos reminders update`: Update a reminder by ID. Flags: `--title` `--due` `--notes` `--list` `--json`.
- `macos safari close`: Close a Safari tab. Flags: `--url` `--index` `--current` `--json`.
- `macos safari execute`: Execute JavaScript in the current Safari tab. Flags: `--window`.
- `macos safari new-tab`: Open a new Safari tab at a URL. Flags: `--url` `--json`.
- `macos safari open`: Open a URL in Safari.
- `macos safari reload`: Reload a Safari tab. Flags: `--url` `--json`.
- `macos screen lock`: Lock the screen.
- `macos script run`: Execute a script and return its result. Flags: `--jxa` `--applescript` `--file` `--timeout` `--silent` `--json`.
- `macos setup`: Interactive setup — check permissions and verify every capability works.
- `macos shortcuts run`: Run a shortcut by name. Flags: `--input` `--json`.
- `macos spaces switch`: Switch to a space by index (1-based).
- `macos speech say`: Speak text aloud. Flags: `--voice` `--rate` `--output`.
- `macos system audio mute`: Get or set mute state. Flags: `--json`.
- `macos system audio volume`: Get or set system volume. Flags: `--json`.
- `macos system clipboard set`: Write text to clipboard.
- `macos system display brightness`: Get or set display brightness. Flags: `--json`.
- `macos system display dark-mode`: Toggle or get dark mode. Flags: `--json`.
- `macos system display wallpaper set`: Set the desktop wallpaper (all displays). Flags: `--json`.
- `macos system lock`: Lock the screen immediately. Flags: `--json`.
- `macos system sleep`: Put the Mac to sleep. Flags: `--json`.
- `macos system vpn connect`: Connect a VPN by name. Flags: `--json`.
- `macos system vpn disconnect`: Disconnect a VPN by name. Flags: `--json`.
- `macos system wifi join`: Join a Wi-Fi network. Flags: `--ssid` `--password`.
- `macos system wifi leave`: Disconnect from current Wi-Fi network.
- `macos timemachine start`: Start a backup immediately.
- `macos timemachine stop`: Cancel a running backup.
- `macos trash add`: Move a file or folder to the Trash. Flags: `--json`.
- `macos trash empty`: Empty the Trash. Flags: `--json`.
- `macos update`: Replace this binary with the newest signed Release, in place. Flags: `--check` `--json`.
- `macos window focus`: Bring a window to the front. Flags: `--title`.
- `macos window fullscreen`: Toggle fullscreen for an app window. Flags: `--title`.
- `macos window maximize`: Expand a window to fill the visible screen area. Flags: `--title`.
- `macos window minimize`: Minimize a window. Flags: `--title`.
- `macos window move`: Move a window to a new position. Flags: `--x` `--y` `--title`.
- `macos window resize`: Resize a window. Flags: `--width` `--height` `--title`.
- `macos window snap`: Snap a window to a screen region. Flags: `--title`.

## Answers and errors

Under `--json` a command prints one JSON value on stdout. A failure is one JSON object on stdout,
stderr stays empty, and the exit status says what kind of failure it was. Branch on `error`;
`message` and `hint` are for people and may change.

```json
{
  "ok": false,
  "status": "error",
  "error": "calendar_not_found",
  "message": "No calendar is named 'Nope'.",
  "hint": "Run `macos calendar calendars` to see the names.",
  "calendar": "Nope",
  "exit_code": 3
}
```

| Exit | Meaning | `error` codes |
|---|---|---|
| 0 | Success | |
| 64 | The command line was rejected | `usage`, `invalid_argument`, `invalid_date`, `invalid_date_range`, `invalid_alarm`, `invalid_delete_mode`, `invalid_timezone`, `ambiguous_calendar` |
| 3 | The named thing does not exist | `not_found`, `calendar_not_found`, `event_not_found` |
| 4 | Not allowed | `capability_denied` (the policy), `access_denied` (macOS privacy settings), `person_required` (only a person may do it), `credentials_missing` / `credentials_refused` (a tour connector has no key, or the service refused it) |
| 5 | No answer in time | `timeout`, `fetch_timeout` |
| 6 | The system or an app reported an error | `app_error` |

A command that only performs an action (move a window, click, play) prints a line of text and has
no `--json` output; asked for `--json`, it answers with a `usage` error. A filter that names a
list, calendar or folder that does not exist returns nothing or an error, never everything.

## Examples

What is on the calendar this week:

```bash
macos doctor --for-agent
macos calendar events --from 2026-11-16 --to 2026-11-22 --json
```

Find a contact, then leave a draft in Mail for the person to read and send:

```bash
macos contacts search "Ana" --limit 5 --json
macos mail draft --to ana@example.com --subject "Thursday" --body "Does 3 pm still work?" --json
```

What the tour does on a show day, from Daysheets or Master Tour (read only; a person saves the
key once with `macos daysheets login` or `macos mastertour login`):

```bash
macos daysheets day 2026-12-04
macos mastertour tours
```

Add a reminder to a named list:

```bash
macos reminders lists --json
macos reminders create --title "Call the venue" --list Work --due "2026-11-12 10:00" --json
```
