## Description: <br>
Read Bluesky profiles, posts, feeds, followers, and threads via the AT Protocol using mostly public endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to retrieve public Bluesky profiles, posts, feeds, follower lists, follow lists, and threads. Post search is available when users provide dedicated Bluesky credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional post search places a Bluesky app password in the gateway URL, which can expose the credential if the URL is logged, shared, or reused. <br>
Mitigation: Use the anonymous public tools when possible; if search is needed, use a dedicated Bluesky app password, treat the configured URL as secret, and rotate or revoke the password after use. <br>


## Reference(s): <br>
- [Pipeworx Bluesky homepage](https://pipeworx.io/packs/bluesky) <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-bluesky) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Configuration] <br>
**Output Format:** [JSON tool responses and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Public read endpoints work anonymously; search_posts requires Bluesky credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
