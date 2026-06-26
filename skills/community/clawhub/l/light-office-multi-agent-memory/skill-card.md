## Description: <br>
通用多Agent记忆系统 - 自动捕获、RRF检索、知识图谱、矛盾检测、Token追踪 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liucunguang](https://clawhub.ai/user/liucunguang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to add persistent memory across single-agent and multi-agent workflows, including automatic capture, retrieval, knowledge graph construction, conflict checks, token tracking, and agent registration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently records prompts, tool activity, and errors in a local memory workspace. <br>
Mitigation: Use it only when persistent local memory capture is intended, choose a private MEMORY_WORKSPACE outside /tmp, and review retention and redaction behavior before shared or production use. <br>
Risk: The setup flow and configuration can handle optional API keys. <br>
Mitigation: Keep API keys in environment variables or a secret manager rather than storing them in setup-generated configuration files. <br>
Risk: Captured prompts or tool summaries may contain sensitive information. <br>
Mitigation: Avoid placing secrets in prompts or tool summaries and review captured memory artifacts before broad access or reuse. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liucunguang/light-office-multi-agent-memory) <br>
- [Publisher profile](https://clawhub.ai/user/liucunguang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python scripts, YAML configuration, JSON records, and local HTML dashboard output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent local memory artifacts in the configured MEMORY_WORKSPACE.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
