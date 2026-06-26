## Description: <br>
Outline is a local Bash productivity logging CLI for capturing, searching, reviewing, and exporting timestamped notes across categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill as a local command-line productivity logger for plans, tasks, reviews, reminders, tags, timelines, and exports. It is not a document outline generator despite the public summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is advertised as a document outline generator, but the artifact implements a local productivity logger. <br>
Mitigation: Install only when a local logging CLI is desired, and verify expected behavior against the artifact before use. <br>
Risk: User-entered notes are stored in plain text under ~/.local/share/outline and may be included in searchable history and exports. <br>
Mitigation: Avoid entering secrets, confidential drafts, private reminders, or sensitive project notes unless plain-text local storage is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/outline) <br>
- [Publisher profile](https://clawhub.ai/user/ckchzh) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, JSON, CSV] <br>
**Output Format:** [Plain text CLI output with local log files and optional JSON, CSV, or text exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores command history and category logs locally under ~/.local/share/outline.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release evidence; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
