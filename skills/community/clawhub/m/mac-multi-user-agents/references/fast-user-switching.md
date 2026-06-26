# Fast User Switching

Use this file when one Mac should host several OpenClaw agent users.

## Why Use It

Fast User Switching is the least awkward built-in way to keep multiple macOS users alive on one machine without logging out the whole system.

For agent hosts, that means:

- separate browser state per user
- separate `~/.openclaw` per user
- faster handoff between agent sessions

## Rules

- keep agent users lightweight
- avoid running heavy human desktop workloads inside every user
- name users clearly, for example `agent1`, `agent2`, `agent3`
- do not mix the human operator profile with all agent activity if you can avoid it

## Setup Guidance

- enable Fast User Switching in macOS user settings
- verify enough RAM and swap headroom before adding more users
- prefer one managed browser profile per user

## Failure Mode

If one user session wedges:

- kill or log out only that user
- leave the other agent users and shared Homebrew intact
