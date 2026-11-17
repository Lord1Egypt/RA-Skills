## Description:

Openclaw San Sheng Liu Bu Lobster helps an OpenClaw agent decompose work across multiple subagents, notify Feishu participants, create Feishu documents, update Bitable records, and summarize deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiebao360](https://clawhub.ai/user/jiebao360)

### License/Terms of Use:

MIT-0

## Use Case:

Small business operators, solo founders, content creators, and OpenClaw users can use this skill to coordinate task decomposition, parallel agent execution, Feishu notifications, document creation, task tracking, and final content handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes live-looking Feishu OpenIDs, chat IDs, Bitable tokens, URLs, and folder destinations.

Mitigation: Replace all bundled Feishu identifiers and destinations with resources you control before installing or running the skill.

Risk: The workflow posts outputs, task metadata, local paths, and document links to Feishu and stores records in Bitable.

Mitigation: Avoid confidential tasks unless this cloud posting is acceptable, or require explicit confirmation before sending or storing each item.

Risk: Cloud document creation and task tracking are mandatory in the documented workflow.

Mitigation: Use a local-only variant or remove the Feishu posting steps for sensitive or restricted work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiebao360/skills/openclaw-san-sheng-liu-bu-lobster)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Lobster team configuration](artifact/config/lobster-team.md)
- [Feishu document automation guide](artifact/docs/auto-create-feishu-doc.md)
- [Task tracking guide](artifact/docs/task-tracking.md)
- [Task templates](artifact/templates/task-templates.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions, task templates, Feishu document links, Bitable update guidance, and completion summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local task files and Feishu-linked deliverables when configured with user-controlled Feishu resources.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
