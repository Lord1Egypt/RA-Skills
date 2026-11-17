## Description:

Defines the contract for deferred-item capture across plugins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and plugin maintainers use this skill to build or validate deferred-capture wrappers, source labels, and issue templates across plugins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wrappers built from this contract may publish verbatim context, absolute paths, session IDs, or other sensitive metadata into GitHub issues.

Mitigation: Review wrappers before use, redact secrets and sensitive metadata, preview issue bodies, and require confirmation before creating issues.

Risk: Issue creation in public repositories may expose private or customer work if wrapper safeguards are missing.

Mitigation: Use dry-run output for review first and avoid using wrappers on private or customer work until redaction and confirmation behavior are verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-deferred-capture)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with CLI examples and JSON output conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defines a contract; conforming wrappers may create GitHub issues or emit dry-run JSON.]

## Skill Version(s):

1.9.19 (source: server release metadata; artifact frontmatter says 1.9.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
