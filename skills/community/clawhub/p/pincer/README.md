# pincer 🛡️

Security-first wrapper for installing agent skills. Scans for malware, prompt injection, and suspicious patterns before installation.

## Why?

Agent skills are powerful — they're basically executable documentation. The ClawHub ecosystem has already seen [malware campaigns](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/) distributing infostealers via innocent-looking skills. pincer adds a security layer.

## Quick Start

```bash
# Install
clawhub install pincer

# Use instead of clawhub install
pincer install some-skill

# Scan without installing
pincer scan suspicious-skill

# Audit all installed skills
pincer audit
```

## Features

- **Pre-install scanning** — Analyze skills before they touch your system
- **mcp-scan integration** — Leverages [Invariant Labs' mcp-scan](https://github.com/invariantlabs-ai/mcp-scan) for prompt injection and malware detection
- **Pattern detection** — Base64 payloads, `curl | sh`, quarantine removal, and more
- **Publisher trust** — Maintain lists of trusted and blocked publishers
- **Audit mode** — Quick-scan all installed skills
- **JSON output** — Scriptable for CI/CD integration
- **Install logging** — Track what you've installed and when

## Documentation

See [SKILL.md](./SKILL.md) for full documentation.

## License

MIT

## Credits

- [mcp-scan](https://github.com/invariantlabs-ai/mcp-scan) by Invariant Labs
- [1Password Security Research](https://1password.com/blog/from-magic-to-malware-how-openclaws-agent-skills-become-an-attack-surface)
- [Snyk ToxicSkills Report](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
