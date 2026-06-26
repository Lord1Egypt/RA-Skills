## Description: <br>
法眼·AI合同审查 helps agents review contract text for legal risk patterns, unclear terms, compliance issues, and suggested revisions across multiple jurisdictions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, legal operations teams, and agents can use this skill to submit contract text for paid basic or pro review that returns risk counts, issue summaries, clause-level findings, and suggested changes. It is intended for contract screening support, not as a substitute for professional legal advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive contract text, personal data, commercial terms, or payment credentials could be exposed when sent to an unverified endpoint. <br>
Mitigation: Use only sanitized test data until the operator, HTTPS configuration, logging redaction, retention limits, and deletion controls are verified. <br>
Risk: The documented raw-IP HTTP endpoint does not provide transport encryption for contract or payment-related data. <br>
Mitigation: Prefer a verified HTTPS deployment and avoid submitting confidential material to raw HTTP endpoints. <br>
Risk: The deployment script performs privileged package, Nginx, systemd, certificate, and file-permission changes on the host. <br>
Mitigation: Read the script fully and run it only on a disposable or dedicated server after confirming each privileged change is acceptable. <br>
Risk: The review engine is rule and pattern based, so legal findings can be incomplete, jurisdictionally inaccurate, or overly broad. <br>
Mitigation: Treat generated findings as screening guidance and require review by qualified legal counsel before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-gaoqian/laweye-contract-review) <br>
- [Contract review data reference](artifact/references/contract-review.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions and JSON contract-review reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The service expects contract text and optional tier or jurisdiction inputs, and may require payment credentials before returning review results.] <br>

## Skill Version(s): <br>
2.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
