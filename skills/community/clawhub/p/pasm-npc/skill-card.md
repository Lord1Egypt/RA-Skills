## Description:

pasm-npc helps agents guide developers in using PASM game NPC agents with persistent local memory, emotion-modulated replies, persona-weighted actions, and feedback-shaped behavior without an LLM dependency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arronjack](https://clawhub.ai/user/arronjack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game teams use this skill to add NPCs that remember player events, vary responses by mood and persona, and adapt action preferences from player feedback while running offline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: NPC memory snapshots are saved locally under ~/.pasm-agents and may contain player interaction details.

Mitigation: Review what the application passes to observe and chat flows, avoid storing sensitive data unless policy permits it, and protect or clear the local state directory as needed.

Risk: The skill relies on installing and running the third-party pasm-agents package and related PASM packages.

Mitigation: Confirm the package source and version are trusted before installation, and run normal dependency review for the target deployment environment.

Risk: Most artifact documentation is in Chinese, which can cause setup or policy misunderstandings for non-Chinese-speaking users.

Mitigation: Provide localized deployment notes or translation before use by teams that cannot review the original documentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arronjack/skills/pasm-npc)
- [Publisher profile](https://clawhub.ai/user/arronjack)
- [pasm-agents homepage](https://github.com/arronJack/pasm-agents)
- [pasm-skills tutorial](https://github.com/arronJack/pasm-skills/blob/master/docs/TUTORIAL.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local setup guidance and examples for NPC memory, mood, actions, feedback, persistence, and tier behavior.]

## Skill Version(s):

0.5.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
