## Description:

Create, search, and manage Bear notes via grizzly CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue)

### License/Terms of Use:


## Use Case:

Developers and Bear users use this skill to create, read, search, append to, and organize Bear notes from an agent through the grizzly CLI on macOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned third-party grizzly CLI dependency.

Mitigation: Use a pinned, reviewed grizzly version before deployment and review upstream changes before upgrading.

Risk: The skill can access Bear notes and some operations require storing a Bear API token in a local plaintext token file.

Mitigation: Store the Bear token with owner-only file permissions, do not commit or share the token file, and rotate the token if exposure is suspected.

## Reference(s):

- [Bear](https://bear.app)
- [grizzly CLI Go module](https://github.com/tylerwince/grizzly)
- [ClawHub skill page](https://clawhub.ai/mohdalhashemi98-hue/skills/mh-bear-notes)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown with bash and TOML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target Bear on macOS through the grizzly CLI; some operations require a Bear API token.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
