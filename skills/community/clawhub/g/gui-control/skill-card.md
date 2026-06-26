## Description: <br>
Control the GUI desktop on this machine using xdotool, scrot, and Firefox. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vibes-me](https://clawhub.ai/user/vibes-me) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent open Firefox, navigate websites, type into focused windows, press keys, inspect active windows, and capture screenshots in a Linux GUI session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over the visible desktop, including opening Firefox, typing text, pressing keys, and closing browser processes. <br>
Mitigation: Use it only in an intended GUI session, supervise actions closely, and require explicit approval before passwords, account changes, purchases, deletion, posting, or other sensitive actions. <br>
Risk: Screenshot capture can expose private messages, credentials, account details, or other sensitive on-screen information. <br>
Mitigation: Avoid displaying sensitive information during use and review screenshots before sharing or storing them. <br>
Risk: Gateway use through Telegram or Discord can extend GUI control to external chat channels. <br>
Mitigation: Run gateway access only for trusted channels and users, and keep the same explicit approval rules for sensitive GUI actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vibes-me/gui-control) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Assumes DISPLAY=:1 with xdotool, scrot, and Firefox available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
