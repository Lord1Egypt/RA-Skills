## Description:

Enhances OpenClaw memory by automatically recalling relevant saved memories before agent turns and capturing durable facts, preferences, and decisions after successful runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhoulf1006](https://clawhub.ai/user/zhoulf1006)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using OpenClaw use this plugin to preserve useful workspace context across sessions and automatically surface relevant prior memories during future agent interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived facts may be persisted automatically and reused in later prompts.

Mitigation: Disable autoCapture in sensitive or shared workspaces unless users intentionally want durable memory capture.

Risk: Recalled memories can influence future model behavior if untrusted users can shape stored memory.

Mitigation: Disable autoRecall or limit use to trusted workspaces until review-before-save or per-message filtering controls are in place.

Risk: Automatic recall may expose prior workspace context in prompts where it is not expected.

Mitigation: Review memory files regularly and tune recall limits before enabling the plugin for confidential work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhoulf1006/skills/memory-core-plus)
- [npm package](https://www.npmjs.com/package/memory-core-plus)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [Prompt context injection and Markdown memory entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Auto-recall and auto-capture are enabled by default; captured memories are appended to dated Markdown files.]

## Skill Version(s):

1.0.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
