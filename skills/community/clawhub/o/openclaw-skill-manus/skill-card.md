## Description:

Agente de IA autonomo de Manus con capacidades de investigacion, desarrollo, automatizacion y generacion de medios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[disi3r](https://clawhub.ai/user/disi3r)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw agents use this skill to send research, development, workflow automation, file-upload, project, status, result, and webhook tasks to the Manus API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, uploaded files, and connector actions may be sent to Manus as a remote autonomous service.

Mitigation: Use the skill only when that remote processing is intended, avoid uploading secrets or sensitive documents, and review prompts before execution.

Risk: Gmail, Slack, Calendar, and Notion connector tasks can act on user or workspace data.

Mitigation: Use least-privilege or test connector accounts where possible and review requested actions before asking Manus to execute them.

Risk: The webhook server can receive public traffic if exposed without additional controls.

Mitigation: Keep the webhook endpoint private unless needed, and add authentication, request limits, and network controls before public exposure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/disi3r/skills/openclaw-skill-manus)
- [Publisher profile](https://clawhub.ai/user/disi3r)
- [Manus homepage](https://manus.im)
- [Manus API base URL](https://api.manus.ai/v1)
- [Manus task API](https://api.manus.ai/v1/tasks)
- [Manus projects API](https://api.manus.ai/v1/projects)
- [Manus files API](https://api.manus.ai/v1/files)
- [Manus webhooks API](https://api.manus.ai/v1/webhooks)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, terminal output, API responses, and generated task artifacts returned by Manus]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MANUS_API_KEY and sends prompts, uploaded files, and connector-driven tasks to the remote Manus service.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
