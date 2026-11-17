## Description:

Provides emotional support and submits health questions, text, and medical files to the Mentx.com API to generate auxiliary medical decision-support reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dj801117](https://clawhub.ai/user/dj801117)

### License/Terms of Use:

MIT-0

## Use Case:

External users in mainland China use this skill to ask health questions or submit medical images and reports for a Mentx.com auxiliary analysis report. The skill also provides non-diagnostic emotional support while the external report is generated.

### Deployment Geography for Use:

China (mainland)

## Known Risks and Mitigations:

Risk: Sensitive health questions and medical files may be sent to Mentx.com.

Mitigation: Obtain explicit user consent before sending data and confirm what data is transmitted, retained, and accessible.

Risk: Broad automatic triggering for casual health mentions may send data unexpectedly.

Mitigation: Require a deliberate user confirmation step before starting the external API task.

Risk: API keys and generated reports may be exposed on shared machines through shell startup files or temporary report storage.

Mitigation: Use a trusted single-user environment, avoid persistent shell-profile API keys when possible, and clear temporary report files after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dj801117/skills/mentx-doctor)
- [Mentx developer documentation](https://developer.mentx.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with shell command examples and API-generated report content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include emotional-support responses, emergency-care prompts for urgent symptoms, polling status, and an auxiliary report disclaimer.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
