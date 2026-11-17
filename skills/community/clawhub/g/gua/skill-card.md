## Description:

易经起卦 casts I Ching hexagrams from natural-language questions with a bundled qi_gua.py script, then supports Chinese-first structured interpretation using local Zhouyi references and optional web lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crystalchen1017](https://clawhub.ai/user/crystalchen1017)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn a natural-language question into an I Ching hexagram result, then produce a structured Chinese interpretation grounded in local Zhouyi references and checked with relevant web sources when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search-sensitive personal details may be exposed when the skill performs web lookup for hexagram references.

Mitigation: Avoid including personal, medical, financial, relationship, or other sensitive details in prompts unless the user is comfortable with that exposure.

Risk: Divination output can be mistaken for a determinate answer or high-stakes advice.

Mitigation: Present readings as interpretive reference, distinguish source material from interpretation, and avoid treating the result as a certain conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crystalchen1017/skills/gua)
- [README](README.md)
- [Output format](references/output-format.md)
- [Pre-divination guidance](references/pre-divination-guidance.md)
- [Zhouyi 64 hexagram local reference](references/zhouyi-64-gua.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with plain-text hexagram output and reference links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first output that includes the question, hexagram graphic, primary and changed hexagrams, moving-line basis, targeted interpretation, and cited references.]

## Skill Version(s):

1.0.2 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
