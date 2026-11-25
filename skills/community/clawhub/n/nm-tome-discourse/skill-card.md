## Description:

Scans HN, Lobsters, Reddit, and tech blogs for community experience reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to gather practitioner opinions and experience reports about a technology or approach from community discussions. It searches at least two supported channels and returns findings with source attribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search topics may contain confidential details about the user's research or interests.

Mitigation: Review search topics before use and omit confidential details.

Risk: The security review was partial because a local path-like reference could not be resolved.

Mitigation: Treat the benign verdict as incomplete and review the unresolved reference before relying on the assessment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-tome-discourse)
- [Declared metadata homepage (provenance unavailable)](https://github.com/athola/claude-night-market/tree/master/plugins/tome)

## Skill Output:

**Output Type(s):** [Text, Analysis]

**Output Format:** [Source-attributed community finding summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries at least two community channels; reports explicitly when all available search methods fail.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
