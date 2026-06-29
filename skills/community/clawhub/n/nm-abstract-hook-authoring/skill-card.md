## Description: <br>
Guides developers in creating Claude Code hooks with security-first design for validation and enforcement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to author and review Claude Code and Claude Agent SDK hooks for validation, enforcement, logging, context injection, scope selection, performance, and testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Raw hook examples may encourage permission bypass or auto-approval patterns without enough guardrails. <br>
Mitigation: Keep permission prompts for risky actions and narrow any approval logic to explicit, reviewed operations. <br>
Risk: Logging and persistent-state examples may capture sensitive tool inputs, outputs, or local context. <br>
Mitigation: Redact secrets, minimize stored data, and review retention behavior before copying examples into a real project. <br>
Risk: Silent context-injection examples may include local file context without clear user consent. <br>
Mitigation: Require explicit consent for local context injection and limit injected data to the minimum needed for the hook. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-abstract-hook-authoring) <br>
- [clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract) <br>
- [Claude Code hooks documentation](https://docs.anthropic.com/en/docs/claude-code/hooks) <br>
- [Claude Agent SDK documentation](https://docs.anthropic.com/en/docs/claude-agent-sdk) <br>
- [Claude Code settings documentation](https://docs.anthropic.com/en/docs/claude-code/settings) <br>
- [Hook types overview](artifact/modules/hook-types.md) <br>
- [Performance guidelines for hooks](artifact/modules/performance-guidelines.md) <br>
- [Hook scope selection guide](artifact/modules/scope-selection.md) <br>
- [SDK callbacks and implementation patterns](artifact/modules/sdk-callbacks.md) <br>
- [Testing hooks](artifact/modules/testing-hooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON, Python, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; examples require review before use.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
