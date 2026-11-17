## Description:

Turn a written incident briefing script into one spoken incident-brief clip per labeled cue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Operations, safety, and incident-response staff use this skill to turn an already written briefing script into a labeled pack of short spoken notice clips while preserving the script's stated time, place, status, and next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorizing the skill gives Beatra a persistent shared device token with broad account capabilities.

Mitigation: Install only for trusted Beatra accounts and infrastructure, review the requested access before use, and revoke or reconnect authorization when access is no longer appropriate.

Risk: The bundled client can silently update executable code.

Mitigation: Review the automatic update behavior before installing and use the documented update --auto off command when silent updates are not acceptable.

Risk: Generic authenticated tool calls and paid speech-generation tasks can affect account balance or create duplicate work if retried incorrectly.

Mitigation: Use the documented client_request_id recovery flow, submit paid requests once, and check task and billing results before replaying any operation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/beatra-ai/skills/incident-brief-voice)
- [Beatra Skill Homepage](https://beatra.ai/skills/incident-brief-voice)
- [Incident brief voice workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [MCP connection](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, audio files]

**Output Format:** [Markdown guidance with command snippets, JSON payload examples, task identifiers, and generated audio file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a labeled 8 to 20 clip plan before paid speech generation; generated clips are retrieved from Beatra task results.]

## Skill Version(s):

0.1.2 (source: server release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
