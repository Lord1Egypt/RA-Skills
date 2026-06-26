## Description: <br>
Creates vertical WeryAI absence shorts with a quiet-home arc, timed English captions, and safety boundaries against self-harm content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to generate melancholic short-form videos about safe absence or disappearance hypotheticals, with prompt expansion, duration scaling, subtitles, and WeryAI video generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts or image URLs are sent to WeryAI during generation and may contain sensitive personal details. <br>
Mitigation: Review the expanded prompt before generation and avoid private images or sensitive personal information unless the user intends to send them to WeryAI. <br>
Risk: The theme can be misused for crisis, self-harm, or mental-health-support requests. <br>
Mitigation: Refuse self-harm or suicide-method content and offer safer emotional or hopeful framing. <br>
Risk: The skill requires a paid WeryAI API key and external network calls. <br>
Mitigation: Install only when WeryAI use is intended, keep WERYAI_API_KEY in the environment, and do not commit the secret. <br>


## Reference(s): <br>
- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md) <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/if-you-vanished-video-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with an expanded prompt, inline shell commands, and a final video link or JSON error.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, paid WeryAI network access, and supported model parameters.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
