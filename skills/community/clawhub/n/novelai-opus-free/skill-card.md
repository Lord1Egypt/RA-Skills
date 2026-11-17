## Description:

Opus zero-Anlas NovelAI workflows for OpenClaw: fiction writing, cost-aware single-image generation, img2img, inpainting, pre-encoded Vibe use, annotation, selected free Director tools, and same-session verification reuse with strict account and balance guards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techotaku39](https://clawhub.ai/user/techotaku39)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to plan fiction workflows and run tightly gated NovelAI Opus image operations that must remain at an explicit zero Image Anlas estimate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OpenClaw host receives access to the user's NovelAI token and account status.

Mitigation: Install only in a trusted OpenClaw environment and keep NOVELAI_TOKEN out of prompts, logs, files, and generated metadata.

Risk: NovelAI provider billing or Usage Limit behavior can change after a zero-cost workflow has been tested.

Mitigation: Use the skill's account checks, exact cost estimates, single-image limits, and post-operation audit before continuing image work.

Risk: Ambiguous, missing, or non-zero cost signals could lead to unintended paid image operations.

Mitigation: Block image generation unless the estimator returns an explicit numeric zero Anlas result and stop on account warnings or balance discrepancies.

## Reference(s):

- [OpenClaw NovelAI Opus Free ClawHub listing](https://clawhub.ai/techotaku39/skills/novelai-opus-free)
- [OpenClaw NovelAI Opus Free source homepage](https://github.com/techotaku39/openclaw-novelai/tree/main/variants/openclaw-novelai-opus-free)
- [Opus Free Enhancement Mode: Costs and Quotas](docs/COSTS-AND-QUOTAS.md)
- [NovelAI Subscription](https://docs.novelai.net/en/subscription/)
- [NovelAI FAQ - Opus Usage Limits](https://docs.novelai.net/en/faq/)
- [Steps & Prompt Guidance](https://docs.novelai.net/en/image/stepsguidance/)
- [NovelAI Image Generation](https://docs.novelai.net/en/image/)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, configuration, tool calls]

**Output Format:** [Markdown guidance with guarded NovelAI workflow steps and tool-use constraints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NOVELAI_TOKEN in the OpenClaw host environment and targets win32, linux, and darwin hosts.]

## Skill Version(s):

0.2.3 (source: frontmatter, changelog, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
