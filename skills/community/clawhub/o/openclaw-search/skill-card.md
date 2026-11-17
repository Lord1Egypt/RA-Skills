## Description:

Openclaw Search helps agents run web, multi-source, and last-30-days research through AIsa for search, synthesis, competitor scans, trend discovery, and structured retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agent operators use this skill to gather recent web and academic evidence, compare tools or companies, and turn multi-source retrieval into concise research briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, URLs, and selected result data are sent to AIsa/Tavily-backed external APIs.

Mitigation: Avoid confidential internal names, private URLs, or sensitive investigations unless the organization approves that external data flow.

Risk: External providers may time out or return partial results, which can make research findings incomplete.

Mitigation: Report provider timeouts or missing sources clearly and do not claim sources that were not actually queried.

## Reference(s):

- [Openclaw Search ClawHub Page](https://clawhub.ai/baofeng-tech/skills/openclaw-search)
- [AIsa API Endpoint](https://api.aisa.one/apis/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; external provider failures should be reported as partial results.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
