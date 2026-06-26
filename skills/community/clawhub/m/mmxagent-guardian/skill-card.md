## Description: <br>
Provide file protection while users work with openclaw. All file operations are version-indexed and support delete recovery and modification rollback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OreoAndYuumi](https://clawhub.ai/user/OreoAndYuumi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to protect local file modifications and deletions during OpenClaw work. It records versioned local rollback data, supports restore flows, and prompts users before protected file operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores unencrypted local rollback data under ~/.openclaw/minivcs/, including copies of files that are edited or deleted. <br>
Mitigation: Avoid using it on secrets, credentials, private OpenClaw state, or other sensitive files unless local backups are intended; periodically review or clean ~/.openclaw/minivcs/. <br>
Risk: Binary-file protection and delete recovery can store full local copies and may increase disk usage, especially for files over 50 MB. <br>
Mitigation: Confirm local copy behavior with the user before protected binary operations and surface size warnings before continuing with similarly large files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OreoAndYuumi/mmxagent-guardian) <br>
- [Dependency notes](artifact/file_guardian.DEPENDENCIES.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local MiniVCS records, diffs, snapshots, trash backups, and restore guidance when used.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
