# env-health-check

Checks required environment variables, critical directories, and write permissions.

## Usage

```bash
node index.js --env OPENAI_API_KEY --env ANTHROPIC_API_KEY --dir ./memory --dir ./out --out ./out/env_health_report.md
```
