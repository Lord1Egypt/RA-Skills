## Description: <br>
Schedule and publish social media posts to 9 platforms (Instagram, Facebook, TikTok, YouTube, X/Twitter, LinkedIn, Threads, Pinterest, Bluesky) from your AI agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mehrang0](https://clawhub.ai/user/mehrang0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External social media teams and individual operators use this skill to draft, schedule, publish, edit, and review posts across connected Outfeed social accounts from an AI agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish, cancel, delete, or bulk schedule content across connected social media accounts. <br>
Mitigation: Verify each post, target account, timezone, and bulk schedule before approving publication or destructive actions. <br>
Risk: The Outfeed API key can grant the agent access to connected social accounts. <br>
Mitigation: Use a revocable API key when available and connect only the accounts the agent should manage. <br>


## Reference(s): <br>
- [Outfeed](https://outfeed.ai) <br>
- [Outfeed API key settings](https://app.outfeed.ai/settings) <br>
- [ClawHub release page](https://clawhub.ai/mehrang0/outfeed-social-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with MCP tool-call instructions and a JSON configuration snippet] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OUTFEED_API_KEY and npx; bulk draft creation supports up to 25 posts per call.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
