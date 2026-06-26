## Description: <br>
Controls a user's local Chrome browser through the MCP chrome-devtools protocol for web navigation, Outlook mail review, content search, tab management, snapshots, screenshots, and form interactions after Chrome remote debugging and OpenClaw MCP are configured. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyun2000](https://clawhub.ai/user/yuyun2000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect an agent to a locally logged-in Chrome browser for browser automation, Outlook mail reading, and web content search tasks. It is intended for users who intentionally enable Chrome remote debugging and configure the chrome-devtools MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can access logged-in Chrome pages, email, private sites, and account data through the user's active browser session. <br>
Mitigation: Use a separate Chrome profile with only the accounts needed for the task, keep unrelated sensitive tabs closed, and require explicit approval before reading email, opening private sites, submitting forms, posting content, or changing account data. <br>
Risk: Leaving Chrome remote debugging enabled can continue exposing browser-control capabilities after the intended task. <br>
Mitigation: Disable Chrome remote debugging when finished and only enable it for sessions where browser automation is intentionally required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yuyun2000/m5stack-chrome-browser-control) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown instructions with JSON configuration snippets and MCP tool command flows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct browser actions against the user's active Chrome session and logged-in sites.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
