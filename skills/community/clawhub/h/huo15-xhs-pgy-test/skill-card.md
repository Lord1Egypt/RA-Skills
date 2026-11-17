## Description:

Guides an agent through authorized Xiaohongshu PGY blogger discovery, profile data extraction, and structured reporting for keyword and region-based creator research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, creator partnership teams, and authorized agents use this skill to search PGY for relevant Xiaohongshu bloggers and compile profile, audience, performance, and pricing details into reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to handle a PGY password.

Mitigation: Use only PGY accounts the user is authorized to access, prefer browser-only login when possible, and avoid sharing passwords in chat.

Risk: The skill extracts logged-in PGY page text and can place account-gated creator data into reports.

Mitigation: Review generated reports for sensitive or unnecessary account-gated data before saving or sharing them.

Risk: The security verdict is suspicious because the workflow lacks enough safeguards around credentials and logged-in scraping.

Mitigation: Review the skill before installing or running it, and confirm the intended use complies with the PGY account's permissions.

## Reference(s):

- [PGY Operation Guide](artifact/references/pgy-operation-guide.md)
- [Xiaohongshu PGY Platform](https://pgy.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [guidance, code, markdown, text]

**Output Format:** [Markdown report with browser automation steps and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authorized PGY account; generated reports may include account-gated creator metrics and should be reviewed before saving or sharing.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
