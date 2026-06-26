## Description: <br>
Output text and variable values to standard output for displaying messages, script output, and debug information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to print supplied text or variable values to standard output for simple messaging, script output, and debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented -n, -e, and multi-argument behavior is not implemented by the bundled script. <br>
Mitigation: Use the skill only for single-argument plain-text output unless implementation support is added and reviewed. <br>
Risk: Values passed to the tool are written to standard output, which can expose secrets in logs or transcripts. <br>
Mitigation: Do not pass credentials, tokens, or other secrets unless intentional disclosure to standard output is acceptable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Plain text on standard output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script prints one positional argument; documented flags and multi-argument behavior are not implemented.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
