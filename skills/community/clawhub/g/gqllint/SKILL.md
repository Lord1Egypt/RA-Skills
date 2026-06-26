---
name: GQLLint
version: 1.0.0
description: "GraphQL anti-pattern & security analyzer -- detects query depth/complexity issues, resolver N+1 problems, over/under fetching, rate limiting & auth gaps, schema design issues, and client query safety problems in GraphQL codebases"
homepage: https://gqllint.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83d\udd78\ufe0f",
      "primaryEnv": "GQLLINT_LICENSE_KEY",
      "requires": {
        "bins": ["git", "bash", "python3", "jq"]
      },
      "configPaths": ["~/.openclaw/openclaw.json"],
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

# GQLLint -- GraphQL Anti-Pattern & Security Analyzer

GQLLint scans codebases for GraphQL anti-patterns: query depth/complexity issues, resolver N+1 problems, over/under fetching, rate limiting & auth gaps, schema design issues, and client query safety problems. It uses regex-based pattern matching against 90 GraphQL-specific patterns across 6 categories, lefthook for git hook integration, and produces markdown reports with actionable remediation guidance. 100% local. Zero telemetry.

**Note:** GQLLint focuses on GraphQL-specific patterns (schema definitions, resolvers, client queries, server configuration). It does NOT analyze general JavaScript/TypeScript quality or REST API patterns.

## Commands

### Free Tier (No license required)

#### `gqllint scan [file|directory]`
One-shot GraphQL quality scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Discovers all source files (skips .git, node_modules, binaries, images, .min.js)
3. Runs 30 GraphQL patterns against each file (free tier limit)
4. Calculates a GraphQL quality score (0-100) per file and overall
5. Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
6. Outputs findings with: file, line number, check ID, severity, description, recommendation
7. Exit code 0 if score >= 70, exit code 1 if GraphQL quality is poor
8. Free tier limited to first 30 patterns (QD + RN categories)

**Example usage scenarios:**
- "Scan my code for GraphQL issues" -> runs `gqllint scan .`
- "Check this file for N+1 resolver problems" -> runs `gqllint scan src/resolvers/`
- "Find query depth vulnerabilities" -> runs `gqllint scan src/`
- "Audit my GraphQL schema" -> runs `gqllint scan .`
- "Check for introspection leaks" -> runs `gqllint scan .`

### Pro Tier ($19/user/month -- requires GQLLINT_LICENSE_KEY)

#### `gqllint scan --tier pro [file|directory]`
Extended scan with 60 patterns covering depth, N+1, fetching, and auth issues.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --tier pro
```

**What it does:**
1. Validates Pro+ license
2. Runs 60 GraphQL patterns (QD, RN, OF, RL categories)
3. Detects over/under fetching and missing pagination
4. Identifies auth gaps, rate limiting issues, and open playgrounds
5. Full category breakdown reporting

#### `gqllint scan --format json [directory]`
Generate JSON output for CI/CD integration.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format json
```

#### `gqllint scan --format html [directory]`
Generate HTML report for browser viewing.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format html
```

#### `gqllint scan --category RN [directory]`
Filter scan to a specific check category (QD, RN, OF, RL, SD, CQ).

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --category RN
```

### Team Tier ($39/user/month -- requires GQLLINT_LICENSE_KEY with team tier)

#### `gqllint scan --tier team [directory]`
Full scan with all 90 patterns across all 6 categories including schema design and client safety.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --tier team
```

**What it does:**
1. Validates Team+ license
2. Runs all 90 patterns across 6 categories
3. Includes schema design checks (input types, naming, JSON scalars, deprecation)
4. Includes client query safety (injection, error handling, caching, codegen)
5. Full category breakdown with per-file results

#### `gqllint scan --verbose [directory]`
Verbose output showing every matched line and pattern details.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --verbose
```

#### `gqllint status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" status
```

#### `gqllint patterns`
List all available detection patterns with IDs, severities, and descriptions.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" patterns
```

## Check Categories

GQLLint detects 90 GraphQL anti-patterns across 6 categories:

| Category | Code | Patterns | Description | Severity Range |
|----------|------|----------|-------------|----------------|
| **Query Depth & Complexity** | QD | 15 | Unbounded depth, no complexity limit, introspection leak, recursive fragments | low -- critical |
| **Resolver N+1** | RN | 15 | Database calls in loops, no DataLoader, sequential awaits, missing batching | low -- critical |
| **Over/Under Fetching** | OF | 15 | SELECT *, no pagination, eager loading, missing projections, full object returns | low -- critical |
| **Rate Limiting & Auth** | RL | 15 | No auth on mutations, open playground, missing rate limit, no CORS, no persisted queries | low -- critical |
| **Schema Design** | SD | 15 | Raw scalars in mutations, no input types, JSON scalar, naming issues, no deprecation | low -- high |
| **Client Query Safety** | CQ | 15 | String concatenation, template injection, no error handling, missing variables, no codegen | low -- critical |

## Tier-Based Pattern Access

| Tier | Patterns | Categories |
|------|----------|------------|
| **Free** | 30 | QD, RN |
| **Pro** | 60 | QD, RN, OF, RL |
| **Team** | 90 | QD, RN, OF, RL, SD, CQ |
| **Enterprise** | 90 | QD, RN, OF, RL, SD, CQ + priority support |

## Scoring

GQLLint uses a deductive scoring system starting at 100 (perfect):

| Severity | Point Deduction | Description |
|----------|-----------------|-------------|
| **Critical** | -25 per finding | Severe risk (query injection, N+1 loops, introspection leak, unauth mutations) |
| **High** | -15 per finding | Significant problem (no depth limit, no pagination, open playground, resolver waterfalls) |
| **Medium** | -8 per finding | Moderate concern (schema design gaps, missing rate limits, over-fetching) |
| **Low** | -3 per finding | Informational / best practice suggestion |

### Grading Scale

| Grade | Score Range | Meaning |
|-------|-------------|---------|
| **A** | 90-100 | Excellent GraphQL quality |
| **B** | 80-89 | Good GraphQL with minor issues |
| **C** | 70-79 | Acceptable but needs improvement |
| **D** | 60-69 | Poor GraphQL quality |
| **F** | Below 60 | Critical GraphQL problems |

- **Pass threshold:** 70 (Grade C or better)
- Exit code 0 = pass (score >= 70)
- Exit code 1 = fail (score < 70)

## Configuration

Users can configure GQLLint in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "gqllint": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "medium",
          "ignorePatterns": ["**/test/**", "**/fixtures/**", "**/*.test.*"],
          "ignoreChecks": [],
          "reportFormat": "text"
        }
      }
    }
  }
}
```

## Important Notes

- **Free tier** works immediately with no configuration
- **All scanning happens locally** -- no code is sent to external servers
- **License validation is offline** -- no phone-home or network calls
- Pattern matching only -- no AST parsing, no external dependencies beyond bash
- Supports scanning all file types in a single pass
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = pass (score >= 70), 1 = fail (for CI/CD integration)
- Output formats: text (default), json, html

## Error Handling

- If lefthook is not installed and user tries hooks, prompt to install it
- If license key is invalid or expired, show clear message with link to https://gqllint.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable files found in target, report clean scan with info message
- If an invalid category is specified with --category, show available categories

## When to Use GQLLint

The user might say things like:
- "Scan my code for GraphQL issues"
- "Check my resolvers for N+1 problems"
- "Find query depth vulnerabilities"
- "Detect over-fetching in my GraphQL API"
- "Are there any auth gaps in my GraphQL schema?"
- "Check if introspection is enabled in production"
- "Audit my GraphQL schema design"
- "Find security issues in my GraphQL setup"
- "Check for query injection vulnerabilities"
- "Scan for missing pagination on list fields"
- "Run a GraphQL quality audit"
- "Generate a GraphQL health report"
- "Check if my resolvers use DataLoader"
- "Find N+1 database query patterns"
- "Check my client code for unsafe GraphQL patterns"
