## Description: <br>
Nex Keyring helps agents manage and track local API keys, secrets, and tokens with rotation status, risk levels, auditing, and policy enforcement without storing actual secret values. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexaiguy](https://clawhub.ai/user/nexaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, and system administrators use this skill to inventory local credential metadata, check rotation status, identify stale credentials, and export audit-oriented reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans .env files and environment variables, which can reveal sensitive credential metadata and local file paths. <br>
Mitigation: Scan only intended local files or environments, avoid casual production scans, and review outputs before sharing or storing them. <br>
Risk: The local database and exported reports can contain sensitive secret metadata even when actual secret values are not stored. <br>
Mitigation: Treat ~/.nex-keyring and all JSON, CSV, or Markdown exports as sensitive files; keep them out of shared folders and repositories. <br>
Risk: Security evidence warns that advertised protection may be overstated, especially when cryptography is unavailable. <br>
Mitigation: Verify the local protection model before relying on it, install cryptography when appropriate, and do not treat base64 obfuscation as encryption. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nexaiguy/nex-keyring) <br>
- [Nex AI homepage](https://nex-ai.be) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI guidance with optional JSON, CSV, or Markdown registry exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may describe sensitive credential metadata and local file paths; exported reports should be handled as sensitive files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
