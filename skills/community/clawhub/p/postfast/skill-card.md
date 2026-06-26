## Description: <br>
Schedule and manage social media posts across TikTok, Instagram, Facebook, X, YouTube, LinkedIn, Threads, Bluesky, Pinterest, Telegram, and Google Business Profile using the PostFast API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peturgeorgievv](https://clawhub.ai/user/peturgeorgievv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and social media operators use this skill to schedule posts, upload media, manage connected accounts, cross-post content, inspect analytics, and manage PostFast drafts across supported social platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a PostFast API key that can operate a user's workspace. <br>
Mitigation: Store the API key only in the `POSTFAST_API_KEY` environment variable and restrict use to trusted agents and workspaces. <br>
Risk: The skill can publish content, delete scheduled posts, upload media, and send account connection emails. <br>
Mitigation: Require explicit user confirmation before publishing, deleting posts, uploading media, or sending connect-link emails. <br>
Risk: Connect-link emails can be sent to recipients through the PostFast API. <br>
Mitigation: Confirm the recipient and purpose first, and prefer generating connect links without automatic email unless sending is clearly intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/peturgeorgievv/postfast) <br>
- [PostFast](https://postfa.st) <br>
- [API reference](references/api-reference.md) <br>
- [Media specifications](references/media-specs.md) <br>
- [Platform controls](references/platform-controls.md) <br>
- [Media upload flow](references/upload-flow.md) <br>
- [Request examples](examples/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with curl commands and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires `POSTFAST_API_KEY`; generated requests may create, modify, or delete social media scheduling resources.] <br>

## Skill Version(s): <br>
1.10.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
