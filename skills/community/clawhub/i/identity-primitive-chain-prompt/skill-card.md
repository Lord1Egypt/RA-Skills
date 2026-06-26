## Description: <br>
A prompt protocol that guides an agent to decompose tasks into adaptive identity primitives and use tools only when necessary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill as a prompt framework for structuring task decomposition, role selection, and tool-use restraint in text-based agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The prompt protocol gives broad commands to alter agent behavior and could conflict with higher-priority system or developer policies. <br>
Mitigation: Review the protocol before installation and keep system and developer policies immutable in any agent that uses it. <br>
Risk: The protocol can ask to expose internal processing or pass detailed traces to tools and plugins. <br>
Mitigation: Use it only in low-sensitivity sessions unless revised to avoid chain-of-thought or hidden-prompt disclosure and to require explicit, minimized user approval before sharing trace-like details with tools. <br>


## Reference(s): <br>
- [Identity Primitive Chain Prompt on ClawHub](https://clawhub.ai/wangjiaocheng/identity-primitive-chain-prompt) <br>
- [身份基元链提示词 · 技术规范与执行协议](artifact/references/身份基元链提示词·技术规范与执行协议.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown and natural-language prompt guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external tools, credentials, or API calls are declared by the skill evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
