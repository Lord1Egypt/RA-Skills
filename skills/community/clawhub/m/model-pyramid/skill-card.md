## Description:

Recommends a model, effort level, and optional advisor for a session or each delegated task based on capability and thoroughness needs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentjiang06](https://clawhub.ai/user/vincentjiang06)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to choose model and effort settings for a session or individual subagents and decide when an advisor may help. Its recommendations are advisory and do not change settings or spawn agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dated model defaults or advisor pairing guidance may become inaccurate.

Mitigation: Re-check current provider documentation before using exact defaults or pairing rules.

Risk: Model, effort, advisor, or token-budget choices may affect cost and task thoroughness.

Mitigation: Review the recommendations against the task and available budget before applying them.

## Reference(s):

- [Model and effort reference](references/model-and-effort.md)
- [Orchestration reference](references/orchestration.md)
- [Runtime knobs reference](references/runtime-knobs.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Text]

**Output Format:** [Markdown with per-agent model and effort recommendations and optional validation findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory only; model facts are dated and should be rechecked before use.]

## Skill Version(s):

1.1.0 (source: ClawHub release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
