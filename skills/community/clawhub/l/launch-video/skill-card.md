## Description: <br>
Make a launch video for your startup or product with Pexo by relaying a product brief, landing-page URL, screenshot, or uploaded media to the hosted Pexo video agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pexo](https://clawhub.ai/user/pexo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, founders, marketers, and product teams use this skill to submit launch-video requests to Pexo, upload supporting media, monitor production, and retrieve the final video asset URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product briefs, screenshots, URLs, and uploaded media are sent to Pexo for remote processing. <br>
Mitigation: Do not upload secrets, sensitive internal content, private customer data, or media that should not be shared with Pexo. <br>
Risk: The skill requires a PEXO_API_KEY stored in ~/.pexo/config or provided through the environment. <br>
Mitigation: Protect the config file, avoid pasting the key into chats or logs, and rotate the key if it may have been exposed. <br>
Risk: Creating projects and requesting production may consume Pexo credits. <br>
Mitigation: Confirm the user wants to start production and check credit or entitlement status before retrying after credit-related failures. <br>


## Reference(s): <br>
- [Launch Video on ClawHub](https://clawhub.ai/pexo/launch-video) <br>
- [Pexo](https://pexo.ai) <br>
- [Setup Checklist](references/SETUP-CHECKLIST.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON command responses, project links, and final asset URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Pexo project IDs, uploaded asset IDs, preview selections, polling status, credit guidance, and signed final asset URLs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
