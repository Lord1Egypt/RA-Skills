## Description:

Analyzes a patent’s backward and forward citations, supplementing incomplete forward-citation data with clearly labeled later similar patents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Patent researchers, analysts, and IP professionals use this skill to trace a patent’s cited technical sources and later follow-on activity, then review the results in a spreadsheet-compatible table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials, authenticated redirects, or cache-file handling may expose secrets or local data.

Mitigation: Before using a paid key, seek fixes for credential storage, authenticated redirects, and cache-path validation; provide credentials through a protected environment, not chat.

Risk: Retrying after a timeout may lead to unexpected charges.

Mitigation: Use a limited-spending key and check account charges before retrying timeouts.

Risk: Patent searches may transmit unpublished invention details to PatentMax.

Mitigation: Keep unpublished invention details out of searches unless that transmission is approved.

## Reference(s):

- [PatentMax API reference](references/api-reference.md)
- [Patent search workflow](references/search-workflow.md)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [PatentMax](https://api.ip930.com)
- [ClawHub skill release](https://clawhub.ai/ip930/skills/patent-citation-map)
- [Publisher profile](https://clawhub.ai/user/ip930)

## Skill Output:

**Output Type(s):** [Analysis, Files, Text]

**Output Format:** [UTF-8 CSV with BOM, plus a concise written summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates actual citations from later similar patents; similar patents are labeled as non-citations.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
