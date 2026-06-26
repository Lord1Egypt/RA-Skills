## Description: <br>
Scans ClawHub skills for malicious code, obfuscated payloads, and social engineering indicators before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sypsyp97](https://clawhub.ai/user/sypsyp97) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to inspect ClawHub skills before installation or review installed local skill directories. It reports pattern, deobfuscation, and manual LLM-review findings so users can decide whether a skill needs review or should not be installed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner is a lightweight pre-install check and does not prove that a skill is safe. <br>
Mitigation: Use findings as review signals, then manually inspect the skill and apply normal security review before installation. <br>
Risk: Suspicious code snippets may be copied to a temporary file for manual analysis. <br>
Mitigation: Treat temporary suspicious-code output as untrusted and possibly sensitive, and delete it after review. <br>
Risk: The advertised LLM analysis is a manual handoff rather than an integrated security check. <br>
Mitigation: Do not rely on the LLM step unless a reviewer explicitly runs and evaluates the suggested manual analysis. <br>


## Reference(s): <br>
- [OpenClaw Skill Auditor on ClawHub](https://clawhub.ai/sypsyp97/openclaw-skill-auditor) <br>
- [341 Malicious ClawHub Skills Incident](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html) <br>
- [OpenClaw Security Guide](https://docs.openclaw.ai/gateway/security) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal report with severity findings, verdict text, and follow-up shell commands for manual review.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write suspicious snippets to a temporary file for manual analysis when suspicious code is found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
