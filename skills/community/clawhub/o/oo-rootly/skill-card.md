## Description:

Rootly (rootly.com). Use this skill for ANY Rootly request — searching and reading data. Whenever a task involves Rootly, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People who manage incidents use this skill to search and read Rootly users, incidents, services, and teams through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run a remote installer whose contents were unavailable for inspection, without a clear approval step.

Mitigation: Review the setup first; install a reviewed, version-pinned CLI yourself and require approval before software installation or changes to other agent skills.

Risk: Rootly access is mediated through OOMOL, and connected account permissions affect what the skill can access.

Mitigation: Use read-only Rootly access where available and understand that OOMOL mediates account access.

## Reference(s):

- [Rootly](https://rootly.com)
- [Rootly API documentation](https://docs.rootly.com/api-reference/overview)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-rootly)

## Skill Output:

**Output Type(s):** [API calls, JSON, Text, Guidance]

**Output Format:** [Shell commands with JSON input; connector results as JSON summarized in text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented Rootly information and setup guidance.]

## Skill Version(s):

1.0.4 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
