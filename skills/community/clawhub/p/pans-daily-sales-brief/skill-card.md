## Description: <br>
Generates a daily sales brief for AI compute sales by summarizing customer follow-ups, expiring contracts, new leads, performance metrics, and competitor news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashiming](https://clawhub.ai/user/dashiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales representatives and account managers use this skill to maintain local customer pipeline data and generate daily sales reports for follow-up planning. It supports adding clients, contracts, and leads, listing pipeline data, and producing text or JSON briefs for daily automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sales and customer pipeline data in a local JSON file. <br>
Mitigation: Use it only on protected machines and avoid entering regulated, secret, or highly confidential customer information unless local storage and backups are secured. <br>
Risk: Add and update commands mutate the local pipeline data file. <br>
Mitigation: Review JSON inputs before running mutating commands and keep backups for important pipeline records. <br>
Risk: The competitor-news feature can use an external search helper and may return unverified snippets. <br>
Mitigation: Review the referenced helper skill before enabling competitor-news searches and verify news results before using them in sales decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dashiming/pans-daily-sales-brief) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Plain text daily brief or structured JSON, with shell command examples in documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read, write, and update local sales pipeline JSON data used to generate the brief.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
