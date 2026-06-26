## Description: <br>
Install, start, repair, and smoke-test a Windows QQ + NapCat + OpenClaw bridge. Use this when the user explicitly wants an end-to-end local QQ bot setup, needs NTQQ/NapCat downloaded from public sources, or needs an existing NapCat bridge fixed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyspot114514](https://clawhub.ai/user/sunnyspot114514) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install or repair a local Windows QQ bot bridge that connects NTQQ/NapCat to an OpenClaw agent through WSL and Docker. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local bridge can expose chat logs, configuration, tokens, and message-sending controls if installed on a shared or exposed machine. <br>
Mitigation: Install on a dedicated Windows machine or dedicated bot QQ account, review generated configuration and tokens, and restrict bridge, NapCat WebUI, and API services to localhost where possible. <br>
Risk: The bridge reads QQ chats and can send QQ messages through the configured account. <br>
Mitigation: Avoid personal QQ sessions and shared networks unless authentication, firewall rules, and service exposure have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunnyspot114514/napcat-qq-bridge-installer) <br>
- [NapCat QQ latest release API](https://api.github.com/repos/NapNeko/NapCatQQ/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline PowerShell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to create local runtime files, generated tokens, and health or smoke-test output on the user's Windows host.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
