## Description: <br>
Read, write, append, and list local files in the session's working directory for agents that need to persist output, read inputs, or manage text, JSON, CSV, and Markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[000sonic](https://clawhub.ai/user/000sonic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and automation agents use this skill to read local input files, save generated outputs, append logs, create directories, list workspace files, and perform basic local file operations within the session workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe shell execution and argument handling can make local file operations risky without review. <br>
Mitigation: Install only in a disposable or tightly sandboxed workspace and replace the shell wrapper with safe argument handling and path validation before trusted use. <br>
Risk: File-boundary claims are inconsistent, including logging behavior outside the workspace. <br>
Mitigation: Keep logging inside the workspace or make it explicit opt-in, and require clear confirmation for destructive actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/000sonic/local-file-manager-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration] <br>
**Output Format:** [Plain text file contents, directory listings, and operation status or error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read, write, append, list, create directories, and delete files; supports dry-run behavior and file-size configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
