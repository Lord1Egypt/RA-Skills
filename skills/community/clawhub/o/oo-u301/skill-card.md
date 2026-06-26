## Description: <br>
U301 helps agents list available short-link domains, create short links, and delete U301 links through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage U301 short links from an agent session, including listing available domains, creating shortened links, and deleting existing links after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on installing and running the external OOMOL oo CLI. <br>
Mitigation: Install only when the user trusts OOMOL and review the CLI installer before running it. <br>
Risk: The skill can create short links or delete existing links in a connected U301 account. <br>
Mitigation: Confirm write or destructive actions with the user after checking the exact short-link target, destination, domain, and slug. <br>
Risk: The skill requires a connected U301 account with sensitive credentials managed through OOMOL. <br>
Mitigation: Connect only the intended U301 account and resolve authentication, expired credential, or missing-scope errors through OOMOL connection settings. <br>


## Reference(s): <br>
- [U301 homepage](https://u301.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [OOMOL U301 connection settings](https://console.oomol.com/app-connections?provider=u301) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses include JSON data and an execution identifier when actions run successfully.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
