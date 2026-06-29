## Description: <br>
1Password (1password.com). Use this skill for ANY 1Password request - searching and reading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect a user's connected 1Password account through OOMOL, including listing vaults and item summaries and retrieving requested vault or item details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive 1Password vault and item data through a connected OOMOL integration. <br>
Mitigation: Install and use it only when that access is intended, and review requested 1Password actions before execution. <br>
Risk: Future connector actions marked write or destructive could change or remove 1Password data. <br>
Mitigation: Confirm the exact payload, target, and user approval before running any write or destructive action. <br>


## Reference(s): <br>
- [ClawHub 1Password Skill Page](https://clawhub.ai/oomol/oo-one-password) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [1Password](https://1password.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs the agent to inspect live connector schemas before running 1Password actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
