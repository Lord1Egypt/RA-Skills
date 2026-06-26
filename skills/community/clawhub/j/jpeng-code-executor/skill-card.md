## Description: <br>
Safe code execution in sandboxed environments. Supports Python, JavaScript, Bash, and more with resource limits and timeout controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run code snippets or scripts with claimed timeout, memory, output, network, and filesystem controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill claims safe execution of untrusted code, but the artifact does not include the execution script or sandbox controls needed to verify that protection. <br>
Mitigation: Do not use it for untrusted code until the execution implementation is supplied and independently reviewed. <br>
Risk: Code execution without verified sandbox controls can expose host filesystem, network, memory, or process resources. <br>
Mitigation: Run only in an audited isolated environment with explicit network, filesystem, timeout, memory, and output restrictions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-code-executor) <br>
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, JSON, Guidance] <br>
**Output Format:** [Markdown with shell command examples and JSON execution results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Claims support for Python, JavaScript, Bash, Ruby, and Go with default timeout, memory, network, filesystem, and output limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
