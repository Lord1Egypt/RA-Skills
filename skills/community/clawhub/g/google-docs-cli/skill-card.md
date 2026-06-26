## Description: <br>
Google Docs Secure Management. Use when the user wants to create, read, or edit Google Docs content; or manage sharing, permissions, renames, and deletes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[porteden](https://clawhub.ai/user/porteden) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate Google Docs through the PortEden CLI, including creating, reading, editing, sharing, renaming, and trashing documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The PortEden CLI may access Google Docs and Drive using sensitive credentials or persisted keyring tokens. <br>
Mitigation: Install only from trusted PortEden sources, use the minimum required Google account and Drive scopes, and remove stored credentials when access is no longer needed. <br>
Risk: Share, edit, rename, and delete commands can change document content, permissions, or file state. <br>
Mitigation: Review generated commands before execution, confirm target file identifiers, and require explicit confirmation before sharing publicly or deleting documents. <br>
Risk: Environment variables such as PE_API_KEY can expose API credentials if logged or shared. <br>
Mitigation: Keep credential environment variables out of transcripts, logs, and committed files; prefer scoped credentials and rotate keys after suspected exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/porteden/google-docs-cli) <br>
- [PortEden homepage](https://porteden.com) <br>
- [PortEden publisher profile](https://clawhub.ai/user/porteden) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON operation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of compact JSON CLI output flags and Google Docs file identifiers.] <br>

## Skill Version(s): <br>
1.0.8 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
