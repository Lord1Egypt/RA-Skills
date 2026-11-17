## Description:

Openclaw Never Forget is a bilingual memory-management skill that directs an agent to keep episodic daily logs, periodic context snapshots, long-term semantic notes, and explicit recall summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenyh1226](https://clawhub.ai/user/chenyh1226)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an OpenClaw agent persistent working memory across active sessions, including daily task logs, compressed context checkpoints, distilled project knowledge, and recall summaries grounded in stored memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs ongoing local memory retention and silent automatic capture of user and project context.

Mitigation: Install only when persistent local memory is intended, review memory files regularly, avoid sharing secrets while active, and prefer releases with confirmation, deletion, redaction, and opt-out controls.

Risk: Stored memory may contain outdated or incorrect facts that could affect later recall.

Mitigation: Use the skill's no-fabrication rule during recall and correct or remove inaccurate memory entries when identified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenyh1226/skills/openclaw-never-forget)
- [Publisher profile](https://clawhub.ai/user/chenyh1226)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown memory logs and synthesized natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English/Chinese output that adapts to the user's primary language.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
