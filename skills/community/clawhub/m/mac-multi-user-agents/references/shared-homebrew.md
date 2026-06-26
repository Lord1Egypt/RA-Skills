# Shared Homebrew

Use this file when multiple agent users on one Mac need the same toolchain.

## Goal

Share the binary/toolchain layer:

- `/opt/homebrew/bin`
- `/opt/homebrew/sbin`
- shared formulae and casks

Do not share user runtime state:

- `~/.openclaw`
- `~/.ssh`
- browser profiles
- app tokens stored in user homes

## Recommended Pattern

- Homebrew owned by the main administrative user or a controlled admin group
- agent users consume the shared binaries on PATH
- agent users do not each install their own duplicate Node/OpenClaw trees

## What To Verify

- every agent user sees `/opt/homebrew/bin` on PATH
- `brew`, `node`, `npm`, and `openclaw` resolve to the shared path
- per-user configs stay in the user home, not under `/opt/homebrew`

## Rollback

If one agent user is removed:

- do not remove Homebrew
- only remove that user’s home state and trust material
