## Description: <br>
Create, discover, and coin Lingry words with a local Sugarchain wallet, explicit terminal approval, and no wallet-passphrase exposure to OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[svetlyoh](https://clawhub.ai/user/svetlyoh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Lingry users use this skill to check Lingry service status, list public words, prepare account-bound word candidates, and prepare coining or starter-grant requests while keeping wallet signing in a private terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan marks the release suspicious because it involves wallet and API-session credentials and references helper files that are not present in this package. <br>
Mitigation: Review the installed package before use, confirm the expected Lingry helper files are present from a trusted source, and avoid running missing or substituted helper code. <br>
Risk: Wallet private keys, passphrases, session tokens, and local credential files could be exposed if users paste them into chat or store them in unsafe locations. <br>
Mitigation: Keep secrets in a private terminal flow only, do not paste them into chat, and treat ~/.openclaw/.env and ~/.lingry as sensitive local credential locations. <br>
Risk: Prepared coining, grant, or payment requests could be mistaken for completed blockchain actions. <br>
Mitigation: Require explicit terminal review and approval for signing or broadcasting, and report success only when the Lingry API or node response confirms it. <br>


## Reference(s): <br>
- [Server-resolved source import](https://github.com/svetlyoh/web-wallet/tree/master/openclaw/skills/lingry) <br>
- [Lingry website](https://lingry.net) <br>
- [ClawHub skill page](https://clawhub.ai/svetlyoh/skills/lingry) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise status or setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May refer to optional Lingry environment variables and local wallet/session state; must not print or request secrets.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; artifact frontmatter reports 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
