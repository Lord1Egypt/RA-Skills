# paperclip-resilience

Production resilience patterns for AI agents running on [Paperclip](https://github.com/paperclipai/paperclip), orchestrated through [OpenClaw](https://github.com/openclaw/openclaw).

See [SKILL.md](./SKILL.md) for full documentation, architecture, and configuration guide.

## Install

```bash
clawhub install paperclip-resilience
```

## Modules

- **spawn-with-fallback** — Automatic provider failover on rate limits / billing errors
- **model-rotation** — Track attempts, rotate models + thinking levels on repeated failures
- **run-recovery** — Detect and auto-recover failed Paperclip heartbeat runs
- **blocker-routing** — Route stuck/blocked agent signals to file, stdout, or webhook
- **task-injection** — Enrich spawn tasks with issue tracking, PR rules, and UX checklists

## License

MIT
