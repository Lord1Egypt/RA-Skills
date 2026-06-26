## Description: <br>
Fetches NetEase Cloud Music personalized daily recommendations and public chart songs, with SMS-code login and optional scheduled push output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[T-Evan](https://clawhub.ai/user/T-Evan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and end users use this skill to log in to NetEase Cloud Music, retrieve personalized daily song recommendations or public charts, and format those results for manual or scheduled delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves reusable NetEase login cookies locally, which are sensitive account credentials. <br>
Mitigation: Protect or delete /root/.openclaw/workspace/secrets/netease_cookies.json when needed and avoid sharing the workspace with untrusted users. <br>
Risk: SMS login requires entering a phone number and verification code in the terminal. <br>
Mitigation: Use the login flow only in a private terminal and avoid entering phone numbers or SMS codes in shared sessions. <br>
Risk: A scheduled cron job can create recurring automated access to the NetEase account. <br>
Mitigation: Add the cron job only when recurring account access is intended and review or remove it when no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/T-Evan/netease-music-pusher) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style instructions and formatted plain-text song recommendation output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or reuse a local NetEase cookie file for authenticated daily recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
