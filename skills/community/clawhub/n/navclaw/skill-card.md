## Description: <br>
NavClaw is an Amap-based driving route planner that searches many congestion-avoidance options and returns route comparisons with one-tap iOS and Android navigation links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AI4MSE](https://clawhub.ai/user/AI4MSE) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Drivers and agent users use NavClaw to compare Amap driving routes, identify congestion-avoidance alternatives, and open the selected route in a mobile navigation app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle Amap keys, optional Mattermost bot tokens, home/default destinations, exact route data, and trip logs. <br>
Mitigation: Prefer local output with --no-send, avoid storing secrets in long-term memory, and review or delete generated logs after private trips. <br>
Risk: When Mattermost posting is configured, route results and log attachments can be sent automatically to the configured channel. <br>
Mitigation: Use a low-privilege Mattermost bot, verify the target channel is private and correct, and disable posting unless sharing is intended. <br>


## Reference(s): <br>
- [ClawHub NavClaw release](https://clawhub.ai/AI4MSE/navclaw) <br>
- [Amap Open Platform](https://lbs.amap.com/) <br>
- [Technical documentation](docs/technical_EN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style route summaries, plain-text logs, and mobile navigation deep links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include route comparison tables, final recommendations, iOS/Android deep links, stdout output, and optional Mattermost messages or log attachments.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
