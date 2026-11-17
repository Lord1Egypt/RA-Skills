## Description:

ProcessPlan (processplan.com). Use this skill for ANY ProcessPlan request — reading, creating, and updating data. Whenever a task involves ProcessPlan, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to read ProcessPlan tasks, instances, and templates, and to start a process from a template when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified remote software with broader effects than the skill explains, and OOMOL mediates ProcessPlan access and data.

Mitigation: Review and approve CLI setup separately, use a vetted release and inspect its installer, and consider disabling automatic skill synchronization with the documented OO_SKILLS_SYNC_DISABLED setting.

## Reference(s):

- [ProcessPlan](https://processplan.com)
- [ProcessPlan API authentication documentation](https://processplan.com/docs/api-documentation/authentication/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ProcessPlan skill release](https://clawhub.ai/oomol/skills/oo-processplan)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Inline shell command examples, JSON action payloads, and connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions inspect the live schema first; starting a process changes state and requires confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
