## Description: <br>
Syncs Google Docs content into Feishu Docs through a manual workflow that converts document blocks to Markdown and writes the result to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turbos7](https://clawhub.ai/user/turbos7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers or operators use this skill to copy an authorized Google Docs document into Feishu, optionally targeting a Feishu folder or owner. It is suited for manual document transfer workflows where Google OAuth and Feishu access are already configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The current script builds shell commands from document and user-controlled values. <br>
Mitigation: Review or patch the script before installing, avoid documents with shell metacharacters in titles or contents, and prefer escaped arguments or direct API calls over shell command construction. <br>
Risk: Reusable Google OAuth credentials and tokens are stored locally. <br>
Mitigation: Protect the local credential directory, limit document access to the minimum required scope, and revoke or remove saved tokens when the transfer is complete. <br>
Risk: Content may be copied to the wrong Feishu folder or owner. <br>
Mitigation: Verify the destination folder token and owner before syncing, and use only documents intended for Feishu. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/turbos7/google-docs-to-feishu) <br>
- [Google Cloud Console](https://console.cloud.google.com) <br>
- [Google Docs readonly OAuth scope](https://www.googleapis.com/auth/documents.readonly) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON status and console text, with converted Markdown written to a Feishu document] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Google OAuth credentials, a saved Google token, and a configured Feishu document integration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
