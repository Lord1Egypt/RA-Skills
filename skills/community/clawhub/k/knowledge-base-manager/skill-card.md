## Description: <br>
Manage and maintain a shared Obsidian knowledge base by organizing files, performing task reviews, archiving, and ensuring up-to-date, linked knowledge content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diliumentu](https://clawhub.ai/user/diliumentu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and agent operators use this skill to keep a shared Obsidian vault organized through task retrospectives, knowledge linking, archival routines, and periodic cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to manage files in an Obsidian vault, including cleanup, archival, and deletion decisions. <br>
Mitigation: Use it only on the intended vault, keep backups, and require confirmation before deletion or large reorganizations. <br>
Risk: The artifact contains stray shell-style footer lines that may confuse downstream tooling or reviewers. <br>
Mitigation: Review the installed skill text and remove the stray footer lines before relying on the release in stricter environments. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with templates, file naming conventions, and vault organization rules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill focuses on Obsidian vault maintenance and should be used with confirmation for destructive or broad file operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
