## Description:

Instantly publish a single self-contained HTML page to htmlcode.fun for fast live URLs. Alias of html-deploy, updated for the current versioned htmlcode.fun API and safer agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[520xiaomumu](https://clawhub.ai/user/520xiaomumu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to publish, update, inspect, and manage single-file HTML pages on htmlcode.fun when fast sharing is more important than full project hosting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overwriting, unpublishing, deleting, or switching versions can affect a live shared HTML page.

Mitigation: Confirm the exact short code and version before these actions, inspect version history first, and append a new version when there is uncertainty.

Risk: A liked htmlcode.fun version is intended to be preserved as an immutable snapshot.

Mitigation: Do not overwrite or delete versions with likeCount greater than zero; append a new version instead.

## Reference(s):

- [htmlcode.fun live guide](https://www.htmlcode.fun/s/htmlcode-fun-guide)
- [ClawHub skill page](https://clawhub.ai/520xiaomumu/skills/html-deploy-easy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deployment URLs, version details, preserve hints, troubleshooting fields, and local HTML output when fetching content.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
