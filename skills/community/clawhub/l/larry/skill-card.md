## Description: <br>
Larry helps agents run a TikTok slideshow marketing workflow by researching competitors, generating images, adding text overlays, creating Postiz draft posts, tracking analytics, and iterating on hooks and calls to action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OllieWazza](https://clawhub.ai/user/OllieWazza) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers, founders, and marketing operators use this skill to set up repeatable TikTok slideshow campaigns for an app, product, or service. It guides onboarding, competitor research, content generation, draft posting, analytics review, and RevenueCat-informed conversion tracking when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare public social posts and cross-posts through Postiz. <br>
Mitigation: Keep posts as drafts where possible and review every caption, slide, platform target, and sound choice before publishing. <br>
Risk: The workflow uses API keys for Postiz, image generation providers, and optionally RevenueCat business data. <br>
Mitigation: Use least-privilege credentials, store generated config outside version control and synced folders, and rotate keys if exposed. <br>
Risk: RevenueCat analytics can include sensitive customer, subscriber, trial, churn, and revenue information. <br>
Mitigation: Limit access to authorized operators, minimize retained snapshots, and remove generated reports or JSON snapshots that are no longer needed. <br>
Risk: RevenueCat dashboard scraping is mentioned as a fallback when API data is unavailable. <br>
Mitigation: Use official APIs where available and only approve browser sessions for a narrow, documented analytics task. <br>
Risk: Connecting the wrong TikTok video ID to a Postiz post can permanently associate analytics with the wrong post. <br>
Mitigation: Wait for TikTok indexing, verify chronological matches, and confirm the number of unconnected posts matches the number of new TikTok videos before updating release IDs. <br>
Risk: Competitor research and account warmup guidance can encourage behavior that may conflict with platform expectations if applied carelessly. <br>
Mitigation: Require user approval for browser research, avoid spam-like activity, and align posting and engagement practices with each platform's terms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OllieWazza/larry) <br>
- [Publisher profile](https://clawhub.ai/user/OllieWazza) <br>
- [Analytics & Feedback Loop](references/analytics-loop.md) <br>
- [App Category Templates](references/app-categories.md) <br>
- [Competitor Research Guide](references/competitor-research.md) <br>
- [RevenueCat Integration](references/revenuecat-integration.md) <br>
- [Slide Structure & Hook Writing](references/slide-structure.md) <br>
- [Postiz signup link](https://postiz.pro/oliverhenry) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with JSON configuration files, Node.js scripts, generated PNG slides, Postiz API calls, and daily Markdown reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local campaign files under tiktok-marketing/ and requires user-provided API credentials for posting, image generation, and optional conversion tracking.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
