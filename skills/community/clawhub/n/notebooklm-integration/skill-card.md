## Description:

Integrates Google NotebookLM capabilities into agent workflows through the unofficial notebooklm-py library for notebook management, source import, research queries, generated overviews, exports, and artifact downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oki3505f](https://clawhub.ai/user/oki3505f)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research-oriented users use this skill to automate NotebookLM notebook management, source imports, research workflows, and generated content exports from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on mutable unofficial notebooklm-py code and undocumented Google APIs for NotebookLM operations.

Mitigation: Review the skill before installing, use a dedicated Python environment, and pin and verify the notebooklm-py dependency where possible.

Risk: The skill can affect Google account data through Drive import, sharing, export, local-file processing, and notebook deletion workflows.

Mitigation: Use a least-privilege Google account and require explicit approval before importing Drive files, processing sensitive local files, sharing, exporting, or deleting notebooks.

Risk: NotebookLM API behavior, quotas, and permissions may change unexpectedly.

Mitigation: Add retry and fallback handling, monitor rate-limit failures, and validate generated outputs before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oki3505f/skills/notebooklm-integration)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, markdown, files]

**Output Format:** [Markdown with Python and bash code blocks; may direct NotebookLM artifact outputs such as MP3, MP4, PDF, PPTX, PNG, JSON, Markdown, and HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires notebooklm-py and an authenticated Google account.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
