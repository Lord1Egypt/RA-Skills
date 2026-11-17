## Description:

Analyzes patent activity across problem-by-technical-means matrices and highlights sparse combinations as candidate R&D or patent-filing opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

R&D teams, patent strategists, and engineers use the skill to map patent activity by technical problem and solution, then investigate sparse combinations as possible research or filing directions.

### Deployment Geography for Use:

China and selected international patent collections, including the United States, Europe, Japan, South Korea, and WIPO.

## Known Risks and Mitigations:

Risk: API credentials could be exposed.

Mitigation: Use an isolated workspace and limited trial key; keep production credentials out of chat and unprotected files.

Risk: The client may access files outside its intended cache.

Mitigation: Prefer a version that restricts authenticated destinations and redirects and validates cache filenames; use an isolated workspace until then.

Risk: Search terms may disclose confidential information, and API calls may incur charges.

Mitigation: Approve search terms before transmission, set a spending limit, and review usage costs.

## Reference(s):

- [Patent search workflow](artifact/references/search-workflow.md)
- [Query construction guide](artifact/references/query-construction.md)
- [PatentMax API reference](artifact/references/api-reference.md)
- [ClawHub release](https://clawhub.ai/ip930/skills/patent-gap-finder)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [text, markdown, CSV files]

**Output Format:** [Spreadsheet-friendly CSV matrix with a candidate-gap list and concise textual findings.]

**Output Parameters:** [2D (technical problems × technical means)]

**Other Properties Related to Output:** [Highlights candidate sparse combinations; findings require relevance checks and do not establish technical feasibility, commercial value, or patentability.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
