## Description:

协作拍档核心规范（Core Spec）的可加载封装。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill as a loadable core specification for collaborative partner agents, including identity, governance posture, multilingual response behavior, quality gates, and role instantiation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger terms may cause this documentation skill to load more often than intended in environments with aggressive auto-loading.

Mitigation: Narrow or namespace the trigger terms before deployment in shared or production agent environments.

Risk: The manifest describes broad governance and cross-session ambitions beyond the documentation-only behavior present in the artifact.

Mitigation: Treat the skill as guidance unless separate implementation evidence is reviewed and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoxinghua09-cell/skills/laopaidang-core)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and plain-text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no code, credential use, persistence, or destructive behavior was identified by the server security evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter, manifest, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
