## Description: <br>
Operate FileBrowser via REST API to authenticate, list, upload, download, share, delete, and organize scoped files, with optional user-management operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kami1983](https://clawhub.ai/user/kami1983) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate FileBrowser REST API workflows, including scoped file listing, upload, download, sharing, deletion, purchase-order discovery, and date-based file organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authority over FileBrowser files, including upload, download, sharing, deletion, and organization operations. <br>
Mitigation: Use a least-privilege FileBrowser account, configure the narrowest practical scope, and review exact file lists before organization or deletion. <br>
Risk: Admin-capable API operations can manage users when used with an administrator account. <br>
Mitigation: Avoid admin credentials unless account management is intentional, and reserve administrator tokens for narrowly reviewed tasks. <br>
Risk: Share links may expose files without requiring login. <br>
Mitigation: Prefer short-lived share links and revoke links after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kami1983/kam-filebrowser-operator) <br>
- [Publisher profile](https://clawhub.ai/user/kami1983) <br>
- [FileBrowser API reference](artifact/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown, JSON] <br>
**Output Format:** [Markdown with HTTP examples, curl commands, JSON configuration, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce file lists, numbered download selections, share links, organization summaries, and reasons for files that could not be organized.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
