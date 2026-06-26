## Description: <br>
Configure and manage OpenClaw Dreaming — background memory consolidation, auto-promotion to MEMORY.md, dream diary <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silverod](https://clawhub.ai/user/silverod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to configure, check, and troubleshoot Dreaming for background memory consolidation, dream diary management, and controlled promotion into MEMORY.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dreaming can read notes or session transcripts and promote selected content into MEMORY.md on a schedule. <br>
Mitigation: Review the OpenClaw configuration before applying it and confirm the heartbeat and promotion settings match the intended workspace. <br>
Risk: Manual promotion or backfill commands can alter MEMORY.md or DREAMS.md. <br>
Mitigation: Back up MEMORY.md and DREAMS.md and run preview commands before using --apply or backfill options. <br>
Risk: Server metadata includes wallet and sensitive-credential capability tags that may not match the artifact behavior. <br>
Mitigation: Verify those tags are irrelevant for the target installation before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/silverod/openclaw-dreaming-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON5 configuration snippets and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; commands and configuration should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
