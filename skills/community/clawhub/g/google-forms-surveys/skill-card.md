## Description: <br>
Google Forms API integration with managed OAuth. Create forms, inspect structure, review responses, change publishing settings, and manage response notification watches. Use this skill when users want to create surveys, collect responses, or manage Google Forms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect a Google account through ClawLink, discover available Google Forms tools, create and update forms, review responses, manage publishing settings, and manage response notification watches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives OpenClaw agents access to Google Forms through a connected Google account. <br>
Mitigation: Install only when this access is intended, and disconnect the Google account when the integration is no longer needed. <br>
Risk: Write or destructive actions can affect sharing, publishing, deletion, batch changes, or response watches. <br>
Mitigation: Review each preview before approving write actions, and remove response watches when they are no longer needed. <br>


## Reference(s): <br>
- [Google Forms API Overview](https://developers.google.com/forms/api) <br>
- [Forms Resource](https://developers.google.com/forms/api/reference/rest/v1/forms) <br>
- [Form Responses Reference](https://developers.google.com/forms/api/reference/rest/v1/forms.responses) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [Google Forms Skill on ClawHub](https://clawhub.ai/hith3sh/google-forms-surveys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown with shell command examples and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ClawLink OAuth connection and user confirmation before write or destructive actions.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
