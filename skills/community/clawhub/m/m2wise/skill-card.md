## Description: <br>
M2Wise helps AI agents maintain long-term memory, extract user preferences and facts from conversations, and track wisdom evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zengyi-thinking](https://clawhub.ai/user/zengyi-thinking) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agent users use this skill to add persistent memory workflows to an agent, including saving preferences or facts, retrieving relevant context, and consolidating memories into higher-level guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can encourage proactive storage of personal conversation details without clear consent or retention controls. <br>
Mitigation: Require explicit user consent before saving personal data and define retention, review, and deletion rules before use. <br>
Risk: Stored memories could include passwords, API keys, tokens, regulated data, or other sensitive information. <br>
Mitigation: Instruct the agent never to store secrets or regulated data, and periodically audit and delete stored memories. <br>
Risk: The skill relies on an external m2wise package and provider API keys. <br>
Mitigation: Review the package before installation and use scoped provider keys with only the permissions needed. <br>
Risk: The optional MCP server can expose memory operations if it is reachable by untrusted clients. <br>
Mitigation: Keep the MCP server local or otherwise access-controlled. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/zengyi-thinking/m2wise) <br>
- [Reference Index](REFERENCE.md) <br>
- [Examples](EXAMPLES.md) <br>
- [API Reference](references/api.md) <br>
- [Memory System](references/memory.md) <br>
- [Wisdom System](references/wisdom.md) <br>
- [PyPI Package](https://pypi.org/project/m2wise/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require local storage, provider API keys, and optional MCP server access.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
