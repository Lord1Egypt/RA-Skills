## Description:

Plays internet radio streams via Foobar2000 by mapping mood or genre requests to stations from the Internet Radio Music DB, with playback controls and history support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dynamicsalex](https://clawhub.ai/user/dynamicsalex)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to control internet radio playback from an agent, including mood-based station selection, playback controls, status checks, and listening history review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill opens external stream URLs and performs outbound stream checks.

Mitigation: Install only in environments where outbound radio stream access is acceptable, and prefer explicit radio-specific requests to reduce accidental activation.

Risk: The skill can control and force-stop local Foobar2000 processes.

Mitigation: Use it on systems where agent-driven Foobar2000 control is expected, and avoid running it during unrelated manual Foobar2000 sessions.

Risk: Playback history exports can include stream metadata in HTML or CSV formats.

Mitigation: Sanitize exported history before opening files that contain untrusted stream metadata.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dynamicsalex/skills/internet-radio-music-player)
- [Internet Radio Music WebUI Plugin](https://clawhub.ai/dynamicsAlex/internet-radio-music-webui)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Plain text command output with optional CSV, HTML, or JSON history exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, Foobar2000, and the Internet Radio Music DB skill.]

## Skill Version(s):

2.5.3 (source: server release evidence; artifact frontmatter says 2.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
