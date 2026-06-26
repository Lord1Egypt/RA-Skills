## Description: <br>
BoxHero lets an agent read BoxHero inventory items, team information, and locations through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect BoxHero inventory data, including items, locations, and linked team information, from an already connected OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads BoxHero inventory data through a connected account. <br>
Mitigation: Install and use it only when the user trusts OOMOL and intends to grant agent access to that BoxHero inventory data. <br>
Risk: First-time setup may require running an external oo CLI installer. <br>
Mitigation: Review the installer URL before running setup, and run setup only when the oo command is missing or authentication fails. <br>


## Reference(s): <br>
- [ClawHub BoxHero skill page](https://clawhub.ai/oomol/oo-boxhero) <br>
- [BoxHero homepage](https://www.boxhero-app.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL BoxHero connection settings](https://console.oomol.com/app-connections?provider=boxhero) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector runs return JSON with data and meta.executionId when executed through the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
