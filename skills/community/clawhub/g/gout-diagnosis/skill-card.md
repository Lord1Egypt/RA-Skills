## Description:

Chinese-language gout likelihood assessment skill that scores 16 clinical elements and returns a reference-only gout probability recommendation that does not replace clinician diagnosis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenlcj](https://clawhub.ai/user/kenlcj)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to organize gout-related symptom, lab, and imaging details into a transparent 16-item scoring table before consulting a clinician. It is intended as an informational checklist and likelihood assessment, not a medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may rely on the checklist as a diagnosis or delay urgent clinical care.

Mitigation: State that the output is not a diagnosis and direct users to a clinician, especially for fever, severe trauma, rapidly worsening symptoms, suspected infection, or abnormal imaging.

Risk: The skill processes user-provided medical details and may produce misleading results if information is incomplete or unclear.

Mitigation: Ask follow-up questions for missing elements and make uncertainty visible in the scoring table and conclusion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kenlcj/skills/gout-diagnosis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown scoring table with total score and diagnostic guidance text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask follow-up questions for missing clinical elements and should preserve the clinician-diagnosis caveat.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
