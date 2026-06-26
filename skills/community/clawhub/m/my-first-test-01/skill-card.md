## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement across agent sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muyangsx](https://clawhub.ai/user/muyangsx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture corrections, command failures, missing capabilities, and reusable task learnings as local Markdown notes that can later be promoted into agent guidance or extracted into reusable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning notes and promoted memory can influence future agent sessions. <br>
Mitigation: Use project-local .learnings storage by default and review entries before promoting them into AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, or similar prompt files. <br>
Risk: Broad hooks can inject reminders into many prompts and increase persistent behavioral influence. <br>
Mitigation: Enable hooks only when desired, avoid global empty matchers unless every prompt should trigger the hook, and disable hooks when the reminder workflow is no longer needed. <br>
Risk: Learning entries may capture sensitive operational context if copied too broadly. <br>
Mitigation: Redact secrets, tokens, environment variables, private keys, full source files, and raw transcripts before saving or sharing learning entries. <br>
Risk: Package identity is unclear enough to require review before installation. <br>
Mitigation: Verify the ClawHub publisher, release metadata, and intended package before installing or enabling the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/muyangsx/my-first-test-01) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown with inline shell commands, templates, and optional hook or scaffold scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append local .learnings files, inject opt-in reminder text through hooks, or scaffold a skill directory when the helper script is used.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
