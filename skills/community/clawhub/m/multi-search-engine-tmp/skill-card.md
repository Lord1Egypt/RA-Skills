## Description:

Multi search engine integration with 17 engines (8 CN + 9 Global). Supports advanced search operators, time filters, site search, privacy engines, and WolframAlpha knowledge queries. No API keys required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelaner](https://clawhub.ai/user/kelaner)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to compose direct search-engine requests across Chinese and global search providers, including advanced operators, time filters, site-specific search, privacy-oriented search, DuckDuckGo Bangs, and WolframAlpha knowledge queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags unsafe search examples that could support credential-hunting patterns or searches for deleted or unsafe content.

Mitigation: Keep searches user-directed, avoid credential-hunting patterns, and prefer safe-search defaults.

Risk: The skill sends query text to third-party search engines.

Mitigation: Avoid submitting secrets, personal data, or confidential business information in search queries.

## Reference(s):

- [International Search Guide](references/international-search.md)
- [ClawHub Skill Page](https://clawhub.ai/kelaner/skills/multi-search-engine-tmp)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with example web_fetch commands and search URL patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API keys required; outputs depend on third-party search engine availability and policies.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact documentation also references v2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
