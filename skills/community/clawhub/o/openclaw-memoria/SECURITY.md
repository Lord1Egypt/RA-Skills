# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 3.4.x   | ✅ Active |
| 3.0.x - 3.3.x | ⚠️ Critical fixes only |
| < 3.0   | ❌ Not supported |

## Reporting a Vulnerability

If you discover a security vulnerability in Memoria, please **do not open a public issue**.

Instead, email us at: **contact@primo-studio.fr**

Include:
- Description of the vulnerability
- Steps to reproduce
- Impact assessment
- Suggested fix (if any)

We will respond within **48 hours** and aim to release a fix within **7 days** for critical issues.

## Security Considerations

### Data Storage
- All data is stored **locally** in SQLite (`memoria.db`) — no cloud sync by default
- API keys in config are **never** sent to third parties (only to the configured LLM providers)
- The `.md` sync files may contain extracted facts — treat your workspace as sensitive

### LLM Provider Security
- Fact extraction sends conversation content to your configured LLM (Ollama = 100% local)
- If using cloud providers (OpenAI, Anthropic), conversation data leaves your machine
- Use `fallback` config carefully — ensure only trusted providers are listed

### Best Practices
- **Never commit API keys** — use environment variables (`OPENAI_API_KEY`)
- **Restrict workspace permissions** — `memoria.db` contains all your agent's memory
- **Backup regularly** — `cp memoria.db memoria.db.bak` (or use `VACUUM INTO`)
- **Review .md sync output** — ensure no sensitive data leaks into shared files

## Disclosure Policy

We follow responsible disclosure. Security researchers who report valid vulnerabilities will be credited in the release notes (unless they prefer to remain anonymous).
