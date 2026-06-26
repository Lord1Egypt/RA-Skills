## Description: <br>
Postiz helps agents schedule social media and chat posts across 28+ connected channels, including X, LinkedIn, Reddit, Instagram, Facebook, YouTube, TikTok, Discord, Slack, Mastodon, Bluesky, and others. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nevo-david](https://clawhub.ai/user/nevo-david) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, social media operators, developers, and AI agents use this skill to authenticate with Postiz, discover connected integrations, upload media, draft or schedule posts across supported channels, manage posts, and review analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create, upload, schedule, connect, and delete content on real connected social accounts. <br>
Mitigation: Before create, delete, upload, connect, or bulk scheduling actions, require the agent to show the exact content, target accounts, integration IDs, schedule, and deletion target; prefer drafts or test accounts first. <br>
Risk: Long-lived Postiz API keys can be exposed if stored in shell profile files or echoed during setup. <br>
Mitigation: Use temporary environment exports or a secrets manager for POSTIZ_API_KEY, and avoid persisting credentials in shell startup files. <br>
Risk: Incorrect platform settings or media references can publish unintended content or fail on provider-specific requirements. <br>
Mitigation: Review integration settings, media upload results, target provider settings, and scheduled timestamps before allowing the post command to run. <br>


## Reference(s): <br>
- [Postiz public API documentation](https://docs.postiz.com/public-api/introduction) <br>
- [Postiz website](https://postiz.com) <br>
- [Postiz npm package](https://www.npmjs.com/package/postiz) <br>
- [Postiz GitHub repository](https://github.com/gitroomhq/postiz-app) <br>
- [ClawHub skill page](https://clawhub.ai/nevo-david/postiz) <br>
- [README.md](artifact/README.md) <br>
- [Provider settings](artifact/PROVIDER_SETTINGS.md) <br>
- [Integration tools workflow](artifact/INTEGRATION_TOOLS_WORKFLOW.md) <br>
- [Supported file types](artifact/SUPPORTED_FILE_TYPES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POSTIZ_API_URL and POSTIZ_API_KEY environment variables when using API-key authentication.] <br>

## Skill Version(s): <br>
1.0.15 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
