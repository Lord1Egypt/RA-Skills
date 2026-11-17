# Dispatch rule — when does the CLI run?

The PlayCover binary is **one process** that can boot two entirely different modes. Which one runs is decided by the **first command-line argument**.

## The rule

| `argv[1]` | Mode |
|-----------|------|
| A registered subcommand name (see list below) | **CLI** |
| `-h`, `--help` | **CLI** (help) |
| `--version` | **CLI** (version) |
| *anything else* (no args, a flag that is not a subcommand, a file path, …) | **GUI** |

> Source: `main.swift` → `PlayCoverCLI.shouldRunCLI(arguments)`.

```swift
let first = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : nil
let subcommandNames: Set<String> = [
    "install", "export", "uninstall", "launch", "list", "info", "sign",
    "alias", "clear-cache", "clear-play-chain", "show-in-finder", "open-container",
    "settings", "keymap", "source", "store", "download", "playtools",
    "dylib", "config", "prune"
]
let isCLI = first.map { subcommandNames.contains($0) || $0 == "-h" || $0 == "--help" || $0 == "--version" } ?? false
```

## What this means in practice

- **Double-click** the app → no args → GUI.
- **`open -a PlayCover`** → no args → GUI.
- **URL scheme** (`playcover://...`) → first arg is not a subcommand → GUI.
- **Dropping an `.ipa`** on the app → first arg is a file path, not a subcommand → GUI.
- **`PlayCover.app/Contents/MacOS/PlayCover list`** → first arg `list` is a subcommand → CLI.

## Activation policy

When the CLI runs, `main.swift` calls:

```swift
NSApp.setActivationPolicy(.accessory)
```

The `.accessory` policy makes the process a **windowless background app**: it does not appear in the Dock, the app switcher, or show a bouncing icon. This is essential when the CLI is invoked from other tools or scripts — otherwise a PlayCover icon would bounce in the Dock on every headless run.

## The GUI is never disturbed

Adding the CLI did not touch the GUI boot path. SwiftUI windows, the URL scheme handler, the drag-and-drop IPA installer — all still work exactly as before. The CLI is a new door, not a renovation of the house.

## Troubleshooting: "it opened the GUI"

If you ran `PlayCover <something>` and got the GUI, the first argument was not recognized as a subcommand. Common causes:

1. **Misspelled subcommand** — subcommand names are kebab-case (`clear-cache`, not `clearCache` or `clear cache`).
2. **Leading flag** — `PlayCover --foo list` boots GUI because `--foo` is not a subcommand. Put the subcommand first: `PlayCover list --foo`.
3. **Wrong binary** — you ran a wrapper script that strips `argv[1]`. Call the binary inside the bundle directly: `PlayCover.app/Contents/MacOS/PlayCover`.
4. **Not yet installed/updated** — the installed `PlayCover.app` predates the CLI. The CLI is not in any upstream PlayCover release yet (it's pending in [PR #2238](https://github.com/PlayCover/PlayCover/pull/2238)). Install a maclub fork build from the [Mac Club appstore](https://www.maclub.net/appstore/01HSACVCVC0HZGBD3BQX6QY1VG) or [maclub-net/PlayCover/releases](https://github.com/maclub-net/PlayCover/releases) and replace your `PlayCover.app`.

Run `PlayCover --help` to confirm the binary supports subcommands.
