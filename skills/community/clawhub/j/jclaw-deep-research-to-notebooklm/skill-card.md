## Description: <br>
Orchestrates an end-to-end workflow that runs Gemini Deep Research, uploads the report to NotebookLM, and generates selected NotebookLM artifacts such as audio, video, infographics, and slides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skywalker-lili](https://clawhub.ai/user/skywalker-lili) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research-oriented users use this skill to turn a research topic into a Deep Research report and then create NotebookLM content artifacts with bounded polling and optional downloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can continue through a background agent handoff after the initial confirmation. <br>
Mitigation: Confirm the full research topic, artifact choices, language, download setting, and polling limits before launch, and monitor the status notifications. <br>
Risk: The workflow sends Discord updates and re-invokes an OpenClaw agent to start the NotebookLM phase. <br>
Mitigation: Use it only in an intended channel or workspace and verify that the dependency skills and OpenClaw delivery path are trusted. <br>
Risk: The generated research report is uploaded to NotebookLM, and optional downloads may be written to an ObsidianVault path. <br>
Mitigation: Avoid sensitive inputs unless NotebookLM use is approved, and review local download paths before enabling downloads. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/skywalker-lili/jclaw-deep-research-to-notebooklm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and bash command/script snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates task configuration and polling scripts; may save reports and optional NotebookLM downloads through the agent workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
