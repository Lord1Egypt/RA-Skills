## Description: <br>
Orchestrate complex multi-agent workflows with explicit coordinator planning, execution governance, and *automatic output management*. Each skill run creates its own isolated output namespace to prevent file accumulation and confusion from repeated executions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rubencoppensongit](https://clawhub.ai/user/rubencoppensongit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to coordinate complex multi-agent analysis or execution work through a governed planning, sequencing, verification, reporting, and cleanup process. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow writes coordinator run artifacts and debug traces that could include sensitive task context if users place secrets in prompts. <br>
Mitigation: Do not include secrets, tokens, or private data in task prompts; provide required credentials through environment variables or approved tools. <br>
Risk: Debug mode and cleanup behavior can affect retained run evidence and old coordinator outputs. <br>
Mitigation: Review generated run folders and retention settings before relying on cleanup, especially for audit or compliance workflows. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, coordinator run artifacts, agent prompts, and optional logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates an isolated run directory for each execution; debug mode can persist planning, prompt, output, and traceability files.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
