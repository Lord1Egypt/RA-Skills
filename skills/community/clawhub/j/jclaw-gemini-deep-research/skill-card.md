## Description:

Executes Gemini Deep Research through the gemini-deep-research MCP extension for Gemini CLI, then polls in the background and saves the resulting research report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skywalker-lili](https://clawhub.ai/user/skywalker-lili)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to launch a paid Gemini Deep Research workflow for complex multi-source research topics and save the resulting report for later use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses a paid Gemini API key and may handle research topics that are sensitive or proprietary.

Mitigation: Confirm billing and credential setup before use, and avoid sensitive or proprietary topics unless the runtime behavior has been separately reviewed.

Risk: The skill writes local task files and reports and launches a detached background poller.

Mitigation: Review the task directory, output path, timeout, and polling script before execution, and monitor or stop the background process when needed.

Risk: The workflow depends on a mutable third-party Gemini extension.

Mitigation: Install only a reviewed extension version and periodically re-review updates before running production research.

Risk: A completed report may be automatically handed to a NotebookLM workflow through another agent.

Mitigation: Disable or confirm downstream chaining before use when automatic handoff is not intended.

## Reference(s):

- [Gemini Deep Research setup guide](references/setup-guide.md)
- [gemini-cli-deep-research extension](https://github.com/allenhutchison/gemini-cli-deep-research)
- [Google AI Studio API keys](https://aistudio.google.com/apikey)
- [ClawHub skill page](https://clawhub.ai/skywalker-lili/skills/jclaw-gemini-deep-research)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status messages, shell command snippets, JSON task metadata, and saved Markdown research reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local task files and reports, polls in the background, and may chain the completed report into a NotebookLM workflow.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
