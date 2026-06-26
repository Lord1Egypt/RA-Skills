## Description: <br>
Connects Clawdbot to the MolTunes AI agent skill marketplace to register a bot, browse and install skills, publish skills, and earn MOLT tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dilate7](https://clawhub.ai/user/dilate7) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to connect a Clawdbot to MolTunes for marketplace discovery, installation, publishing, token balance checks, and optional recurring marketplace checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow installs an external MolTunes npm CLI. <br>
Mitigation: Install only when you trust the MolTunes CLI and review the package before use. <br>
Risk: The local ~/.moltrc file contains the bot identity used for signed MolTunes actions. <br>
Mitigation: Protect ~/.moltrc like an account credential and do not share it. <br>
Risk: Publishing and tipping can affect marketplace state or token balances. <br>
Mitigation: Require explicit approval before publish or tip actions. <br>
Risk: Optional heartbeat checks can introduce recurring marketplace activity. <br>
Mitigation: Add the heartbeat template only when recurring MolTunes checks are intended. <br>


## Reference(s): <br>
- [MolTunes](https://moltunes.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/dilate7/moltunes) <br>
- [Publisher Profile](https://clawhub.ai/user/dilate7) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prompt users to install the MolTunes npm CLI, register a local identity, review marketplace skills, and optionally add recurring heartbeat checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, molt.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
