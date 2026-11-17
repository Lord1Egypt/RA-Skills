## Description:

Pans Meeting Summarizer generates structured sales meeting notes, action items, customer insights, and follow-up suggestions from meeting audio or transcript text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams and account teams use this skill to turn customer meeting audio or transcripts into follow-up notes, decisions, action items, and sales-oriented customer insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting audio and transcripts may contain confidential customer or sales information that is processed through OpenAI-backed tooling.

Mitigation: Use only when organizational data-handling policy permits that flow, and avoid highly confidential customer calls unless approved.

Risk: Generated meeting summaries, action items, and customer insights may be incomplete or inaccurate.

Mitigation: Review generated summaries before relying on them, sharing them, or using them for CRM follow-up.

Risk: The documented CRM synchronization path is not implemented in the artifact script.

Mitigation: Treat CRM sync output as unavailable until the integration is implemented and tested.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown or JSON meeting summary content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include meeting summaries, action item tables, customer insights, follow-up suggestions, and fallback metadata when API-backed summarization is unavailable.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
