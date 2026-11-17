## Description:

Extracts structured insights from journal entries and generates an interactive local visualization with thought cards, mood timelines, growth dimensions, and a knowledge graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smorzandos](https://clawhub.ai/user/smorzandos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to analyze personal diary files and turn recurring reflections, moods, growth signals, and topic relationships into local reports. It is suited for users who already keep journal markdown files and want a generated insight dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may contain private diary-derived content in persistent local HTML, JavaScript, and JSON files.

Mitigation: Review generated outputs before sharing, keep the output directory access-restricted, and remove or redact sensitive journal content when needed.

Risk: The security review reports unsafe browser-script behavior and remote CDN/font loading in reports that may contain sensitive diary content.

Mitigation: Do not open sensitive generated reports until user content is safely escaped and remote dependencies are bundled locally or explicitly gated.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/smorzandos/skills/openclaw-diary-insights)
- [Project Homepage](https://github.com/openclaw-community/diary-system)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated JavaScript, JSON, and local HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent local diary insight outputs under ~/write_me/02notes/insights/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
