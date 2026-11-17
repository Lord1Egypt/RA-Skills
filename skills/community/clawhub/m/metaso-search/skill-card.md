## Description:

Metaso Search helps agents query the MetaSo Chinese AI search API and return structured Chinese search results and answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiuxinyuan321](https://clawhub.ai/user/qiuxinyuan321)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to perform Chinese-language web searches, retrieve structured results, and optionally request JSON output for downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if stored in the documented plaintext local secrets file.

Mitigation: Use the METASO_API_KEY environment variable or a secret manager, avoid shared or version-controlled storage, and rotate any key that may have been exposed.

Risk: Search queries are sent to a third-party MetaSo API endpoint.

Mitigation: Avoid submitting confidential data in queries and review returned content before using it in user-facing or automated workflows.

## Reference(s):

- [ClawHub Metaso Search Skill Page](https://clawhub.ai/qiuxinyuan321/skills/metaso-search)
- [MetaSo Search API Playground](https://metaso.cn/search-api/playground)
- [MetaSo](https://metaso.cn/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Markdown guidance with PowerShell examples; search results can be returned as text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MetaSo API key supplied through METASO_API_KEY or another secret-management mechanism.]

## Skill Version(s):

1.2.0 (source: server release, artifact skill.json, artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
