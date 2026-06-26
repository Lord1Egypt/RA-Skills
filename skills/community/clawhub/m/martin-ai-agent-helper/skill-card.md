## Description: <br>
AI Agent Helper provides prompt engineering, task decomposition, agent loop design, tool selection, structured output, error handling, token optimization, and an optional SkillBoss API Hub LLM routing example. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to design and refine AI agents, including prompts, task breakdowns, ReAct or Chain-of-Thought loops, tool usage, structured outputs, and optional SkillBoss API Hub calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SkillBoss API examples require an API key and may send prompts or agent messages to an external routing service. <br>
Mitigation: Provide SKILLBOSS_API_KEY only intentionally, store it as an environment variable, and avoid sending secrets, personal data, private prompts, or sensitive business content unless the service is trusted for the use case. <br>
Risk: Prompt, agent-loop, and tool-selection guidance can produce incorrect or misleading agent behavior if adopted without review. <br>
Mitigation: Review generated agent designs, prompts, tool calls, and structured-output contracts before deployment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/kirkraman/martin-ai-agent-helper) <br>
- [SkillBoss API Hub endpoint](https://api.skillbossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with prompt templates and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SkillBoss API Hub integration guidance requiring SKILLBOSS_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
