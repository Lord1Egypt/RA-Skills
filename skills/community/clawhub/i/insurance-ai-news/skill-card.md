## Description:

Generates a bilingual daily briefing on global insurance AI news, covering regional updates, investment, regulation, key companies, and AI talent movements, then syncs the report to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suiclaw](https://clawhub.ai/user/suiclaw)

### License/Terms of Use:

MIT-0 License

## Use Case:

Insurance, strategy, research, and operations teams use this skill to produce a bilingual daily scan of insurance AI developments across regions, investments, regulation, priority companies, and talent moves. The skill formats each item with dates, takeaways, source links, and a Feishu document link for distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated publication could write the brief to an unintended Feishu account or workspace.

Mitigation: Confirm the Feishu account, target workspace, and whether daily scheduled publishing should be enabled before deployment.

Risk: The news brief could include stale, incomplete, or unsourced items when search results are weak.

Mitigation: Require a publication date and original source URL for every news item, and clearly state when no same-day news is available.

Risk: A Feishu document could be created with only a title if the body append step fails.

Mitigation: Append the full report after document creation and verify the resulting document contains more than the title before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suiclaw/skills/insurance-ai-news)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Bilingual Markdown news brief with source links, takeaways, sectioned regional coverage, and a Feishu document URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily 08:30 scheduled posture is described by the skill; Feishu publication depends on the configured document tool and workspace.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
