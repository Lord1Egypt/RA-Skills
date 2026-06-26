## Description: <br>
Idiom Dictionary provides offline lookup for a small Chinese idiom collection with meanings and learning-oriented commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and language learners use this skill to look up Chinese idioms, browse a compact idiom list, and generate command-line dictionary output for study or reference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled helper can store local command data and private notes in a configured data directory. <br>
Mitigation: Avoid entering secrets or private notes, and inspect or clear the configured local data directory when needed. <br>
Risk: The helper's remove command should not be relied on to delete stored entries. <br>
Mitigation: Manually inspect or delete entries from the configured local data directory for reliable cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain1/idiom-dictionary) <br>
- [Publisher profile](https://clawhub.ai/user/bytesagain1) <br>
- [Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local command-line output and may read or write a user-configured local data directory.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
