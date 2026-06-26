## Description: <br>
Mechanical enforcement tools to help AI coding agents follow project standards with git hooks, secret detection, deployment verification, and import registries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzOcb](https://clawhub.ai/user/jzOcb) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to install local guardrails that discourage reimplementation, hardcoded secrets, deployment gaps, and skill-update drift in AI-assisted coding workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installers can change repository git hooks and guardrail files, which may affect local commit workflows. <br>
Mitigation: Inspect the install scripts and generated .git/hooks files before enabling them, and back up existing hooks first. <br>
Risk: The optional skill-update feedback loop adds a post-commit hook and semi-automatic commit helper for skills updates. <br>
Mitigation: Enable that loop only in repositories where this automation is desired, and review generated tasks and commits before accepting them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jzOcb/jz-agent-guardrails) <br>
- [Project Homepage](https://github.com/anon/agent-guardrails#readme) <br>
- [Claude Code Install Guide](CLAUDE_CODE_INSTALL.md) <br>
- [Deployment Verification Guide](references/deployment-verification-guide.md) <br>
- [Agent Rules Template](references/agents-md-template.md) <br>
- [Skill Update Feedback](references/skill-update-feedback.md) <br>
- [Enforcement Research](references/enforcement-research.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, and local script references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup guidance and references to scripts that modify repository hooks and guardrail files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
