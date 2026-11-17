## Description:

screenshot.fyi (screenshot.fyi). Use this skill for ANY screenshot.fyi request — searching and reading data. Whenever a task involves screenshot.fyi, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users use this skill to capture a website screenshot through screenshot.fyi from an OOMOL-connected account and retrieve the resulting URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may affect skills installed in other agents, and the remote installer contents remain unverified.

Mitigation: Review and separately approve CLI setup; review automatic cross-agent skill installation and disable synchronization if unwanted.

Risk: Screenshot creation may bypass the skill's stated confirmation boundary and may incur charges.

Mitigation: Explicitly authorize each new screenshot and check possible charges before running it.

Risk: URLs and options are sent through OOMOL to screenshot.fyi and may contain confidential information or embedded tokens.

Mitigation: Avoid sending confidential URLs, options, or embedded tokens.

## Reference(s):

- [screenshot.fyi documentation](https://www.screenshot.fyi/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-screenshot-fyi)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Text]

**Output Format:** [JSON request and response containing a generated screenshot URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The screenshot URL is returned after a screenshot action.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
