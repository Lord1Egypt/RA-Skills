## Description: <br>
Query Korea's national statistics portal (KOSIS, kosis.kr) via the official OpenAPI for title search, category browsing, table metadata, and statistics data covering population, employment, prices, business demographics, household income, and regional indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, journalists, researchers, policy teams, and developers use this skill to discover KOSIS statistical tables, inspect table metadata, and retrieve Korean national statistics as line-delimited JSON for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a KOSIS API key, which is a sensitive credential. <br>
Mitigation: Use a dedicated KOSIS API key, keep it in the environment, and avoid sharing command transcripts that expose it. <br>
Risk: KOSIS queries may count against the user's API quota. <br>
Mitigation: Use focused searches, explicit filters, and recent-period limits before running broad table or bulk requests. <br>
Risk: Changing KOSIS_BASE can redirect requests away from the official KOSIS endpoint. <br>
Mitigation: Leave KOSIS_BASE at the default official endpoint unless intentionally testing a trusted alternate endpoint. <br>


## Reference(s): <br>
- [KOSIS OpenAPI developer guide](https://kosis.kr/openapi/devGuide/devGuide_0101.do) <br>
- [KOSIS OpenAPI key guide](https://kosis.kr/openapi/devGuide/devGuide_0102.do) <br>
- [KOSIS OpenAPI error codes](https://kosis.kr/openapi/devGuide/devGuide_0103.do) <br>
- [KOSIS statistics topic tree](https://kosis.kr/statisticsList/statisticsListIndex.do) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; scripts emit JSONL from KOSIS API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, jq, and a user-provided KOSIS_API_KEY.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
