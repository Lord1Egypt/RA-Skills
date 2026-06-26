## Description: <br>
Create and monitor NotebookLM Studio content, including Audio Overview, Video Overview, Infographics, and Slides, via the notebooklm-mcp-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skywalker-lili](https://clawhub.ai/user/skywalker-lili) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content teams use this skill to generate NotebookLM Studio artifacts from a selected NotebookLM notebook, monitor generation progress, and download completed outputs to a chosen workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use an existing NotebookLM account session when creating or downloading content. <br>
Mitigation: Install and run it only in an environment where that account use is acceptable, and confirm the target notebook, artifact type, language, and output path before execution. <br>
Risk: Detached background polling can leave processes, temporary files, logs, or downloaded artifacts behind. <br>
Mitigation: Track the generated task directory, check for active polling processes after completion or timeout, and review temporary files before cleanup. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/skywalker-lili/notebooklm-content-creation) <br>
- [Publisher profile](https://clawhub.ai/user/skywalker-lili) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON task metadata examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create temporary task metadata, logs, polling scripts, and downloaded NotebookLM artifacts when executed by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
