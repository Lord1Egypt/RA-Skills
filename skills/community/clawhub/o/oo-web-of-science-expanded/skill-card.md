## Description:

Web of Science Expanded (clarivate.com). Use this skill for ANY Web of Science Expanded request — searching and reading data. Whenever a task involves Web of Science Expanded, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, academics, and analysts use this skill to search Web of Science Expanded, retrieve records, review citation metrics, and explore cited, citing, and related documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup directs the agent to execute downloaded installer code that was unavailable for inspection, without clear user approval.

Mitigation: Review and approve setup separately; prefer an inspected, version-pinned release and review its automatic skill synchronization.

Risk: Research queries use the connected OOMOL account and may consume credits.

Mitigation: Check the connected account and expected credit use before running queries.

## Reference(s):

- [Web of Science](https://clarivate.com/academia-government/scientific-and-academic-research/research-discovery-and-referencing/web-of-science/)
- [Web of Science API documentation](https://developer.clarivate.com/apis/wos)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-web-of-science-expanded)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, JSON, Text]

**Output Format:** [Web of Science records and citation results as JSON, with text summaries where requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Web of Science account, query, selected record detail, and available credits.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
