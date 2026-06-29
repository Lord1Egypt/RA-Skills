## Description: <br>
Scan AI prompts for injection, jailbreak, and sensitive data leak risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan prompts before they reach an LLM, identify prompt injection, jailbreak, and sensitive-data leak patterns, and receive remediation or redaction guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security reports can print matched secrets or sensitive snippets to the terminal for review. <br>
Mitigation: Use auto-redaction before sharing reports, avoid pasting real secrets into prompts, and rotate any real key or password detected by the tool. <br>
Risk: Pattern-based detection can miss novel prompt attacks or flag benign text for review. <br>
Mitigation: Treat findings as review support, keep detection patterns configurable, and apply human review before relying on a prompt in production. <br>


## Reference(s): <br>
- [Prompt Guard Detection Patterns Reference](references/patterns.md) <br>
- [Prompt Defender ClawHub Skill Page](https://clawhub.ai/harrylabsj/prompt-defender) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON security report with a risk score, findings, optional sanitized prompt, and command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Auto-redaction is opt-in; the CLI exits nonzero when the score is below 80.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
