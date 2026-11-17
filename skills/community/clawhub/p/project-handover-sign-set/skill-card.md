## Description:

Creates matching project handover sign stills from contractor-confirmed titles, unit names, project names, and dates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Contractors and supervisors use the skill to plan and generate three matching handover sign stills from confirmed inscriptions, then extend them into a project set after separate approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorization uses a shared full-scope Beatra device token with broader account access than sign generation needs.

Mitigation: Connect only an account whose access and generated-content exposure are acceptable; keep the token private.

Risk: Generating or editing stills spends credits from a paid wallet.

Mitigation: Review the current price and obtain explicit approval for each batch or correction; use an account with an acceptable spending balance.

Risk: Package updates install silently by default.

Mitigation: Disable automatic updates with the documented command if you require manual review of new versions.

Risk: Installation registration sends package and coarse runtime metadata to Beatra.

Mitigation: Review the documented registration fields before connecting the skill.

## Reference(s):

- [Project handover sign workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Project Handover Sign Set homepage](https://beatra.ai/skills/project-handover-sign-set)

## Skill Output:

**Output Type(s):** [Markdown, Image files, Guidance]

**Output Format:** [Markdown pack list and generated sign stills]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports observed formats and dimensions, task IDs, and charged credits when available.]

## Skill Version(s):

0.1.9 (source: server-resolved release and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
