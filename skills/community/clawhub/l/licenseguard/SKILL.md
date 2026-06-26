---
name: licenseguard
description: Open source license compliance scanner — catches copyleft, viral, and problematic licenses in your dependencies before they create legal risk
homepage: https://licenseguard.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83d\udcdc",
      "primaryEnv": "LICENSEGUARD_LICENSE_KEY",
      "requires": {
        "bins": ["git", "bash"]
      },
      "install": [
        {
          "id": "lefthook",
          "kind": "brew",
          "formula": "lefthook",
          "bins": ["lefthook"],
          "label": "Install lefthook (git hooks manager)"
        }
      ],
      "os": ["darwin", "linux", "win32"]
    }
  }
user-invocable: true
disable-model-invocation: false
---

# LicenseGuard -- Open Source License Compliance Scanner

LicenseGuard scans your dependency manifests for copyleft, viral, and problematic open source licenses before they create legal risk. It detects license declarations across 8 package manager ecosystems (npm, Python, Ruby, Go, Java/Kotlin, Rust, PHP, .NET), classifies risk levels from Critical (copyleft/viral) to Low (permissive), and produces compliance reports with compatibility matrices. All scanning happens locally using pattern matching on manifest files and license text -- no code or dependency data is sent externally.

## Commands

### Free Tier (No license required)

#### `licenseguard scan [file|directory]`
One-shot license compliance scan of dependency manifests.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/licenseguard.sh" scan [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Auto-detects package managers in use (npm, Python, Ruby, Go, Java, Rust, PHP, .NET)
3. Finds all dependency manifest files (package.json, go.mod, Cargo.toml, pom.xml, etc.)
4. Parses declared licenses from manifests and lock files
5. Searches for LICENSE/COPYING/NOTICE files in dependency directories
6. Matches SPDX license identifiers and common license text patterns
7. Classifies each dependency license by risk level (Critical/High/Medium/Low/Unknown)
8. Flags dependencies with NO declared license (unknown risk)
9. Flags dual-licensed packages where one option is copyleft
10. Calculates a compliance score (0-100)
11. Free tier: limited to scanning up to 5 manifest files
12. Exit code 0 if score >= 70, exit code 1 if score < 70 or critical issues found

**Example usage scenarios:**
- "Scan my project for license issues" -> runs `licenseguard scan .`
- "Check if my dependencies have copyleft licenses" -> runs `licenseguard scan .`
- "Are my npm packages license-compliant?" -> runs `licenseguard scan package.json`
- "Audit the licenses in this Go module" -> runs `licenseguard scan go.mod`
- "What licenses are in my Rust dependencies?" -> runs `licenseguard scan Cargo.toml`

### Pro Tier ($19/user/month -- requires LICENSEGUARD_LICENSE_KEY)

#### `licenseguard scan [file|directory]` (unlimited)
Full license compliance scan with no manifest file limit.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/licenseguard.sh" scan [target]
```

**What it does (beyond free):**
1. Unlimited manifest file scanning
2. Deep license text pattern matching (GPL boilerplate, MIT text, Apache notice)
3. Dual-license detection and risk assessment
4. Detailed remediation advice per finding

#### `licenseguard hooks install`
Install git pre-commit hooks that scan dependency manifests for license issues before every commit.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/licenseguard.sh" hooks install
```

**What it does:**
1. Validates Pro+ license
2. Copies lefthook config to project root
3. Installs lefthook pre-commit hook
4. On every commit: scans staged manifest files for license issues, blocks commit if copyleft/viral licenses detected

#### `licenseguard hooks uninstall`
Remove LicenseGuard git hooks.

```bash
bash "<SKILL_DIR>/scripts/licenseguard.sh" hooks uninstall
```

#### `licenseguard report [directory]`
Generate a full markdown license compliance report.

```bash
bash "<SKILL_DIR>/scripts/licenseguard.sh" report [directory]
```

**What it does:**
1. Validates Pro+ license
2. Runs full scan of the directory
3. Generates a formatted markdown report with risk breakdown
4. Includes per-dependency findings, compliance score, and remediation steps
5. Lists all dependencies grouped by risk level
6. Output written to LICENSEGUARD-REPORT.md

#### `licenseguard matrix [directory]`
Generate a license compatibility matrix.

```bash
bash "<SKILL_DIR>/scripts/licenseguard.sh" matrix [directory]
```

**What it does:**
1. Validates Pro+ license
2. Discovers all unique licenses in the project dependencies
3. Produces a compatibility matrix showing which licenses can be combined
4. Flags incompatible license combinations (e.g., GPL + proprietary)
5. Helps with license selection for your own project

### Team Tier ($39/user/month -- requires LICENSEGUARD_LICENSE_KEY with team tier)

#### `licenseguard policy [directory]`
Enforce an approved license list.

```bash
bash "<SKILL_DIR>/scripts/licenseguard.sh" policy [directory]
```

**What it does:**
1. Validates Team+ license
2. Loads approved license list from ~/.openclaw/openclaw.json (licenseguard.config.approvedLicenses)
3. Scans all dependencies and flags any using a license NOT on the approved list
4. Produces a pass/fail report for CI/CD gating
5. Exit code 0 if all dependencies use approved licenses, 1 otherwise

#### `licenseguard sbom [directory]`
Generate a Software Bill of Materials (SBOM).

```bash
bash "<SKILL_DIR>/scripts/licenseguard.sh" sbom [directory]
```

**What it does:**
1. Validates Team+ license
2. Discovers all dependencies across all package managers
3. Generates a CycloneDX-like SBOM in JSON and markdown formats
4. Includes: package name, version, license, risk level, source URL
5. Suitable for compliance audits, supply chain security, and regulatory requirements
6. Output written to LICENSEGUARD-SBOM.json and LICENSEGUARD-SBOM.md

## License Risk Categories

LicenseGuard classifies open source licenses into five risk levels:

| Risk Level | Licenses | Impact |
|------------|----------|--------|
| **Critical (Copyleft/Viral)** | GPL-2.0, GPL-3.0, AGPL-3.0, SSPL, EUPL | Must open-source your code |
| **High (Weak Copyleft)** | LGPL-2.1, LGPL-3.0, MPL-2.0, EPL-2.0, CDDL | Must share modifications to the library |
| **Medium (Notice Required)** | Apache-2.0, BSD-2-Clause, BSD-3-Clause, MIT, ISC | Must include license notice |
| **Low (Permissive)** | Unlicense, CC0, WTFPL, 0BSD | Minimal restrictions |
| **Unknown** | NOASSERTION, Custom, Missing | Cannot determine risk -- review manually |

## Supported Package Managers

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

## Detection Methods

1. **Manifest parsing** -- Extract declared licenses from package manager files
2. **License file scanning** -- Search for LICENSE, COPYING, NOTICE files in dependency directories
3. **SPDX matching** -- Match SPDX license identifiers (MIT, Apache-2.0, GPL-3.0-only, etc.)
4. **Text pattern matching** -- Detect common license boilerplate (GPL preamble, MIT text, Apache notice)
5. **Missing license detection** -- Flag dependencies with no license declaration
6. **Dual-license detection** -- Identify packages offering multiple license options (OR expressions)

## Configuration

Users can configure LicenseGuard in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "licenseguard": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "riskThreshold": "high",
          "approvedLicenses": ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC"],
          "excludePackages": [],
          "excludePatterns": ["**/node_modules/**", "**/vendor/**"],
          "reportFormat": "markdown"
        }
      }
    }
  }
}
```

## Important Notes

- **Free tier** works immediately with no configuration (limited to 5 manifest files)
- **All scanning happens locally** -- no code or dependency data is sent to external servers
- **License validation is offline** -- no phone-home or network calls
- **Zero telemetry** -- no usage data, analytics, or tracking
- Pattern matching on manifests + license files, no network calls during scanning
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = compliant (score >= 70), 1 = issues found (for CI/CD integration)
- Compliance score calculation: starts at 100, deducts points per risk level (Critical: -15, High: -10, Medium: -3, Unknown: -8)

## Error Handling

- If lefthook is not installed and user tries `hooks install`, prompt to install it
- If license key is invalid or expired, show clear message with link to https://licenseguard.pages.dev/renew
- If a manifest file cannot be parsed, warn and continue with other files
- If no manifest files found in target, report clean scan with info message
- If package manager is not recognized, skip with a warning

## When to Use LicenseGuard

The user might say things like:
- "Scan for license issues in my dependencies"
- "Check if any of my packages use GPL"
- "Are my npm dependencies license-compliant?"
- "Find copyleft licenses in this project"
- "Generate a license compliance report"
- "Set up license checking on my commits"
- "Create an SBOM for this project"
- "What licenses are my Go dependencies using?"
- "Check license compatibility"
- "Enforce our approved license list"
- "Are there any viral licenses in my Rust crates?"
- "Scan my Python requirements for problematic licenses"
