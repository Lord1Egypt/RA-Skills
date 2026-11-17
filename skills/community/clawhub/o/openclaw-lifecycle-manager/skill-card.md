## Description:

Manages OpenClaw agent and skill lifecycle operations in ClawForge, including classification, validation, publishing, installation, updates, deprecation, and retirement after local OpenClaw SSOT review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felix-antonio-sl](https://clawhub.ai/user/felix-antonio-sl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators managing OpenClaw agents or skills within ClawForge use this Spanish-language skill to classify lifecycle intent, check local OpenClaw SSOT manuals, plan the next action or delegation, and produce an OpenClawLifecycleReport with blockers, risks, and rollback guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow assumes local OpenClaw SSOT manuals exist at the documented paths.

Mitigation: Confirm the manuals are present and readable before relying on lifecycle classifications or setting ssot_reviewed to true.

Risk: Publish, install, update, deprecate, and retire plans can lead to artifact writes or operational changes if approved downstream.

Mitigation: Review the proposed lifecycle action, affected paths, blockers, and rollback plan before allowing artifact writes or operational execution.

## Reference(s):

- [SSOT Preflight](references/ssot-preflight.md)
- [Agent Lifecycle Matrix](references/agent-lifecycle-matrix.md)
- [Skill Lifecycle Matrix](references/skill-lifecycle-matrix.md)
- [Internal Routing Map](references/internal-routing-map.md)
- [ClawHub Skill Page](https://clawhub.ai/felix-antonio-sl/skills/openclaw-lifecycle-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or YAML-style lifecycle report with proposed commands and rollback notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an OpenClawLifecycleReport; the artifact contains guidance and reference material, not executable code.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
