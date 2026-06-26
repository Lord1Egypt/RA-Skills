## Description: <br>
Generate images, videos, and text/LLM completions via the imgnAI Katana API, with support for E2EE and anonymized models plus optional media post-processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imgn](https://clawhub.ai/user/imgn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route an agent through imgnAI Katana workflows for paid image generation, video generation, text/LLM completions, and local media post-processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid API requests can spend credits. <br>
Mitigation: Review model, cost, recipient details, prompt, and media inputs before approving each generation request. <br>
Risk: Prompts, files, and media inputs may be sent to imgnAI Katana. <br>
Mitigation: Use the skill only for content you are comfortable sending to the Katana service, and choose privacy tiers that match the sensitivity of the task. <br>
Risk: API credentials can authorize paid requests if exposed. <br>
Mitigation: Store the Katana API key and secret in a private secrets file, keep the file permissions restricted, and never display credentials in command output. <br>
Risk: Optional ffmpeg setup can modify the host environment. <br>
Mitigation: Approve package-manager installation commands only when host changes are intended, and review local post-processing commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imgn/katana) <br>
- [Publisher profile](https://clawhub.ai/user/imgn) <br>
- [imgnAI homepage](https://app.imgnai.com) <br>
- [Katana API page](https://app.imgnai.com/katana-api) <br>
- [Katana API reference](https://kat.imgnai.com/llms.txt) <br>
- [Model catalogue](models.md) <br>
- [Image workflow](workflows/image.md) <br>
- [Video workflow](workflows/video.md) <br>
- [Text workflow](workflows/text.md) <br>
- [Post-processing workflow](workflows/post-process.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API calls, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON API payloads, generated text, and media result URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Katana API credentials and user confirmation before paid generation requests; optional ffmpeg post-processing can create or modify local media files.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter, release evidence, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
