## Description:

Build ORBCAFE advanced analytics interactions using CPivotTable/usePivotTable and voice navigation using CAINavProvider/useVoiceInput.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenruiyang](https://clawhub.ai/user/shenruiyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement ORBCAFE pivot-table analytics and voice-navigation workflows with the appropriate module choice, minimal implementation pattern, and operational note.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The copied voice-navigation recipe uses a local WebSocket endpoint as an example, which can be unsafe if reused unchanged in a real application.

Mitigation: Configure the ASR endpoint outside the recipe, use authenticated secure transport for non-local endpoints, and avoid hardcoded secrets.

Risk: Voice-triggered workflows can create privacy and action-confirmation risks if microphone state or sensitive commands are unclear.

Mitigation: Show clear microphone state and consent, keep input-focus safeguards enabled, and require confirmation for sensitive voice-triggered actions.

## Reference(s):

- [Domain Patterns](artifact/references/domain-patterns.md)
- [Guardrails](artifact/references/guardrails.md)
- [Recipes](artifact/references/recipes.md)
- [ClawHub Skill Page](https://clawhub.ai/shenruiyang/skills/orbcafe-pivot-ainav)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript/TSX examples and concise implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include module choice, a minimal implementation, and one operational note about preset persistence or ASR endpoint configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
