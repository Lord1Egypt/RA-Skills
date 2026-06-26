## Description: <br>
Cincopa (cincopa.com). Use this skill for ANY Cincopa request - searching and reading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect Cincopa account data through an OOMOL-connected account, including assets, galleries, gallery items, and asset tag clouds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Cincopa account and uses OOMOL as an intermediary for read access. <br>
Mitigation: Use it only with accounts and data that are approved for access through OOMOL, and review the OOMOL connection before use. <br>
Risk: The setup path includes remote shell installer commands for the oo CLI. <br>
Mitigation: Review OOMOL's official installation guidance before running an installer, and avoid executing remote shell commands blindly. <br>
Risk: Connector payloads may become stale if action schemas change. <br>
Mitigation: Inspect the live Cincopa connector schema before constructing each payload. <br>


## Reference(s): <br>
- [Cincopa homepage](https://www.cincopa.com/) <br>
- [OOMOL oo CLI repository](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs agents to inspect the live connector schema before running read-only Cincopa actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
