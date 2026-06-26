## Description: <br>
Pre-flight trust verification for AI agents. Verify behavior, detect injection vulnerabilities, check for PII leaks, and measure reliability before granting Write/Execute permissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brainhiveinc](https://clawhub.ai/user/brainhiveinc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run Operon Guard checks before granting AI agents write, execute, spawn, delete, or similar high-impact permissions. It helps evaluate determinism, concurrency behavior, prompt-injection resistance, PII leakage, latency, and guardfile configuration before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external operon-guard CLI package. <br>
Mitigation: Install only from a trusted package source and review the package before using results for permission decisions. <br>
Risk: Operon Guard commands that inspect Python agents can execute target-file top-level code during import. <br>
Mitigation: Review target code first and run checks for third-party or untrusted agents in a sandboxed environment. <br>
Risk: The documented scan command always exits 0, even when it detects injection or PII issues. <br>
Mitigation: Use operon-guard test, not scan, for gating workflows because test exits nonzero when the trust score fails. <br>
Risk: Modules with multiple top-level callables may cause the CLI to test the wrong callable. <br>
Mitigation: Specify the entry point explicitly with file.py:callable syntax. <br>
Risk: Machine-readable output is not pure JSON because the CLI emits preamble lines before the JSON block. <br>
Mitigation: Extract the JSON object before piping the result to JSON parsers or CI tooling. <br>


## Reference(s): <br>
- [Operon Guard on ClawHub](https://clawhub.ai/brainhiveinc/operon-guard) <br>
- [BrainHive publisher profile](https://clawhub.ai/user/brainhiveinc) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe Operon Guard CLI behavior, trust scores, thresholds, guardfile YAML, and JSON-output handling.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
