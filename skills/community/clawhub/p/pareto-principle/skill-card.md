## Description:

Guides agents through measuring an outcome distribution, identifying its vital few contributors, and making an explicit decision about the long tail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

Teams and analysts use this skill to prioritize backlogs, resources, and initiatives by measuring which inputs contribute most to a clearly defined outcome. It guides them to check the actual distribution, document what to do with the long tail, and remeasure over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Assuming an 80/20 split without measuring the chosen outcome can lead to poor prioritization.

Mitigation: Measure and rank contributions for one precisely defined outcome, then report the observed ratio rather than assuming a canonical split.

Risk: Applying Pareto triage in safety-critical or regulated settings could leave required obligations unaddressed.

Mitigation: Do not use the method to deprioritize safety-critical obligations; review proposed cuts and verify consequential claims before acting.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/deciqai/skills/pareto-principle)
- [Source bibliography](references/sources.md)
- [Microsoft Office bug-fix example](examples/microsoft-office-bug-fix-pareto-2002.md)
- [Realized AI value example](examples/ai-value-concentration-2024-2026.md)
- [McKinsey State of AI](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai)
- [Stanford AI Index Report](https://aiindex.stanford.edu/report/)
- [Microsoft WinHEC 2002 keynote](https://news.microsoft.com/source/2002/04/18/gates-winhec-keynote-address-outlines-industrywide-vision-for-continued-vibrant-pc-ecosystem/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown Pareto Analysis and step-by-step guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The analysis depends on the user's chosen outcome, input set, contribution measurements, and review interval.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
