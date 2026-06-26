## Description: <br>
Create tamper-proof receipts for AI agent work by hashing artifacts or action manifests, sending them to api.mpps.io, and receiving an HSM-signed receipt without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gdlg-ai](https://clawhub.ai/user/gdlg-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create verifiable receipts for completed tasks, generated artifacts, workflow steps, releases, payments, or delivery events. It helps build an audit trail by recording hashes and minimal receipt metadata with an external attestation service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipt metadata is sent to mpps.io and may be retained for years. <br>
Mitigation: Submit only hashes and minimal non-sensitive labels or context needed for verification. <br>
Risk: Sensitive data could be exposed if secrets, customer data, raw prompts, or private source text are included in receipt context. <br>
Mitigation: Do not include secrets, customer data, raw prompts, or private source text in requests to the external attestation service. <br>
Risk: Hashes of short guessable secrets may be vulnerable to guessing. <br>
Mitigation: Avoid hashing short secrets directly; use larger payloads or an appropriate salt before creating a receipt. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gdlg-ai/mpps-attestation) <br>
- [mpps.io Skills Homepage](https://mpps.io/skills) <br>
- [mpps.io API Documentation](https://github.com/gdlg-ai/mpps.io/blob/main/docs/api.md) <br>
- [mpps.io Verification Documentation](https://github.com/gdlg-ai/mpps.io/blob/main/docs/verify.md) <br>
- [mpps.io Security Policy](https://github.com/gdlg-ai/mpps.io/blob/main/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces API request examples and verification guidance; receipt data is returned by the external mpps.io service.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
