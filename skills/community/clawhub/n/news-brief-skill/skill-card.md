## Description: <br>
News Brief Skill creates personalized daily news summaries from configured topics and sources, then delivers them through user-selected channels with feedback-based preference updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[17oko](https://clawhub.ai/user/17oko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to receive recurring, interest-based news briefs across configured topics such as technology, finance, politics, and general news. It also supports feedback-driven adjustments to content, format, delivery channel, and schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores user identifiers, preferences, logs, backups, and delivery credentials. <br>
Mitigation: Use revocable webhook or bot tokens, avoid reusing sensitive email passwords, and delete stored configs, logs, backups, and feedback history when no longer needed. <br>
Risk: Scheduled outbound delivery can send content to configured channels without a manual action each time. <br>
Mitigation: Confirm delivery channels, schedule, and frequency before enabling recurring briefs, and ensure operators can pause or disable delivery. <br>
Risk: Privacy and secret-handling disclosures are incomplete in the available evidence. <br>
Mitigation: Review local storage, credential handling, and retention behavior before deployment, especially for shared or managed environments. <br>


## Reference(s): <br>
- [News Brief Skill documentation](references/documentation.md) <br>
- [ClawHub release page](https://clawhub.ai/17oko/news-brief-skill) <br>
- [Publisher profile](https://clawhub.ai/user/17oko) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Plain text or Markdown news brief with structured news items, credibility labels, and feedback prompts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local user preferences and delivery settings based on feedback.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
