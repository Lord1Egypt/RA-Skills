## Description:

Let agents operate your iCloud Drive, Photos, and Find My safely with local 2FA authentication and explicit confirmation gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent inspect and operate their own iCloud Drive, Photos, and Find My account through local authentication, read-first workflows, and confirmation gates for risky actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants sensitive Apple account and iCloud data access through the pyicloud dependency.

Mitigation: Install only if comfortable with that dependency and iCloud access; prefer session-only mode unless local notes are needed.

Risk: Find My actions, uploads, renames, deletes, and bulk downloads can affect devices or cloud data.

Mitigation: Require explicit confirmation before those actions and verify state with a read-back check after execution.

Risk: Family-device discovery can expose additional device information.

Mitigation: Do not use family-device discovery unless it is required for the task and explicitly approved.

## Reference(s):

- [ClawHub iCloud skill page](https://clawhub.ai/ivangdavila/skills/icloud)
- [iCloud skill homepage](https://clawic.com/skills/icloud)
- [Setup guidance](setup.md)
- [Authentication and session handling](auth-session.md)
- [Safety boundaries](safety-boundaries.md)
- [PyPI package index](https://pypi.org)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local operational notes under ~/icloud/ when the user approves persistence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
