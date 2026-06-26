## Description: <br>
Research-before-coding workflow. Search for existing tools, libraries, and patterns before writing custom code. Invokes the researcher agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill before starting new features, integrations, utilities, or abstractions to compare existing libraries, MCP servers, skills, and reference implementations before deciding whether to adopt, extend, compose, or build. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proposed packages, MCP servers, or configuration changes could introduce unsuitable dependencies or operational changes. <br>
Mitigation: Review each recommendation, license, maintenance signal, and proposed configuration change before accepting it. <br>
Risk: Research prompts may expose secrets or sensitive private project data. <br>
Mitigation: Avoid putting secrets or sensitive private data into research prompts or external searches. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and structured recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prompt a researcher agent and propose package, MCP, or configuration changes for human review.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
