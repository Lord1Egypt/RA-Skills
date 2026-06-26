## Description: <br>
Infrastructure as Code security auditor for Terraform (.tf), CloudFormation (YAML/JSON), and Pulumi (TypeScript/Python) that detects high-impact cloud misconfigurations and supports CI fail-gating without external scanner dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers, DevOps engineers, and security reviewers use this skill to scan Terraform, CloudFormation, and Pulumi infrastructure files for common AWS misconfigurations before merge or deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill is a lightweight local Terraform-oriented checker and may overstate coverage for CloudFormation, Pulumi, and Lambda trust-policy assurance. <br>
Mitigation: Use it as one local signal, not as a comprehensive IaC security gate, and pair clean results with established IaC security scanners and human review for production changes. <br>
Risk: Scan output may include secret-like snippets from infrastructure files. <br>
Mitigation: Keep reports private, avoid posting findings in public logs, and rotate any exposed credentials found during review. <br>


## Reference(s): <br>
- [Canlah AI homepage](https://canlah.ai) <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-iac-sec-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and security findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local static-analysis guidance and CI usage instructions; no external API calls are required by the documented script.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
