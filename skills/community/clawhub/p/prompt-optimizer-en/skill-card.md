## Description: <br>
Optimizes complex prompts through explicit, iterative prompt refinement using ACON-style signal preservation and APE-style candidate scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ucsdzehualiu](https://clawhub.ai/user/ucsdzehualiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and other external users use this skill when they explicitly request prompt optimization for complex tasks. It rewrites prompts while preserving role, task, constraints, format, variables, examples, tool rules, and success criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts submitted for optimization may contain secrets or sensitive private data. <br>
Mitigation: Remove secrets and sensitive private data before asking the skill to optimize a prompt. <br>
Risk: A rewritten prompt may omit, weaken, or alter important task constraints. <br>
Mitigation: Review the final rewritten prompt for accuracy and constraint preservation before using it for important work. <br>


## Reference(s): <br>
- [ACON paper](https://arxiv.org/abs/2510.00615) <br>
- [APE paper](https://arxiv.org/abs/2211.01910) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with a fenced optimized prompt and a brief feedback request] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no files, shell commands, or configuration are produced.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
