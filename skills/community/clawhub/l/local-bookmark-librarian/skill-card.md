## Description: <br>
Local Bookmark Librarian organizes and deduplicates exported local bookmarks or link lists, then produces topic indexes and maintenance recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to review exported bookmark HTML, CSV, link lists, or dedicated bookmark folders before reorganizing browser bookmarks or knowledge libraries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports can include local file names, paths, headings, and sampled content when broad directories are used as input. <br>
Mitigation: Keep input narrowly scoped to exported bookmark copies, CSV/link lists, or a dedicated bookmark folder; do not use a home directory, browser profile, source repository, or other private folder. <br>
Risk: Duplicate or low-value link recommendations may be mistaken for permission to delete or modify bookmarks. <br>
Mitigation: Review generated output before making browser changes, and only delete or reorganize links after explicit user confirmation. <br>
Risk: Bookmark exports can contain private URLs or sensitive personal context. <br>
Mitigation: Use local exported copies and redact sensitive links or personal data before sharing reports outside the user's trusted environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/local-bookmark-librarian) <br>
- [Publisher Profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [README.md](artifact/README.md) <br>
- [resources/spec.json](artifact/resources/spec.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown reports, optional JSON reports, and reviewed shell commands for local execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local report file when the user supplies an output path; dry-run mode avoids file writing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
