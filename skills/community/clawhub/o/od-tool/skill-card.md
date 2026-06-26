## Description: <br>
Dump file contents in octal, decimal, hexadecimal, and ASCII formats for binary data inspection and low-level file analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect raw file bytes, debug binary data, and compare octal, decimal, hexadecimal, and ASCII representations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can print raw contents from local files, which may expose secrets or sensitive binary data if used on the wrong path. <br>
Mitigation: Run it only on files intended for inspection and review dump output before sharing it outside the local environment. <br>
Risk: The skill documentation describes hexadecimal, decimal, ASCII, and address-base options, while the bundled script evidence only emits octal byte output. <br>
Mitigation: Verify the command behavior in the target agent environment before relying on non-octal formats. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/od-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands and plain-text dump output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a file or standard input and emits byte offsets with octal byte values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
