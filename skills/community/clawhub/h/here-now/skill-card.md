## Description:

Publishes websites and files to live here.now URLs and helps manage site access, workspaces, and domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamludwin](https://clawhub.ai/user/adamludwin)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to publish user-provided websites or files to live URLs and manage access, team workspaces, and domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A path-handling bug may expose saved site-control tokens, and some credential safeguards are incomplete.

Mitigation: Prefer a corrected version that normalizes paths and excludes private state. Until then, publish only a clean output directory without credentials, .herenow state, or other private files.

Risk: Publishing, API access, and Drive sharing can expose files or grant broader access than intended.

Mitigation: Choose publication and access settings explicitly, restrict API destinations to the documented service, and give Drive shares narrow paths, minimal permissions, and short expirations. Pin installation versions where possible.

## Reference(s):

- [here.now documentation](https://here.now/docs)
- [here.now API specification](https://here.now/openapi.json)

## Skill Output:

**Output Type(s):** [Files, URLs, Guidance]

**Output Format:** [Published website or file URLs with Markdown status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Site access settings depend on the user's publication choices.]

## Skill Version(s):

1.35.1 (source: artifact SKILL.md and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
