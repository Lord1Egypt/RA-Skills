## Description: <br>
Jimeng Skills helps an agent generate images and videos with Volcengine Jimeng AI and return plain-text results with local file paths, remote links, and optional public sharing links for enterprise messaging tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[klaus1534](https://clawhub.ai/user/klaus1534) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Jimeng image or video generation tasks and package the results for OpenClaw workflows in Feishu, WeCom, DingTalk, or similar enterprise messaging environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced Jimeng script and skill.yaml are not included in the artifact. <br>
Mitigation: Confirm those files come from a trusted source before installing or running the skill. <br>
Risk: The skill requires Volcengine credentials for Jimeng generation. <br>
Mitigation: Use temporary or least-privilege credentials where possible and avoid exposing VOLCENGINE_AK, VOLCENGINE_SK, or VOLCENGINE_TOKEN in logs or shared outputs. <br>
Risk: Public sharing links can expose generated files outside the local environment. <br>
Mitigation: Set JIMENG_PUBLIC_BASE_URL only when the generated files are intended to be publicly reachable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/klaus1534/jimeng-skills) <br>
- [Publisher profile](https://clawhub.ai/user/klaus1534) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text with optional shell command examples and JSON-like result fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns local file paths, remote URLs, optional public URLs, pending status text, and simple numbered text suitable for enterprise IM clients.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
