## Description:

Retrieves public Xiaohongshu (RedNote) notes, note details, comments, and creator posts for research and analysis, returning structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, brand and marketing teams, and analysts use it to search public RedNote notes, inspect notes and comments, and review creators’ public posts for topic research, competitor monitoring, KOL screening, and sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags privacy and tool-scope concerns, with some files only partially inspected.

Mitigation: Review the intended action and data sharing before use; send only explicitly requested, non-sensitive public search terms and links to the GuaiKei API.

## Reference(s):

- [GuaiKei service and API access](https://www.guaikei.com)
- [ClawHub skill listing](https://clawhub.ai/engheng-art/skills/guaikei-rednote-harvest)
- [Output contract](artifact/references/contract.md)
- [Intent routing](artifact/references/routing.md)
- [Error handling](artifact/references/errors.md)
- [Environment and FAQ](artifact/references/faq.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON with a consistent status, request, metadata, and results envelope, plus concise usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers public content only and read-only lookups; searches and links are sent to the GuaiKei API.]

## Skill Version(s):

1.2.2 (source: frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
