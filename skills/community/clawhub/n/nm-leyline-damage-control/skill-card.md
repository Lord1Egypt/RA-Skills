## Description:

Recovers broken agent state via crash recovery, context overflow, and merge conflict protocols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent orchestrators use this skill to recover work after crashes, context loss, merge conflicts, or inconsistent task and file state. It also provides a risk checklist for Level 1 and higher tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks this release suspicious because its recovery instructions may be disruptive and part of the referenced material was only partially inspected.

Mitigation: Review the recovery instructions and fully inspect the partially inspected module before installation; the suspicious verdict is not a finding of malicious intent.

## Reference(s):

- [Declared project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-leyline-damage-control)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Step-by-step recovery procedures and checklists.]

## Skill Version(s):

1.10.3 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
