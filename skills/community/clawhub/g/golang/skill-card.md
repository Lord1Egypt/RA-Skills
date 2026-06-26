## Description: <br>
Records, searches, and exports local Go development activity entries for build, test, lint, format, and related workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams can use this skill to record, search, and export local notes about Go build, test, lint, format, and related development activity. Treat it as an offline activity log, not as a substitute for actual Go build, test, lint, or formatting tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is marketed as Go build, test, lint, and format tooling, but the artifact records user-entered text in persistent local logs. <br>
Mitigation: Use it only as a local activity log and run actual Go toolchain commands separately for build, test, lint, and formatting results. <br>
Risk: Entries are saved under ~/.local/share/golang and can later be searched or exported. <br>
Mitigation: Do not enter secrets, confidential code snippets, customer data, or private incident details. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bytesagain3/golang) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may write local log and export files under ~/.local/share/golang.] <br>

## Skill Version(s): <br>
2.0.1 (source: release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
