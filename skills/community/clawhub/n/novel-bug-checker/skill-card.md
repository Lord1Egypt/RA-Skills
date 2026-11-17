## Description:

Audits Chinese novel manuscripts for plot logic flaws, character inconsistency, pacing issues, and narrative bugs, then produces graded findings and repair suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bbroot](https://clawhub.ai/user/bbroot)

### License/Terms of Use:

MIT-0

## Use Case:

External authors, editors, and writing-focused agents use this skill to review Chinese novel chapters or full manuscripts for narrative continuity, character behavior, pacing, and foreshadowing problems before revision or publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill can cross into another local skill workspace and run scripts from that location when optional novel-master integration is enabled.

Mitigation: Use the integration only after reviewing the other local skill and confirming the target project path.

Risk: The security review says dependency, environment, and file-output behavior is under-scoped.

Mitigation: Install pinned dependencies yourself, run the skill in an isolated trusted project, and avoid directories containing sensitive .env files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bbroot/skills/novel-bug-checker)
- [Bug pattern classification](references/bug-patterns.md)
- [Character consistency guide](references/character-consistency.md)
- [Narrative theory foundation](references/narrative-theory.md)
- [Repair strategies library](references/repair-strategies.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with optional shell commands and generated report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports classify issues by severity and include multiple repair options per bug.]

## Skill Version(s):

2.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
