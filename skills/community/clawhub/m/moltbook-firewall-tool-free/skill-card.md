## Description: <br>
Agent防火墙免费版 provides a basic AI agent security layer for prompt injection detection, tool-call filtering, input sanitization, and security policy checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual agent builders use this skill to add local safety checks for agent inputs and proposed tool calls before execution. It is intended for prompt-injection screening, basic tool-call filtering, input sanitization, and static policy checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests command-execution capability while relying on simple local prompt and tool-call checks. <br>
Mitigation: Keep execution permissions narrow, review proposed commands, and require explicit user confirmation before running commands or tools. <br>
Risk: Security claims may be interpreted as a complete firewall, vulnerability scanner, encryption protection tool, or reliable default-deny gate. <br>
Mitigation: Use the skill as an advisory pre-check layer and pair it with platform permissions, sandboxing, allowlists, and human review for sensitive workflows. <br>
Risk: The documented callback_url input could expose sensitive data if callbacks are sent to untrusted destinations. <br>
Mitigation: Avoid sending sensitive inputs through callback URLs and restrict callback destinations to reviewed, trusted endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/moltbook-firewall-tool-free) <br>
- [Detailed reference](artifact/references/detail.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON result objects, markdown guidance, and inline Python or bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include action decisions, findings, sanitized input, execution logs, and configuration examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
