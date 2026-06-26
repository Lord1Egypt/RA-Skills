## Description: <br>
Performance analysis and optimization. Profiles code execution, identifies bottlenecks, and suggests optimizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to profile code execution, identify performance bottlenecks, run benchmarks, and receive optimization guidance for Python and C/C++ projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads source files or directories selected by the user. <br>
Mitigation: Run it only on intended project paths and avoid passing directories that contain sensitive source or data unless that access is acceptable. <br>
Risk: Profiling or benchmarking can execute code supplied by the user. <br>
Mitigation: Profile or benchmark untrusted code only in an isolated environment with appropriate review and resource controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/michealxie001/oc-performance) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-style text with command examples and structured analysis output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read user-selected source files or directories and may execute profiling or benchmarking commands against supplied code.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
