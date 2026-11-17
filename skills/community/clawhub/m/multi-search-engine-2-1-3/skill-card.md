## Description:

Multi Search Engine integrates 16 Chinese and global search engines for advanced, privacy-aware web searching without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcdentoncore](https://clawhub.ai/user/jcdentoncore)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to issue web searches across Chinese and global providers, apply advanced operators and time filters, and aggregate results into a concise search report. It is suited to agents that need broad public-web discovery without search API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and request metadata are sent to selected third-party search engines, despite artifact privacy text claiming no external data transmission.

Mitigation: Avoid secrets, credentials, personal data, and confidential business queries; constrain engines and regions before use.

Risk: The server security verdict is suspicious because the privacy notice conflicts with the skill's external search behavior.

Mitigation: Review the skill before installing and communicate the external data-sharing behavior to users.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jcdentoncore/skills/multi-search-engine-2-1-3)
- [Advanced Domestic Search Guide](artifact/references/advanced-search.md)
- [International Search Guide](artifact/references/international-search.md)
- [Publisher Profile](https://clawhub.ai/user/jcdentoncore)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown search report with inline web_fetch command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Aggregates results from selected search engines; no API keys required.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata also reports 2.1.3 and 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
