## Description: <br>
将 Andrej Karpathy 的 LLM 编程四大行为规范打包为 OpenClaw Skill <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to apply four concise programming behavior guidelines: clarify uncertainty, prefer simple implementations, keep changes narrowly scoped, and verify work against the goal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases could activate the coding-guidance skill unexpectedly. <br>
Mitigation: Review trigger wording before deployment and narrow generic Chinese behavior or programming-standard phrases when predictable activation is required. <br>
Risk: Guidance-oriented skills can influence coding behavior even when they do not access data or execute hidden actions. <br>
Mitigation: Review generated coding plans, edits, and validation steps against the user's actual request before accepting changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-karpathy-guidelines) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, shell commands] <br>
**Output Format:** [Markdown guidance and optional terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled shell script prints a quick-reference checklist for the same programming behavior guidelines.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter and _meta.json report 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
