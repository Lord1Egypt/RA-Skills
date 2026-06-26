## Description: <br>
Captures learnings, errors, corrections, and feature requests in local Markdown logs so agents can review and promote recurring knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j-meow-666](https://clawhub.ai/user/j-meow-666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent users use this skill to record command failures, user corrections, missing feature requests, and reusable lessons in `.learnings/` Markdown files. It also provides optional hook-based reminders and guidance for promoting broadly useful learnings into agent context files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local learning logs may persist sensitive context or shape future agent behavior. <br>
Mitigation: Keep routine notes in `.learnings/`, redact secrets and raw command output, and review entries before reuse or sharing. <br>
Risk: Promoting learnings into agent instruction or memory files can make temporary observations affect future sessions. <br>
Mitigation: Require user approval before promoting entries into `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `CLAUDE.md`, or other persistent instruction files. <br>
Risk: The optional Bash error-detection hook inspects command output to identify failures. <br>
Mitigation: Enable the error-detection hook only in trusted environments and only when command output inspection is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/j-meow-666/meowceshi) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local learning-log entries and optional hook setup guidance; users should redact sensitive details before logging.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
