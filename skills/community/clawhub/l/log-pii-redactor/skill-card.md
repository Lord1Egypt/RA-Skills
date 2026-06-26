## Description: <br>
Detects and redacts PII and secrets in application logs, with strategy guidance, regex patterns, scanner code, pipeline recipes, and compliance mapping for GDPR, CCPA, HIPAA, and PCI DSS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and compliance teams use this skill to audit logs for sensitive data, choose redaction strategies, and generate pipeline-ready redaction assets before logs reach retained or indexed sinks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste live production logs, PHI, payment data, credentials, or other sensitive records into an agent session while asking for redaction help. <br>
Mitigation: Use synthetic or minimized samples where possible, and handle live sensitive logs only in an explicitly controlled environment. <br>
Risk: Generated scanner or pipeline configuration can block builds, change logging behavior, or miss edge cases if applied directly to production. <br>
Mitigation: Review generated rules, validate them in staging, and roll out redaction controls through sampled canaries before enforcing production filtering or CI failures. <br>
Risk: Installer capability prompts may include unrelated wallet, purchase, OAuth, or sensitive-credential permissions despite the artifact being markdown-only. <br>
Mitigation: Decline unrelated permissions and grant only the access required for the intended log-redaction workflow. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration, shell commands] <br>
**Output Format:** [Markdown with YAML, Python, TOML, INI, Ruby, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PII surface reports, strategy tables, regex packs, pipeline configuration, scanner scripts, compliance mappings, placement guidance, and rollout plans.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, created 2026-05-03) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
