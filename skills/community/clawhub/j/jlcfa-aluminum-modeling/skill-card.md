## Description:

Builds and reviews JLCFA/JiaLiChuang FA aluminum alloy enclosure modeling attributes for manufacturable enclosure design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhoushoujianwork](https://clawhub.ai/user/zhoushoujianwork)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and engineers use this skill to convert aluminum enclosure requirements into JLCFA-oriented modeling notes, structured attributes, process checks, and open questions before CAD or ordering review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manufacturing guidance is advisory and based on transcribed JLCFA references that may not reflect current ordering requirements.

Mitigation: For expensive or order-critical enclosure decisions, verify dimensions, tolerances, materials, finishes, and acceptance with current JLCFA pages or an engineer.

Risk: Generated enclosure attributes may include assumptions when dimensions, shell model, quantity, finish, or production tolerances are missing.

Mitigation: Review the skill's assumptions and open questions before using the attributes for CAD work or manufacturing review.

## Reference(s):

- [JLCFA Aluminum Alloy Enclosure Reference](references/jlcfa-standards.md)
- [JLCFA Help Manual](https://www.jlcfa.com/help/44006)
- [JLCFA Process Parameters](https://ke.jlcfa.com/housing/11)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with JSON-like attribute blocks and optional SVG snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses millimeters, declares face-local coordinate assumptions, and can respond in Chinese when the user writes Chinese.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
