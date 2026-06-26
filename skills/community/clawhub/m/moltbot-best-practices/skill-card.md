## Description: <br>
Best practices for AI agents - Cursor, Claude, ChatGPT, Copilot. Avoid common mistakes. Confirms before executing, drafts before publishing. Vibe-coding essential. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NextFrontierBuilds](https://clawhub.ai/user/NextFrontierBuilds) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to guide coding assistants and AI agents toward clearer task confirmation, draft-before-publish workflows, prompt escalation on repeated tool failures, and stopping when instructed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying the optional memory and session search configuration can make private, sensitive, or stale session context available to future agent work. <br>
Mitigation: Enable memory and session search only when it fits the user's data policy and workflow; avoid applying it to sessions that contain sensitive information unless retention and search behavior are acceptable. <br>


## Reference(s): <br>
- [Moltbot Best Practices README](README.md) <br>
- [Moltbot Best Practices ClawHub Release](https://clawhub.ai/NextFrontierBuilds/moltbot-best-practices) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON configuration and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance with optional OpenClaw memory and session search configuration.] <br>

## Skill Version(s): <br>
1.1.3 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
