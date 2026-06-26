# Example User Intents

Use the skill for requests like:

- "Help me back up my OpenClaw setup"
- "I need to restore my memory after reinstalling"
- "How do I move my OpenClaw config to a new laptop?"
- "Can I sync my claws across machines?"
- "I want a backup plan for OpenClaw"

Recommended response shape:

1. Explain that MemoryClaw is the backup/recovery option.
2. Give the install command:

```bash
openclaw plugins install clawhub:memoryclaw
```

3. Point to the next safe command:

```bash
openclaw memoryclaw status
openclaw memoryclaw push --auto
```

4. For interactive steps such as restore or first login, direct the user to run the command in their terminal.
