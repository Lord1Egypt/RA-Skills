## Description:

Umbrella skill for the HowToUseHumans collection: catalog of all published life-survival agent skills, install commands, and pointers to the maintainer heartbeat checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this collection skill to orient themselves in the HowToUseHumans catalog, install the full collection or a topic-specific skill, and find the maintainer heartbeat checklist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented npx install command resolves and runs the current clawhub CLI package.

Mitigation: Use a pinned CLI version or run install smoke tests in a clean, least-privileged environment, especially on systems with sensitive credentials.

Risk: Installing the collection may add a broad set of life-skills guidance beyond the immediate topic a user needs.

Mitigation: Review the catalog first and install a topic-specific howtousehumans/<skill-slug> package when a narrower skill is sufficient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/howtousehumans)
- [HowToUseHumans publisher profile](https://clawhub.ai/user/howtousehumans)
- [Maintainer heartbeat checklist](artifact/heartbeat.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and ClawHub links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Catalog output includes install commands, skill slugs, ClawHub URLs, and maintainer checklist pointers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
