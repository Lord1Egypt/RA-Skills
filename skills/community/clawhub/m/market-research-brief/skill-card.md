## Description:

Turns field notes and survey answers into a US market research brief with fixed sections, word limits and a source for every number. Use when the user asks for market research brief template, primary market research writeup, survey findings summary. For US product managers, consultants and small business owners running primary research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US product managers, consultants, and small business owners use the skill to turn interview notes, survey responses, and published data into a traceable market research brief with documented sources, limits, and unanswered questions.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Research notes and survey answers may contain personal details or unsupported figures.

Mitigation: Use de-identified research, preserve sample sizes, and manually verify each numerical source before sharing the brief.

Risk: The helper replaces market-research-brief.md in its selected output directory.

Mitigation: Choose an output directory where replacing that file is acceptable.

Risk: The optional Windows executable is unsigned and is not covered by the security verdict.

Mitigation: The Python workflow does not require it; assess it separately before downloading or running it.

## Reference(s):

- [Market Research Sources](artifact/references/market-research-sources.md)
- [ClawHub skill release page](https://clawhub.ai/rapidworker1/skills/market-research-brief)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown research brief template and completeness/limits checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fixed sections and per-field word limits; sources and respondent counts accompany findings. The bundled helper reports missing or over-limit fields and does not generate a completed research brief.]

## Skill Version(s):

1.0.7 (source: frontmatter, server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
