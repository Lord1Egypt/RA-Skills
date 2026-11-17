## Description:

JobNimbus (jobnimbus.com). Use this skill for ANY JobNimbus request — reading, creating, and updating data. Whenever a task involves JobNimbus, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

JobNimbus users use this agent skill to read, create, and update contacts and jobs through an OOMOL-connected account. It provides schema-guided connector actions and requires confirmation before writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup can run software from an external download source.

Mitigation: Install and review a known CLI release yourself before using the skill.

Risk: The OOMOL connection mediates access to JobNimbus data, and create or update actions can change records.

Mitigation: Review the exact payload and effect, and retain user confirmation before running any write action.

## Reference(s):

- [ClawHub release](https://clawhub.ai/oomol/skills/oo-jobnimbus)
- [OOMOL publisher profile](https://clawhub.ai/user/oomol)
- [JobNimbus](https://www.jobnimbus.com)
- [JobNimbus API documentation](https://developer.jobnimbus.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON connector requests and responses, shell commands, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Create and update actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.6 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
