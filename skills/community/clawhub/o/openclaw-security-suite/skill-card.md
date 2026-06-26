## Description: <br>
Comprehensive security suite for OpenClaw skills. Includes static scanning (AST + keywords) and AI-powered semantic behavior review to detect malicious code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xunxingyuan](https://clawhub.ai/user/xunxingyuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan OpenClaw skill directories for static indicators of malicious behavior and to request LLM-assisted semantic review of individual files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI review sends the selected file content to the configured LLM, which may expose sensitive source code or secrets. <br>
Mitigation: Run AI review only on files that are approved for disclosure to the configured LLM, and remove secrets before review. <br>
Risk: Static scanning is advisory and may miss relevant files, especially nested files outside the top-level directory scan. <br>
Mitigation: Supplement scan results with recursive review or additional tooling before relying on a clean result for deployment decisions. <br>


## Reference(s): <br>
- [OpenClaw Security Suite on ClawHub](https://clawhub.ai/xunxingyuan/openclaw-security-suite) <br>
- [README](artifact/README.md) <br>
- [SKILL definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Guidance] <br>
**Output Format:** [JSON objects containing scan findings or LLM review results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Static scan results include a safe flag and per-file issues; AI review results depend on the configured LLM.] <br>

## Skill Version(s): <br>
0.2.3 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
