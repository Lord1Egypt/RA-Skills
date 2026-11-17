## Description:

精准文字海报生成技能（两步法）。当用户需要生成中文海报且文字必须100%精准时触发。核心方法：Step1 用 image_synthesize 以参考图生成插画，Step2 用 HTML 精确渲染文字，两者互补。适用场景：健康科普、教育宣传、活动海报、运营素材。

This skill is ready for commercial/non-commercial use.

## Publisher:

[leosheep821-debug](https://clawhub.ai/user/leosheep821-debug)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, educators, healthcare communicators, and operations teams use this skill to produce Chinese poster assets where exact readable text matters more than direct illustration fidelity. The workflow combines image-based illustration generation with HTML-rendered text for precise poster layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated posters may include copyrighted source imagery, commercial素材, or overly close visual references.

Mitigation: Review image sources and generated poster assets before public or commercial deployment; replace protected assets or use original artwork when rights are unclear.

Risk: Medical, educational, or operational poster claims may be inaccurate or insufficiently reviewed.

Mitigation: Have qualified reviewers check final poster text, claims, and context before publication.

Risk: User-supplied text embedded into HTML poster templates can carry unsafe or unintended content.

Mitigation: Sanitize or escape user-provided text before publishing generated HTML and inspect the rendered poster before sharing.

## Reference(s):

- [Poster prompt guide](references/poster_prompt_guide.md)
- [Bone health HTML poster template](references/bone_health_template.html)
- [ClawHub skill page](https://clawhub.ai/leosheep821-debug/skills/poster-precise-text)
- [Publisher profile](https://clawhub.ai/user/leosheep821-debug)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML template code and shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce HTML poster files and deployment guidance when the agent follows the workflow.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
