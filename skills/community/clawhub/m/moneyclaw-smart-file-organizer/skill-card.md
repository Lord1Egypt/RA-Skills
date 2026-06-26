## Description: <br>
A Python-based file organization skill for categorizing local files, renaming them, detecting duplicates, creating backups, and undoing logged operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shianaixuexi-cell](https://clawhub.ai/user/shianaixuexi-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to organize local folders by file type, preview or execute file moves and renames, generate configuration, detect duplicates, and undo logged operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk organization, renaming, and duplicate handling can move or permanently delete many user files. <br>
Mitigation: Use a test folder first, run preview mode before live changes, keep an independent backup, avoid sudo or administrator execution, and manually verify files before enabling duplicate deletion. <br>
Risk: Recovery controls may be incomplete if backups or logs are missing, and deleted duplicate files may not be directly restorable. <br>
Mitigation: Confirm backups and operation logs are created before live runs, and prefer moving duplicates to a review folder instead of deleting them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shianaixuexi-cell/moneyclaw-smart-file-organizer) <br>
- [Publisher profile](https://clawhub.ai/user/shianaixuexi-cell) <br>
- [Python downloads](https://www.python.org/downloads/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local file-operation guidance for Python scripts; no network or credential behavior is described in the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
