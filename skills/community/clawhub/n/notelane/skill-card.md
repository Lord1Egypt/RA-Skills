## Description: <br>
Organize notes as a personal knowledge base with tagging and full-text search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use Notelane to capture local notes, planning entries, reminders, progress updates, tags, timelines, weekly reviews, and searchable personal knowledge-base records from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notes, search results, and export files can contain sensitive plaintext data. <br>
Mitigation: Avoid storing passwords, API keys, confidential client data, or other secrets; treat terminal output and exported files as sensitive. <br>
Risk: Local plaintext storage under ~/.local/share/notelane may be readable by other local processes or users depending on host permissions. <br>
Mitigation: Use host file permissions and local access controls appropriate for the sensitivity of stored notes. <br>


## Reference(s): <br>
- [Notelane ClawHub release page](https://clawhub.ai/bytesagain3/notelane) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, configuration, guidance] <br>
**Output Format:** [Plain text CLI output and local plaintext, JSON, CSV, or TXT files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores notes and exports under ~/.local/share/notelane.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
