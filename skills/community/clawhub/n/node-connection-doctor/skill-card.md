## Description: <br>
Diagnoses OpenClaw node connection failures, recommends targeted CLI fixes, and can run confirmed repair steps for pairing tokens and gateway service issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huoxinjiang](https://clawhub.ai/user/huoxinjiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to troubleshoot failed node pairing, gateway status problems, VPN or connectivity failures, and related configuration errors. It provides diagnosis, command guidance, diagnostic reports, and optional confirmed repairs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic repair mode can reset pairing tokens and restart the OpenClaw gateway, interrupting pairing or active connectivity. <br>
Mitigation: Run diagnosis first, keep repair confirmation enabled, and back up OpenClaw configuration before applying fixes. <br>
Risk: The skill requests background scheduling permission. <br>
Mitigation: Grant cron or background permission only when scheduled monitoring is deliberately needed. <br>
Risk: Network, VPN, firewall, or certificate problems may require manual operator action. <br>
Mitigation: Use the diagnostic recommendations to verify VPN, Tailscale, firewall, DNS, and system time settings before running repair commands. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/huoxinjiang/node-connection-doctor) <br>
- [Publisher profile](https://clawhub.ai/user/huoxinjiang) <br>
- [Validation guide](references/validation-guide.md) <br>
- [FAQ](references/faq.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration instructions, Code] <br>
**Output Format:** [Markdown and console-style diagnostic guidance with inline shell commands and optional JSON or HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute OpenClaw CLI repair commands when the user confirms fix mode.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
