## Description: <br>
pidrive helps AI agents use private S3-backed file storage through a WebDAV-mounted filesystem and standard Unix commands, with persistent data in S3 and a small temporary local read cache. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhishek203](https://clawhub.ai/user/abhishek203) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use pidrive to mount private cloud-backed storage for agents, read and write files with Unix commands, share files explicitly, search stored content, and manage account state without integrating an SDK. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud-backed storage sends file operations through the hosted pidrive service and persists data in S3. <br>
Mitigation: Install and use the skill only when the publisher, installation source, and hosted service are trusted for the files being handled. <br>
Risk: Public link sharing allows anyone with the URL to download the shared file. <br>
Mitigation: Use direct shares for sensitive files, avoid public links for confidential data, and set expirations when public links are necessary. <br>
Risk: The local API key can grant access to the mounted drive if exposed. <br>
Mitigation: Protect the local credentials file, preserve owner-only permissions, and revoke or re-register credentials if compromise is suspected. <br>
Risk: Commands can delete files, share links, revoke access, restore files, or change paid plans. <br>
Mitigation: Require explicit confirmation before destructive, sharing, access-control, or billing-related commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abhishek203/pidrive) <br>
- [pidrive source code](https://github.com/abhishek203/pi-drive) <br>
- [pidrive GitHub releases](https://github.com/abhishek203/pi-drive/releases) <br>
- [pidrive Homebrew tap](https://github.com/abhishek203/homebrew-pidrive) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and filesystem paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include commands that read, write, share, restore, revoke, or change account plan state through the pidrive CLI and mounted filesystem.] <br>

## Skill Version(s): <br>
1.9.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
