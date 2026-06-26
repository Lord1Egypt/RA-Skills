## Description: <br>
Seal AI agent actions with Ed25519 cryptographic receipts. Verify what your agent did and prove what it chose not to do. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hellothere012](https://clawhub.ai/user/hellothere012) <br>

### License/Terms of Use: <br>
BSL-1.1 <br>


## Use Case: <br>
Developers and agent operators use this skill to seal, verify, and look up tamper-evident receipts for AI agent actions, including counterfactual records of actions the agent declined to take. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Action metadata and payload hashes are sent to a third-party signing service. <br>
Mitigation: Confirm this data flow is acceptable, send only minimal payloads, and review tier-specific retention settings before production use. <br>
Risk: Payloads can contain sensitive fields if callers skip sanitization. <br>
Mitigation: Run the included sanitize_payload helper before sealing user or operational data, and extend its blocked fields for local policy requirements. <br>
Risk: Production API credentials can be exposed through agent configuration or logs. <br>
Mitigation: Protect NOTARY_API_KEY as a secret, avoid logging it, and rotate it if disclosure is suspected. <br>
Risk: The external SDK package is installed at runtime from a package registry. <br>
Mitigation: Pin or verify the notaryos package version when higher supply-chain assurance is required. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/hellothere012/notaryos) <br>
- [NotaryOS homepage](https://github.com/hellothere012/notaryos) <br>
- [NotaryOS documentation](https://notaryos.org/docs) <br>
- [NotaryOS API docs](https://notaryos.org/api-docs) <br>
- [NotaryOS PyPI package](https://pypi.org/project/notaryos/) <br>
- [NotaryOS npm package](https://www.npmjs.com/package/notaryos) <br>
- [NotaryOS privacy policy](https://notaryos.org/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces receipt-sealing and verification guidance for use with the NotaryOS SDK and included payload sanitizer.] <br>

## Skill Version(s): <br>
2.4.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
