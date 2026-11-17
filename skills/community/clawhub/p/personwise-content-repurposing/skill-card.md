## Description:

Turns supplied recordings, transcripts, webinars, talks, and long-form material into a grounded interactive digital-human course that learners can interrupt with voice questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, learning teams, marketers, and course creators use this skill to repurpose supplied source content into an askable digital-human course or interactive presentation. It emphasizes source-grounded teaching, review checkpoints, and explicit approval before installation or updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation or update commands can change a local executable or installed skill.

Mitigation: Review the exact PersonWise update or bootstrap command before approval and proceed only when the PersonWise update channel and command are trusted.

Risk: Repurposed courses can carry unsupported, dated, or off-the-cuff claims from source recordings.

Mitigation: Keep course content evidence-locked to supplied materials, flag time-sensitive claims for user confirmation, and remove unsupported claims during review checkpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/personwiseai/skills/personwise-content-repurposing)
- [PersonWise service descriptor](artifact/assets/service-descriptor.signed.json)
- [PersonWise CLI bootstrap](artifact/assets/bootstrap.sh)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with JSON payloads and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces secret-free course workflow instructions, review steps, and PersonWise CLI commands; final course artifacts are created by the PersonWise service.]

## Skill Version(s):

2.1.9 (source: server release evidence and skill attribution block)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
