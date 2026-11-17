## Description:

Automates LimeSurvey survey, participant, response, question, and reporting operations through the RemoteControl 2 JSON-RPC API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olegantonov](https://clawhub.ai/user/olegantonov)

### License/Terms of Use:

MIT

## Use Case:

Developers and survey operators use this skill to manage LimeSurvey instances, export response data, administer participants, and automate survey lifecycle tasks from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive survey responses and participant records.

Mitigation: Treat response exports and participant files as sensitive data, limit local copies, and store outputs only in approved locations.

Risk: The skill can change live survey content or send invitations and reminders.

Mitigation: Confirm survey IDs, participant scopes, and recipient lists before activation, deletion, invitations, or reminders.

Risk: Credential misuse could expose a LimeSurvey instance.

Mitigation: Use a dedicated least-privilege service account, require HTTPS for the RemoteControl endpoint, and avoid full administrator credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/olegantonov/skills/limesurvey-openclaw-skill)
- [Project Homepage](https://github.com/olegantonov/limesurvey-openclaw-skill)
- [API Reference](references/api_reference.md)
- [Examples](references/examples.md)
- [Official LimeSurvey API Documentation](https://api.limesurvey.org/classes/remotecontrol-handle.html)
- [RemoteControl 2 Manual](https://www.limesurvey.org/manual/RemoteControl_2_API)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python examples, JSON snippets, and exported survey files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate LimeSurvey API calls that create, update, delete, export, activate, invite, or remind depending on the selected workflow.]

## Skill Version(s):

1.2.2 (source: server release metadata; artifact frontmatter reports 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
