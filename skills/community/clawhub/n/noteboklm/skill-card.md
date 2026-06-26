## Description: <br>
Complete Google NotebookLM integration for adding sources, asking questions, generating Studio content, downloading artifacts, and managing notebooks programmatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nikolayco](https://clawhub.ai/user/nikolayco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to automate Google NotebookLM workflows from an agent, including source import, Q&A, study material generation, artifact downloads, and notebook, profile, and sharing management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad Google account and sharing authority through an unofficial NotebookLM integration. <br>
Mitigation: Use a low-risk or dedicated Google account where possible and require manual approval before importing local or Drive files, exporting artifacts, saving notes, or changing sharing settings. <br>
Risk: The integration relies on undocumented NotebookLM APIs and may break or behave differently without notice. <br>
Mitigation: Verify the exact notebooklm-py package and version before use, run diagnostic commands first, and test workflows on low-risk notebooks before relying on generated artifacts. <br>
Risk: Uploaded or imported documents may be processed and retained by NotebookLM or Google under the active account. <br>
Mitigation: Do not use confidential, regulated, or sensitive documents unless that processing and retention is intended and approved for the account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nikolayco/noteboklm) <br>
- [notebooklm-py upstream project](https://github.com/teng-lin/notebooklm-py) <br>
- [notebooklm-py troubleshooting docs](https://github.com/teng-lin/notebooklm-py/blob/main/docs/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include NotebookLM CLI commands that read from or write to a user's Google account, local filesystem, Google Drive, or sharing settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
