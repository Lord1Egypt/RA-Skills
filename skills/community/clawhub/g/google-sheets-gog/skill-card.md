## Description: <br>
Use this skill when you need to create, inspect, update, append to, or reorganize Google Sheets from a locally installed `gog` CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kvarts](https://clawhub.ai/user/kvarts) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and spreadsheet operators use this skill to work with Google Sheets through the local `gog` CLI for reads, appends, updates, sheet creation, tab organization, named ranges, and scoped formatting tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a login and password-style secret in configuration even though its documented spreadsheet workflow uses local OAuth. <br>
Mitigation: Avoid storing a real Google password or app-specific secret in configuration unless the publisher clearly explains why it is required; prefer environment or secret storage mechanisms when available. <br>
Risk: The skill can modify Google Sheets, including write, delete, and broad formatting operations. <br>
Mitigation: Verify the spreadsheet ID, tab, range, and operation before approving write, delete, clear, find-replace, or broad formatting actions. <br>


## Reference(s): <br>
- [gog Sheets Reference](references/gog-sheets.md) <br>
- [gogcli homepage](https://github.com/steipete/gogcli) <br>
- [gogcli README](https://github.com/steipete/gogcli/blob/main/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/kvarts/google-sheets-gog) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can read, create, update, append, format, and export Google Sheets through a locally authenticated `gog` CLI.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
