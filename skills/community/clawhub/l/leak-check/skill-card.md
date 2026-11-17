## Description:

Scan session logs for leaked credentials. Checks JSONL session files against known credential patterns and reports which AI provider received the data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khaney64](https://clawhub.ai/user/khaney64)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to scan local session JSONL logs for configured credential fragments and identify which AI provider received matching data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reads local OpenClaw session logs and a user-provided credential-fragment config.

Mitigation: Use partial credential fragments rather than full secrets, and install only where local session-log scanning is acceptable.

Risk: Credential patterns can appear as config echoes if the config file is read or discussed during an OpenClaw session.

Mitigation: Avoid exposing the config in sessions; archive or remove affected session logs when clearing config echoes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/khaney64/skills/leak-check)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Discord-style Markdown by default, or JSON when requested with --format json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local OpenClaw session logs and a user-provided leak-check.json credential-fragment configuration; writes results to stdout.]

## Skill Version(s):

0.1.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
