## Description:

Enforces validation and evidence before claiming work complete. Use before declaring implementation done, creating a PR, or submitting deliverables for review

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software agents use this skill to verify implementation work against acceptance criteria and produce reproducible evidence before reporting completion or submitting deliverables for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a suspicious verdict with medium confidence and incomplete analysis of one referenced file.

Mitigation: Review the skill contents and available scan details before installation, and use an isolated environment when evaluating it.

Risk: The security guidance flags mutable package execution and global installation.

Mitigation: Review package commands before running them; prefer pinned versions and local or isolated installs where applicable.

Risk: Evidence logs may contain sensitive information.

Mitigation: Check and redact credentials or other sensitive values before saving or sharing evidence.

Risk: A referenced command can rewrite Git history.

Mitigation: Inspect the command and its target repository state before execution, and preserve a recoverable copy of important work.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-imbue-proof-of-work)
- [Project homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/imbue)
- [Acceptance criteria best practices](https://www.atlassian.com/agile/project-management/definition-of-done)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with checklists, evidence references, and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Variable detail based on the task and available verification evidence.]

## Skill Version(s):

1.10.4 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
