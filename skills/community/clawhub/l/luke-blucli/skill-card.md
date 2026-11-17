## Description:

BluOS CLI (blu) for discovery, playback, grouping, and volume.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banalit](https://clawhub.ai/user/banalit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and apply the blu CLI for discovering and controlling BluOS, Bluesound, and NAD players, including playback, grouping, and volume tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs the blu CLI from a mutable upstream Go module version.

Mitigation: Use a pinned and reviewed blu module version when reproducible installs or stricter supply-chain controls are required.

Risk: The CLI can discover and control BluOS, Bluesound, and NAD devices on the local network.

Mitigation: Confirm the selected target device before changing playback, grouping, or volume.

## Reference(s):

- [blucli homepage](https://blucli.sh)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend JSON-formatted CLI output for scripting.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
