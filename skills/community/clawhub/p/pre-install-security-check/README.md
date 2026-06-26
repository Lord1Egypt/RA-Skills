# 🔒 Security Check

[![ClawHub](https://img.shields.io/badge/ClawHub-pre--install--security--check-blue?logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTIgMkw0IDdWMTJDNCAxNi40MiA3LjU4IDIwIDEyIDIwQzE2LjQyIDIwIDIwIDE2LjQyIDIwIDEyVjdMMTIgMloiIGZpbGw9IndoaXRlIi8+PC9zdmc+)](https://clawhub.com/gawezepobi09-debug/pre-install-security-check)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/gawezepobi09-debug/security-check-skill?style=social)](https://github.com/gawezepobi09-debug/security-check-skill/stargazers)

> **Automated security verification before installing dependencies, cloning repositories, or downloading external code.**

Pre-installation security scanning for GitHub repos, npm packages, PyPI libraries, and shell scripts. Integrates seamlessly with OpenClaw to provide automated risk analysis **before** you execute potentially dangerous commands.

---

## 🎯 Why This Matters

Every `git clone`, `pip install`, or `npm install` is a trust decision. External code can contain:

- 🦠 **Malicious code** — Backdoors, data exfiltration, cryptominers
- 🔓 **Known vulnerabilities** — Unpatched CVEs in dependencies
- 🕸️ **Supply chain attacks** — Compromised maintainer accounts
- 💀 **Abandoned projects** — No security updates for years

**Security Check** automates the verification process inspired by industry tools like [Snyk](https://snyk.io), [Dependabot](https://github.com/dependabot), and [Adyen's Skantek](https://www.adyen.com/blog/skantek).

---

## ✨ Features

- ✅ **Multi-source support** — GitHub, npm, PyPI, direct URLs
- 📊 **Risk scoring** — Threshold-based analysis (Safe/Review/Dangerous)
- 🔍 **Vulnerability detection** — Query CVE databases (Snyk, Safety DB, GitHub Advisory)
- 📈 **Repository metrics** — Stars, forks, activity, maintainer reputation
- 🚦 **Smart confirmations** — Auto-proceed for safe packages, manual approval for risky ones
- 🎯 **Zero false positives** — Conservative thresholds prioritize security over convenience

---

## 🚀 Quick Start

### Installation

```bash
# Install via ClawHub (recommended)
clawhub install pre-install-security-check

# Or clone directly
git clone https://github.com/gawezepobi09-debug/security-check-skill ~/.openclaw/workspace/skills/security-check
```

### Usage

The skill triggers automatically when OpenClaw detects installation commands:

```bash
# Before installation, security check runs automatically:
git clone https://github.com/user/suspicious-repo
# 🔒 Security Check triggered...
# ❌ DANGEROUS: suspicious-repo (Risk: 35)
#   - Last commit: 3 years ago
#   - No license
#   - Open security issues: 3
# Proceed anyway? [y/N]

pip install requests
# ✅ SAFE: requests (Risk: -12)
#   - Downloads: 50M/month
#   - License: Apache 2.0
#   - Known CVEs: 0
# Proceeding...

npm install left-pad@1.0.0
# ⚠️  REVIEW: left-pad (Risk: 8)
#   - CVE-2024-xxxxx: Prototype pollution
#   - Fixed in: v1.0.1
# Install v1.0.1 instead? [Y/n]
```

---

## 📸 Examples

### Safe Package (Auto-proceed)

```
🔒 Security Check: requests (PyPI)

Risk Level: ✅ SAFE

Metrics:
  ✅ Downloads: 50M/month
  ✅ Last release: 2 weeks ago
  ✅ License: Apache 2.0
  ✅ Dependencies: 5
  ✅ Known CVEs: 0

Proceeding with installation...
```

### Risky Repository (Manual Review)

```
🔒 Security Check: suspicious/tool

Risk Level: ❌ DANGEROUS

Metrics:
  ⚠️  Stars: 12 (low popularity)
  ❌ Last commit: 3 years ago
  ❌ Open security issues: 3
  ❌ No license
  ⚠️  Dependencies: 47 (high complexity)

Risk Score: 35

⚠️  This repository shows multiple red flags.
   Consider alternatives or manual code review.

Proceed anyway? [y/N]
```

### Update Recommendation

```
🔒 Security Check: left-pad@1.0.0

Risk Level: ⚠️ REVIEW

Known Issues:
  - CVE-2024-12345 (High severity)
    Prototype pollution vulnerability
    Fixed in: v1.0.1

Recommendation: Install v1.0.1 instead.

Use latest version? [Y/n]
```

---

## 🛠️ How It Works

### 1. Command Detection

Skill monitors for installation commands:
- `git clone <url>`
- `pip install <package>`
- `npm install <package>`
- `curl <url> | bash`

### 2. Source Identification

Determines source type:
- GitHub/GitLab URL → Repository check
- PyPI package → Python package check
- npm package → Node package check
- Direct URL → Script verification

### 3. Security Metrics Collection

**For GitHub repos:**
- ⭐ Stars, forks, watchers
- 📅 Last commit date
- 🐛 Open issues (especially `security` labels)
- 👥 Contributors count
- 📄 License type

**For packages (PyPI/npm):**
- 📦 Downloads per month/week
- 🔄 Release frequency
- 👤 Maintainer reputation
- 🔓 Known CVEs (via Snyk/Safety DB)
- 🕸️ Dependencies count

### 4. Risk Calculation

```python
Risk Score = 0

# Positive signals (reduce risk):
- High stars/downloads: -10
- Recent activity (< 30 days): -5
- Well-known maintainer: -5
- Clear license: -3
- Few dependencies: -5

# Negative signals (increase risk):
- No activity (> 1 year): +15
- No license: +10
- Many dependencies: +5 per 10
- Known CVEs: +20 per CVE
- Suspicious patterns: +25
```

**Risk Levels:**
- `Score < 0` → ✅ **Safe** (auto-proceed)
- `0 ≤ Score < 15` → ⚠️ **Review** (ask confirmation)
- `Score ≥ 15` → ❌ **Dangerous** (strong warning)

### 5. User Confirmation

Based on risk level:
- ✅ Safe → Inform + auto-proceed
- ⚠️ Review → Show summary + ask
- ❌ Dangerous → Block + require manual approval

---

## 🔌 Integration Points

| Service | API Endpoint | Data Retrieved |
|---------|-------------|----------------|
| **GitHub** | `api.github.com/repos/{owner}/{repo}` | Stars, forks, activity, issues |
| **PyPI** | `pypi.org/pypi/{package}/json` | Downloads, releases, maintainers |
| **npm** | `registry.npmjs.org/{package}` | Downloads, dependencies, license |
| **Snyk** | `security.snyk.io` | npm vulnerabilities |
| **Safety DB** | `github.com/pyupio/safety-db` | Python vulnerabilities |
| **GitHub Advisory** | `github.com/advisories` | Cross-platform CVEs |

---

## 📋 Roadmap

- [ ] **Local caching** — Cache risk scores for 24h to reduce API calls
- [ ] **Pattern detection** — Scan code for suspicious patterns (eval, exec, shell commands)
- [ ] **CI/CD integration** — Block deployments with vulnerable dependencies
- [ ] **Custom rules** — User-defined thresholds and blocklists
- [ ] **Reports** — Generate security audit logs

See [open issues](https://github.com/gawezepobi09-debug/security-check-skill/issues) for planned features and discussion.

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** this repository
2. **Create a branch** (`git checkout -b feature/amazing-feature`)
3. **Commit changes** (`git commit -m 'Add amazing feature'`)
4. **Push to branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

Please read our [Contributing Guidelines](CONTRIBUTING.md) (coming soon) for details.

### Development Setup

```bash
# Clone repository
git clone https://github.com/gawezepobi09-debug/security-check-skill
cd security-check-skill

# Install to OpenClaw skills directory (symlink for development)
ln -s $(pwd) ~/.openclaw/workspace/skills/security-check

# Test changes
openclaw agent "Test security check with: pip install requests"
```

---

## 📚 References

This skill is inspired by industry best practices:

- [Snyk](https://snyk.io) — Vulnerability scanning
- [Dependabot](https://github.com/dependabot) — Automated dependency updates
- [Adyen's Skantek](https://www.adyen.com/blog/skantek) — Supply chain security
- [npm audit](https://docs.npmjs.com/cli/v8/commands/npm-audit) — npm security checks
- [pip-audit](https://github.com/pypa/pip-audit) — Python dependency auditing

See `references/` directory for detailed documentation.

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- OpenClaw team for the skills framework
- Security research community for vulnerability databases
- All contributors who help improve this skill

---

## 🔗 Links

- **ClawHub**: https://clawhub.com/gawezepobi09-debug/pre-install-security-check
- **GitHub**: https://github.com/gawezepobi09-debug/security-check-skill
- **Report Issues**: https://github.com/gawezepobi09-debug/security-check-skill/issues
- **OpenClaw Docs**: https://openclaw.com/docs

---

<div align="center">

**⭐ If this skill helps you stay secure, please star the repo!**

Made with 🔒 for OpenClaw by [@gawezepobi09-debug](https://github.com/gawezepobi09-debug)

</div>
