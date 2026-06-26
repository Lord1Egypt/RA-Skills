## Description: <br>
Operate the Luckee AI e-commerce assistant via the luckee-tool OpenClaw plugin for Amazon seller advertising diagnosis, keyword research, competitor analysis, listing optimization, and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xing89qs](https://clawhub.ai/user/xing89qs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers, e-commerce operators, and supporting developers use this skill to install, configure, authenticate, and run Luckee AI queries for advertising, product, competitor, keyword, and listing workflows through OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs mutable external code for the Luckee plugin and CLI. <br>
Mitigation: Review and pin trusted plugin and CLI versions before installation, and disable automatic CLI installation when tighter change control is required. <br>
Risk: The skill handles persistent seller tokens and channel credentials. <br>
Mitigation: Use sender-specific tokens where possible, avoid shared default tokens, redact tokens in all outputs, and limit channel credentials to the minimum scopes needed. <br>


## Reference(s): <br>
- [Luckee Skill Reference](artifact/reference.md) <br>
- [Luckee Skill Release Page](https://clawhub.ai/xing89qs/luckee-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands, JSON snippets, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authentication, token management, plugin installation, troubleshooting, and Luckee query invocation guidance.] <br>

## Skill Version(s): <br>
0.1.2026210402 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
