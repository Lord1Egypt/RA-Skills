## Description: <br>
Privacy-first, self-hosted chat memory for OpenClaw that saves and recalls conversation history across sessions without a cloud dependency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ukkit](https://clawhub.ai/user/ukkit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Memcord to add local, persistent chat memory through an MCP server so agents can save meaningful conversation context and recall it in later sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist chat contents locally and recall them later, which may retain sensitive conversation content. <br>
Mitigation: Use explicit save requests where possible, avoid saving secrets or credentials, and review local retention expectations before installing. <br>
Risk: Storage location, deletion, retention, and consent behavior are not clearly documented in the available evidence. <br>
Mitigation: Review the package documentation and local files before relying on it for ongoing memory, especially in shared or regulated environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ukkit/memcord) <br>
- [Publisher Profile](https://clawhub.ai/user/ukkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with JSON5 configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides OpenClaw MCP configuration guidance and operational guidance for saving and reading local chat memory.] <br>

## Skill Version(s): <br>
4.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
