## Description:

Multi search engine integration with 17 engines (8 CN + 9 Global). Supports advanced search operators, time filters, site search, privacy engines, and WolframAlpha knowledge queries. No API keys required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasdkc](https://clawhub.ai/user/jasdkc)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to run searches across Chinese and global search providers for current information, news, academic papers, site-specific queries, privacy-focused search, and WolframAlpha-style knowledge questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and optional API keys may be exposed to configured third-party search providers.

Mitigation: Do not search for secrets, tokens, private URLs, regulated data, or real passwords; keep optional API keys out of version control and rotate them if exposed.

Risk: Remote password-generation and credential-dork examples can create unsafe credential-handling workflows if used operationally.

Mitigation: Treat those examples only as search syntax references and avoid using them for real password generation or credential discovery.

## Reference(s):

- [International Search Reference](artifact/references/international-search.md)
- [ClawHub Skill Page](https://clawhub.ai/jasdkc/skills/itisbig-multi-search-engine)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python, Bash, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search queries may be sent to configured third-party search providers; optional API keys are supported.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact docs also list 2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
