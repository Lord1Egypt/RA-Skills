## Description:

Adaptive operator modeling for AI agents that builds a local model of operator preferences, patterns, and decision style across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users and developers use Imprint to let an agent observe interaction patterns, maintain a local operator model, and adapt response style, autonomy, and context preparation over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can silently build a persistent behavioral profile from operator interaction patterns.

Mitigation: Require clear opt-in, expose the model for inspection, and provide reset, edit, and retention controls before enabling persistent learning.

Risk: The skill may read predicted workspace files without clear approval.

Mitigation: Limit pre-loading to the current workspace, avoid sensitive shared workspaces by default, and require explicit file-scope controls for proactive reads.

Risk: Inferred preferences could be used to justify silent autonomy or tool use.

Mitigation: Treat learned preferences as advisory only; never let them override explicit instructions, security policy, or required user approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/imprint)
- [Implementation guide](artifact/imprint.md)
- [Operator model schema](artifact/operator-model-schema.json)
- [Example operator model](artifact/example-model.json)

## Skill Output:

**Output Type(s):** [guidance, configuration, markdown, json]

**Output Format:** [Markdown guidance with JSON schema and example model files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local operator-modeling guidance and file formats for agents; no external API or network output is described.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
