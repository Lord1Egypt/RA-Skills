## Description: <br>
Provides fast, read-only codebase search and exploration using grep for content, glob for filenames, and tree for directory structure with filtering and limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yanxingang](https://clawhub.ai/user/Yanxingang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill to inspect unfamiliar codebases, find definitions and usages, locate files by pattern, and view directory structure without modifying project files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search output can expose private code, filenames, or configuration contents to the agent conversation. <br>
Mitigation: Run searches against specific intended project directories and avoid broad home or system paths. <br>
Risk: The skill depends on local rg, fd, and tree binaries. <br>
Mitigation: Install dependencies from trusted package managers or verified upstream releases before use. <br>


## Reference(s): <br>
- [OpenClaw Code Search on ClawHub](https://clawhub.ai/Yanxingang/openclaw-code-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Structured text and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only search output may include file paths, matched lines, result counts, truncation notices, dependency status, or error messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
