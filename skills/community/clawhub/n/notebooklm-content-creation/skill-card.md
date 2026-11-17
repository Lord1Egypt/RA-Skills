## Description:

Create and monitor NotebookLM Studio content, including Audio Overview, Video Overview, Infographics, and Slides, via the notebooklm-mcp-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skywalker-lili](https://clawhub.ai/user/skywalker-lili)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and NotebookLM users use this skill to select notebooks, generate Studio artifacts such as podcasts, videos, infographics, and slides, monitor generation, and download completed outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Background polling uses a predictable temporary script path and detached execution.

Mitigation: Review before installing, run only in a trusted local environment, use a private mktemp directory, launch the task-specific poll script path, preserve logs, and provide visible status and stop controls.

Risk: The workflow depends on an authenticated NotebookLM CLI.

Mitigation: Pin and verify the notebooklm-mcp-cli dependency before use and keep authentication scoped to the intended local environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/skywalker-lili/skills/notebooklm-content-creation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create task metadata, progress logs, and downloaded NotebookLM Studio artifacts when executed by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
