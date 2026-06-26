## Description: <br>
Educational security training sandbox for AI agents with intentionally vulnerable systems, exploit documentation, and patch examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and AI-agent builders use this skill to run a controlled defensive security lab, inspect vulnerable mock systems, test exploit patterns, and produce patch guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local commands and code as part of a hands-on security lab. <br>
Mitigation: Run it only in a disposable container, VM, or throwaway workspace with no sensitive files mounted. <br>
Risk: The included vaccine files are educational examples rather than production-ready security patches. <br>
Mitigation: Review, test, and adapt any patch before using the pattern in production code. <br>
Risk: The skill contains exploit examples for intentionally vulnerable mock systems. <br>
Mitigation: Use it only on the included systems or on targets you are clearly authorized to test. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/morgana-mordred-security-sandbox) <br>
- [Mordred Security Sandbox manifest](artifact/SKILL.md) <br>
- [Demo guide](artifact/examples/demo.md) <br>
- [Security analysis workflow](artifact/skills/security-analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include vulnerability findings, vaccine status, and security recommendations for the included mock systems.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
