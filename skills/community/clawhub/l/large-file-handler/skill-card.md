## Description: <br>
Large File Handler asynchronously saves and processes large user files with background Python processors so Gateway workflows can stay responsive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunkaikai123](https://clawhub.ai/user/sunkaikai123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to accept large uploaded files, route them through synchronous or asynchronous processing, and return status or extracted results without blocking the calling Gateway flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded files are stored in the local OpenClaw workspace. <br>
Mitigation: Use restrictive filesystem permissions, validate paths before processing, and enforce scheduled cleanup for retained files. <br>
Risk: Background Python processors can consume local CPU, memory, and disk resources. <br>
Mitigation: Apply resource limits, monitor pending and processing directories, and keep file-size thresholds aligned with the deployment environment. <br>
Risk: Sensitive tokens or identifiers can be exposed when passed directly on shared command lines. <br>
Mitigation: Use secure secret handling instead of command-line token arguments on shared systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunkaikai123/large-file-handler) <br>
- [README.md](README.md) <br>
- [INTEGRATION.md](INTEGRATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown status and processing results, with optional shell commands and configuration guidance for integration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes files up to 500 MB; files over 10 MB are handled asynchronously and stored in local pending, processing, and completed directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
