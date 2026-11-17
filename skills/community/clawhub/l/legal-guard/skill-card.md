## Description:

Prevents autonomous signing of legal agreements or contracts by requiring a concise terms summary and explicit `/approve <id> allow-once` authorization before signing or formal confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[echoofzion](https://clawhub.ai/user/echoofzion)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use Legal Guard to pause signature, contract, Terms of Service, subscription, CLA, and wallet-signing flows until the agent summarizes key terms and receives explicit user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Permanent approvals could allow future legal or financial actions without per-action review.

Mitigation: Prefer `/approve <id> allow-once`; use `allow-always` only when the host approval system is narrowly scoped and revocable.

Risk: Summaries may omit or misunderstand important contract terms.

Mitigation: Review the underlying document before approving and deny the action when terms are unclear or incomplete.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown text with approval commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes executive summaries, approval command prompts, approval IDs, and optional declination drafts.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
