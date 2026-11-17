## Description:

法律助手与法条检索工具，用于检索民法典、刑法、劳动法、合同法等国家法律法规知识库并返回相关法律条文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[eastern-law-firm](https://clawhub.ai/user/eastern-law-firm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route Chinese legal queries to a national-law knowledge search workflow and present matched statutes with legal names, chapters, article numbers, article text, and relevance scores. It is intended for legal lookup and triage support, not as a substitute for professional legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Legal queries may include personal, case-specific, or confidential details that are sent to an external Orientlaw-hosted search API.

Mitigation: Use only non-confidential queries, remove identifying details before use, and require clear external data-handling documentation before deployment.

Risk: The artifact contains an embedded bearer token for the search API.

Mitigation: Require the publisher to remove the built-in token, rotate the exposed credential, and load credentials from a protected runtime secret.

Risk: The skill triggers broadly for legal consultation and may be mistaken for authoritative legal advice.

Mitigation: Constrain use to retrieval and citation of matched legal text, preserve the documented empty-result behavior, and route legal decisions to qualified review.

## Reference(s):

- [API response format and parsing guide](artifact/references/api_response_format.md)
- [ClawHub skill page](https://clawhub.ai/eastern-law-firm/skills/national-law-knowledge-search)
- [Publisher profile](https://clawhub.ai/user/eastern-law-firm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown legal-search responses with shell command examples and JSON API output handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selects topk based on query specificity and formats empty results without unsupported speculation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
