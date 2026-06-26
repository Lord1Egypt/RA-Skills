## Description: <br>
Moses Audit provides a SHA-256 chained, append-only local governance ledger for logging agent actions and verifying tamper-evident audit history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SunrisesIllNeverSee](https://clawhub.ai/user/SunrisesIllNeverSee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Moses Audit to log governed agent actions into a local chained ledger, review recent entries, and verify chain integrity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes persistent local audit and governance files, including recovery-state updates beyond simple logging. <br>
Mitigation: Install only when a local audit ledger is desired; review the documented state directories and require clear controls for retention and recovery flags. <br>
Risk: MOSES_OPERATOR_SECRET is required for local HMAC attestation. <br>
Mitigation: Provide the secret only in controlled environments, do not include it in ledger details or command history, and rotate it if exposure is suspected. <br>
Risk: The freeform detail field can capture sensitive operational data if users paste secrets, tokens, private keys, or PII. <br>
Mitigation: Log action descriptions and outcomes only; avoid raw secrets, credentials, private keys, and personal data. <br>


## Reference(s): <br>
- [Moses Audit release page](https://clawhub.ai/SunrisesIllNeverSee/moses-audit) <br>
- [Publisher profile](https://clawhub.ai/user/SunrisesIllNeverSee) <br>
- [MOSES origin DOI](https://zenodo.org/records/18792459) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline tool-call examples and bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill writes local JSONL audit entries and prints status text for log, verify, and recent commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact metadata.openclaw.version is 0.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
