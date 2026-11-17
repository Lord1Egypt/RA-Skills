## Description:

Test webhooks and expose local services using HookCatch - a developer-friendly webhook testing tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hookcatch](https://clawhub.ai/user/hookcatch)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to create webhook bins, inspect captured webhook requests, replay requests, and expose localhost services while testing integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can exercise broad HookCatch CLI capabilities, including creating bins, reading captured requests, replaying requests, and exposing localhost services.

Mitigation: Run the skill only in trusted workflows, review commands before execution, use test data where possible, and tunnel only services intended for external webhook testing.

Risk: HookCatch tokens, webhook payloads, and local-service traffic may be exposed to the HookCatch CLI and service.

Mitigation: Use scoped or short-lived tokens when available, prefer private or password-protected bins, avoid sensitive payloads, and revoke tokens after testing.

Risk: The wrapper passes the process environment through to an external executable, which may include unrelated secrets.

Mitigation: Run the skill in a restricted environment containing only the HookCatch credentials and configuration needed for the task.

## Reference(s):

- [HookCatch Homepage](https://hookcatch.dev)
- [HookCatch Documentation](https://docs.hookcatch.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke the HookCatch CLI or wrapper, which can emit JSON for supported commands.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
