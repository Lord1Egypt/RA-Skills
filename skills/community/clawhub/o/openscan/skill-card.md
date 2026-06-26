## Description: <br>
Scan binaries and scripts for malicious patterns before trusting them. Use when installing skills, evaluating unknown binaries, or auditing tool dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dev-null321](https://clawhub.ai/user/dev-null321) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use OpenScan to perform lightweight static analysis of macOS and Linux binaries, scripts, and skill folders before trusting or installing them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: On macOS, a specially crafted filename may cause the signature check to run unintended shell commands. <br>
Mitigation: Avoid scanning untrusted directories until the signature check uses a non-shell API such as execFileSync or spawn with an argument array. <br>
Risk: Published source metadata is inconsistent and server-resolved import provenance is unavailable. <br>
Mitigation: Verify the intended publisher and source before installing or relying on the release. <br>
Risk: Static analysis may miss runtime-only behavior, sophisticated obfuscation, or malware without matching patterns. <br>
Mitigation: Use scan results as a review aid alongside source review, sandboxing, and established security tools. <br>


## Reference(s): <br>
- [OpenScan README](README.md) <br>
- [OpenScan on ClawHub](https://clawhub.ai/dev-null321/openscan) <br>
- [Harkonnen antimalware engine](https://github.com/dev-null321/Harkonnen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JavaScript integration examples, human-readable scan summaries, and optional JSON scan results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI exit codes indicate clean, suspicious, or high-threat scan outcomes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
