---
name: openmandate
description: >-
  Access historical OpenMandate mandates and matches or close retained work for
  an existing account. OpenMandate is in private development and is not
  accepting new mandates or integrations. Requires an existing API key.
license: MIT
metadata:
  author: openmandate
  version: "0.6.2"
  homepage: https://openmandate.ai
  openclaw:
    emoji: "handshake"
    requires:
      env:
        - OPENMANDATE_API_KEY
        - OPENMANDATE_BASE_URL
      bins:
        - python3
    primaryEnv: OPENMANDATE_API_KEY
---

# OpenMandate

> [!IMPORTANT]
> OpenMandate is in private development. We are not currently accepting new mandates or new integrations.

Use this retained integration only for an existing OpenMandate account. If
`OPENMANDATE_API_KEY` is absent, explain that new integrations are unavailable;
do not direct the user to sign up or create a key.

## Available operations

Prefer the hosted MCP endpoint at `https://mcp.openmandate.ai/mcp`. The bundled
stdlib-only helper remains available as:

```bash
python3 {baseDir}/scripts/openmandate.py <command> [args]
```

Existing users may:

- list or retrieve their historical mandates and matches;
- list retained contacts;
- close an existing mandate;
- decline a match; and
- delete a contact.

Do not attempt to create or reactivate work, add or verify contacts, submit
intake answers or outcomes, accept matches, or establish a new account/API key.
Those operations return `SERVICE_PRIVATE_DEVELOPMENT`.

Before a consequential withdrawal action such as closing a mandate or deleting
a contact, confirm the exact target with the user. Read-only historical access
does not require extra ceremony.
