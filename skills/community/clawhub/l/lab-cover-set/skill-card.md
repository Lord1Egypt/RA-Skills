## Description:

Turn user-supplied assignment names and points into a four-to-eight still lab cover set.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to plan and generate assignment-specific lab report cover stills through Beatra, using only user-supplied assignment names and points. The skill supports free pack planning, explicit confirmation before paid image generation, task recovery, billing reporting, and delivery of the resulting stills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs a Beatra account connection with authority to spend credits.

Mitigation: Review the requested permissions before installation and require the documented production confirmation card before any paid generation call.

Risk: The skill stores a shared bearer token under ~/.beatra.

Mitigation: Keep the token only in the documented credential file with user-only permissions, never expose it in chat, logs, command arguments, environment variables, or package directories, and revoke the connection when it is no longer needed.

Risk: The skill sends package, version, platform, and installation metadata to Beatra.

Mitigation: Review the installation registration and MCP connection references before connecting the skill.

Risk: The bundled client silently updates package files by default.

Mitigation: Disable automatic updates with the documented update control when each code change should require explicit review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/beatra-ai/skills/lab-cover-set)
- [Beatra Skill Homepage](https://beatra.ai/skills/lab-cover-set)
- [Lab Cover Pack Workflow](references/workflow.md)
- [Installation and Authentication](references/installation-and-auth.md)
- [Installation Registration](references/installation-registration.md)
- [Tasks and Results](references/tasks-and-results.md)
- [Billing, Errors, and Recovery](references/billing-errors-and-recovery.md)
- [MCP Connection](references/mcp-connection.md)
- [Automatic Updates and Safety](references/automatic-updates-and-safety.md)
- [Uninstall and Disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with JSON payload examples and generated image artifacts returned by Beatra tasks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One still per assignment by default, normally four to eight stills; paid work uses one request identity per still.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
