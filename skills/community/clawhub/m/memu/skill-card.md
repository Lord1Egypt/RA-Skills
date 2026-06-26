## Description: <br>
memU provides persistent memory infrastructure for 24/7 agents, replacing flat-file memory with a three-layer Resource -> Memory Item -> Memory Category architecture for lower-token, proactive context retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ProjectSnowWork](https://clawhub.ai/user/ProjectSnowWork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent engineers use this skill to integrate memU into long-running agents that need persistent, structured memory across days, weeks, or months. It helps replace flat conversation-history storage with retrieval, examples, and configuration guidance for in-memory, PostgreSQL/pgvector, or hosted memU deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-lived memory may store sensitive or regulated user data across sessions. <br>
Mitigation: Define retention, deletion, and data-classification rules before use, and avoid storing secrets or regulated data unless the deployment is approved for that data. <br>
Risk: Example configurations send memory extraction and retrieval requests to external OpenAI-compatible providers. <br>
Mitigation: Use only data you are allowed to send to the configured provider, or route chat and embedding calls to local or self-hosted OpenAI-compatible endpoints for sensitive deployments. <br>
Risk: Debug or operational logs could expose memory content, prompts, identifiers, or connection details. <br>
Mitigation: Disable or redact debug logging in production and review log sinks before connecting real user or operational data. <br>
Risk: Persistent memory accumulates unless retention is managed separately. <br>
Mitigation: Implement cleanup, expiration, and user deletion workflows around memU storage before relying on it for 24/7 production agents. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ProjectSnowWork/memu) <br>
- [Official memU repository](https://github.com/NevaMind-AI/memU) <br>
- [Official memU README](https://github.com/NevaMind-AI/memU#readme) <br>
- [memU English documentation](https://github.com/NevaMind-AI/memU/blob/main/readme/README_en.md) <br>
- [memU benchmark results](https://memu.pro/benchmark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and an OpenAI-compatible API key; PostgreSQL with pgvector is optional for persistent storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, and METADATA.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
