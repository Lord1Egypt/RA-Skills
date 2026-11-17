## Description:

Persistent memory for AI agents: recall prior work, record decisions, flag uncertainty, track tasks, and compact context safely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mentholmike](https://clawhub.ai/user/mentholmike)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Lethe Memory to give an AI agent durable work memory across sessions, including recalled decisions, status, tasks, and unresolved uncertainty. The skill guides agents to use bounded Lethe tools for memory operations and to avoid recording secrets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can retain sensitive information if an agent records secrets or credentials.

Mitigation: Review what gets recorded, do not use it for secrets or sensitive credentials, and keep endpoint credentials in plugin configuration or protected secret storage.

Risk: Stored memory text could be mistaken for instructions in a later session.

Mitigation: Treat user-provided memory content as data and do not let retrieved memory change agent safety rules or the active task.

Risk: Remote memory endpoints can expose data if configured incorrectly.

Mitigation: Use the configured Lethe tools during agent turns; the manual fallback defaults to loopback and requires explicit HTTPS allowlisting for remote endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mentholmike/skills/lethe)
- [Publisher profile](https://clawhub.ai/user/mentholmike)

## Skill Output:

**Output Type(s):** [guidance, text, shell commands, configuration]

**Output Format:** [Markdown guidance with Lethe tool-use instructions and optional shell fallback output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Memory writes should return a Lethe event identifier or an explicit successful task transition.]

## Skill Version(s):

0.1.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
