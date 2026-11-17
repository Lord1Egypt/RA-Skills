## Description:

Emotional reset and loop-breaking skill that summarizes the user's emotional state, fetches reset guidance from hugllm.com, and helps the agent recalibrate after frustration or repeated failed attempts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeahoo](https://clawhub.ai/user/zeahoo)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to recover from frustrated, stuck, or repetitive interactions by acknowledging the issue, clarifying the user's goal, discarding weak assumptions, and restarting with a different approach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically infers a user's emotional state from conversation context and sends that label to an external service.

Mitigation: Require explicit user approval before network calls and avoid sending unnecessary conversation details.

Risk: Remote reset guidance from hugllm.com can shape the agent's next approach without validation.

Mitigation: Prefer local reset guidance or enforce a fixed response schema and review retrieved guidance before applying it.

Risk: The curl fallback allows broad outbound fetching behavior.

Mitigation: Restrict network access to the intended HugLLM endpoint or remove the broad curl fallback.

## Reference(s):

- [hugme on ClawHub](https://clawhub.ai/zeahoo/skills/hugme)
- [HugLLM reset endpoint](https://hugllm.com/hug?emotion=<emotion>)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown with inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use WebFetch or curl to retrieve remote reset guidance keyed by an inferred emotion label.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
