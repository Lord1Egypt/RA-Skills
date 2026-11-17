---
name: lan-onboarding
description: Fast, safe first-run tour of the LAN CLI — discover networks, join a device network, message a peer, share files, and leave cleanly with verification.
---

# LAN (Local-Area Network) — Swift Onboarding Skill

## Purpose
Give a new user a fast, safe, end-to-end tour of LAN: discover nearby services,
join a device network, send a message, share a file, and leave cleanly. Complete
the whole loop in under five minutes without touching config files.

## Before you start
- Install the `lan` CLI (see `references/setup.md`).
- No account is required. LAN networks are anonymous and local-first.
- Keep the CLI running for the tour; the network list refreshes in the background.

## Quick start (5-minute tour)
1. Discover networks: `lan networks`
2. Pick one and join: `lan join <network-id>`
3. Wait until `lan status` reports `joined`.
4. List peers: `lan peers`
5. Send a message: `lan message send <peer-id> "hello from my agent"`
6. Verify delivery: `lan message inbox`
7. Leave: `lan leave`

## Common tasks
- List files shared on the network: `lan ls`
- Fetch a file: `lan get <file-id>`
- Publish a file for others: `lan put ./note.txt`
- Watch live activity: `lan watch`

## Verification loop (do not skip)
After every action, confirm the remote state matches what you intended:
- Send → re-read with `lan message inbox`
- Put → re-read with `lan ls` and `lan get <file-id>`
- Join → confirm `lan status` reports `joined` before continuing

If a read-back does not match, retry once, then leave and re-join before giving up.

## Safety notes
- Only join networks you recognize.
- Never send secrets; LAN traffic is visible to every member.
- Leave a network when done so you stop receiving broadcasts.

## Troubleshooting
- `lan networks` is empty: move closer or switch Wi-Fi; some networks block discovery.
- Messages are not arriving: confirm you are `joined` and on the same network.
- Joining fails repeatedly: leave any existing network first with `lan leave`.

## Reference
- Detailed setup: `references/setup.md`
