## Description:

Checks a site's robots.txt to determine whether major AI search and answer crawlers are allowed, blocked, or partially blocked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxaeo](https://clawhub.ai/user/maxaeo)

### License/Terms of Use:

MIT-0

## Use Case:

External site owners, SEO/AEO teams, and developers use this skill to review a public robots.txt file for AI crawler access and get the specific rules and edits that affect visibility in AI answer engines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested robots.txt edits could change crawler access and affect search or AI answer visibility if applied without review.

Mitigation: Review any proposed robots.txt changes before applying them to a live site.

Risk: The skill checks robots.txt only, so server-side bot controls may still block crawlers even when robots.txt allows them.

Mitigation: Treat the result as a first-gate access check and separately review WAF, CDN, IP reputation, and bot-management settings when crawler access still fails.

## Reference(s):

- [MaxAEO crawler matrix](https://maxaeo.ai/geo-method/)
- [MaxAEO homepage](https://maxaeo.ai/)
- [ClawHub skill page](https://clawhub.ai/maxaeo/skills/llm-crawler-access-check)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown table with concise findings and robots.txt change snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads one public robots.txt file and advises on crawler access without editing the site.]

## Skill Version(s):

1.1.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
