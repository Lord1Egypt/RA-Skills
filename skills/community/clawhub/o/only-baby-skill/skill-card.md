## Description:

Analyze contraction JSON and baby log JSON to assess labour contraction patterns and baby feeding and diaper status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacklandrin](https://clawhub.ai/user/jacklandrin)

### License/Terms of Use:


## Use Case:

External users and caregivers use this skill to summarize contraction timing and baby feeding or diaper logs, compare them with documented thresholds, and receive a concise non-diagnostic status report with recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical-style safe or healthy verdicts could be mistaken for professional medical advice.

Mitigation: Keep the caveat explicit and direct users to contact a midwife, OB, paediatrician, emergency service, or other qualified professional for urgent symptoms, uncertainty, or red flags.

Risk: Incomplete or inaccurate contraction and baby-log JSON can lead to misleading summaries.

Mitigation: Base conclusions only on parsed user-provided records, state the relevant time window and counts, and recommend professional follow-up when data is missing or concerning.

## Reference(s):

- [OnlyBaby ClawHub skill page](https://clawhub.ai/jacklandrin/skills/only-baby-skill)
- [Data Schemas and Health/Safety Thresholds](references/schemas-and-thresholds.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with headings, bullet points, verdicts, supporting statistics, and a medical-advice caveat]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes user-provided JSON inputs and should keep medical-style labels non-diagnostic.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
