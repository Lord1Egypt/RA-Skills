🪪 **clawhub** is the OpenClaw skill registry.
It runs as the `clawhub` CLI, published to npm as `clawhub`.

Make sure `clawhub` is available:
```bash
npm i -g clawhub
```

## 🌍 Using the Registry

Login (once):
```bash
clawhub login
clawhub whoami  # verify
```

Search:
```bash
clawhub search email assistant
clawhub explore --limit 20
```

Install a skill:
```bash
clawhub install email-assistant
```

## 📤 Publishing to ClawHub

Publish your local skill directory:
```bash
clawhub publish <path-to-skill> --slug <slug> --name "<Skill Name>" --version 1.0.0 --changelog "Initial release"
```

After publishing, users can install with:
```bash
clawhub install <slug>
```

Update an existing skill:
```bash
clawhub publish <path> --slug <slug> --version 1.1.0 --changelog "Auto-reply rules + hourly sync"
```

Use `--force` to republish the same version if needed.

## ⚠️ Known Issue (2026-06)

On some versions, `clawhub login` may show the "Browser callback is no longer supported" error.
Workaround: Ensure you are using the latest version:
```bash
npm update -g clawhub
```
Then run `clawhub login` again — it should switch to device-code login.
