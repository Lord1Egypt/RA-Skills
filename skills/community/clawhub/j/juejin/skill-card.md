## Description: <br>
掘金平台自动化操作。支持发布沸点、查询话题列表等功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lang50](https://clawhub.ai/user/lang50) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate Juejin pin publishing, topic selection, and related account checks from a command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Juejin login cookie that can post to the user's account. <br>
Mitigation: Run it only for intentional posting workflows, protect the cookie like a password, and rotate or revoke the session if it is exposed. <br>
Risk: The artifact includes an unrelated EvoMap publishing and heartbeat script with an embedded secret and outbound behavior. <br>
Mitigation: Do not run scripts/publish_to_evomap.py unless that behavior is explicitly intended; remove or isolate it before deployment and rotate the exposed secret. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lang50/juejin) <br>
- [Juejin homepage](https://juejin.cn) <br>
- [Juejin short-message publish API](https://api.juejin.cn/content_api/v1/short_msg/publish) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, text, API calls] <br>
**Output Format:** [Markdown guidance with Python command invocations and script status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, network access, and a Juejin login cookie; metadata also declares curl.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
