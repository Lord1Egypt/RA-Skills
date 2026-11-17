## Description:

Runs the full Dawn CLI strategy lifecycle from authentication and funding through strategy creation, launch, monitoring, and termination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[njdawn](https://clawhub.ai/user/njdawn)

### License/Terms of Use:


## Use Case:

External developers and operators use this skill to create, revise, launch, monitor, troubleshoot, and stop Dawn prediction-market strategies through the Dawn CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live trading and funding workflows that may cause financial loss if run without clear user approval.

Mitigation: Default to paper mode, require explicit confirmation before funding or any `--live` launch, and verify budget and duration before execution.

Risk: The documented global install uses an unpinned Dawn CLI package.

Mitigation: Prefer a pinned or isolated Dawn CLI installation from a trusted source before use.

## Reference(s):

- [Dawn homepage](https://dawn.ai)
- [ClawHub skill page](https://clawhub.ai/njdawn/skills/prediction-market-bot-dawn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and command summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected outputs include conversationId, strategyId when launched, run mode, monitoring summary, and the next or last Dawn CLI command.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
