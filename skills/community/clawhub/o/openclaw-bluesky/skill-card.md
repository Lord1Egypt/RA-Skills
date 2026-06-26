## Description: <br>
Bluesky/AT Protocol orchestration skill for authenticated interaction with the Bluesky Social network: post, reply, like, repost, quote, bookmark, and upload media. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Heather-Herbert](https://clawhub.ai/user/Heather-Herbert) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an authenticated agent interact with a Bluesky account for posting, replies, quotes, likes, reposts, bookmarks, and media uploads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform live account-changing Bluesky actions such as posting, liking, reposting, quoting, bookmarking, and uploading media. <br>
Mitigation: Require manual confirmation before each account-changing action. <br>
Risk: The skill requires a Bluesky app password for authenticated use. <br>
Mitigation: Use a dedicated revocable app password and store it only in secrets or environment configuration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Heather-Herbert/openclaw-bluesky) <br>
- [Publisher Profile](https://clawhub.ai/user/Heather-Herbert) <br>
- [AT Protocol Docs](https://atproto.com/) <br>
- [Bluesky Developer Docs](https://docs.bsky.app/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python API usage and shell setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce authenticated Bluesky API actions when configured with a handle and app password.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
