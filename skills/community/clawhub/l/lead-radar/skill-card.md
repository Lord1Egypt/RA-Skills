## Description: <br>
Lead Radar scans Reddit, Hacker News, Indie Hackers, Stack Overflow, Quora, Hashnode, Dev.to, GitHub, and Lobsters each morning for people actively asking for what the user sells, then delivers the top buying-intent leads to Telegram with draft replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bencpnd](https://clawhub.ai/user/bencpnd) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External sales and marketing users use Lead Radar to monitor public communities for posts matching their offer, score likely buying intent, and receive a daily Telegram digest with suggested replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the offer description and scraped post snippets to Google Gemini for scoring and sends the lead digest through Telegram. <br>
Mitigation: Avoid confidential business secrets in OFFER_DESCRIPTION and install only when these external data flows are acceptable. <br>
Risk: The skill runs as a daily background job that contacts multiple public platforms and the publisher's license backend. <br>
Mitigation: Review the configured schedule and required environment variables before deployment, and monitor source-health warnings in Telegram. <br>
Risk: Draft replies may be inaccurate, poorly targeted, or inappropriate for a sales context. <br>
Mitigation: Review and edit all drafted replies before sending them to prospects. <br>
Risk: The skill stores a local seen-posts database for deduplication. <br>
Mitigation: Treat the local .lead-radar data directory as operational data and remove it when decommissioning the skill if retention is not desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bencpnd/lead-radar) <br>
- [Lead Radar Website](https://lead-radar.pro) <br>
- [GitHub REST Search API](https://docs.github.com/en/rest/search) <br>
- [Forem API Documentation](https://developers.forem.com/api/v1) <br>
- [Stack Exchange API Documentation](https://api.stackexchange.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Telegram message containing ranked leads, source links, intent scores, explanations, and draft replies.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Daily scheduled digest; normally returns up to 10 leads and may truncate content to fit Telegram message limits.] <br>

## Skill Version(s): <br>
1.3.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
