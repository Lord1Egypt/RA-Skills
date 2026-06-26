## Description: <br>
Reduce MCP token costs by up to 94% and enforce least-privilege tool access by creating YAML policies that control which MCP tools each agent can see and call. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivanpantheon](https://clawhub.ai/user/ivanpantheon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform teams use this skill to reduce MCP tool-schema token overhead, scope agent-visible tools, and draft least-privilege policy files for MCP-based workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation or setup commands can change local Python packages or system-level agent tooling. <br>
Mitigation: Review commands before execution, prefer an isolated Python environment where practical, and confirm the installed package and source match the intended Navil release. <br>
Risk: Policy changes can accidentally hide required tools from agents or leave broad tool access in place. <br>
Mitigation: Test policies with explicit allow and deny checks, review generated policies before copying them into the active policy file, and keep rollback steps available. <br>


## Reference(s): <br>
- [Navil Policy on ClawHub](https://clawhub.ai/ivanpantheon/navil-policy) <br>
- [Navil homepage](https://github.com/navilai/navil) <br>
- [Policy documentation](https://github.com/navilai/navil#tool-scoping) <br>
- [Community policy templates](https://github.com/navilai/navil/tree/main/policies) <br>
- [Token cost guide](https://navil.ai/docs/token-costs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and YAML policy examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include installation checks, policy examples, token-savings estimates, and rollback guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
