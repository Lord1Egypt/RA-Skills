## Description: <br>
Curates twice-daily English Telegram news pushes covering industry, financial, and global political news with strict formatting, deduplication, and trusted-source filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chamic24](https://clawhub.ai/user/chamic24) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance and trading readers use this skill to receive Telegram-ready morning and evening news updates. It selects high-signal headlines across trading industry, macro-financial, and global political categories and formats them for direct posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled Telegram posting could publish to an unintended audience or send without adequate review. <br>
Mitigation: Use a dedicated Telegram bot limited to the intended chat or channel, require preview or explicit opt-in for scheduled sends, and keep a clear pause or stop process. <br>
Risk: Overbroad account permissions could expose trading, payment, purchase, or unrelated account actions beyond the skill's news-posting purpose. <br>
Mitigation: Grant only news browsing and tightly scoped Telegram posting permissions; do not grant purchase, trading, payment, or broad account access. <br>
Risk: News selection can include duplicate, low-quality, or misleading stories if source controls are not maintained. <br>
Mitigation: Use the trusted-source and deduplication rules from the artifact, and review high-impact posts before distribution. <br>


## Reference(s): <br>
- [News Telegram Push on ClawHub](https://clawhub.ai/chamic24/news-telegram-push) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [English Telegram-ready Markdown-style list with three sections, numbered headlines, and indented Read more links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exactly three sections with 10 numbered items each; no summaries, source labels, or commentary.] <br>

## Skill Version(s): <br>
2.0.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
