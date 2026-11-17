## Description:

Web of Science (clarivate.com). Use this skill for ANY Web of Science request — searching and reading data. Whenever a task involves Web of Science, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with an OOMOL-connected Web of Science account can search documents and journals or retrieve individual records by accession number or journal identifier.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup may execute an unverified remote installer without separate approval.

Mitigation: Install a verified CLI release yourself, review automatic skill-sync settings, and require approval before additional installation.

Risk: Web of Science searches use the connected account and may consume credit.

Mitigation: Check account and credit implications before running searches.

## Reference(s):

- [Web of Science homepage](https://clarivate.com/academia-government/scientific-and-academic-research/research-discovery-and-referencing/web-of-science/)
- [Web of Science Starter API documentation](https://developer.clarivate.com/apis/wos-starter)
- [oo CLI project (the CLI used by this skill)](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-web-of-science)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Web of Science action results in JSON, with text summaries as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected read action, query, and connected account.]

## Skill Version(s):

1.0.4 (source: frontmatter; server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
