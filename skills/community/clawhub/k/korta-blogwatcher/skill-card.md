## Description:

Monitor blogs and RSS/Atom feeds for updates using the blogwatcher CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[landercortazarromero](https://clawhub.ai/user/landercortazarromero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to install and operate the blogwatcher CLI for tracking blog and RSS/Atom feed updates, scanning for new articles, and managing read/unread status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned third-party Go command, so future upstream releases could change behavior between installations.

Mitigation: Review the upstream blogwatcher module before use and pin a trusted version instead of @latest when reproducibility or supply-chain control is required.

## Reference(s):

- [Korta Blogwatcher on ClawHub](https://clawhub.ai/landercortazarromero/skills/korta-blogwatcher)
- [blogwatcher homepage](https://github.com/Hyaxia/blogwatcher)
- [blogwatcher Go install module](github.com/Hyaxia/blogwatcher/cmd/blogwatcher@latest)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command guidance for installing and using the blogwatcher CLI; does not itself fetch feeds unless the user runs the CLI.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
