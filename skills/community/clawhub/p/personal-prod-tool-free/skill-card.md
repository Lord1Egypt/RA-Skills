## Description: <br>
个人效率顾问基础版 helps individual users diagnose productivity issues, organize tasks, plan time blocks, reduce distractions, and apply practical anti-procrastination methods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals use this skill for lightweight personal productivity coaching, including diagnosing bottlenecks, creating task capture systems, designing time-block plans, improving focus, and choosing concrete methods to overcome procrastination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad command and API capability, including examples that inspect environment variables. <br>
Mitigation: Review exact commands before execution and do not allow environment inspection or shell access unless the command is necessary and understood. <br>
Risk: The artifact makes a local-only privacy claim while also describing possible network and external API use. <br>
Mitigation: Treat privacy claims as unverified until the publisher explains what data may leave the local environment and when user confirmation is required. <br>
Risk: Credential handling guidance is inconsistent across the artifact. <br>
Mitigation: Avoid storing secrets in skill configuration, redact command output, and confirm API key handling before using connected features. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/personal-prod-tool-free) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with optional structured JSON, text, CSV-style responses, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free edition is described as single-task, community-supported, and limited to basic analysis.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
