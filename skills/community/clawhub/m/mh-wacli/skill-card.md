## Description: <br>
Send WhatsApp messages to other people or search/sync WhatsApp history via the wacli CLI (not for normal user chats). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users use this skill when they explicitly want an agent to send WhatsApp messages to third parties or search and synchronize WhatsApp history through the wacli CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can send WhatsApp messages or files to a recipient through the user's account. <br>
Mitigation: Require explicit recipient and message or file path, then confirm those details before sending. <br>
Risk: Continuous sync and history backfill can expose or process WhatsApp chat history. <br>
Mitigation: Use sync or backfill only when needed, and treat returned chat history as sensitive user data. <br>
Risk: The skill depends on an externally installed wacli CLI package. <br>
Mitigation: Review the external package source and installation method before enabling the skill. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/mohdalhashemi98-hue/mh-wacli) <br>
- [wacli homepage](https://wacli.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use JSON-formatted CLI output when parsing wacli responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
