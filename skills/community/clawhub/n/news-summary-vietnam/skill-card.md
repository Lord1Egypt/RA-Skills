## Description:

Collects Vietnamese news headlines from Bao Moi, VnExpress, Tuoi Tre, and Dan Tri and posts linked summaries to a Telegram channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[padit69](https://clawhub.ai/user/padit69)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to set up a scheduled Telegram bot that summarizes Vietnamese news and links readers to original articles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and uses a Telegram bot token locally.

Mitigation: Keep config.json private, exclude it from version control, and rotate the token if it is exposed.

Risk: The installer can add a cron job that runs the news sender three times daily.

Mitigation: Review or add the cron entry manually so the schedule and command path match the intended deployment.

Risk: The Bao Moi scraper launches Chromium with sandbox-disabling flags.

Mitigation: Run the browser scraper in a restricted environment and prefer enabling Chromium sandboxing where the host supports it.

Risk: The skill depends on Playwright for browser-based scraping.

Mitigation: Pin and review Playwright versions before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/padit69/skills/news-summary-vietnam)
- [Bao Moi](https://baomoi.com)
- [VnExpress RSS Feed](https://vnexpress.net/rss/tin-moi-nhat.rss)
- [Tuoi Tre RSS Feed](https://tuoitre.vn/rss/homepage.rss)
- [Dan Tri RSS Feed](https://dantri.com.vn/rss/home.rss)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Telegram HTML message with linked news items; setup guidance in Markdown and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Telegram bot token and chat ID configuration.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
