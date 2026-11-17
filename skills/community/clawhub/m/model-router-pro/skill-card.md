## Description:

Routes substantive user requests to an LLM model by scoring task complexity across 12 dimensions, selecting an available model, and instructing the agent when to switch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bevanding](https://clawhub.ai/user/bevanding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to automate model selection for OpenClaw sessions, especially when they want requests routed by complexity, task type, availability, and configurable cost or capability profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic routing instructions may affect routine agent behavior and persist if the suggested AGENTS.md note is added.

Mitigation: Install only when automatic model routing is desired, and review the persistent AGENTS.md instruction before adding it.

Risk: The router processes raw user messages through a CLI argument, which can be unsafe if callers build shell commands by interpolation.

Mitigation: Pass user messages as direct process arguments or otherwise use safe argument handling instead of shell-interpolating raw text.

Risk: The skill reads OpenClaw configuration to filter available models.

Mitigation: Review the declared access to ~/.openclaw/openclaw.json and inspect the generated models.json before relying on automatic switching.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bevanding/skills/model-router-pro)
- [Publisher Profile](https://clawhub.ai/user/bevanding)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON routing result from the CLI and Markdown instructions for setup or disclosure when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Router output includes full_id, tier, confidence, and optional debug scoring details; setup can generate models.json.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
