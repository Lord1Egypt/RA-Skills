# licenseguard

<p align="center">
  <img src="https://img.shields.io/badge/ecosystems-8-blue" alt="8 ecosystems">
  <img src="https://img.shields.io/badge/licenses-40+-purple" alt="40+ licenses">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License">
  <img src="https://img.shields.io/badge/install-clawhub-blue" alt="ClawHub">
  <img src="https://img.shields.io/badge/zero-telemetry-brightgreen" alt="Zero telemetry">
</p>

<h3 align="center">Know your licenses before your lawyer does.</h3>

<p align="center">
  <a href="https://licenseguard.pages.dev">Website</a> &middot;
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#supported-ecosystems">Ecosystems</a> &middot;
  <a href="https://licenseguard.pages.dev/#pricing">Pricing</a>
</p>

---

## That GPL dependency you just shipped? Your legal team would like a word.

It starts innocently. A utility library for date formatting. A CSV parser. A markdown renderer. You `npm install` without a second thought.

Three months later, legal discovers you shipped AGPL-3.0 code in your proprietary SaaS product. Now you owe the world your source code -- or you owe your lawyers a lot of billable hours.

**LicenseGuard catches copyleft, viral, and problematic licenses before they create legal risk.** Local scanning. 8 ecosystems. 40+ license patterns. Zero data leaves your machine.

## Quick Start

```bash
# 1. Install via ClawHub (free)
clawhub install licenseguard

# 2. Scan your project
licenseguard scan

# 3. Install pre-commit hooks (Pro)
licenseguard hooks install
```

That's it. Every dependency change is now checked for license compliance.

## What It Does

### Scan dependencies for license risks
One command to scan any manifest file, directory, or your entire project. Detects licenses across npm, Python, Ruby, Go, Java/Kotlin, Rust, PHP, and .NET ecosystems. Classifies every dependency by risk level: Critical (copyleft), High (weak copyleft), Medium (notice required), Low (permissive), or Unknown.

### Block risky licenses with pre-commit hooks
Install a lefthook pre-commit hook that scans every staged manifest file. If a copyleft or viral license is detected, the commit is blocked with a clear explanation and remediation options.

### Generate compliance reports
Produce markdown reports with full dependency inventories, risk breakdowns, and remediation steps. Ideal for legal reviews, compliance audits, and due diligence.

### License compatibility matrix
See which licenses in your dependency tree are compatible with each other -- and which combinations create legal conflicts.

### Enforce approved license lists
Define your organization's approved license list and gate CI/CD on it. Any dependency using an unapproved license fails the check.

### Generate SBOMs
Produce a Software Bill of Materials in CycloneDX-like format. Lists every dependency with its name, version, license, risk level, and source URL. Required for supply chain compliance and regulatory frameworks.

## How It Compares

| Feature | LicenseGuard | FOSSA | Snyk | Mend (WhiteSource) | FOSSology |
|---------|:------------:|:-----:|:----:|:-------------------:|:---------:|
| Local-only (no cloud) | Yes | No | No | No | Yes |
| Pre-commit hooks | Yes | No | No | No | No |
| Zero config scan | Yes | No | Config required | Config required | Complex setup |
| 8 package ecosystems | Yes | Yes | Yes | Yes | Yes |
| SPDX matching | Yes | Yes | Yes | Yes | Yes |
| License text detection | Yes | Yes | Yes | Yes | Yes |
| Compatibility matrix | Yes | Yes | Limited | Yes | No |
| SBOM generation | Yes | Yes | Yes | Yes | Yes |
| Policy enforcement | Yes | Yes | Yes | Yes | Limited |
| Offline license validation | Yes | N/A | N/A | N/A | N/A |
| Zero telemetry | Yes | No | No | No | Yes |
| ClawHub integration | Yes | No | No | No | No |
| Price (individual) | Free/$19/mo | ~$230/mo | $25/dev/mo | Custom pricing | Free (complex) |

## Supported Ecosystems

LicenseGuard scans dependency manifests across 8 package manager ecosystems:

| Ecosystem | Manifest Files | Lock Files |
|-----------|---------------|------------|
| **npm** | package.json | package-lock.json, yarn.lock |
| **Python** | requirements.txt, Pipfile, pyproject.toml, setup.py, setup.cfg | Pipfile.lock |
| **Ruby** | Gemfile | Gemfile.lock |
| **Go** | go.mod | go.sum |
| **Java/Kotlin** | pom.xml, build.gradle, build.gradle.kts | - |
| **Rust** | Cargo.toml | Cargo.lock |
| **PHP** | composer.json | composer.lock |
| **.NET** | *.csproj, packages.config | *.sln |

## License Risk Levels

| Risk | Licenses | What It Means |
|------|----------|---------------|
| **Critical** | GPL-2.0, GPL-3.0, AGPL-3.0, SSPL, EUPL | Your entire application must be open-sourced under the same license |
| **High** | LGPL-2.1, LGPL-3.0, MPL-2.0, EPL-2.0, CDDL | Modifications to the library must be shared; your code stays proprietary if properly isolated |
| **Medium** | Apache-2.0, BSD-2-Clause, BSD-3-Clause, MIT, ISC | Must include copyright notice and license text in distributions |
| **Low** | Unlicense, CC0, WTFPL, 0BSD | Essentially public domain; minimal or no restrictions |
| **Unknown** | NOASSERTION, Custom, Missing | No license found; legally you have NO permission to use the code |

## Pricing

| Feature | Free | Pro ($19/user/mo) | Team ($39/user/mo) |
|---------|:----:|:------------------:|:-------------------:|
| License compliance scan | 5 files | Unlimited | Unlimited |
| 40+ license patterns | Yes | Yes | Yes |
| 8 ecosystem support | Yes | Yes | Yes |
| Compliance score | Yes | Yes | Yes |
| Pre-commit hooks | | Yes | Yes |
| Compliance reports | | Yes | Yes |
| Compatibility matrix | | Yes | Yes |
| Policy enforcement | | | Yes |
| SBOM generation | | | Yes |
| Approved license list | | | Yes |

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "licenseguard": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY",
        "config": {
          "riskThreshold": "high",
          "approvedLicenses": ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC"],
          "excludePackages": ["internal-tools"],
          "excludePatterns": ["**/test-fixtures/**"]
        }
      }
    }
  }
}
```

## Privacy

- 100% local -- no code or dependency data sent externally
- Zero telemetry
- Offline license validation
- No network calls during scanning
- Pattern matching on manifests and license files only

## ClawHub Ecosystem

LicenseGuard is part of the ClawHub developer tools suite:

- **[EnvGuard](https://envguard.pages.dev)** -- Pre-commit secret detection
- **[DepGuard](https://depguard.pages.dev)** -- Dependency health and vulnerability scanning
- **[APIShield](https://apishield.pages.dev)** -- API endpoint security auditing
- **[GitPulse](https://gitpulse.pages.dev)** -- Git workflow analytics
- **[DocSync](https://docsync.pages.dev)** -- Documentation drift detection
- **[LicenseGuard](https://licenseguard.pages.dev)** -- Open source license compliance

## License

MIT
