## Description:

Oclaw Hermes bridges OpenClaw, Hermes, and DeerFlow into a memory-driven multi-agent workflow for task routing, shared memory, research, coding, browser work, skill calls, and expert-style skill distillation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruiyongwang](https://clawhub.ai/user/ruiyongwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect OpenClaw skills, Hermes memory, and DeerFlow-style multi-agent workflows so an agent can route research, coding, browser, memory, and skill tasks with shared context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation content, skill inputs, skill outputs, and extracted facts can be stored in local memory databases and synchronized across connected platforms.

Mitigation: Avoid placing secrets or private data in prompts, use least-privilege test credentials, enable sync only to trusted HTTPS endpoints, and define clear retention and deletion procedures before production use.

Risk: Docker services mount agent state, memory directories, scripts, and credentials with writable access.

Mitigation: Bind services to localhost where possible, pin container images, narrow mounts to the minimum required paths, and make mounts read-only when write access is not required.

Risk: The bridge and agent workflows can invoke local commands, platform CLIs, and generated code workflows.

Mitigation: Review commands before execution, run first with non-production data, and keep command execution inside constrained environments with least-privilege credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruiyongwang/skills/oclaw-hermes)
- [artifact README](artifact/README.md)
- [artifact skill definition](artifact/SKILL.md)
- [Hermes Agent](https://github.com/NousResearch/hermes)
- [DeerFlow](https://github.com/bytedance/deerflow)
- [OpenClaw](https://openclawmp.stepfun.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Text or Markdown responses with optional code snippets, shell commands, configuration examples, JSON status data, and generated skill or distillation files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include memory retrieval results, task status, research summaries, generated code, suggested skills, or expert distillation artifacts depending on the invoked workflow.]

## Skill Version(s):

3.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
