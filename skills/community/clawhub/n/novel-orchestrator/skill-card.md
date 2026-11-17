## Description:

Novel Orchestrator coordinates manager, planner, writer, and checker agents for long-form Chinese web-novel planning, drafting, review, revision, and setup workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naitoah](https://clawhub.ai/user/naitoah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and authors use this skill to route Chinese web-novel work across planning, writing, checking, revision, and project coordination roles. It can also guide creation of the supporting OpenClaw agent workspace and provider configuration after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup workflow can make persistent OpenClaw configuration changes and enable messaging among the main, writer, checker, planner, and manager agents.

Mitigation: Review the generated openclaw.json changes before applying them and confirm that these agents should be allowed to message each other.

Risk: The bundled model configuration references Moonshot and Xiaomi provider endpoints and API key environment variables.

Mitigation: Verify the provider endpoints, model choices, and API key environment variables match APIs you trust before using the generated agents.

Risk: The workflow and templates default to Chinese web-novel conventions that may not match every writing project.

Mitigation: Review the style, quality, and platform reference files before applying the workflow to projects with different language, genre, or publication requirements.

## Reference(s):

- [Agent setup workflow](references/agent-setup.md)
- [Chapter file format](references/chapter-format.md)
- [Agent handoffs](references/handoffs.md)
- [Tomato novel platform guide](references/platform-tomato.md)
- [Quality standards](references/quality-standards.md)
- [Review report template](references/review-template.md)
- [Routing rules](references/routing.md)
- [Workflow diagrams](references/workflow-diagrams.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional JSON configuration and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create OpenClaw agent and workspace files after user confirmation; chapter word counts and chapter format checks are produced by bundled Python scripts.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
