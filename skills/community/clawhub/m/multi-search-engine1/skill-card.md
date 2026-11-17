## Description:

Multi search engine integration with 17 engines (8 CN + 9 Global), advanced search operators, time filters, site search, privacy-oriented engines, and WolframAlpha knowledge queries without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp33333333333](https://clawhub.ai/user/cp33333333333)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to choose search providers, construct search URLs, and apply advanced operators for web, site-specific, file-type, time-filtered, privacy-oriented, and knowledge queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to the selected external search engine and may expose secrets, personal data, internal project names, or confidential research topics.

Mitigation: Avoid sensitive query terms and prefer a privacy-oriented provider when searches are sensitive.

Risk: Privacy claims for individual search providers may not fully describe how queries are handled after the agent sends them.

Mitigation: Treat provider privacy notes as guidance, not guarantees, and review provider terms before using the skill for sensitive work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cp33333333333/skills/multi-search-engine1)
- [International search guide](references/international-search.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with inline search URL and web_fetch examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API keys are required; search terms are sent to the selected external search provider.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact files reference 2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
