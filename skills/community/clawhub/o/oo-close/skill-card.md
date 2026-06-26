## Description: <br>
Operates Close through the OOMOL-connected close connector for reading, creating, and updating CRM records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use this skill to let an agent inspect schemas and then read or update Close CRM leads, contacts, opportunities, and tasks through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and update Close CRM data through an OOMOL-connected account. <br>
Mitigation: Install it only when that access is intended, and review write payloads and expected effects before approving state-changing actions. <br>
Risk: Setup commands may be needed if the oo CLI or account connection is missing. <br>
Mitigation: Use setup commands only from OOMOL's documented source and only after an auth, connection, or missing CLI error occurs. <br>


## Reference(s): <br>
- [Close homepage](https://www.close.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-close) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Close connector JSON responses that include data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
