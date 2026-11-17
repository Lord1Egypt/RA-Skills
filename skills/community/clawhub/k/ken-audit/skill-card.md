## Description:

Audit the whole repo for Thompson-mode violations and produce a ranked list of what to rewrite, delete, or take back into the trusted base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rajnandan1](https://clawhub.ai/user/rajnandan1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to audit an entire repository for Thompson-mode simplification opportunities and receive ranked rewrite, deletion, or trusted-base reduction recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce broad rewrite or deletion recommendations after reading repository contents and git history.

Mitigation: Review each finding before acting, especially before changing architecture, deleting layers, or removing dependencies.

Risk: Correctness bugs, security holes, and performance issues are outside the skill's stated audit scope.

Mitigation: Use a normal review or security pass for those concerns rather than relying on this skill's output.

## Reference(s):

- [Project homepage](https://github.com/rajnandan1/ken)
- [ClawHub skill page](https://clawhub.ai/rajnandan1/skills/ken-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown lines with ranked findings and a final net summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lists findings only and does not apply repository changes.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
