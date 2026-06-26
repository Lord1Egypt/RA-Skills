## Description: <br>
Posta helps agents create, upload, schedule, publish, and analyze social media posts across Instagram, TikTok, LinkedIn, YouTube, X/Twitter, Facebook, Pinterest, Threads, and Bluesky from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stgime](https://clawhub.ai/user/stgime) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and marketing operators use this skill to manage Posta-connected social accounts from an agent: draft content, upload media, schedule or publish posts, and review analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect live social accounts by scheduling, publishing, deleting media, exporting analytics, or triggering third-party image generation. <br>
Mitigation: Require a visible preview and explicit user approval before mutating account state, exporting analytics, or spending third-party generation credits. <br>
Risk: Credentials and API responses may be exposed on shared machines or through temporary token and response caching. <br>
Mitigation: Prefer a revocable POSTA_API_TOKEN over email/password, avoid shared machines, and clear local temporary token or response files after sensitive sessions. <br>
Risk: Generated or uploaded content can be published to the wrong platform, account, time, or caption length limit. <br>
Mitigation: Validate target accounts, platform requirements, caption limits, media properties, and scheduled time before publish or schedule actions. <br>


## Reference(s): <br>
- [Posta ClawHub Skill Page](https://clawhub.ai/stgime/posta) <br>
- [Posta API Reference](references/posta-api-reference.md) <br>
- [Content Generation Patterns](references/content-generation.md) <br>
- [Workflow Examples](examples/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POSTA_API_TOKEN, curl, and jq; FAL_KEY is optional for image generation.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
