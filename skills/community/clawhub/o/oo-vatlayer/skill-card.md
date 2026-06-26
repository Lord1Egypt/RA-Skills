## Description: <br>
VATlayer helps agents validate VAT numbers, retrieve EU VAT rates, list reduced-rate types, and calculate VAT-inclusive or VAT-exclusive prices through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for VAT validation, EU rate lookup, reduced-rate type lists, and VAT price calculations through their connected VATlayer account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected VATlayer API key brokered through OOMOL. <br>
Mitigation: Confirm trust in OOMOL as the credential broker and connect only the intended VATlayer account before use. <br>
Risk: One-time CLI install, login, or connection steps may be needed when authentication or connection errors occur. <br>
Mitigation: Run setup commands only when the corresponding command failure occurs, and avoid repeating authentication or connection steps unnecessarily. <br>


## Reference(s): <br>
- [ClawHub VATlayer Skill](https://clawhub.ai/oomol/oo-vatlayer) <br>
- [VATlayer Homepage](https://vatlayer.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed and authenticated oo CLI plus an OOMOL-connected VATlayer API key.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
