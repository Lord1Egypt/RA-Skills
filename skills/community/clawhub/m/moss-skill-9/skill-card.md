## Description: <br>
Give your AI agent eyes to see the entire internet by installing and configuring upstream access tools for social, video, code, RSS, and web sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangwzh](https://clawhub.ai/user/jiangwzh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to install, configure, check, and troubleshoot upstream platform tools for internet research and content access across Twitter/X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, Douyin, LinkedIn, Boss Zhipin, WeChat public articles, RSS, and general webpages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may request live browser cookies or extract local browser sessions for third-party platforms. <br>
Mitigation: Use a dedicated browser profile or throwaway accounts, avoid pasting raw cookies into chat, and only enable browser-cookie extraction after reviewing and trusting the upstream tools. <br>
Risk: The skill installs broad upstream tools that can access many external platforms. <br>
Mitigation: Review installation commands and run health checks before use; install only the channels needed for the current workflow. <br>
Risk: Some referenced upstream tools include social posting actions beyond setup and read-access workflows. <br>
Mitigation: Do not enable publishing actions unless explicitly required and approved for the account or workspace being used. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jiangwzh/moss-skill-9) <br>
- [Agent Reach upstream installer archive](https://github.com/Panniantong/agent-reach/archive/main.zip) <br>
- [Cookie-Editor Chrome Web Store listing](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell, Python, curl, and CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct agents to install upstream tools, configure cookies or proxies, run health checks, and call external platform tools directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
