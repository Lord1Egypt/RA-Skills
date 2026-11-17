## Description:

Run when the user asks for TraumaCodex, biometric IBI timing to dual offline/online digests, an LDQ-style waveform from a timing list, or mirror dig seals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

LYGO Sovereign License v2.0

## Use Case:

External users and developers use this skill to process inter-beat interval timing lists locally into protocol digests, offline and online summary packages, mirror dig seals, and optional waveform output. It is not for health diagnosis or treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heartbeat timing data and derived outputs may be sensitive if clinical or PHI data is used.

Mitigation: Use demo or non-clinical data unless the user understands and accepts the local files that will be written.

Risk: The skill writes derived JSON packages, hashes, seals, and optionally a WAV file to disk.

Mitigation: Write to a controlled local output directory, use explicit consent for skill state writes, and manage or delete generated outputs according to local data-handling needs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-traumacodex)
- [TraumaCodex documentation](https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/TRAUMA_CODEX.md)
- [Security notes](references/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated local JSON packages and optional WAV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Python or Python 3; writes to ./traumacodex_out, a user-selected --out directory, or skill state only with explicit consent.]

## Skill Version(s):

1.0.2 (source: frontmatter, claw.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
