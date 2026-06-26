## Description: <br>
Move or rename files and directories. Use for file organization, relocation, and renaming operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to move or rename local files and directories during file organization, relocation, and cleanup tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Moving or renaming files can relocate or overwrite data if source or destination paths are incorrect. <br>
Mitigation: Use explicit source and destination paths and review planned moves before execution. <br>
Risk: The documentation describes prompt, force, verbose, batch, and interactive behavior that the bundled script does not implement. <br>
Mitigation: Use only simple source-to-destination moves unless the script is updated; do not rely on documented -i, -f, -v, batch, or interactive safeguards. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/mv-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text] <br>
**Output Format:** [Markdown with shell command examples and plain text status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Moves files on the local filesystem; no network or credential output is expected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
