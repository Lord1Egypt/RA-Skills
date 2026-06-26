## Description: <br>
PAN-OS zone-based security policy audit with App-ID/Content-ID analysis, Security Profile Group validation, zone protection assessment, and decryption policy review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network security engineers, firewall administrators, and auditors use this skill to perform read-only PAN-OS security policy audits, assess App-ID and Content-ID coverage, validate Security Profile Group and zone protection coverage, and produce prioritized remediation findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Firewall or Panorama API credentials and audit output may expose sensitive network security data. <br>
Mitigation: Use a dedicated low-privilege read-only account, store PAN_API_KEY as a secret, avoid placing credentials in URLs or logged commands, and rotate any credential that may have been exposed. <br>
Risk: Audit results can be misleading when content signatures, running configuration, or Panorama hierarchy data are stale or incomplete. <br>
Mitigation: Verify content update status, evaluate the committed running configuration and effective managed-firewall rulebase, and validate representative traffic with read-only policy-match commands. <br>


## Reference(s): <br>
- [PAN-OS CLI and API Reference - Audit Commands](references/cli-reference.md) <br>
- [PAN-OS Security Policy Evaluation Chain](references/policy-model.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown audit guidance with inline PAN-OS CLI and API commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only audit procedures, finding severity guidance, and a report template for PAN-OS firewall policy review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
