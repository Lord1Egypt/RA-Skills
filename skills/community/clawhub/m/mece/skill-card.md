## Description:

Guides an agent through MECE decomposition to structure complex questions into non-overlapping, exhaustive branches and identify where to focus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and strategy teams use the skill to structure complex problems, option sets, and market questions into clear branches. It helps check for overlap and missing cases, compare possible ways to divide the problem, and focus on the branches that matter most.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A decomposition may create misleading confidence if its categories overlap, leave gaps, or use the wrong dimension.

Mitigation: Check overlap and missing cases, sum the branches back to the defined whole, consider alternative dimensions, and independently verify important conclusions.

Risk: Documented failure examples could expose confidential details.

Mitigation: Avoid including confidential details when recording failure examples.

## Reference(s):

- [MECE skill page](https://clawhub.ai/deciqai/skills/mece)
- [MECE overview and examples](https://www.deciqai.com/c/mece)
- [Primary sources and supporting references](artifact/references/sources.md)
- [IBM Investor Relations](https://www.ibm.com/investor/)
- [NVIDIA Investor Relations](https://investor.nvidia.com/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown decomposition]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defines the whole, proposed branches, overlap and coverage checks, load-bearing branch, and action implications; depth adapts to the problem.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
