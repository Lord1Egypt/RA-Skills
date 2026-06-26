# Contributing to SOUL Backup

Thank you for considering contributing to SOUL Backup! This document provides guidelines for contributing.

## How to Contribute

### Reporting Bugs

- Check existing issues first
- Include steps to reproduce
- Provide system info (OS, Node.js version)
- Include error messages and logs

### Suggesting Features

- Open an issue with the `enhancement` label
- Describe the use case
- Explain why it would be useful

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Run validation: `node scripts/validate.mjs`
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

### Code Style

- Use ES modules (`.mjs`)
- Follow existing code patterns
- Add comments for complex logic
- Keep functions focused and small

### Testing

- Test on macOS, Linux, and Windows (WSL)
- Verify backup/restore cycle
- Check sanitization of openclaw.json
- Validate error handling

## Development Setup

```bash
git clone https://github.com/YOUR-USERNAME/soul-backup.git
cd soul-backup
chmod +x scripts/*.mjs
node scripts/backup.mjs --name test
node scripts/validate.mjs
node scripts/restore.mjs --name test --dry-run
```

## Questions?

Open an issue or join the OpenClaw Discord: https://discord.com/invite/clawd
