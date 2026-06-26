## Description: <br>
Interact with Google Drive, Docs, and Sheets using the drivectl CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ghchinoy](https://clawhub.ai/user/ghchinoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to list, search, download, create, export, and update Google Drive, Docs, and Sheets content through the drivectl command-line tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant an agent broad Google Workspace access beyond basic Drive, Docs, and Sheets workflows. <br>
Mitigation: Use the narrowest OAuth scopes and a low-privilege Google account, and require explicit approval before write, sharing, permission, Gmail, Calendar, or other non-Drive/Docs/Sheets actions. <br>
Risk: The bundled installer downloads an external drivectl release and the security evidence flags an integrity-check weakness. <br>
Mitigation: Install only from a trusted upstream release and manually verify downloaded binaries before use. <br>


## Reference(s): <br>
- [Google Drive CLI skill page](https://clawhub.ai/ghchinoy/google-drive-cli) <br>
- [Google Drive API v3 discovery document](https://www.googleapis.com/discovery/v1/apis/drive/v3/rest) <br>
- [Dynamic API Discovery](references/discovery.md) <br>
- [Google Docs Operations](references/docs.md) <br>
- [Google Drive Operations](references/drive.md) <br>
- [Google Sheets Operations](references/sheets.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance commonly requests structured drivectl output with -O json for programmatic parsing.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
