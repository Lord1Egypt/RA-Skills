## Description: <br>
Privacy pipeline for OpenClaw that uses regex rules and Qwen2.5 to scrub PII such as names, emails, SSNs, phones, wallets, IPs, and paths before external AI processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solmas](https://clawhub.ai/user/solmas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manually anonymize OpenClaw message text before passing it to external AI services or workflow scripts. It is best suited for reviewed workflows because automatic hook interception is not working in the provided artifact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Redaction may miss some PII or return incomplete anonymization. <br>
Mitigation: Review redacted output before sending it to external APIs, especially for real customer or sensitive data. <br>
Risk: The configured Ollama endpoint receives privacy-sensitive text for name detection. <br>
Mitigation: Keep OLLAMA_URL on localhost or a trusted private Ollama instance. <br>
Risk: Automatic hook interception is unfinished and should not be relied on for protection. <br>
Mitigation: Use manual, reviewed workflows until the hook behavior is fixed and validated. <br>


## Reference(s): <br>
- [OpenClaw PII Anonymizer ClawHub page](https://clawhub.ai/solmas/openclaw-pii-anonymizer) <br>
- [Publisher profile](https://clawhub.ai/user/solmas) <br>
- [Artifact homepage](https://github.com/solmas/openclaw-pii-anonymizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text redacted output with Markdown documentation and bash usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Replaces detected PII with bracketed tokens such as [NAME], [EMAIL], [SSN], [PHONE], [WALLET], [IP], and [PATH].] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact version notes) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
