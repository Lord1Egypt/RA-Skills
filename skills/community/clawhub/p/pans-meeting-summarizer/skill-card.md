## Description: <br>
AI sales meeting summarization tool that turns meeting audio or transcripts into structured minutes, action items, and customer insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashiming](https://clawhub.ai/user/dashiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales teams and account managers use this skill after customer calls to generate follow-up notes, action items, and sales-oriented customer insights from audio recordings or text transcripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting audio or transcripts may be processed through OpenAI services. <br>
Mitigation: Use only recordings and transcripts approved for OpenAI processing, avoid regulated or highly confidential meetings without review, and use a dedicated OpenAI API key with spending controls. <br>
Risk: CRM synchronization is advertised but not implemented in this release. <br>
Mitigation: Treat CRM sync as unavailable and manually verify follow-up records until a future version documents a working CRM integration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dashiming/pans-meeting-summarizer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON meeting summaries written to stdout or an output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs structured meeting minutes, action items, customer insights, and follow-up suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
