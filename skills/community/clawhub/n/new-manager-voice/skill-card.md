## Description:

Turns an office's written first-week checklist into 8 to 20 labeled onboarding voice clips for a new manager.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Managers, HR teams, and onboarding teams use this skill to turn an existing first-week checklist into labeled voice clips for manager onboarding. The skill plans the clip list first, then guides confirmed paid speech or voice-clone generation through Beatra.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a shared device bearer token and broad Beatra media-generation and account permissions.

Mitigation: Install only when the user trusts Beatra for those permissions, keep credentials in the documented local credential file, and avoid exposing tokens in chat, logs, command arguments, or generated files.

Risk: The bundled client can silently replace package-owned code through default automatic updates.

Mitigation: Review the package before installation and disable automatic updates after install when changes should require an explicit user action.

Risk: Voice cloning and speech synthesis are paid operations and may create duplicate charges if retried incorrectly.

Mitigation: Require the documented confirmation card before each paid stage, use one opaque client_request_id per logical request, and retry uncertain paid calls only with byte-identical arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/new-manager-voice)
- [Beatra skill homepage](https://beatra.ai/skills/new-manager-voice)
- [New manager week voice workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Bundled MCP Client diagnostics](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, audio files]

**Output Format:** [Markdown guidance with JSON payloads and generated MP3 clip files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a labeled 8 to 20 clip plan before paid work; each paid clone or speech request uses a separate confirmation and request identity.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
