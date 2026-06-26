## Description: <br>
Automates monitoring 6v movie listings, filtering by IMDb and Douban ratings, adding selected movies to 115 offline downloads, copying them to a NAS, and renaming media files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuexinguo](https://clawhub.ai/user/yuexinguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and media-library operators use this skill to run or adjust an automated movie acquisition pipeline that monitors 6v520, sends qualifying movies to 115 offline download, copies completed media to a NAS, and normalizes file names. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically modify both a 115 cloud account and local NAS media library using stored cookies, including bulk rename and cleanup operations. <br>
Mitigation: Install only when the agent is expected to operate those accounts and directories; confirm exact paths and cookie files before running cleanup or full-flow commands. <br>
Risk: Stored 115 cookies are required for download and rename operations and separate cookie files must remain synchronized. <br>
Mitigation: Keep cookie files protected, rotate them when needed, and verify both movie-monitor and renamer cookie paths before cloud rename tasks. <br>
Risk: Cleanup and rename commands can change local and cloud file or folder names in bulk. <br>
Mitigation: Prefer a manual preview or dry run when supported by the underlying scripts, and keep backups before running cleanup or full-flow automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuexinguo/movie-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to run Python and Node.js scripts that operate on a 115 account and NAS media directories.] <br>

## Skill Version(s): <br>
1.4.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
