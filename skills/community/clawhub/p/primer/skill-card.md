## Description: <br>
The Primer helps an agent set up a personal growth and accountability protocol that adapts to the user's life stage, goals, permissions, and Miranda check-ins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucko](https://clawhub.ai/user/brucko) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to configure an AI assistant as a personal tutor for growth goals, life transitions, accountability, pattern surfacing, and periodic check-ins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent changes to future agent behavior by creating a personal coaching profile and updating agent startup files. <br>
Mitigation: Review PRIMER.md, AGENTS.md, and SOUL.md edits before accepting them, and keep only coaching permissions the user explicitly wants. <br>
Risk: The skill may schedule recurring reflection or Miranda check-in automation. <br>
Mitigation: Enable recurring jobs only after confirming the desired cadence, timezone, and scope; remove or disable jobs that are no longer wanted. <br>
Risk: The generated profile may contain sensitive personal goals, reflections, failure modes, and accountability notes. <br>
Mitigation: Decide what personal information should be stored, redact sensitive details where possible, and periodically review retention or deletion needs. <br>


## Reference(s): <br>
- [Life Stages Framework](references/life-stages.md) <br>
- [The Miranda Protocol](references/miranda-protocol.md) <br>
- [Primer Permissions](references/permissions.md) <br>
- [PRIMER.md Template](assets/PRIMER-TEMPLATE.md) <br>
- [ClawHub skill page](https://clawhub.ai/brucko/primer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create PRIMER.md, update AGENTS.md and SOUL.md, and propose recurring reflection or check-in schedules.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
