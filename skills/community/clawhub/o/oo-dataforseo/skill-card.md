## Description:

DataForSEO (dataforseo.com). Use this skill for ANY DataForSEO request — reading, creating, and updating data. Whenever a task involves DataForSEO, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use the connected DataForSEO account to retrieve search, keyword, backlink, and marketplace data, and to submit supported research tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The missing-CLI setup instructs the agent to execute a downloaded installer whose contents were not inspected.

Mitigation: Install and verify the oo CLI yourself, and prevent automatic installer execution during error recovery. Review automatic skill synchronization and the OOMOL account permissions you grant.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [DataForSEO API documentation](https://docs.dataforseo.com/v3/)
- [DataForSEO](https://dataforseo.com)

## Skill Output:

**Output Type(s):** [JSON data, Analysis, Guidance]

**Output Format:** [Structured DataForSEO results with natural-language summaries or guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action and the connected DataForSEO account.]

## Skill Version(s):

1.0.6 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
