## Description:

Guides Chinese-language Liuyao and I Ching hexagram generation and interpretation using traditional texts and the user's question.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinlio](https://clawhub.ai/user/jinlio)

### License/Terms of Use:

MIT

## Use Case:

People seeking a Chinese-language Liuyao or I Ching reading can generate a hexagram using simulated coin tosses, a yarrow-stalk model, or manual input and receive an interpretation grounded in the included texts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Divination readings may be mistaken for reliable predictions or professional advice.

Mitigation: Treat readings as cultural or reflective guidance, not as a substitute for professional advice.

Risk: Broad divination-related keywords may activate the skill when it is not wanted.

Mitigation: Confirm the user wants a Liuyao reading before generating or interpreting a hexagram.

Risk: Generating hexagrams runs bundled local Python code.

Mitigation: Review the bundled script before allowing execution in your environment.

## Reference(s):

- [ClawHub release: liuyao-skill](https://clawhub.ai/jinlio/skills/liuyao-skill)
- [64 hexagrams quick reference](references/64gua-table.md)
- [Hexagram texts](references/guaci-full.md)
- [Line texts](references/yaoci-full.md)
- [Interpretation guide](references/jiegu-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese-language Markdown reading with hexagram details, traditional texts, interpretation, and suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled local script supplies hexagram data; the agent presents a question-specific reading.]

## Skill Version(s):

0.1.2 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
