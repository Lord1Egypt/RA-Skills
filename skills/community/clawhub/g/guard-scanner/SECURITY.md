# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability in guard-scanner itself, please report it responsibly:

1. **Do NOT open a public issue**
2. Use [GitHub Security Advisories](https://github.com/koatora20/guard-scanner/security/advisories/new)
3. Include: affected version, steps to reproduce, potential impact

We will respond within 48 hours and provide a fix within 7 days for critical issues.

## Supported Versions

| Version | Status |
|---------|--------|
| Latest major (`16.x`) | ✅ Supported |
| Older releases | ⚠️ Best effort only |

## Scope

guard-scanner is a **static analysis tool** — it reads files but never executes them. It does not:
- Execute any code from scanned skills
- Make network requests (except optional VirusTotal integration)
- Modify any files in the scan directory
- Require elevated privileges

The only files guard-scanner writes are output reports (`--json`, `--sarif`, `--html`) to the scan directory.

## Supply Chain Security

guard-scanner itself keeps runtime dependencies intentionally small. As of `16.0.1`, it ships with **one runtime dependency** (`ws`) to support the MCP server.

- Small runtime surface area
- No `postinstall` scripts
- SBOM generated in CI/release
- Provenance-enabled npm publish

## Pattern Updates

The threat pattern database (`src/patterns.ts`) and IoC database (`src/ioc-db.ts`) are updated based on:
- Snyk ToxicSkills taxonomy
- OWASP LLM Top 10 & Agentic Security Top 10
- CVE reports affecting AI agents
- Community-reported incidents
- Original research from real-world attacks

## Responsible Disclosure

The test fixtures in `tests/fixtures/malicious-skill/` contain **intentionally malicious patterns** for testing purposes. These files are:
- Clearly marked as test fixtures
- Non-functional (will error if executed)
- Necessary for validating detection capabilities
