## Description: <br>
Monitor keywords through Google Alerts RSS feeds and format results for brand, product, industry, and competitor tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bgoodwinstudio](https://clawhub.ai/user/bgoodwinstudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, communications, product, and competitive intelligence teams use this skill to fetch Google Alerts results for selected keywords and turn them into concise monitoring summaries. Agents can use the JSON output and formatted cards in recurring reports or review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitored keywords and the Google Alerts feed identifier are sent to Google Alerts and may appear in shared logs or screenshots. <br>
Mitigation: Run the skill as a normal user, keep the feed identifier out of shared material, and confirm that monitored keywords are appropriate to send to Google Alerts. <br>
Risk: Automated monitoring summaries can include incomplete, stale, or misleading search results. <br>
Mitigation: Review generated reports before forwarding them or using them in decisions. <br>


## Reference(s): <br>
- [Google Alerts](https://www.google.com/alerts) <br>
- [Google Alerts feed endpoint](https://www.google.com/alerts/feeds/) <br>
- [Setup guide](references/setup-guide.md) <br>
- [Keyword examples](references/keywords.md) <br>
- [ClawHub skill page](https://clawhub.ai/bgoodwinstudio/google-alerts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [JSON arrays from search results plus formatted text monitoring cards] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, python3, and a GOOGLE_ALERT_FEED_ID value.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
