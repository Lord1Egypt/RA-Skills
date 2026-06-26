## Description: <br>
Scans OpenClaw agent memory files and workspace configs for malicious content, credential leaks, prompt injections, and security threats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dgriffin831](https://clawhub.ai/user/dgriffin831) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to scan OpenClaw memory, daily logs, and workspace configuration files for embedded prompt injection, credential leakage, data exfiltration, guardrail bypass, privilege escalation, and prompt stealing risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads OpenClaw memory and workspace configuration files that may contain sensitive content. <br>
Mitigation: Install and run it only where that file access is acceptable, and review findings before sharing or acting on them. <br>
Risk: Remote analysis can send redacted memory content to OpenAI or Anthropic when explicitly enabled. <br>
Mitigation: Keep remote scanning disabled unless intentional, and ensure API-key and data-handling expectations are acceptable before using --allow-remote. <br>
Risk: Quarantine actions can modify important files by redacting lines or whole files. <br>
Mitigation: Inspect each proposed quarantine action manually and rely on the generated backups if restoration is needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dgriffin831/memory-scan) <br>
- [Publisher Profile](https://clawhub.ai/user/dgriffin831) <br>
- [Detection Prompt](artifact/docs/detection-prompt.md) <br>
- [Testing and Evaluation](artifact/TESTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Human-readable terminal output, optional JSON, quiet severity output, and Markdown guidance for alerts and quarantine decisions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote LLM analysis is opt-in; quarantine is opt-in and creates backups before redaction.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog, released 2026-02-01) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
