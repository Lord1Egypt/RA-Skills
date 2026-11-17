## Description:

Drimify (drimify.com). Use this skill for ANY Drimify request — searching and reading data. Whenever a task involves Drimify, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to search and read Drimify app data collections through an OOMOL-connected account, using the oo CLI to inspect action schemas and retrieve records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup helper can install persistent skills into other agents, a broader change than this skill explains.

Mitigation: Review the helper's persistent changes before setup; use a separately verified oo CLI installation and set OO_SKILLS_SYNC_DISABLED=1 if additional agent skills are unwanted.

## Reference(s):

- [Drimify API data structure documentation](https://help.drimify.com/en/article/api-data-structure-1ykdmtj/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Drimify](https://drimify.com)
- [Drimify skill release](https://clawhub.ai/oomol/skills/oo-drimify)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON records returned by Drimify actions, with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
