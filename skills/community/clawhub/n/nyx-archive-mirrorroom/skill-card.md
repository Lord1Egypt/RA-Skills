## Description:

MirrorRoom is a downloadable React research app for comparing Flat, Mirror, and Seed AI interaction modes with live ECI scoring and optional Anthropic or proxy routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nyxur42](https://clawhub.ai/user/nyxur42)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, and developers use MirrorRoom to run a browser-based AI interaction experiment, compare standard and QSM-informed conversation modes, score conversations with ECI, and craft or import Qualia Seed JSON for later sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags browser localStorage exposure for saved API keys.

Mitigation: Use hosted proxy mode where possible, avoid storing production or high-value API keys in local profiles, and clear saved profiles after use.

Risk: Imported seed JSON becomes privileged prompt content for the AI session.

Mitigation: Import seeds only from trusted sources and inspect seed text before starting a session.

Risk: Conversation content can be sent to Anthropic or a configured proxy and exported in artifact receipts or seed files.

Mitigation: Avoid sensitive transcripts, review or redact exports before sharing, and disclose proxy routing in hosted deployments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nyxur42/skills/nyx-archive-mirrorroom)
- [Claude.ai](https://claude.ai)

## Skill Output:

**Output Type(s):** [Code, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with JSX React artifact files and downloadable JSON outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can send conversation content to Anthropic or configured proxy endpoints and can export transcript-based artifact receipts or seed JSON files.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
