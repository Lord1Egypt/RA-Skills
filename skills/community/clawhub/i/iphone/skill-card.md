## Description:

Run iPhone mission playbooks for battery, storage, privacy, connectivity, and daily automation with live operator-style guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill for guided iPhone troubleshooting and optimization across battery, storage, privacy, connectivity, notifications, and daily routines. The skill provides live operator-style tap paths, checkpoints, and recovery ladders while requiring user confirmation for sensitive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide changes that affect device behavior, including deletions, resets, profile changes, privacy settings, or automations.

Mitigation: Require explicit user confirmation before sensitive or potentially disruptive actions, and prefer reversible actions before escalation.

Risk: Local mission notes may include device model, preferences, recurring problems, and approved actions under ~/iphone/.

Mitigation: Keep stored notes concise, local, and limited to context that improves future guided troubleshooting.

Risk: Operator-style guidance can be mistaken for direct or silent device control.

Mitigation: Make clear that the skill provides instructions only and that the user performs each iPhone action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/iphone)
- [Skill homepage](https://clawic.com/skills/iphone)
- [Mission Catalog](artifact/mission-catalog.md)
- [Tap Script Engine](artifact/tap-script-engine.md)
- [Rescue Ladders](artifact/rescue-ladders.md)
- [Shortcuts Bridge](artifact/shortcuts-bridge.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown with step-by-step tap paths, checkpoints, and short configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only output; no direct device control or network access by default.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
