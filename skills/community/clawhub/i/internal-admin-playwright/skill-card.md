## Description: <br>
Internal Admin Playwright automates controlled access to internal admin panels with Python and Playwright, configurable L2TP/IPsec VPN access, domain whitelisting, Chinese command routing, and fixed menu workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wulooongcha](https://clawhub.ai/user/wulooongcha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized internal developers and operators use this skill to run predefined Playwright workflows against an internal admin panel, including VPN setup, login, menu navigation, and comment moderation flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled admin or VPN credentials may expose sensitive access if used as-is. <br>
Mitigation: Remove and rotate bundled credentials before installation, and supply production secrets through approved environment variables or secret management. <br>
Risk: Whitelist enforcement may not cover every request type, allowing supporting browser traffic outside the intended boundary. <br>
Mitigation: Audit and tighten whitelist handling before use, especially for non-document requests and externally loaded resources. <br>
Risk: VPN setup can modify system-wide routing and network services on the host. <br>
Mitigation: Run VPN operations only on an isolated machine or container where route changes and service restarts are acceptable. <br>
Risk: Debug logging, screenshots, and saved HTML may capture sensitive admin content. <br>
Mitigation: Disable, redact, or securely retain debug artifacts according to the operating team's data-handling requirements. <br>
Risk: Privileged moderation workflows can take admin actions automatically. <br>
Mitigation: Restrict execution to authorized operators, keep command mappings under review, and test moderation rules before production use. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Menu Map](references/menu_map.yaml) <br>
- [Review Rules](references/rules.json) <br>
- [Team Configuration Template](references/team-template.md) <br>
- [VPN Configuration](references/vpn_config.yaml) <br>
- [Domain Whitelist](references/whitelist.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run Playwright browser automation and VPN commands when invoked by an authorized agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
