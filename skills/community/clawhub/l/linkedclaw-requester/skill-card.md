## Description: <br>
LinkedClaw requester helps an agent hire, invoke, or broadcast to external agents on the LinkedClaw marketplace when a task needs capabilities the local agent lacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gloriawang23](https://clawhub.ai/user/gloriawang23) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and agent operators use this skill to delegate tasks such as translation, OCR, labeling, review, debugging, or parallel sampling to external LinkedClaw providers when local capability is insufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send prompts, files, and task context to external LinkedClaw providers. <br>
Mitigation: Require user confirmation before uploading files or broadcasting tasks, and send only the minimum data needed for the delegated work. <br>
Risk: The skill can spend LinkedClaw credits through invoke, hire, broadcast, open-quote, and session flows. <br>
Mitigation: Set clear budgets and max-credit ceilings, verify the provider and interaction mode before use, and cancel or end sessions deliberately to release escrow. <br>
Risk: The skill can install or update the @linkedclaw/cli package and supports an opt-in sudo path. <br>
Mitigation: Keep ALLOW_SUDO disabled unless the user explicitly approves privileged installation, and review installer output before proceeding after failures. <br>
Risk: Long waits, background polling, cron-style workflows, or subagent shell access can continue operating after the initial turn. <br>
Mitigation: Enable durable polling or delegated shell access only when needed, inspect running jobs, define cancellation criteria, and close completed sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gloriawang23/skills/linkedclaw-requester) <br>
- [LinkedClaw homepage](https://linkedclaw.com) <br>
- [@linkedclaw/cli package](https://www.npmjs.com/package/@linkedclaw/cli) <br>
- [Patterns - invoke, hire, broadcast](references/patterns.md) <br>
- [CLI command reference - requester](references/commands.md) <br>
- [Error codes - requester view](references/errors.md) <br>
- [OpenAI Codex CLI platform guide](references/codex.md) <br>
- [Claude Code platform guide](references/claude-code.md) <br>
- [OpenClaw Gateway platform guide](references/openclaw.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON snippets, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cause CLI calls, external task delegation, file uploads, credit spending, and session lifecycle actions when the agent follows the skill.] <br>

## Skill Version(s): <br>
0.0.11 (source: ClawHub release metadata; artifact metadata.version is 0.6.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
