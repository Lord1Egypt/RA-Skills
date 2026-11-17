## Description:

Automates controlled access to internal admin panels with Python and Playwright, using configurable L2TP/IPsec VPN access, a domain whitelist, and preconfigured Chinese command routes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wulooongcha](https://clawhub.ai/user/wulooongcha)

### License/Terms of Use:

MIT-0

## Use Case:

Internal operations and engineering teams use this skill to run preconfigured Playwright navigation and moderation workflows against an authorized internal admin panel after configuring VPN access, allowed hosts, and credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports packaged VPN or admin credentials and possible exposure of real secrets.

Mitigation: Do not use packaged credentials; rotate any real VPN or admin credentials that may have been exposed before installation or execution.

Risk: The security assessment says the VPN helper can make broad host networking changes, including global /etc updates, default-route replacement, and broad process termination.

Mitigation: Run only in a disposable or dedicated environment unless the VPN helper is rewritten to avoid global system changes and broad process termination.

Risk: The security guidance identifies shell injection risk, OTP logging, and unsanitized debug captures.

Mitigation: Review and harden command execution, disable sensitive debug logging, sanitize captured pages, and avoid storing OTPs or secrets in logs or debug artifacts.

Risk: The skill can perform admin-panel and moderation actions with weak safeguards if commands or menu routes are misconfigured.

Mitigation: Restrict use to authorized internal operators, keep command routes and allowlists under review, and require human approval before deploying changes to live admin workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wulooongcha/skills/internal-admin-playwright)
- [Command route map](references/menu_map.yaml)
- [Domain whitelist configuration](references/whitelist.yaml)
- [VPN configuration](references/vpn_config.yaml)
- [Team configuration template](references/team-template.md)
- [Moderation rules](references/rules.json)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, text]

**Output Format:** [Markdown with shell command examples, configuration guidance, and execution status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided credentials, OTP, VPN settings, domain whitelist, and preconfigured command routes before execution.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
