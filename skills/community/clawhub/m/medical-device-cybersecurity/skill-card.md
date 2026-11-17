## Description:

A working reference for medical device cybersecurity that helps teams prepare regulatory submissions and manage security after a device is in use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Medical device regulatory, engineering, and security teams use this skill to compare United States, European Union, and China requirements, prepare SBOMs and submission checklists, and organize post-market vulnerability handling. Treat it as a reference starter: verify current requirements and device applicability before relying on its guidance.

### Deployment Geography for Use:

Global (focus: United States, European Union, and China)

## Known Risks and Mitigations:

Risk: Regulatory requirements and their applicability to a specific device can change or vary.

Mitigation: Confirm current jurisdiction-specific guidance and device applicability before using the material in a submission or compliance decision.

Risk: The included vulnerability helper is a CVSS-style keyword heuristic and can misclassify severity.

Mitigation: Use a proper CVSS assessment and qualified review before making remediation decisions.

Risk: An SBOM can disclose sensitive software inventory information.

Mitigation: Review the SBOM contents and confirm recipients are authorized before sharing it.

Risk: The verifier reads skill-package files and overwrites its local reports.

Mitigation: Back up existing reports or run the verifier in a disposable copy of the package.

## Reference(s):

- [Regulatory overview](references/01-网络安全全景与监管.md)
- [United States FDA requirements](references/02-美国FDA网络安全要求.md)
- [European Union requirements](references/03-欧盟网络安全要求.md)
- [China NMPA requirements](references/04-中国NMPA网络安全要求.md)
- [SBOM practice](references/05-SBOM实操.md)
- [Vulnerability management and coordinated disclosure](references/06-漏洞管理与协调披露.md)
- [Cybersecurity program and documentation](references/07-网络安全体系与文档.md)
- [FAQ](references/08-FAQ.md)
- [ClawHub skill page](https://clawhub.ai/zhaoxinghua09-cell/skills/medical-device-cybersecurity)
- [Publisher homepage](https://zhaoxinghua09-cell.github.io/lgd-hub/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON configuration, Shell commands]

**Output Format:** [Markdown guidance and checklists, JSON SBOM templates, and command-line text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local toolkit prints results to standard output and does not scan networks or collect data.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
