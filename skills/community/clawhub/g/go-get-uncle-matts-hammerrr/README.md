# Go Get Uncle Matt's HAMMERRR

Hardcore Audit of Misleading Models, Evidence Reliability, Runtime, and Reality.

When the repo's story stops matching the system, go get Uncle Matt's HAMMERRR.

## What This Is

`go-get-uncle-matts-hammerrr` is a read-only project-truth audit skill for
Agent Skills compatible clients. It reconciles project claims with reachable
runtime behavior, configuration and deployment reality, tests and executable
proof, and installation, packaging, upgrade, and release behavior.

It is the HAMMERRR-branded successor/variant of the `project-truth-audit`
capability family.

## Public Links

- GitHub: https://github.com/uncmatteth/go-get-uncle-matts-hammerrr
- ClawHub: https://clawhub.ai/uncmatteth/skills/go-get-uncle-matts-hammerrr

## What It Produces

- `PROJECT_TRUTH_AUDIT.md`
- optional `PROJECT_TRUTH_AUDIT.json`
- optional remediation plan, only when explicitly requested

## What It Does Not Do

- modify application source during the audit
- install dependencies by default
- publish, deploy, push, or commit
- reproduce secret values
- claim proof that was not executed or inspected

## Use It For

- stale public claims
- contract drift
- ignored CLI flags or false-success paths
- bypassable safeguards
- missing runtime wiring
- env vars that are documented but never loaded
- release packages that omit claimed artifacts
- tests that do not prove the behavior they are used to justify

## Do Not Use It For

- normal PR review
- style review
- implementation
- isolated debugging
- generic security scanning

## Installation

### Generic Agent Skills Client

Install this folder wherever your client loads skills:

```bash
go-get-uncle-matts-hammerrr/
  SKILL.md
  references/
  templates/
  schemas/
  examples/
```

### Codex Repo-Scoped Skill

From a target repo, link or copy this folder into `.agents/skills/`:

```bash
mkdir -p .agents/skills
ln -s /absolute/path/to/go-get-uncle-matts-hammerrr .agents/skills/go-get-uncle-matts-hammerrr
```

Invoke it explicitly:

```text
$go-get-uncle-matts-hammerrr
```

or:

```text
Go Get Uncle Matt's HAMMERRR
```

Do not rely on implicit activation for generic review, readiness, repo reality,
or truth-audit wording.

### ClawHub

Install from the public ClawHub page:

```text
https://clawhub.ai/uncmatteth/skills/go-get-uncle-matts-hammerrr
```

## Validation

Run:

```bash
python3 quick_validate.py
```

The validator checks the skill frontmatter, required sections, required
reference files, report templates, and JSON schema parseability. It does not
pretend to benchmark model behavior.

## Public Package Boundary

This repository is a skill package, not a Codex plugin. A plugin wrapper should
only be added if distribution needs app integrations, MCP servers, or a plugin
marketplace lifecycle.
