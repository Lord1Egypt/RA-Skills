## Description:

商品图生成（非服饰类）。支持单张或套图：白底主图、场景图、特写图、卖点版式图、A+详情页图。单张单类型直接出图；多张多类型自动编排规划。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and commerce teams use this skill to generate non-apparel product images for marketplace listings, including white-background images, scene images, close-ups, selling-point layouts, and A+ detail images. Developers and agents use it to plan multi-image product sets, prepare prompt and image-generation parameters, dispatch generation jobs, and return image results with manifests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Job-provided script path overrides could cause the skill to run unexpected local code.

Mitigation: Remove or constrain script path overrides before use and run only reviewed script paths from the installed skill and approved dependencies.

Risk: Configurable account, payment, and gateway endpoints may expose users to credential or billing-flow misuse.

Mitigation: Allowlist expected LinkFox HTTPS hosts and review the onboarding and payment flow before enabling it for users.

Risk: Prompt templates may infer or require race or ethnicity in generated scene descriptions.

Mitigation: Fix the affected prompt templates before deployment and prohibit demographic inference unless explicitly justified and reviewed.

Risk: Shared or untrusted workspaces can allow environment variables or collection-state files to be modified between planning and dispatch.

Mitigation: Run the skill in a controlled workspace with restricted file and environment access.

## Reference(s):

- [Skill definition](artifact/SKILL.md)
- [Runtime workflow index](artifact/references/runtime/00-index.md)
- [Planning phase](artifact/references/runtime/01-plan.md)
- [Confirmation and dispatch phase](artifact/references/runtime/02-confirm.md)
- [Image delivery protocol](artifact/references/runtime/03-deliver.md)
- [White-background image type](artifact/references/types/white-bg.md)
- [Scene image type](artifact/references/types/scene.md)
- [Close-up image type](artifact/references/types/close-up.md)
- [Selling-point image type](artifact/references/types/selling-point.md)
- [A+ image type](artifact/references/types/aplus.md)
- [Onboarding and account recovery](artifact/references/onboarding.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown with inline image references, JSON parameter/status files, shell command snippets, and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write image plans, collection state, task results, asset manifests, prompt parameter files, and generated media files into the session workspace.]

## Skill Version(s):

1.2.5 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
