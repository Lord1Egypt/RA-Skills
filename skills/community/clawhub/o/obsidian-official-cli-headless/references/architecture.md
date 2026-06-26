# Architecture notes

## Why this skill exists

Official Obsidian CLI is desktop-first. It does not behave like a fully standalone headless CLI.

On a headless Linux server, the main blockers are:
- Electron is unstable or restricted when launched as `root`
- there is no native display session
- the CLI talks to a running Obsidian instance

## Adaptation pattern

Use four layers:

1. **Official Obsidian install**
   - provides `/usr/bin/obsidian`
2. **Dedicated non-root user**
   - avoids Electron/root sandbox pain
3. **Xvfb virtual display**
   - gives Electron a display target on a headless host
4. **Wrapper command**
   - hides `su - obsidian` + `xvfb-run` + working-directory setup

## Why ACLs

When the vault lives under `/root`, changing ownership is heavier than needed.
ACLs allow the dedicated `obsidian` user to traverse `/root` and read/write only the chosen vault path.

## Operational model

The wrapper typically runs:

```bash
su - obsidian -c 'cd /root/obsidian-vault && xvfb-run -a /usr/bin/obsidian --disable-gpu ...'
```

This is the practical bridge between:
- a desktop-first application
- a server-style workflow

## Verified commands from field use

- `help`
- `vault`
- `create`
- `read`
- `daily`
- `daily:append`
- `daily:read`
- `search`

## Boundaries

This pattern is for headless Linux adaptation only. It is intentionally narrower than full Obsidian environment management.
