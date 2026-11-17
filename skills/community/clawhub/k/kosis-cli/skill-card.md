## Description:

Query Korea's national statistics portal (KOSIS, kosis.kr) via the official OpenAPI for title search, category browsing, table metadata, and statistical data including population, employment, prices, business demographics, household income, and regional indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, journalists, researchers, and policy teams use this skill to discover KOSIS tables, inspect table metadata, and retrieve Korean national statistics as JSONL for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be configured through KOSIS_BASE to send the user's KOSIS API key to a non-KOSIS server.

Mitigation: Before use, ensure KOSIS_BASE is unset or exactly the official KOSIS OpenAPI endpoint, and avoid running the skill where environment variables may be controlled by others.

## Reference(s):

- [KOSIS OpenAPI Developer Guide](https://kosis.kr/openapi/devGuide/devGuide_0101.do)
- [KOSIS OpenAPI Key Guide](https://kosis.kr/openapi/devGuide/devGuide_0102.do)
- [KOSIS OpenAPI Error Codes](https://kosis.kr/openapi/devGuide/devGuide_0103.do)
- [KOSIS Statistics Topic Tree](https://kosis.kr/statisticsList/statisticsListIndex.do)
- [Kosis Cli ClawHub Skill Page](https://clawhub.ai/chloepark85/skills/kosis-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with bash command examples; scripts return JSONL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KOSIS_API_KEY, bash, curl, and jq; command errors are written to stderr with non-zero exit codes.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
