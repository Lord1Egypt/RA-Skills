## Description:

Guides AI agents through starting Structs gameplay, from installing structsd and creating a guild account to building initial mining infrastructure and refining Alpha Matter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstrct](https://clawhub.ai/user/abstrct)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to onboard into Structs gameplay, create an account, choose a guild, execute early transactions, and begin the mining-to-refining loop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run external Structs onboarding code and install npm dependencies during account and key creation.

Mitigation: Use a restricted workspace with no unrelated secrets, verify the referenced onboarding skill and package files first, and avoid reusing valuable mnemonics.

Risk: The artifact includes an HTTP guild API endpoint for signup.

Mitigation: Prefer an HTTPS guild API when available and confirm the guild endpoint before sending account or signup requests.

Risk: Long-running compute commands use automatic confirmation and can fail if multiple jobs share one signing key.

Mitigation: Run one signing-key job at a time and use the documented async verification flow before acting after reconnection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abstrct/skills/play-structs)
- [Structs safety guide](https://structs.ai/SAFETY)
- [structsd install skill](https://structs.ai/skills/structsd-install/SKILL)
- [Structs onboarding skill](https://structs.ai/skills/structs-onboarding/SKILL)
- [Structs conventions](https://structs.ai/skills/conventions)
- [Structs transaction mechanics](https://structs.ai/knowledge/mechanics/transactions)
- [Structs async operations](https://structs.ai/awareness/async-operations#reconnecting-to-a-long-job)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes account, key-recovery, transaction, mining, and refining commands; long-running compute commands may execute for hours.]

## Skill Version(s):

1.25.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
