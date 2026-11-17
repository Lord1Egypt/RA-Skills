## Description:

Checks primer sequences for basic Tm, GC content, and simplified hairpin and self-dimer signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, lab scientists, and developers use this skill to run a local primer quality check for qPCR, sequencing, or mutagenesis primer assessment before redesign decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release advertises off-target BLAST and template-genome validation, but the security evidence says the code does not implement those features.

Mitigation: Treat the output as a basic primer property check and verify off-target specificity with a validated BLAST or template-genome workflow before relying on results.

Risk: Primer decisions based only on simplified local checks can be misleading for experimental design.

Mitigation: Review primer inputs and outputs before use, and confirm final designs with domain-appropriate validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/primer-design-check)
- [AIPOCH publisher profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Console text report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports each primer sequence, length, Tm, GC content, hairpin warning, self-dimer warning, and pass/fail status.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
