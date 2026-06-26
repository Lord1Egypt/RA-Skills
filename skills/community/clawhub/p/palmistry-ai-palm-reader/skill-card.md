## Description: <br>
AI-powered palm reading and analysis from palm images, with support for English, Tamil, Telugu, Kannada, and Hindi. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit a palm photo to ToolWeb for palmistry analysis, including heart line, head line, life line, fate line, mounts, and an overall reading in one of five supported languages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Palm photos and request metadata are sent to ToolWeb for processing. <br>
Mitigation: Use the skill only with consent from the person whose palm is uploaded, and avoid submitting images that should not be shared with ToolWeb. <br>
Risk: Successful API calls may count against a paid ToolWeb quota or billing plan. <br>
Mitigation: Use a dedicated or limited API key where possible and monitor quota, rate limits, and billing activity. <br>
Risk: The skill requires a ToolWeb API key in the agent environment. <br>
Mitigation: Store TOOLWEB_API_KEY as a secret, rotate it if exposed, and avoid placing it directly in shared configuration files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/palmistry-ai-palm-reader) <br>
- [ToolWeb API Portal](https://portal.toolweb.in) <br>
- [ToolWeb Platform](https://toolweb.in) <br>
- [ToolWeb Palmistry API Endpoint](https://portal.toolweb.in/apis/lifestyle/palmistry) <br>
- [ToolWeb OpenClaw Skills](https://toolweb.in/openclaw/) <br>
- [ToolWeb RapidAPI Profile](https://rapidapi.com/user/mkrishna477) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown palm-reading report with API request guidance and optional downloadable HTML report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY, curl, and a user-provided palm image encoded as base64.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
