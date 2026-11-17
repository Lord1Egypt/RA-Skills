## Description:

Self-assess AI systems against the LGD three laws—registration, evidence, and gates—to produce a scorecard and practical improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

AI system owners, developers, and governance teams use the skill to assess identity and lineage records, evidence artifacts, and change gates, then review a scorecard and suggested gaps. Its heuristic results should be confirmed against evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heuristic scores are prompts for review, not independent certification.

Mitigation: Confirm findings against supporting evidence and treat the scorecard as a self-assessment.

Risk: The documented permission declarations are inconsistent and do not establish sandbox guarantees.

Mitigation: Use --system for text input where practical; otherwise provide only the intended answer file, restrict access to it, and avoid granting unused write or network tools.

## Reference(s):

- [LGD ecosystem hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [LGD theory](https://github.com/zhaoxinghua09-cell/LGD)
- [Formal paper (DOI)](https://doi.org/10.5281/zenodo.22456647)
- [UIBC protocol and reference implementation](https://github.com/zhaoxinghua09-cell/uibc-core)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [JSON scorecard or Markdown audit report; the rubric can also be printed as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a system description for heuristic assessment or a JSON answer file for scored checks; heuristic findings require confirmation.]

## Skill Version(s):

1.0.8 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
