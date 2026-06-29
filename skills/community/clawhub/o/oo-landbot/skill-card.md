## Description: <br>
Landbot (landbot.io) supports reading, creating, and updating Landbot data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Landbot through an OOMOL-connected account, including reading channels, customers, and message history. It can also prepare authenticated write actions such as sending text messages and updating typed customer fields after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated write actions can change Landbot state, including sending messages and updating customer fields. <br>
Mitigation: Inspect the live connector schema, confirm the exact payload and effect with the user, and run only after the user approves the write action. <br>
Risk: Setup or recovery commands can affect the active CLI authentication or connected account context. <br>
Mitigation: Run first-time setup steps only after a matching command failure, and confirm the intended account or connection before retrying. <br>


## Reference(s): <br>
- [ClawHub Landbot Skill](https://clawhub.ai/oomol/skills/oo-landbot) <br>
- [Landbot Homepage](https://landbot.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, PowerShell, text, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector actions may return JSON containing data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
