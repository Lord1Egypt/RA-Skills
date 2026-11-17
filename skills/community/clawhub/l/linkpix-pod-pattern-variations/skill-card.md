## Description:

基于一个印花快速生成多个设计版本，支持不同风格、颜色及元素组合，提高 POD 设计效率。当用户要求印花裂变、图案变体、衍生设计、一个图案出多版时必须触发。关键词：LinkPix、qhkit、印花裂变、图案裂变、衍生设计、图案变体、配色版本、设计裂变、POD设计、图案量产。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

POD designers and ecommerce sellers use this skill to create multiple color, style, and composition variations from a reference print for product lines.

### Deployment Geography for Use:

China (mainland LinkPix service)

## Known Risks and Mitigations:

Risk: Reference artwork is uploaded to LinkPix for generation, and generation can consume account credits.

Mitigation: Use artwork you are comfortable uploading and check the applicable credit cost before generating when needed.

Risk: The API key and existing service configuration may be affected during setup or configuration changes.

Mitigation: Protect the API key and review the current service configuration before replacing it.

Risk: Installing or updating qhkit runs third-party software; the available security review covers the skill instructions, not the downloaded CLI code.

Mitigation: Use a reviewed version and limited permissions when stronger control is needed.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [LinkPix POD workspace](https://www.iqinghu.com)
- [ClawHub skill page](https://clawhub.ai/autoagc/skills/linkpix-pod-pattern-variations)

## Skill Output:

**Output Type(s):** [Image-generation requests, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples; generated design image links when run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated variations may differ in print details; review key design elements.]

## Skill Version(s):

0.1.8 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
