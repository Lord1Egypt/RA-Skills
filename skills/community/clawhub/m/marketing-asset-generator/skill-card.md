## Description: <br>
AI-powered marketing asset generation workflow. Combines DuckDuckGo design inspiration search, Gemini Nano Banana Pro image generation, Feishu Drive cloud storage, and Slack team notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams and agent users use this skill to research campaign inspiration, generate marketing images, store the assets in Feishu Drive, and notify a configured Slack channel. It is intended for automated asset workflows such as campaign banners, launch announcements, scheduled generation, event-triggered creation, localization, and A/B test variants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Campaign prompts, generated images, Feishu file links, and research snippets are processed by external services and shared to configured Feishu and Slack destinations. <br>
Mitigation: Install only when this external-sharing workflow is intended, avoid confidential unreleased material unless those services are approved for it, and use a narrow Slack channel and Feishu folder. <br>
Risk: The workflow requires multiple service credentials for Gemini, Feishu, and Slack. <br>
Mitigation: Use least-privilege API keys and bot tokens, store secrets outside source files, and rotate credentials if they are exposed. <br>
Risk: Dependency versions are lower-bounded rather than pinned, which can change runtime behavior in production. <br>
Mitigation: Pin and review dependency versions before production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/marketing-asset-generator) <br>
- [README](README.md) <br>
- [Skill documentation](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, API Calls, Text, Configuration] <br>
**Output Format:** [PNG image files, Feishu file links, Slack notification messages, and Python dictionary workflow results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured Google Gemini, Feishu, and Slack credentials; generated assets and research snippets may be sent to external services and shared to the configured folder and channel.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
