## Description: <br>
Create hard and symbolic links between files. Use for file referencing, shortcuts, and directory organization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create local file links for file referencing, shortcuts, and directory organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates local filesystem links and can affect existing paths. <br>
Mitigation: Check target and link paths before execution, and use force replacement only when replacing the destination is intended. <br>
Risk: The documentation describes hard and symbolic links, while the included Python script creates symbolic links only. <br>
Mitigation: Treat symbolic-link creation as the implemented behavior unless the artifact is updated to support hard links. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/ln-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local filesystem links when executed; the included script supports symbolic links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
