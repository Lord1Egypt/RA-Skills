## Description:

This Chinese-language skill helps government-procurement review committees classify live review disputes, compare similar complaint-decision handling patterns, assess complaint risk, and decide whether lawful clarification or objective supporting evidence is needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

Government-procurement review committee leads and members use the skill during live evaluation disputes to classify one disputed issue, compare similar complaint outcomes, and decide whether clarification, objective evidence, or rejection is warranted.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Users may treat similar administrative decisions as binding precedent or as a substitute for formal legal and procurement authority review.

Mitigation: State that similar cases are non-binding, require current law and case facts to control, and keep final decisions with the review committee or qualified reviewer.

Risk: Knowledge bases may be unavailable or may not contain a matching case, which could make a risk label unsupported.

Mitigation: Mark unsupported outputs as 依据待核, avoid assigning risk levels without cited anchors, and require human verification of laws and knowledge-base results.

Risk: Clarification requests could drift into allowing suppliers to change material bid content.

Mitigation: Limit clarification to existing bid content, require objective support such as brochures or test reports where appropriate, and record the rationale in the review report.

Risk: The skill can be misapplied outside mainland China government-procurement review disputes.

Mitigation: Perform a law-domain check, exclude engineering tendering and Hong Kong/Macau/Taiwan matters, and redirect out-of-scope disputes.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/chesaram/skills/gp-review-expert-caselaw)
- [评审专家即时指引方法论文档](artifact/references/expert-guidance-methodology.md)
- [评审争议类型体系](artifact/references/review-dispute-taxonomy.md)
- [Skill README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance card with concise tables and bullet decisions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language decision support; cites knowledge-base anchors when available and marks unresolved evidence as 依据待核.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, manifest.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
