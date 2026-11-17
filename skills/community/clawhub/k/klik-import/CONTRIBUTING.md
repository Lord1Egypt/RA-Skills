# Contributing

Thanks for your interest in improving klik-import.

## Setup

```bash
git clone https://github.com/minervacap2022/klik-import-skill
cd klik-import-skill
npm install
```

## Workflow

1. Create a branch from `master`
2. Make your changes
3. Run `npm test` and `npm run lint`
4. Open a PR with a clear description

## Guidelines

- Keep it simple — this is a single-purpose tool
- Zero production dependencies — everything uses `node:*` built-ins
- Tests use Node's built-in test runner (`node --test`)
- Follow the existing code style (TypeScript strict mode, ESM)

## Reporting Issues

Open an issue on GitHub. Include:
- Your Node version (`node --version`)
- Your agent (Claude Code, OpenClaw, Hermes, etc.)
- The error message or unexpected behavior
