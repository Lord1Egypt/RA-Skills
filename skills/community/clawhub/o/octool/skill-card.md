## Description: <br>
Openclaw Visual Configuration Assistant that provides a secure wizard for local and Git backup plus workspace migration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donnieclaw](https://clawhub.ai/user/donnieclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and OpenClaw users use this skill to configure local or GitHub-backed backups for OpenClaw settings, agent persona files, and workspace migration. It helps generate commands and browser-based workflow steps for manual review and execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports a mismatch between the skill's no-clipboard claim and behavior that may copy high-impact shell commands to the clipboard. <br>
Mitigation: Inspect generated commands before terminal use, avoid pasting blindly, and clear or replace clipboard contents after review. <br>
Risk: Git mode requires a GitHub personal access token that can write repository contents. <br>
Mitigation: Use a fine-grained token limited to the intended private repository and only the minimum required contents permission. <br>
Risk: Generated shell commands can modify shell profile files and copy or sync workspace data. <br>
Mitigation: Review every generated command, verify paths and repository targets, and keep a separate backup before running profile or restore commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/donnieclaw/octool) <br>
- [Publisher profile](https://clawhub.ai/user/donnieclaw) <br>
- [Project homepage listed in skill metadata](https://github.com/donnieclaw/octool) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Browser UI text with generated shell command snippets and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Git mode uses GitHub API calls with a user-provided token; generated shell commands require manual review and execution.] <br>

## Skill Version(s): <br>
1.0.17 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
