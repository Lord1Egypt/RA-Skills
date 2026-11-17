## Description:

Helps e-commerce merchants, lifestyle brands, and short-video creators turn first-person POV product-ad ideas into a production plan, storyboard scripts, shot prompts, AI-HIVE generation commands, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and marketing teams use this skill to plan and produce authorized first-person POV product advertisements for e-commerce, social media, and short-video channels. It guides users from product facts and owned materials through scripts, shot prompts, AI-HIVE task setup, local video checks, and final review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials could be sent to an unintended API host if the base URL is changed.

Mitigation: Use only the official AI-HIVE endpoint, avoid untrusted AI_HIVE_BASE_URL or config-file base_url values, and keep API keys out of shared command lines, logs, and screenshots.

Risk: Generation calls may incur charges or use unsuitable model parameters.

Mitigation: Review prompts, routing mode, model configuration, pricing snapshot, and task scope before submission; test small samples before batch generation.

Risk: Product advertising output can become misleading if facts, rights, or claims are not verified.

Mitigation: Require product facts and authorized materials, mark uncertain claims for review, and avoid copied protected creative elements, fake testimonials, unsupported performance claims, and platform-rule evasion.

Risk: Local media editing can process untrusted files.

Mitigation: Use trusted media inputs, keep original files, and review ffmpeg operations before running concat, trim, aspect, mute, or loudness-normalization commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/pov-product-ad-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with runnable command examples and JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local production brief JSON files, submit billable AI-HIVE generation tasks after review, and process videos with ffmpeg when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
