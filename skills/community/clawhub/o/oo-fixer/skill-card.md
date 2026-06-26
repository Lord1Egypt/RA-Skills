## Description: <br>
Connects an agent to Fixer exchange-rate data through the OOMOL oo CLI for latest rates, historical rates, and supported currency symbols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Fixer currency exchange-rate data, including latest rates, historical rates for a date, and supported currency symbols. It is intended for ClawHub users who have an OOMOL-connected Fixer account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Fixer account and may route Fixer-related requests through OOMOL. <br>
Mitigation: Install and use it only when that routing and account connection are acceptable for the user's exchange-rate workflow. <br>
Risk: Installer, login, or connection repair commands could change the local CLI setup or account state. <br>
Mitigation: Run one-time setup steps only after an action fails with the matching CLI, authentication, connection, or billing error. <br>
Risk: Fixer action payloads may be invalid if built from stale assumptions. <br>
Mitigation: Fetch the live action schema with oo connector schema before constructing a payload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-fixer) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Fixer homepage](https://fixer.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Fixer connector responses as JSON data with execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
