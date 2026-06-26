## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement for coding agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent users use this skill to capture corrections, command failures, knowledge gaps, and recurring workflow improvements so future sessions can reuse those learnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local learning logs or command-output inspection may capture sensitive details if used in workspaces where tool output contains secrets. <br>
Mitigation: Do not log secrets, tokens, private keys, environment variables, or full transcripts; prefer short sanitized summaries and avoid command-output inspection in sensitive workspaces. <br>
Risk: Optional hooks can add durable reminders or inspect command output after tool use. <br>
Mitigation: Prefer project-level hooks, review hook scripts before enabling them, and enable PostToolUse error detection only when local output inspection is acceptable. <br>


## Reference(s): <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hooks Setup](references/hooks-setup.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>
- [ClawHub Skill Page](https://clawhub.ai/yezhaowang888-stack/huimai-self-improving) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local .learnings markdown files when the user or agent chooses to log learnings.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
