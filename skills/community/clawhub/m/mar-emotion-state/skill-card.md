## Description:

Tracks natural-language emotion state and injects compact emotional context into an OpenClaw agent prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to classify recent user and agent messages into concise emotion summaries, persist emotion history, and add current emotion context to future agent bootstraps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation messages can be sent to a configured classifier endpoint or to SkillBoss for emotion classification.

Mitigation: Use only trusted classifier endpoints and deploy the skill only where this message-processing flow is acceptable to users and operators.

Risk: Inferred emotional history is stored across sessions and injected into future prompts.

Mitigation: Tune history size, displayed entry limits, and confidence thresholds for the deployment, and review stored state for sensitive contexts.

Risk: The hook can read emotion state from sibling agents with limited disclosure.

Mitigation: Use isolated OpenClaw state directories or review the hook configuration and code before enabling cross-agent state sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/mar-emotion-state)
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, and XML-like prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Injects a compact emotion_state block during agent bootstrap; retention, confidence threshold, timezone, and displayed history are controlled by environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
