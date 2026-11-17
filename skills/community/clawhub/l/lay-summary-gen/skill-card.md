## Description:

Converts complex medical abstracts into plain-language summaries for patients, caregivers, and the general public while preserving scientific accuracy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ewankeynes](https://clawhub.ai/user/ewankeynes)

### License/Terms of Use:

MIT-0

## Use Case:

External health communicators, patient education teams, and developers can use this skill to turn medical research abstracts into patient-friendly summaries with key takeaways and jargon substitutions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated lay summaries may omit nuance or introduce medically misleading simplifications.

Mitigation: Require human review by an appropriate subject-matter reviewer before sharing summaries with patients, caregivers, or the public.

Risk: Users may mistake generated summaries for medical advice.

Mitigation: Present outputs as educational drafting aids and avoid using them as a substitute for clinician guidance.

Risk: Future file input or output support could create path or overwrite risks.

Mitigation: Confirm path validation and overwrite behavior before enabling file-based workflows.

## Reference(s):

- [Lay Summary Gen References](artifact/references/guidelines.md)
- [ClawHub skill page](https://clawhub.ai/ewankeynes/skills/lay-summary-gen)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON object containing a lay summary, reading level, key takeaways, word counts, target audience, and replaced jargon.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default maximum summary length is 250 words unless the caller supplies another limit.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
