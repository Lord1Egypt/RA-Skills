## Description: <br>
Performance analysis and optimization. Profiles code execution, identifies bottlenecks, and suggests optimizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Python source files or directories for common performance issues, then receive profiling, benchmark, and optimization guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads source files or directories selected by the user, which can expose sensitive code or secrets if broad paths are scanned. <br>
Mitigation: Analyze only intended project paths and avoid scanning folders that may contain credentials or confidential data. <br>
Risk: Profile and benchmark commands suggested by the skill may execute project code if the user chooses to run them. <br>
Mitigation: Run profiling or benchmarking only for trusted code and review generated commands before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown-style text with command examples and analysis findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports detected issue severity, line numbers, and suggested optimizations when source analysis is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
