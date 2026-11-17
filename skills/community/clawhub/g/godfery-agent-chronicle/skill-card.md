## Description:

Generates detailed, AI-written diary entries from an agent's perspective, capturing emotions, decisions, quotes, curiosities, and relationship evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to generate reflective daily or weekly journal entries from session logs and memory notes, with optional quote, curiosity, decision, and relationship tracking. It can also export saved diary entries to HTML or PDF for review or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API generation can send private session logs and stored memory notes to SkillBoss.

Mitigation: Use the skill only with non-sensitive workspaces, review the generated task payload before sending, or use local/manual modes when private content is present.

Risk: Privacy settings are documented, but evidence.security states they are not currently enforced by the implementation.

Mitigation: Treat all generated entries as private until manually reviewed and sanitized before export or sharing.

Risk: Local diary files, persistent notes, and exports may contain sensitive journal content.

Mitigation: Store outputs in protected workspace locations, keep generated exports out of source control, and review files before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/godfery-agent-chronicle)
- [SkillBoss setup guide](https://skillboss.co/skill.md)
- [Artifact README](README.md)
- [Daily entry template](templates/daily.md)
- [Weekly summary template](templates/weekly.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown diary entries, JSON task payloads, local files, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save entries and persistent notes under the workspace memory directory; API generation can send session context to SkillBoss.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
