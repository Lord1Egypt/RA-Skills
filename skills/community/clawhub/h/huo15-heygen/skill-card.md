## Description: <br>
Uses HeyGen to generate digital avatar videos from written scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jobzhao15](https://clawhub.ai/user/jobzhao15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to prepare HeyGen avatar video generation requests, check generation status, and retrieve completed video URLs for greetings, marketing shorts, product introductions, and batch video workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The HeyGen API key is stored in a local credentials file. <br>
Mitigation: Restrict the credentials file to the current user account and rotate the key if the file is exposed. <br>
Risk: Scripts sent through this skill are submitted to HeyGen and may consume paid API credits. <br>
Mitigation: Review script content before sending it to HeyGen and confirm account limits, rate limits, and expected costs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jobzhao15/huo15-heygen) <br>
- [HeyGen API base URL](https://api.heygen.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance] <br>
**Output Format:** [Markdown with Python and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local HeyGen credential file and may return HeyGen video IDs or download URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
