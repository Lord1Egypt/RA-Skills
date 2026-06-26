## Description: <br>
Táve (vsco.co). Use this skill for Táve requests involving searching and reading data through the OOMOL connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect the live Táve connector contract and run contact or studio read actions through an already connected OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected service account and sensitive credentials managed by OOMOL. <br>
Mitigation: Install only when the connector provider is trusted and the user intends the agent to operate the connected Táve account. <br>
Risk: The release is described as read-oriented, while the skill body includes guidance for possible write or destructive connector actions. <br>
Mitigation: Treat connector actions as potentially write-capable and require explicit confirmation before any create, update, delete, post, or account-changing action. <br>
Risk: Connector payloads can become stale if constructed without the live action schema. <br>
Mitigation: Run `oo connector schema "tave" --action "<action_name>"` before building payloads for connector execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-tave) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Táve homepage](https://www.vsco.co/workspace) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed oo CLI, OOMOL sign-in, and a connected Táve API key before connector actions can run.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
