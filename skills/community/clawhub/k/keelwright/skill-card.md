## Description:

Keelwright is a runtime-agnostic coding-safety skill for AI-assisted development sessions, combining autonomous loop controls, machine-enforced safety gates, an autonomy dial, and plain-language reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ratingtesting](https://clawhub.ai/user/ratingtesting)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, builders, and non-developers using coding agents load Keelwright before loop coding, autonomous runs, or risky commits to catch security, quality, package, and runaway-loop failures with file-backed checks and escalation rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad authority over files, shell commands, git operations, and network checks when used in a repository.

Mitigation: Review the skill before installing and use it only in repositories where that authority is acceptable.

Risk: The companion plugin and verifier behavior should be reviewed before enabling.

Mitigation: Enable the companion plugin only after review, and pin or otherwise verify the plugin path before running web-guard verification from writable or untrusted parent directories.

Risk: Autonomous operation can affect sensitive code paths such as auth, payments, production, or data handling.

Mitigation: Prefer Copilot or Checkpoint mode for sensitive work and require explicit approval for blockers and irreversible actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ratingtesting/skills/keelwright)
- [ratingtesting publisher profile](https://clawhub.ai/user/ratingtesting)
- [Author profile from ClawHub metadata](https://github.com/ratingtesting)
- [README](README.md)
- [ADR-001 layered skill](docs/ADR-001-layered-skill.md)
- [Security gates](references/security-gates.md)
- [Risk glossary](references/risk-glossary.md)
- [Circuit breaker](references/circuit-breaker.md)
- [Web guard](references/web-guard.md)
- [QA results](qa-results/README.md)
- [Provenance notes](references/provenance.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, file paths, configuration snippets, and plain-language status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request explicit operator approval for bootstrap files, optional tooling, irreversible actions, and high-risk blockers.]

## Skill Version(s):

1.11.0 (source: ClawHub release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
