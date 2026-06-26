## Description: <br>
Searches and reads X/Twitter data, supports social listening workflows, and can publish posts, like or unlike tweets, and follow or unfollow users after OAuth authorization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaimengphp](https://clawhub.ai/user/chaimengphp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search Twitter/X, inspect profiles, timelines, mentions, followers, trends, lists, communities, and Spaces, and to perform authorized posting and engagement actions from an account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post, like, follow, and unfollow through a Twitter/X account after OAuth authorization. <br>
Mitigation: Manually verify every post, media file, target tweet, like, follow, and unfollow before executing commands. <br>
Risk: Command output or shared transcripts can expose the AISA API key or authorization status. <br>
Mitigation: Use a limited, revocable AISA API key and redact status, authorize, post, and engagement outputs before sharing logs. <br>
Risk: Search and engagement workflows can act on the wrong account or tweet when natural-language targets are ambiguous. <br>
Mitigation: Confirm ambiguous accounts or targets before action and rely on resolved tweet or user context rather than guessing identifiers. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chaimengphp/openclaw-aisa-twitter) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>
- [OpenClaw Twitter Engagement](references/engage_twitter.md) <br>
- [OpenClaw Twitter OAuth](references/post_twitter.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and curl command examples plus JSON API responses from the service clients] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, python3, AISA_API_KEY, and OAuth authorization for posting, liking, following, and unfollowing actions.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
