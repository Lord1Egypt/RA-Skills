## Description: <br>
Automates TikTok and Instagram slideshow marketing by guiding competitor research, image generation, text overlays, multi-platform posting, analytics tracking, and iterative optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sammy-the-bot](https://clawhub.ai/user/sammy-the-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to set up an agent-assisted social marketing workflow for an app or product, including slideshow creation, posting, analytics checks, and conversion-aware iteration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post to connected social accounts. <br>
Mitigation: Use least-privilege API keys, restrict connected profiles and platforms, and review every generated post before publishing. <br>
Risk: The workflow can persist business data and secrets locally. <br>
Mitigation: Keep configuration files, reports, analytics snapshots, and API keys out of source control and store secrets with the user's normal secret-management process. <br>
Risk: The skill can create recurring jobs for daily reporting or posting workflows. <br>
Mitigation: Enable scheduled jobs only with explicit user approval and document how to disable or modify each schedule. <br>
Risk: The artifact includes platform-detection evasion guidance. <br>
Mitigation: Avoid detection-evasion behavior and require the user to follow each platform's terms, automation rules, and account-safety policies. <br>


## Reference(s): <br>
- [Analytics & Feedback Loop](references/analytics-loop.md) <br>
- [App Category Templates](references/app-categories.md) <br>
- [Competitor Research Guide](references/competitor-research.md) <br>
- [RevenueCat Integration](references/revenuecat-integration.md) <br>
- [Slide Structure & Hook Writing](references/slide-structure.md) <br>
- [Upload-Post](https://upload-post.com) <br>
- [ClawHub skill page](https://clawhub.ai/sammy-the-bot/larry-marketing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, JavaScript helper scripts, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local configuration, slideshow assets, post metadata, analytics summaries, and daily report files when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
