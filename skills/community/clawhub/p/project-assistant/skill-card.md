## Description: <br>
Project Assistant helps agents initialize projects, analyze project structure, and answer project-specific questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Northcipher](https://clawhub.ai/user/Northcipher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to initialize project documentation, identify project type and structure, answer implementation and impact-analysis questions, and preserve project Q&A notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans local repositories and may write project-local .claude documentation, indexes, and cache files. <br>
Mitigation: Use it only on repositories you are comfortable scanning and review generated project documentation before sharing it. <br>
Risk: Plaintext configuration can expose Feishu tokens or other sensitive values if real credentials are stored there. <br>
Mitigation: Do not store real API keys or Feishu tokens in plaintext skill configuration; use a secret manager or short-lived credentials where possible. <br>
Risk: Generated Feishu reports or project answers can contain incomplete or misleading analysis. <br>
Mitigation: Review reports and answers before sending them to external systems or using them for project decisions. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/Northcipher/project-assistant) <br>
- [Project initialization guide](references/guides/init.md) <br>
- [Q&A documentation guide](references/guides/qa.md) <br>
- [Configuration guide](references/guides/config.md) <br>
- [Feishu integration guide](references/guides/feishu.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated project documentation files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project-local .claude documentation, indexes, and cache files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
