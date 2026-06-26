## Description: <br>
Create AI-powered videos via the Hooked Video API, including script-to-video, prompt-to-video, UGC ads, TikTok slideshows, avatar and voice selection, status checks, and trend discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ycfra](https://clawhub.ai/user/ycfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, marketers, and agent users use this skill to ask an agent to create, manage, and download Hooked videos or discover content trends through Hooked's API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video prompts, scripts, product links, or media may be sent to Hooked's external API. <br>
Mitigation: Avoid submitting secrets, confidential business data, regulated personal data, or private media unless the user intends to share it with Hooked. <br>
Risk: Creating videos can spend Hooked credits or incur account usage. <br>
Mitigation: Confirm with the user before actions that create videos or otherwise spend credits. <br>
Risk: API keys can be exposed if pasted into prompts, files, or command history. <br>
Mitigation: Keep the Hooked API key in an environment variable or secret store and avoid echoing it in generated output. <br>
Risk: Webhook callbacks can disclose video status and download URLs to the configured endpoint. <br>
Mitigation: Use webhooks only with endpoints the user controls or explicitly trusts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ycfra/hooked) <br>
- [Publisher Profile](https://clawhub.ai/user/ycfra) <br>
- [Hooked API Documentation](https://docs.hooked.so) <br>
- [Hooked Dashboard](https://hooked.so) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown with inline bash commands, JSON request examples, and API endpoint guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide the agent to make authenticated external API calls to Hooked and poll or receive webhook updates for generated videos.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
