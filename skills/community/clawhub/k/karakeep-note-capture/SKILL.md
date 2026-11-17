---
name: "karakeep-note-capture"
description: "Capture useful durable notes into Karakeep from OpenClaw."
---

# Karakeep Note Capture

Use this skill when you need to store a useful durable note, finding, source, setup detail, or piece of information in Ryan's Karakeep so it is discoverable outside the chat transcript and local memory files.

## When To Use

Use Karakeep capture for information that is useful to rediscover later, especially:

- Homelab service discoveries, URLs, service notes, or admin findings.
- Research findings and references that Ryan may want to browse later.
- Project notes that are more bookmark-like or knowledge-base-like than raw session memory.
- Summaries of completed setup work where Karakeep is a good human-facing archive.

Prefer normal memory files for agent-continuity facts, preferences, and instructions. Prefer both memory and Karakeep when the information is important for future agents and also useful for Ryan to browse.

## Tooling

Use the workspace helper:

```bash
/root/.openclaw/workspace/bin/karakeep-note --title "Useful finding" --tag project-name <<'EOF'
Body text to save.
EOF
```

Defaults:

- Karakeep base URL: `http://192.168.0.64:3000`
- Secret token file: `/root/.openclaw/secrets/karakeep-openclaw-api-token`
- List: `OpenClaw Notes`
- Default tags: `openclaw`, `kevin`

The token is scoped in Karakeep as `openclaw-notes` with bookmark/list/tag read-write permissions. Never print the token.

## Procedure

1. Decide whether the note is worth storing in Karakeep. Avoid saving secrets, private message contents, or noisy raw logs.
2. Write a concise title that Ryan can recognize later.
3. Put the useful content in the body. Include source URLs, hostnames, IDs, or file paths when they help, but do not include credentials.
4. Add one or more project/domain tags using repeated `--tag` flags.
5. Run `karakeep-note` and check that it returns a JSON object with an `id`.
6. If the note is also important for future agent continuity, update the appropriate local memory file as well.

## Examples

```bash
printf '%s\n' 'Zabbix dashboard sync lives in /root/.openclaw/workspace/zabbix-proxmox-services and updates host-a/host-b service status.' \
  | /root/.openclaw/workspace/bin/karakeep-note --title 'Zabbix Proxmox service dashboard notes' --tag zabbix --tag proxmox
```

```bash
/root/.openclaw/workspace/bin/karakeep-note --title 'Karakeep note capture configured' --tag setup <<'EOF'
OpenClaw can capture durable notes into Karakeep using /root/.openclaw/workspace/bin/karakeep-note. Notes go to the OpenClaw Notes list and are tagged openclaw/kevin by default.
EOF
```

## Safety

- Do not save passwords, API tokens, private keys, OAuth codes, or recovery material in Karakeep.
- Do not save private third-party messages unless Ryan explicitly asks and it is appropriate.
- If the helper fails with authentication errors, rotate/regenerate the Karakeep `openclaw-notes` API key and update `/root/.openclaw/secrets/karakeep-openclaw-api-token` with mode `0600`.
