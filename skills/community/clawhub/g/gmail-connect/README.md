# Gmail Connect for OpenClaw

**0.1.3 preview** · Ubuntu · Guided OAuth setup · Gmail read-only by default

Connect a Gmail account using your own Google Cloud project and Desktop OAuth client. The bundled Python app opens a local browser wizard, then lets your OpenClaw agent search and read mail, check recent messages, and prepare drafts for exact review in that wizard.

## Install the source folder

On Ubuntu, clone or download [the GitHub repository](https://github.com/svetlyoh/web-wallet) and install the folder that contains this `SKILL.md`:

```bash
openclaw skills install ./openclaw/skills/gmail-connect/gmail-connect --agent main
```

Replace `main` with your intended agent. Ask it: **Use Gmail Connect to connect my Gmail account.** If host execution is unavailable, launch the wizard in an Ubuntu terminal using the installed skill path:

```bash
python3 "$HOME/.openclaw/workspace/skills/gmail-connect/scripts/gmail_connect.py" wizard
```

Use Python 3.10+ and an existing OpenClaw installation. Follow the Google setup stages in the local browser. Upload OAuth JSON only to that wizard, never to chat or GitHub.

## Documentation

- [SKILL.md](SKILL.md): agent instructions and runtime requirements.
- [CARD.md](CARD.md): listing description, categories, topics, and preview limits.
- [PRIVACY.md](PRIVACY.md): OAuth scopes, local storage, network access, and revocation.
- [references/operations.md](references/operations.md): setup, SSH forwarding, recovery, and acceptance checks.
- [PUBLISHING.md](PUBLISHING.md): GitHub import and versioned updates from GitHub Actions.
- [CHANGELOG.md](CHANGELOG.md): release notes.

This preview has no attachment handling, label editing, deletion, or multi-account UI. Sending requires optional authorization and manual review in the local browser. The separate monitor polls Gmail; automatic chat delivery needs its own explicit automation. Live acceptance and the ClawHub audit remain pending.
