## Description:

Transforms a static Vue index.vue page into a data-driven Vue 2 + Element UI Custom.vue component using only the target page and its directly referenced styles and assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[781818761](https://clawhub.ai/user/781818761)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to convert an existing static Vue page into a self-contained Vue 2 + Element UI component with extracted data, v-for rendering, Element UI component replacements, scoped styles, and route registration when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unbundled ui-ux-max-pro prerequisite skill.

Mitigation: Review or pin ui-ux-max-pro before using this skill, and pause execution if that dependency is unavailable.

Risk: The skill writes Custom.vue, may update router files, and may run npm commands.

Mitigation: Require explicit confirmation before package installation, npm script execution, or router changes, and review generated code before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/781818761/skills/lanhu-code-2-el-vue)
- [Skill documentation index](data/INDEX.md)
- [Element UI documentation](https://element.eleme.cn/#/zh-CN/component/installation)
- [Vue 2 documentation](https://cn.vuejs.org/v2/guide/)
- [Router synchronization guidance](data/router-sync.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Vue single-file component code with concise Markdown status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or overwrite Custom.vue and may propose dependency or router updates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
