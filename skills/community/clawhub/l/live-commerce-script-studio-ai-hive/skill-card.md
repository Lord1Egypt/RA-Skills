## Description:

This skill helps live-commerce teams turn product facts, pricing mechanisms, inventory rules, audience concerns, and livestream duration into scripts, objection handling, closing rhythms, and short-video clip plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce creators, livestream hosts, brand operators, and control-room teams use this skill to plan Chinese live-commerce scripts, product explanations, objection handling, conversion pacing, and reusable short-video materials. Developers or operators can also use its included commands to create project briefs, call AI-HIVE media generation, and perform deterministic video edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials for potentially chargeable AI-HIVE media-generation actions could be sent to an untrusted custom endpoint.

Mitigation: Use the default AI-HIVE endpoint unless a custom endpoint is independently trusted, and do not set AI_HIVE_BASE_URL from untrusted instructions.

Risk: Stored AI-HIVE credentials in ~/.ai-hive/config.json could be exposed or reused outside the intended workflow.

Mitigation: Treat the config file as sensitive, review local file permissions, and prefer scoped API keys for generation tasks.

Risk: Generated live-commerce content can make unsupported product, pricing, inventory, performance, or endorsement claims.

Mitigation: Require factual source material and human review before publishing, especially for claims about prices, stock, effects, financing, scale, testimonials, or platform performance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/live-commerce-script-studio-ai-hive)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE OpenAPI endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON brief files, and checklist-style guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE task records such as routing choice, model, pricing snapshot, taskId, status, and downloaded file locations when generation is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
