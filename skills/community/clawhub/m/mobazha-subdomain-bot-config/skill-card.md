## Description: <br>
Set up a custom domain and Telegram Bot for a Mobazha store. Use when the user wants to configure DNS, TLS, or a Telegram Mini App storefront. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengzie](https://clawhub.ai/user/fengzie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and store operators use this skill to configure DNS, TLS, and Telegram Bot settings for a Mobazha storefront or Telegram Mini App. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the Mobazha installer or server configuration commands against the wrong host can change a live store environment. <br>
Mitigation: Use this only for a Mobazha store and server you control, verify the installer source, and require explicit consent before connecting to a server or running setup commands. <br>
Risk: Incorrect DNS values can route a storefront domain to the wrong server or delay TLS setup. <br>
Mitigation: Double-check DNS records and target IP addresses before changing registrar settings, then verify DNS and HTTPS after propagation. <br>
Risk: Telegram BotFather tokens grant access to bot configuration and should be treated as secrets. <br>
Mitigation: Use BotFather tokens only for the immediate configuration task, avoid logging or storing them, and transmit them only to the intended Mobazha store configuration target. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengzie/mobazha-subdomain-bot-config) <br>
- [Mobazha standalone installer](https://get.mobazha.org/standalone) <br>
- [BotFather](https://t.me/BotFather) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes credential-handling guidance for Telegram Bot tokens.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
