## Description: <br>
Cardly (card.ly) helps agents search and read Cardly account data through the OOMOL Cardly connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to retrieve Cardly balances, credit history, available media, fonts, and writing styles from an OOMOL-connected Cardly account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup, login, Cardly connection, billing, or echo-debugging steps can affect the user's account or environment. <br>
Mitigation: Approve those steps explicitly, and avoid sending sensitive personal data in echo payloads unless intentionally testing the authenticated endpoint. <br>


## Reference(s): <br>
- [ClawHub Cardly skill page](https://clawhub.ai/oomol/skills/oo-cardly) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Cardly homepage](https://www.card.ly) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector action responses are JSON objects containing data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
