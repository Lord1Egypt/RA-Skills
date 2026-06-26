## Description: <br>
Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AISA relay for research, posting, likes, follows, and related workflows without sharing passwords. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research X/Twitter content and perform approved posting or engagement actions through Python clients. Write actions require OAuth authorization and a final confirmation artifact that names the exact action, target, payload, and approval state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post, like, follow, or unfollow on an X/Twitter account after OAuth authorization. <br>
Mitigation: Require OAuth authorization and a final user-approved confirmation artifact naming the exact action, target, text or media payload, and approval state before running any write command. <br>
Risk: Command output from authorize or post workflows may expose sensitive AISA API key material. <br>
Mitigation: Treat authorization and posting output as sensitive, avoid sharing logs publicly, and redact credentials before storing or transmitting command output. <br>
Risk: The workflow depends on the AISA relay for Twitter/X read, posting, media upload, and engagement actions. <br>
Mitigation: Install and use the skill only when the user trusts the AISA relay and is comfortable granting OAuth-backed Twitter/X authority. <br>


## Reference(s): <br>
- [OpenClaw Twitter OAuth](references/post_twitter.md) <br>
- [OpenClaw Twitter Engagement](references/engage_twitter.md) <br>
- [AISA homepage](https://aisa.one) <br>
- [ClawHub skill page](https://clawhub.ai/aisadocs/openclaw-twitter-post-engage-slot3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and OAuth approval before write actions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
