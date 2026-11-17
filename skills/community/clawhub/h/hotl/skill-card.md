## Description:

Use the hotl CLI to search Google Hotels, compare prices, fetch hotel room/rate details, and return machine-readable hotel results from a terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[art22s](https://clawhub.ai/user/art22s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and travel-planning users use this skill to run CLI-only hotel searches, compare Google Hotels prices, fetch room and rate details, and request structured hotel results for shell or agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release installs the current PyPI package for the hotl CLI rather than a pinned, reviewed package version.

Mitigation: Install hotl in an isolated user environment such as pipx, avoid administrator installs, and pin or review the package version when reproducibility or higher assurance is required.

Risk: Google Hotels entity_key values are opaque tokens from search results rather than stable hotel identifiers.

Mitigation: Use entity_key values immediately with hotl details and do not store or treat them as permanent hotel IDs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/art22s/skills/hotl)
- [hotl PyPI package](https://pypi.org/project/hotl/)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON output when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the hotl CLI; use --format json when an agent or downstream tool needs structured hotel data.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
