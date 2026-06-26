## Description: <br>
A simple skill to greet users and demonstrate basic OpenCLAW skill structure. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[luna825](https://clawhub.ai/user/luna825) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and learners use this skill to see a basic OpenCLAW skill respond with a friendly greeting and optional demo script output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases may activate the skill unintentionally. <br>
Mitigation: Review activation context before relying on the generated greeting or running the demo script. <br>
Risk: The demo script prints the local working directory, which may expose path information in a shared transcript. <br>
Mitigation: Avoid running the script in shared conversations when local path disclosure matters. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with optional terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included script prints the current time and local working directory when run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
