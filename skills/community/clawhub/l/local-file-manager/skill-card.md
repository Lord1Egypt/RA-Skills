## Description: <br>
Read, write, append, and list local files in the session's working directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyico](https://clawhub.ai/user/liyico) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to read inputs, write generated outputs, append logs, create directories, and manage local text, JSON, CSV, Markdown, configuration, and code files in a session workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that user-controlled file arguments can be turned into shell commands and that write or delete operations may not provide the advertised safety guarantees. <br>
Mitigation: Review carefully before installation, use only in a disposable workspace, and require scoped filesystem APIs plus explicit confirmation before destructive actions. <br>
Risk: The implementation references a hardcoded local script path and the artifact manifest does not align cleanly with the packaged files. <br>
Mitigation: Verify the packaged entry points in the target runtime and replace local machine paths with package-relative paths before relying on the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liyico/local-file-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Files] <br>
**Output Format:** [Plain text responses and local file contents or filesystem changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operates on local paths within the configured session workspace and defaults to a 10 MB maximum file size.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
