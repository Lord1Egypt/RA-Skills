## Description:

A checklist and pattern library for hardening tool-using agents against prompt injection from web pages, files, emails and tool outputs. Use when building or reviewing any agent that reads untrusted content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manteclaw](https://clawhub.ai/user/manteclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent designers use this skill to map where untrusted content enters an agent workflow, classify that content, and apply and review defenses against prompt injection and unauthorized side effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying general guardrails without adapting them to the workflow could leave trust boundaries or consequential actions unprotected.

Mitigation: Map the guidance to the actual workflow, review proposed controls, and test with a harmless canary before deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/manteclaw/skills/prompt-injection-guardrails)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown hardening report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports trust boundaries, observed patterns, defenses, and a canary test result.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
