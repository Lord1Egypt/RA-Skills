## Description: <br>
Security hardening for OpenClaw. Audit your configuration, scan installed skills for malware, detect CVE-2026-25253, check credential exposure, and get actionable fix recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abdelsfane](https://clawhub.ai/user/abdelsfane) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to audit OpenClaw installations, scan installed skills for malware patterns, check credential handling, and receive prioritized hardening recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run an unpinned npm scanner against sensitive OpenClaw files. <br>
Mitigation: Trust and verify the `hackmyagent` package before use; prefer a pinned reviewed version or a preinstalled reviewed binary. <br>
Risk: Security scans may touch credential-bearing OpenClaw directories. <br>
Mitigation: Run scans in a contained environment and avoid scanning sensitive directories unless the scanner and execution context have been reviewed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/abdelsfane/opena2a-security) <br>
- [hackmyagent npm package](https://www.npmjs.com/package/hackmyagent) <br>
- [hackmyagent source repository](https://github.com/opena2a-org/hackmyagent) <br>
- [OpenClaw trust threat model](https://github.com/openclaw/trust/pull/7) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and optional scanner report formats including text, JSON, SARIF, HTML, and ASP.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local security reports when the scanner is invoked with an output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
