## Description: <br>
Mails helps agents validate email addresses and manage Mails batch validation jobs through an OOMOL-connected Mails account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to validate single email addresses, create batch validation jobs, and retrieve batch validation results from Mails via their connected OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive account access through the connected OOMOL Mails account. <br>
Mitigation: Install it only when the agent should use that account for email validation tasks, and rely on OOMOL server-side credential handling rather than exposing raw tokens. <br>
Risk: Batch validation creation is a write action that can affect the connected Mails account or consume account resources. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write actions. <br>
Risk: CLI installation and account connection steps change local or account setup. <br>
Mitigation: Run setup only after an authentication or connection failure and only when OOMOL and the connector are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-mails-so) <br>
- [Mails homepage](https://mails.so) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [OOMOL Mails connection](https://console.oomol.com/app-connections?provider=mails_so) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful connector runs return JSON with data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release and frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
