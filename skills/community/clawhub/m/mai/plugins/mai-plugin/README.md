# Mai Plugin

`mai-plugin` is the lightweight OpenClaw native bridge for the `mai` skill.

Install the pair:

```bash
clawhub --workdir ~/.openclaw/workspace --dir skills install mai
openclaw plugins install clawhub:mai-plugin
```

The plugin exposes native tools for local catalog actions and hosted registry actions, then calls the Python CLI from the installed `mai` skill. Configure `projectRoot` only if the skill is installed somewhere other than `~/.openclaw/workspace/skills/mai` or `~/.hermes/skills/commerce/mai`.

Environment fallbacks:

- `MAI_ROOT`
- `MAI_DATA`
- `MAI_REGISTRY_URL`
- `MAI_API_KEY`
