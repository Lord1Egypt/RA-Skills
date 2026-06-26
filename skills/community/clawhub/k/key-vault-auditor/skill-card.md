## Description: <br>
Audit Azure Key Vault configuration, access policies, and secret hygiene for credential exposure risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Security engineers and cloud platform teams use this skill to audit exported Azure Key Vault configuration, access policies, RBAC assignments, and secret hygiene for exposure risks. It helps produce findings, hardening guidance, secret rotation recommendations, and managed identity migration steps from user-provided read-only data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may share sensitive Azure Key Vault configuration metadata or accidentally include secret values, tokens, connection strings, or unrelated confidential data. <br>
Mitigation: Run Azure CLI commands yourself with read-only permissions and remove secret values, tokens, connection strings, and unrelated confidential data before sharing outputs with the agent. <br>
Risk: Generated hardening templates, rotation plans, or migration guidance could be applied without environment-specific review. <br>
Mitigation: Treat generated remediation content as a proposal and review it with cloud and security owners before applying changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anmolnagpal/key-vault-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with findings tables, Bicep code blocks, rotation plans, and migration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; analyzes user-provided read-only Azure CLI or console exports and does not request credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
