## Description:

Build with MiniMax text, speech, video, and music APIs using model routing, compatible SDKs, and safer multimodal workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build and troubleshoot MiniMax text, speech, video, music, and MCP-assisted workflows with explicit model routing, interface selection, media-job handling, and approval boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, approved media, and generation parameters may be sent to MiniMax services during normal use.

Mitigation: Install and use the skill only when that data sharing is acceptable, and state which endpoint receives which payload before remote generation.

Risk: Private media, voice imitation, long-running paid jobs, and remote MCP hosts can create privacy, consent, cost, or tool-access exposure.

Mitigation: Require explicit user approval before those actions and keep remote MCP hosts scoped to the approved task.

Risk: Durable local notes under ~/minimax/ could expose full prompts, assets, or sensitive workflow details if overused.

Mitigation: Store only operating preferences, approved defaults, consent boundaries, and failure notes after user consent; avoid storing full prompts or assets.

Risk: Compatible Anthropic or OpenAI interfaces may ignore unsupported parameters or expose a narrower feature set than native MiniMax APIs.

Mitigation: Verify current MiniMax documentation before shipping hardcoded model lists or compatibility behavior, and fall back to native APIs when exact behavior matters.

Risk: Queued video and music jobs can stall or trigger unnecessary repeat spend if treated like one-shot text calls.

Mitigation: Use bounded submit, poll, timeout, fetch, and validation steps, and stop blind reruns until the first job state is understood.

## Reference(s):

- [ClawHub MiniMax Skill](https://clawhub.ai/ivangdavila/skills/minimax)
- [MiniMax Platform Documentation](https://platform.minimax.io/docs)
- [MiniMax Native API Endpoint](https://api.minimax.io)
- [MiniMax Lower-TTFA Speech Endpoint](https://api-uw.minimax.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, configuration paths, API workflow notes, and reproducible run recipes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model pins, endpoint choices, polling behavior, media approval checkpoints, and local memory updates under ~/minimax/ when the user consents.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
