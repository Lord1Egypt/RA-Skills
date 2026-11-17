## Description:

Maps career-life stages to different investment priorities and guides users through a stage-specific investment audit and next-stage plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

People planning their careers use this skill to assess whether their current investments fit their career-life stage and identify a concrete investment and next-stage unlock plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to retain real-use failure patterns, which could expose private career details.

Mitigation: Remove the real-use example instruction or require explicit approval and anonymization before saving anything.

Risk: Users could mistake the career-stage age bands for validated developmental stages or apply them deterministically.

Mitigation: Treat age as a starting hypothesis, weigh behavioral evidence, and explain that the bands are practical defaults rather than empirically validated milestones.

## Reference(s):

- [Primary sources and framework caveats](references/sources.md)
- [Hesiod, Works and Days](https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0132)
- [Erikson, Childhood and Society](https://archive.org/details/childhoodsociety00erik)
- [Charles Darwin Project](https://www.darwinproject.ac.uk/)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown]

**Output Format:** [Markdown with a Lifestage Investment Audit and Next-Stage Unlock Plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Personalized using user-provided age and behavioral evidence; the skill says age bands are practical starting hypotheses, not validated developmental milestones.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
