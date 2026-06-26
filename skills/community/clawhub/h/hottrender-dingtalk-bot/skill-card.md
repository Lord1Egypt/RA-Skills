## Description: <br>
Use when users need a lightweight HotTrender crawler for four-region daily hotspot trends or custom keyword/vertical hotspot discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[7487](https://clawhub.ai/user/7487) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run or configure a small local crawler for daily hotspot trends across Japan, the United States, Taiwan, and Korea, or for custom keyword and vertical hotspot discovery. It helps agents prefer the bundled runtime and provider scripts before proposing code changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live web requests through Google, YouTube, X, and optional TikTok providers. <br>
Mitigation: Use offline provider mode for deterministic local validation, then enable real providers intentionally and inspect explicit provider errors instead of substituting sample data. <br>
Risk: Optional TikTok crawling can require session tokens, browser automation, and proxy configuration. <br>
Mitigation: Enable TikTok only deliberately, keep TIKTOK_MS_TOKEN, cookies, and proxy credentials out of logs and commits, and avoid untrusted proxies. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/7487/hottrender-dingtalk-bot) <br>
- [Setup And Portability](references/setup.md) <br>
- [Command Reference](references/commands.md) <br>
- [Basic Crawler Capability Map](references/capabilities.md) <br>
- [Extension Policy](references/extension-policy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated Markdown or JSON crawler reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled runtime writes local Markdown reports and sibling JSON records for crawler outputs.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
