## Description: <br>
Persistent memory for OpenClaw agents. Exact recall in milliseconds - your agent remembers everything across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgrant1234](https://clawhub.ai/user/lgrant1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Grantai Memory to add persistent local memory to agents, recall prior decisions, import project context, and store session summaries across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The memory service may retain project files, git history, code snippets, and verbatim conversation data across sessions. <br>
Mitigation: Keep imports narrow, avoid secrets and regulated data, and confirm how to inspect, delete, and contain stored memory before relying on it. <br>
Risk: The skill depends on an external local binary or Docker image. <br>
Mitigation: Verify the source of the grantai-mcp binary or Docker image before installation and review the configured storage location. <br>


## Reference(s): <br>
- [GrantAi OpenClaw Integration](https://solonai.com/grantai/integrations/openclaw) <br>
- [GrantAi Download](https://solonai.com/grantai/download) <br>
- [ClawHub Skill Page](https://clawhub.ai/lgrant1234/grantai-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline YAML and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can invoke or configure an external local memory service through the grantai-mcp binary or Docker image.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
