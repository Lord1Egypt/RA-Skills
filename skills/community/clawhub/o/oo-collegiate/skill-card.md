## Description: <br>
Provides Merriam-Webster Collegiate dictionary lookups and spelling suggestions through the OOMOL collegiate connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up words in Merriam-Webster Collegiate from an OOMOL-connected account, using the live connector schema before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lookup requests and account connection depend on OOMOL as an intermediary for Merriam-Webster Collegiate access. <br>
Mitigation: Use the skill only when OOMOL intermediary access is acceptable; OOMOL handles credentials server-side so agents should not request or store raw API tokens. <br>
Risk: The skill may fail until the oo CLI, OOMOL sign-in, Merriam-Webster connection, or OOMOL billing state is configured. <br>
Mitigation: Run setup or recovery steps only after the matching command failure, then resolve authentication, connection, credential, or billing errors before retrying. <br>
Risk: Connector payloads can become invalid if the live action contract changes. <br>
Mitigation: Inspect the live connector schema before each action and send JSON that matches the returned contract. <br>


## Reference(s): <br>
- [Merriam-Webster Collegiate homepage](https://www.merriam-webster.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-collegiate) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches the live OOMOL connector schema before execution; the documented action is the read-only lookup_word operation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
