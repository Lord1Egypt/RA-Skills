## Description: <br>
Transforms static Vue index.vue pages into data-driven Vue 2 and Element UI Custom.vue pages using only the target page and directly referenced styles or assets as page evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[781818761](https://clawhub.ai/user/781818761) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert an existing static Vue page into a dynamic Vue 2 single-file component with Element UI controls, structured data, scoped styling, and optional route registration. It is intended for static-to-dynamic page migration work, not new page creation or non-Vue 2 stacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite Custom.vue and edit router files during the conversion workflow. <br>
Mitigation: Run it in a disposable branch or with backups, and require explicit approval before overwriting Custom.vue or changing routing. <br>
Risk: The skill may install dependencies, start the project, or follow a function.md file outside its advertised source boundary. <br>
Mitigation: Require approval before package installation or project startup, and do not allow reading or executing function.md unless it is separately reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/781818761/lanhu-code-2-el-vue) <br>
- [Artifact documentation index](artifact/data/INDEX.md) <br>
- [Element UI documentation](https://element.eleme.cn/#/zh-CN/component/installation) <br>
- [Vue 2 documentation](https://cn.vuejs.org/v2/guide/) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Vue single-file component code, Markdown progress notes, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or overwrites Custom.vue and may propose router registration or project commands after review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
