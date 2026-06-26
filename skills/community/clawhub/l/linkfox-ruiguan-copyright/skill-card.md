## Description: <br>
This skill checks publicly accessible image URLs with LinkFox's Ruiguan copyright detection service and reports similar copyrighted works, rights-owner details, TRO history, and infringement risk indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External e-commerce sellers, designers, and their agents use this skill to screen publicly accessible images for potential copyright infringement before publication or product listing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image URLs submitted for checking are sent to LinkFox's copyright detection service. <br>
Mitigation: Use only public or approved image URLs, and avoid confidential assets or temporary signed links unless sharing them with LinkFox is explicitly approved. <br>
Risk: The skill requires a LinkFox API key for live checks. <br>
Mitigation: Configure a dedicated API key through LINKFOXAGENT_API_KEY and rotate or revoke it if exposure is suspected. <br>
Risk: The artifact describes an automatic feedback workflow that can send user feedback to a separate endpoint. <br>
Mitigation: Disable or ignore feedback submission unless users explicitly agree and sensitive details have been removed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-ruiguan-copyright) <br>
- [Ruiguan Copyright Detection API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables and concise narrative, with JSON or shell command output when the bundled script is run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a publicly accessible image URL and LINKFOXAGENT_API_KEY for live API calls; results are capped at 200 matches per query.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
