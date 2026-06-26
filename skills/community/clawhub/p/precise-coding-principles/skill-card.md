## Description: <br>
编程原则技能，源于 Andrej Karpathy 的 LLM 编程四大通病与核心原则，帮助代理在非平凡编码任务中保持精确、最小化且目标驱动。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nmww](https://clawhub.ai/user/nmww) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill when writing, reviewing, creating, or refactoring non-trivial code so they ask before making uncertain assumptions, avoid over-design, limit edits to the requested scope, and verify outcomes against explicit success criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can shift an agent toward more cautious, verification-heavy coding behavior during non-trivial tasks. <br>
Mitigation: Review before deployment if that workflow guidance is not desired for the target coding environment. <br>
Risk: Instruction-only guidance may still affect implementation choices even though it has no executable code. <br>
Mitigation: Apply normal code review and validation to any changes produced while the skill is active. <br>


## Reference(s): <br>
- [Karpathy 编程原则](references/karpathy-principles.md) <br>
- [Skill release page](https://clawhub.ai/nmww/precise-coding-principles) <br>
- [andrej-karpathy-skills reference cited by artifact](https://github.com/forrestchang/andrej-karpathy-skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown guidance and concise text recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; produces no executable code or files by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
