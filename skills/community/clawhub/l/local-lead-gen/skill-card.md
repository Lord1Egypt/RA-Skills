## Description:

Automates local business prospecting by finding businesses, scoring their websites, extracting contact emails, and sending personalized outreach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[merjua14](https://clawhub.ai/user/merjua14)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to find local businesses with outdated or low-scoring websites, review candidate leads, and run cold outreach workflows for web services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated cold outreach may send messages to scraped recipients with limited review and suppression controls.

Mitigation: Use dry-run first, review every recipient and message before sending, and configure lawful unsubscribe and suppression handling outside the script.

Risk: The workflow calls external search, crawling, website, and email services while handling outreach credentials.

Mitigation: Run it only in a controlled environment, scope API keys to the intended use, and avoid environments with access to sensitive internal network services.

## Reference(s):

- [Website Scoring Criteria](references/scoring-criteria.md)
- [Cold Email Best Practices](references/email-best-practices.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands for dry-run or live cold-outreach workflows, depending on user configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
