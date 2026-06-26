# Skill Readiness

Use this file when building public skills that should stay ready on a Linux gateway while depending on Mac-owned tools.

## The Publishable Pattern

Instead of pretending Linux can run a Mac-only binary:

- install a Linux-side wrapper path
- point that wrapper at the owning Mac over SSH
- require the wrapper path in the public skill
- document the network and Wake-on-LAN assumptions honestly

## Good Example

Requirement:

- `/home/node/.openclaw/bin/imsg`

Implementation:

- wrapper on Linux
- real binary on the owning Mac
- same-LAN SSH reachability
- optional Wake-on-LAN recovery if the Mac can sleep

## Bad Example

- depending directly on `/opt/homebrew/bin/imsg` from a Linux skill
- claiming Linux natively supports a Mac-only tool
- hiding the need for a reachable Mac owner node
