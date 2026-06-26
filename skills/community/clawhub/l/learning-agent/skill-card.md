## Description: <br>
Captures learnings, errors, and corrections so coding agents can improve their future guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-wuxl](https://clawhub.ai/user/ryan-wuxl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI coding-agent users use this skill to capture command failures, corrections, feature requests, and recurring lessons, then review or promote them into durable project guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable learning notes can accidentally preserve secrets, private transcripts, customer data, or sensitive operational details. <br>
Mitigation: Review and redact entries before keeping them, and do not store secrets, tokens, private transcripts, customer data, or sensitive operational details in learning files. <br>
Risk: Promoting learnings into future agent instruction files can preserve incorrect or unwanted guidance. <br>
Mitigation: Review proposed changes to .learnings, CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, and Copilot instruction files before relying on them. <br>
Risk: Cross-session history or messaging can share context beyond the user's intended session. <br>
Mitigation: Use cross-session history or messaging only with explicit user intent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-wuxl/learning-agent) <br>
- [Examples](references/examples.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration Guide](references/openclaw-integration.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or recommend durable learning files and agent instruction updates when the user permits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
