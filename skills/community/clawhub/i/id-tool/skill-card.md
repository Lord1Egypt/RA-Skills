## Description: <br>
Display basic local user and group identity information for the current process. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for local permission debugging by checking the user and group identity context visible to the running process. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation describes command-line options, username lookup, effective ID output, and supplementary group listing that the current artifact does not implement. <br>
Mitigation: Treat the skill as a basic current-process UID/GID display tool unless the artifact is updated and revalidated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/id-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text or Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Current artifact prints UID and GID for the running process; documented options and username lookup are not implemented.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
