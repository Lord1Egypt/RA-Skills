## Description:

Routes users to ten LGD audit nodes, reports their availability, and provides call guidance; it does not perform the audits itself.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI governance reviewers can use this skill to find the appropriate LGD audit node, check which nodes are available in the current installation, and get routing guidance. The specialized audit work is performed by the selected subskill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags environment capability and subprocess concerns; verification can optionally execute local child-skill help scripts, and the scan is partial because three local references could not be resolved.

Mitigation: Review the local child skills and paths before installation, use presence checks unless execution is needed, and resolve the missing references before relying on the security assessment.

## Reference(s):

- [LGD Skills Index](https://zhaoxinghua09-cell.github.io/lgd-skills-index/)
- [ClawHub release page](https://clawhub.ai/zhaoxinghua09-cell/skills/lgd-audit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON]

**Output Format:** [Text or Markdown guidance, with optional JSON availability evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Availability reflects the local installation; the dispatcher routes to specialized audit skills rather than performing audits itself.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
