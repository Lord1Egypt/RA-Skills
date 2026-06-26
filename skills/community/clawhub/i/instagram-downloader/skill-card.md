## Description: <br>
Guides an agent through collecting an Instagram username, download directory, cookie file, and optional proxy, then prepares gallery-dl commands to download Instagram posts, Reels, avatars, or individual posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zitao666](https://clawhub.ai/user/zitao666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to prepare authenticated gallery-dl commands for downloading Instagram profile content to a local directory. It is intended for accounts and content the user owns or is explicitly authorized to access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide reusable Instagram session credentials. <br>
Mitigation: Use only credential files for owned or explicitly authorized accounts, keep cookie files local, avoid pasting raw cookie values into chat, and revoke or refresh the Instagram session if exposure is suspected. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include paths, proxy settings, Instagram URLs, and credential-file handling guidance supplied by the user.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
