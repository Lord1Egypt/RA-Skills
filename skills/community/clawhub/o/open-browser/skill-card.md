## Description: <br>
Automates complex multi-step browser tasks by visually interacting with pages using screenshots for clicks, typing, scrolling, and verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[softpudding](https://clawhub.ai/user/softpudding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to drive Chrome through the OpenBrowser local agent for multi-step page navigation, form filling, web scraping, UI testing, and browser task verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent high-impact browser and account authority. <br>
Mitigation: Use only with a browser profile the user is comfortable automating, and require explicit user confirmation before purchases, submissions, deletions, account changes, public posts, or other state-changing actions. <br>
Risk: The Chrome UUID functions as a capability token for controlling the browser. <br>
Mitigation: Keep the UUID private, avoid exposing it in shared logs or prompts, and refresh or rotate it when browser access should no longer be trusted. <br>
Risk: Long-running browser tasks can continue through background execution and may act on logged-in sessions. <br>
Mitigation: Monitor task logs and the browser window during execution, prefer non-sensitive sessions, and stop or delete stuck conversations before retrying. <br>


## Reference(s): <br>
- [OpenBrowser ClawHub page](https://clawhub.ai/softpudding/open-browser) <br>
- [OpenBrowser API Reference](references/api_reference.md) <br>
- [Setup Guide](references/setup.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands plus text or JSON status output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local OpenBrowser server, Chrome extension connection, DashScope API configuration, and a Chrome UUID capability token.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
