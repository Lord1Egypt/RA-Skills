## Description:

Lint AI agent instruction files (SKILL.md, CLAUDE.md, AGENTS.md, GEMINI.md), tool definitions, system prompts, and agent configs with the deterministic LintLang CLI. Use when writing, editing, or reviewing agent instructions to catch ambiguous tool descriptions, missing stop conditions, schema/description mismatches, mixed output formats, or prompts embedded in Python before they reach runtime. Zero-LLM static analysis; no model calls and no network calls during a scan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roli-lpci](https://clawhub.ai/user/roli-lpci)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent authors use LintLang to review explicitly selected agent instruction files, tool definitions, prompts, and configurations for structural issues before deployment. It provides deterministic local linting without making model calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetching the pinned CLI requires network access and executes third-party software locally.

Mitigation: Review the pinned package before installation; scans run offline once the CLI is available.

Risk: A passing lint result could be mistaken for proof that an agent is secure.

Mitigation: Treat findings as structural checks only and perform a separate security review.

## Reference(s):

- [LintLang source repository](https://github.com/hermes-labs-ai/lintlang)
- [LintLang on ClawHub](https://clawhub.ai/roli-lpci/skills/lintlang)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text]

**Output Format:** [JSON or human-readable lint findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic structural analysis; scans run offline once the CLI is installed.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
