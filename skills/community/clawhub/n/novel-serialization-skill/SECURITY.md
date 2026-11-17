# Security Policy

## GitHub Novel Serialization Skill

## Supported Versions

This table lists the release lines that currently receive security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.3.x   | :white_check_mark:  |
| 1.2.x   | :warning:  security fixes only |
| < 1.2   | :x:                |

The same information is published in machine-readable form in
[security.txt](security.txt) (RFC 9116) for tooling that crawls repositories.

### End-of-Life (EOL) Policy

- **Active support**: Only the latest minor release within a supported major version receives security updates.
- **Security-only updates**: Previous minor versions within a supported major version may receive critical security fixes only.
- **End of life**: When a major version reaches EOL, all security support ceases immediately. Users must upgrade to a supported version.
- **Deprecation notice**: Major versions scheduled for EOL will receive a deprecation notice at least 90 days before the end-of-life date.

## Reporting a Vulnerability

We take the security of **GitHub Novel Serialization Skill** seriously. If you discover a security
vulnerability, please follow these steps:

### 1. Do NOT open a public GitHub issue

Security vulnerabilities should **never** be reported in public issues, as
this could expose users to risk before a fix is available.

### 2. Report via private channel

Report privately through the repository's
[Security Advisory form](https://github.com/JohnSmithfan/github-novel-serialization-skill/security/advisories/new) —
GitHub's private reporting channel to the maintainer. **Never** open a public
issue for a vulnerability.

Title the report `[SECURITY] <brief description>`.

### 3. Include the following information

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact assessment
- Your suggested fix (if any)
- Your contact information for follow-up

### 4. What to expect

- **Acknowledgment**: We will acknowledge receipt of your report within **48 hours**
- **Assessment**: We will assess the vulnerability and provide an initial response within **5 business days**
- **Fix timeline**: See the [Vulnerability Response Timeline](#vulnerability-response-timeline) below
- **Disclosure**: We will coordinate with you on public disclosure timing
- **Credit**: We will credit reporters in our security advisories (unless you prefer anonymity)

### Vulnerability Response Timeline

| Severity | Description | Fix Timeline | Communication |
|----------|-------------|--------------|---------------|
| Critical | Remote code execution, data breach, authentication bypass | Within 30 days | Immediate notification to all users |
| High | Significant security degradation, privilege escalation | Within 7 days | Notification via security advisory |
| Medium | Moderate security impact, limited exploitation path | Within 30 days | Included in next scheduled release |
| Low | Minimal security impact, theoretical risk | Within 90 days | Included in next scheduled release |

## Security Best Practices for Contributors

When contributing to this project, please adhere to the following security
guidelines:

### Code Security

- **Input validation**: Always validate and sanitize user-provided input, especially
  in prompt templates that may be pasted into AI chat interfaces
- **Secrets management**: Never commit API keys, tokens, passwords, or other
  secrets to the repository. Use environment variables or secret management tools
- **Dependency review**: Review third-party dependencies for known vulnerabilities
  before adding them to the project. Use the following tools:
  - `pip-audit` for Python dependencies: `pip audit`
  - `npm audit` for JavaScript dependencies
  - GitHub Dependabot (automated, enabled by default)
  - `safety check` for Python package vulnerabilities

### Prompt Security

Since this project involves AI prompt templates, be mindful of:

- **Prompt injection**: Design prompts to be resilient against injection attempts.
  Validate and sanitize any user-supplied content before it enters the prompt context.
- **Output sanitization**: Ensure generated content doesn't contain sensitive data
  such as API keys, personal information, or internal project details.
- **Rate limiting**: Be aware of API rate limits when using AI tools programmatically.
  Implement appropriate retry logic and backoff strategies.

### Infrastructure Security

- **GitHub Actions**: Keep workflow files up to date and review permissions.
  Pin action versions to specific commits to prevent supply chain attacks.
- **Dependabot**: Enable Dependabot for automated dependency updates.
  Configure both version updates and security updates.
- **Branch protection**: Enable branch protection rules for main/master branches.
  Require pull request reviews and status checks before merging.
- **Code scanning**: Enable GitHub Code Scanning if available.
  Configure secret scanning to detect accidentally committed secrets.

## Security-Related Configuration Files

The following files should be treated as security-sensitive:

| File | Purpose | Notes |
|------|---------|-------|
| `.github/workflows/*.yml` | CI/CD pipelines | Review for secret exposure |
| `.github/dependabot.yml` | Dependency updates | Configure update schedule |
| `.github/FUNDING.yml` | Funding information | Public-facing |
| `.gitignore` | Git ignore rules | Ensure no secrets are tracked |
| `.editorconfig` | Editor configuration | Code style enforcement |

## Security Advisory Policy

When a security vulnerability is fixed:

1. A security advisory will be created on GitHub
2. Affected versions will be patched and new versions released
3. Users will be notified via GitHub security notifications
4. The advisory will be published after a fix is available

## License and Security

Remember that this project uses dual licensing:

- **GPL-3.0** covers all infrastructure code and templates
- **CC BY-NC-SA 4.0** covers generated novel content

Security fixes to infrastructure components must maintain GPL-3.0 compliance.
Any security-related changes to novel content generation prompts should also
consider the CC BY-NC-SA 4.0 license terms.

---

Thank you for helping keep **GitHub Novel Serialization Skill** secure.
