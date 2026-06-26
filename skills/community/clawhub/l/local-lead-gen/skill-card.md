## Description: <br>
Automated local business lead generation and cold outreach pipeline that scans businesses by niche and city, scores their websites, identifies bad or outdated sites, enriches contact information, and sends personalized cold emails pitching services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[merjua14](https://clawhub.ai/user/merjua14) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, sales operators, and business development teams use this skill to find local businesses with weak websites, score them as prospects, and prepare or send personalized outreach for web design or development services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically scrape contact information and send cold emails from the user's account without a final approval step. <br>
Mitigation: Run with --dry-run first, review every recipient and message before sending, and add an explicit send-confirmation gate before live outreach. <br>
Risk: Cold outreach can violate anti-spam, privacy, provider, or website terms if recipients and messages are not governed carefully. <br>
Mitigation: Maintain suppression and unsubscribe handling, remove bounced contacts, limit sending volume, and confirm compliance requirements before use. <br>


## Reference(s): <br>
- [Website Scoring Criteria](references/scoring-criteria.md) <br>
- [Cold Email Best Practices](references/email-best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration edits, and generated lead/outreach workflow artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external search, crawling, email, and tracking services when configured with user-provided credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
