## Description: <br>
Minimal anti-prompt-injection guardrail for OpenClaw agents. Use when handling untrusted external content, before high-risk actions, and before sending external text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[durugy](https://clawhub.ai/user/durugy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to scan untrusted content, pre-check high-risk local actions, and redact sensitive outbound text before an OpenClaw agent proceeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the package may fail open while claiming protection. <br>
Mitigation: Treat it as an advisory guardrail, validate the scripts and rules before relying on it, and keep human review in the loop for risky actions. <br>
Risk: Missing or unaudited rule files and untrusted local configuration can reduce detection coverage. <br>
Mitigation: Create .env from trusted values, use audited rule files, and verify PSL_RULES_DIR and PSL_MODE before deployment. <br>
Risk: Warn or block results may include false positives or false negatives. <br>
Mitigation: Stop on warn or block results and ask for explicit confirmation or revised content before continuing. <br>


## Reference(s): <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [ClawHub release page](https://clawhub.ai/durugy/prompt-shield-lite) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and single-line JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts return allow, warn, or block decisions with severity, confidence, matched rules, fingerprint, and optional sanitized_text.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
