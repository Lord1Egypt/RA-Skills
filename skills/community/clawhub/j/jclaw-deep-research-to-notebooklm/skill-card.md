## Description:

Orchestrates Deep Research followed by NotebookLM content generation, chaining dependent skills to produce selected audio, video, infographic, or slide artifacts with optional downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skywalker-lili](https://clawhub.ai/user/skywalker-lili)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run a research workflow and then create NotebookLM artifacts from the resulting report without manually transferring content between tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detached background scripts and automatic agent-triggered continuation can keep operating after the initial user interaction.

Mitigation: Require explicit approval before background continuation and provide clear status notifications for each phase.

Risk: Unsafe shell evaluation can execute unintended command text during download handling.

Mitigation: Avoid eval and build download commands from fixed arguments or shell-safe command construction.

Risk: A predictable task directory under /tmp can expose workflow files to accidental disclosure or interference on shared systems.

Mitigation: Use a private, unpredictable task directory with restricted permissions.

Risk: Discord messaging and optional local downloads affect where status and generated artifacts are sent or stored.

Mitigation: Make notification channels, download behavior, and destination paths clear before running the workflow.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/skywalker-lili/skills/jclaw-deep-research-to-notebooklm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON snippets and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create background polling scripts, task JSON, report files, status notifications, and optional downloaded NotebookLM artifacts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
