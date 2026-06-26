## Description: <br>
Make AI-powered phone calls via Bland AI to book restaurants, make appointments, inquire about services, and report back with transcripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dru-ca](https://clawhub.ai/user/dru-ca) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to place outbound Bland AI calls for bookings, appointment inquiries, and service questions, then retrieve call status, transcripts, and summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real outbound calls through Bland AI and may incur usage costs or contact the wrong recipient. <br>
Mitigation: Confirm the phone number, task, expected cost, recording setting, and maximum duration before each call. <br>
Risk: Call transcripts, summaries, recordings, or call tasks may contain sensitive personal or business information. <br>
Mitigation: Avoid sending secrets, regulated personal data, or sensitive business details unless Bland AI privacy, retention, and consent requirements have been reviewed. <br>
Risk: Privacy and recording disclosures are not strong enough in the artifact. <br>
Mitigation: Make recording and consent expectations explicit before enabling call recording or using the skill in regulated contexts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dru-ca/phone-calls-bland) <br>
- [Bland AI App](https://app.bland.ai) <br>
- [Bland AI Dashboard](https://app.bland.ai/dashboard) <br>
- [Bland AI Billing Dashboard](https://app.bland.ai/dashboard/billing) <br>
- [Bland AI API Base](https://api.bland.ai/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text, JSON, Configuration] <br>
**Output Format:** [Command-line text and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BLAND_API_KEY; may return call IDs, status, transcripts, summaries, and recording URLs when recording is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
