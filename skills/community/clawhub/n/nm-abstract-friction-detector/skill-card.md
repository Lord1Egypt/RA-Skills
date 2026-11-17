## Description:

Detect friction signals; graduate patterns into rules. Use for session retrospectives

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use it during session retrospectives to identify recurring corrections, failures, retries, and other friction signals. It summarizes patterns for review and possible promotion into durable guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A referenced document was missing from the inspected artifact, so the security review may not cover all linked details.

Mitigation: Consult the complete release documentation and verify any document-dependent assumptions before adopting the guidance.

Risk: Recurring patterns can be written to persistent friction logs and LEARNINGS.md, where inaccurate signals could become durable guidance.

Mitigation: Review generated signals and LEARNINGS.md changes before relying on them; assess Tier 3 proposals before approving any permanent rule.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-abstract-friction-detector)
- [Clawdis homepage link](https://github.com/athola/claude-night-market/tree/master/plugins/abstract)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Markdown friction reports and JSON session records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes weighted signals, recurring patterns, and graduation proposals.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
