## Description:

Operates Intervals.icu through an OOMOL-connected account to search and read athlete data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Athletes and coaches use the skill to search and read Intervals.icu activities, calendar events, wellness records, athlete profiles, and training settings through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is marked suspicious because scanners report it can run a remotely fetched installer unrelated to its Intervals.icu purpose, without version or integrity checks or a system-change warning.

Mitigation: Avoid installing unless needed; review the installer and its source first, and understand the system changes it may make.

## Reference(s):

- [Intervals.icu API documentation](https://intervals.icu/api-docs.html)
- [Intervals.icu](https://intervals.icu)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown instructions with shell command examples and JSON request/response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented activity, calendar, wellness, profile, and training data; activity streams can contain thousands of samples per stream.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
