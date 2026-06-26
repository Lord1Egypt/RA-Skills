## Description: <br>
Prompt-ZS is a Chinese-oriented assistant for generating structured AI image, video, and prompt-optimization outputs for tools such as Midjourney, Stable Diffusion, Runway, and Pika. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bozoyan](https://clawhub.ai/user/bozoyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn Chinese or bilingual creative requests into image-generation prompts, video-generation prompts, concise translations, or structured JSON prompt fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases such as prompt optimization, image generation, or video generation may route requests into this skill even when the user only meant to discuss those topics. <br>
Mitigation: Confirm that the user wants a generated or optimized creative prompt before applying the skill's structured output rules. <br>
Risk: Generated creative prompts or translations may be inaccurate, culturally inappropriate, or unsuitable for a target model or production workflow. <br>
Mitigation: Review generated prompts before use, especially for brand, safety, localization, or commercial deliverables. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bozoyan/prompt-zs) <br>
- [Publisher profile](https://clawhub.ai/user/bozoyan) <br>
- [README](README.md) <br>
- [CHANGELOG](CHANGELOG.md) <br>
- [Evaluation cases](evals/evals.json) <br>
- [Basic prompt example](examples/basic-example.json) <br>
- [Expert prompt example](examples/expert2-example.json) <br>
- [Text-to-video example](examples/video-text-example.md) <br>
- [Image-to-video example](examples/video-image-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text, Markdown examples, or JSON arrays with Chinese and English prompt fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Video prompt outputs are described as a single concise paragraph under 500 Chinese characters; JSON modes use cn, en, cn-tag, and en-tag fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter, README, CHANGELOG released 2025-03-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
