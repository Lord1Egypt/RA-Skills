## Description: <br>
Use this skill when OpenClaw needs to store files in mnemospark-lite, pay the x402 upload flow, complete uploads, list wallet-scoped uploads, fetch download details, mint share links, or delete uploads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pawlsclick](https://clawhub.ai/user/pawlsclick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to upload, list, download, share, and delete files through mnemospark-lite cloud storage. It is intended for OpenClaw workflows that need paid x402 upload handling, wallet-scoped access, and bearer-token based file operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a funded wallet to pay for cloud file uploads. <br>
Mitigation: Confirm the file, storage tier, expected payment, and payer wallet before initiating paid upload requests. <br>
Risk: Uploaded files, bearer tokens, download URLs, and 24-hour anonymous share links can expose sensitive content. <br>
Mitigation: Avoid uploading secrets unless the 30-day remote retention model is acceptable, protect bearer tokens, and mint share links only when explicitly needed. <br>
Risk: Delete operations remove wallet-scoped uploads. <br>
Mitigation: Confirm upload IDs before deletion and re-run the upload list operation afterward to verify the intended files were removed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pawlsclick/mnemospark-lite) <br>
- [mnemospark-lite web app](https://app.mnemospark.ai/mnemospark-lite) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return upload IDs, public URLs, site URLs, share URLs, bearer tokens, and payment status fields for the active task.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
