## Description: <br>
Automatically updates PROJECT_STATE.md after each commit with recent git information and optional AI-generated summaries to track project status and next steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Joe3112](https://clawhub.ai/user/Joe3112) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents working in Git repositories use this skill to keep a local PROJECT_STATE.md current with recent commit history, changed files, current focus, and suggested next steps. It supports continuity across agent sessions by refreshing project context after each commit or on demand. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a persistent post-commit hook in the target repository. <br>
Mitigation: Use it only in repositories where automated post-commit updates are acceptable, and uninstall the hook when the workflow is no longer needed. <br>
Risk: AI summary mode may send branch names, commit messages, filenames, author data, and recent change context to the local Clawdbot gateway and its configured model provider. <br>
Mitigation: Set ai_summary: false in .project-context.yml for repositories with sensitive metadata unless the local gateway and downstream provider are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Joe3112/project-context-sync) <br>
- [Publisher profile](https://clawhub.ai/user/Joe3112) <br>
- [Clawdbot gateway](https://github.com/clawdbot/clawdbot) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, YAML configuration, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or updates a repo-local PROJECT_STATE.md file from Git metadata, with optional summaries generated through a local Clawdbot gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
