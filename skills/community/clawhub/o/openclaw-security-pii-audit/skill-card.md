## Description: <br>
Multi-region async PII detection for OpenClaw sessions across CN, US, AU, UK, DE, FR, SG, MY, TH, and ID, covering phone numbers, emails, names, addresses, passports, bank cards, national IDs, and social accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtoby8326](https://clawhub.ai/user/mtoby8326) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security or privacy reviewers use this skill to scan OpenClaw session inputs, prompts, context, and knowledge base content for personal data. It supports local audit trails for detected, clean, and skipped scan outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local audit logs may retain masked PII previews and content hashes. <br>
Mitigation: Protect the audit directory and apply the documented cleanup workflow for retention control. <br>
Risk: Passing sensitive content with --text can expose it through process metadata during background scans. <br>
Mitigation: Use --file with --delete-after-read for background or automated scans. <br>
Risk: Sampling and cache behavior can skip repeated or sampled content. <br>
Mitigation: Use --no-cache when full scan coverage is required. <br>
Risk: --delete-after-read removes the input file after scanning. <br>
Mitigation: Reserve --delete-after-read for temporary files that are safe to remove. <br>


## Reference(s): <br>
- [OpenClaw Security PII Audit on ClawHub](https://clawhub.ai/mtoby8326/openclaw-security-pii-audit) <br>
- [README.md](README.md) <br>
- [Detection Patterns Reference](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with shell commands; the audit worker emits JSON responses and local NDJSON audit records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Audit records store masked previews and content hashes, cap input at 32,768 characters, and may use sampling or cache skips unless forced with --no-cache.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
