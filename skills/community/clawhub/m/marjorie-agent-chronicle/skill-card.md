## Description:

Agent Chronicle generates reflective diary entries for agents from session context, with optional quote tracking, curiosity backlog, decision notes, relationship notes, memory integration, and exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use Agent Chronicle to create and maintain personal AI diary entries from daily work context. The skill supports reflective journaling, quote collection, curiosity tracking, decision logging, relationship notes, and optional diary export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read and upload sensitive memory logs while generating diary entries.

Mitigation: Use it only with explicit consent, review selected context before generation, and prefer --emit-task or interactive/local workflows for sensitive logs.

Risk: Path-handling issues could expose or overwrite Markdown files outside the intended diary area.

Mitigation: Keep diary and export paths inside a dedicated workspace diary directory, avoid untrusted --date values, and review output paths before writing files.

Risk: Generated Markdown, HTML, or PDF diary artifacts may contain private conversations, credentials, project plans, or relationship notes.

Mitigation: Treat diary outputs as sensitive artifacts and sanitize them before sharing or exporting outside the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/marjorie-agent-chronicle)
- [SkillBoss setup guide](https://skillboss.co/skill.md)
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [Markdown, Text, JSON, Shell commands, Configuration]

**Output Format:** [Markdown diary entries, JSON generation payloads, command guidance, configuration values, and optional HTML/PDF export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated diary entries target roughly 400-600 words and may include summaries, wins, frustrations, learnings, emotional state, notable interactions, quotes, curiosity items, decisions, relationship notes, and next-day focus.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
