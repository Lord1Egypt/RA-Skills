## Description: <br>
Human-machine interface design tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to work with a simple local HMI note tracker that stores, lists, searches, removes, exports, and reports statistics for entries on the user's machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Entries are stored in plaintext local files under the HMI data directory. <br>
Mitigation: Do not store secrets, credentials, or sensitive operational notes unless plaintext local storage is acceptable. <br>
Risk: Export commands create files in the current working directory. <br>
Mitigation: Run exports from an appropriate directory and review generated files before sharing or committing them. <br>
Risk: Remove commands permanently change the saved local data. <br>
Mitigation: Review the target entry number before removal and keep backups when the data matters. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/bytesagain1/hmi) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands; CLI output is plain text with optional JSONL or CSV export files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The HMI_DIR environment variable can change the local data directory; exports are written to the current working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
