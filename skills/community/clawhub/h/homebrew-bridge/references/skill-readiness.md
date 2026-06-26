# Skill Readiness

Use this file when building public skills that should stay ready on a Linux gateway while depending on a Mac node's Homebrew binaries.

## The Publishable Pattern

Instead of requiring Linux to have `/opt/homebrew/bin/<tool>`:

- install a Linux-side wrapper path
- point the wrapper at the owning Mac over SSH
- make the published skill require the Linux wrapper
- document the same-LAN and Wake-on-LAN assumptions honestly

## Good Example

Requirement:

- `/home/node/.openclaw/bin/gh`

Implementation:

- wrapper on Linux
- real `gh` at `/opt/homebrew/bin/gh` on the Mac
- same-LAN SSH reachability
- optional Wake-on-LAN recovery

## Bad Example

- depending on `/opt/homebrew/bin/gh` directly from Linux
- pretending a Mac Homebrew tool is Linux-native
- hiding the need for a reachable Mac owner node
