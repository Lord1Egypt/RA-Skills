## Description: <br>
Security guard for OpenClaw users. Audit configs, scan secrets, manage access, and generate security reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hkall](https://clawhub.ai/user/hkall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw administrators use this skill to audit local OpenClaw configuration, scan for exposed secrets, review access state, rotate tokens, apply hardening checks, and produce security reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool reads local OpenClaw credential, access, and configuration files. <br>
Mitigation: Run it only on trusted machines and review who can access terminal output, generated reports, and saved scan artifacts. <br>
Risk: Token rotation and auto-fix operations can modify authentication configuration and may print token-related details in the terminal. <br>
Mitigation: Back up OpenClaw configuration first, run token rotation or --fix only in a trusted terminal, and avoid sharing logs from those sessions. <br>
Risk: JSON and Markdown reports may expose sensitive file paths, secret findings, access state, or operational details. <br>
Mitigation: Store reports securely and redact sensitive findings before attaching them to tickets, chats, or public documentation. <br>


## Reference(s): <br>
- [OpenClaw Security Best Practices](references/security-best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI report output can be table text, JSON, or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may describe local credential files, access state, scan findings, and token operations; treat generated reports and terminal logs as sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release metadata and artifact CHANGELOG, released 2026-03-11) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
