## Description: <br>
Sleep records unfinished OpenClaw session work to a preview file, resets the current session through the Gateway API, and restores pending items through a bootstrap hook in the next session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agents use Sleep to pause a session, preserve unfinished work with actionable next steps, reset the session, and resume from the saved context after bootstrap. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A persistent workspace hook can restore saved preview content into later sessions after reset. <br>
Mitigation: Install the hook only when automatic context restoration is desired, review preview files before reset, and disable the hook when it is no longer needed. <br>
Risk: Preview files can contain sensitive task details or credentials if an agent records them. <br>
Mitigation: Do not store secrets or tokens in preview files, and review preview contents before invoking the reset flow. <br>
Risk: The skill can reset the current OpenClaw session through the Gateway API. <br>
Mitigation: Require explicit confirmation before running /sleep and verify the current session key so the reset targets the intended session. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/axelhu/openclaw-sleep) <br>
- [OpenClaw Hooks Documentation](https://docs.openclaw.ai/automation/hooks) <br>
- [Implementation Instructions](references/implementation.md) <br>
- [Session Sleep-Wake Hook](references/hook-template/HOOK.md) <br>
- [Hook Handler Template](references/hook-template/handler.ts) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown instructions with bash snippets and a TypeScript hook template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a per-session preview file and uses a bootstrap hook to inject pending context when status is pending.] <br>

## Skill Version(s): <br>
1.7.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
