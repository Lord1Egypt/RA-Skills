## Description: <br>
Scans AI agent memory files for common security issues such as malicious instructions, prompt injection patterns, credential exposure, and data-exfiltration cues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to audit local agent memory files for prompt injection, malicious instructions, credential-like strings, and related security concerns. It supports periodic memory review, post-ingestion checks after adding external data, and manual quarantine workflows for suspicious lines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory files may contain private data or credentials. <br>
Mitigation: Review the skill carefully before installing and avoid running it on memory files that contain secrets unless the environment and workflow are acceptable. <br>
Risk: The artifact describes local-only scanning but also includes callback_url and external API-key configuration language. <br>
Mitigation: Use it only as a local scanner when callback_url and external API configuration can be avoided. <br>
Risk: Quarantine behavior can modify memory files by replacing flagged lines. <br>
Mitigation: Confirm each quarantine action before allowing file changes and verify that backups exist before relying on restore. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/memory-radar-free) <br>
- [Skill Homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON scan results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports findings by file and line, assigns severity levels from SAFE through CRITICAL, and may guide user-confirmed quarantine or restore actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
