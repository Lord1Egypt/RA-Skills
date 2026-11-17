## Description:

Use the OOMOL-connected oo CLI to read Gitee account and repository information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill with an OOMOL-connected Gitee account to inspect the current user profile and repositories visible to that account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run remote CLI installers whose behavior was not inspected.

Mitigation: Review and install a specific CLI version yourself, and require approval before downloading or executing installers; check the Gitee permissions granted and whether setup adds agent skills.

## Reference(s):

- [Gitee API documentation](https://gitee.com/api/v5/swagger)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Gitee](https://gitee.com)
- [Gitee skill on ClawHub](https://clawhub.ai/oomol/skills/oo-gitee)

## Skill Output:

**Output Type(s):** [Text, API Calls]

**Output Format:** [Text returned from Gitee connector actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns account or repository information for read-only actions.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
