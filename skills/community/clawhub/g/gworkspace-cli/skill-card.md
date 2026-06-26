## Description: <br>
Interact with Google Workspace Drive, Docs, and Sheets through the `gw` CLI so an agent can browse, read, create, search, upload, and update workspace files from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robinsadeghpour](https://clawhub.ai/user/robinsadeghpour) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to operate Google Drive, Docs, and Sheets from terminal workflows, including browsing shared drives, reading documents, creating or appending documents, and reading or writing spreadsheet data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent create, upload, write, or append content in Google Drive, Docs, and Sheets. <br>
Mitigation: Confirm the exact target file, folder, document, spreadsheet, and intended change before allowing write-capable commands. <br>
Risk: The skill depends on a third-party npm package and can authenticate to Google Workspace accounts. <br>
Mitigation: Review the package and source before installation, and prefer supplying your own Google OAuth client credentials instead of relying on defaults. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/robinsadeghpour/gworkspace-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance describes terminal commands whose runtime output may be JSON, tables, IDs, or plain text depending on `gw` flags.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
