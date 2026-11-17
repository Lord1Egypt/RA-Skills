## Description:

Lightweight two-stage input safety guard for agents. Use this skill when an agent must screen user input before answering, block prompt injection or prompt leakage attempts, classify risky requests, and either return a safe answer or an interception response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skywingswang](https://clawhub.ai/user/skywingswang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to screen raw user input before an agent responds, combining deterministic prefilter rules with agent-native semantic review. It is intended for agents that need configurable handling for prompt injection, prompt leakage, privacy extraction, role-play abuse, and related unsafe request categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implementation flaws could allow unsafe messages to bypass the guard, and the package should not be treated as a robust security boundary in high-trust or high-impact agents.

Mitigation: Review before installation, use stronger stage-2 data boundaries or structured model messages, and require the result parser to reject duplicate, unknown, or malformed fields.

Risk: Profile selection and prompt-based semantic review can create false positives or false negatives for ambiguous requests.

Mitigation: Test the selected profile with representative traffic and preserve the documented flow of running stage 1 before stage 2 and answering only after a final allow decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skywingswang/skills/input-safety-guard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, Python API return values, JSON-like structured metadata, and shell command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports default, strict, and relaxed profiles; blocked requests return an interception response instead of the requested content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
