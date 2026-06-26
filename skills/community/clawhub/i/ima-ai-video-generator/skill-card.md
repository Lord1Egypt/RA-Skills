## Description: <br>
AI video generator with premier models including Wan 2.6, Kling O1/2.6, Google Veo 3.1, Sora 2 Pro, Pixverse V5.5, Hailuo 2.0/2.3, SeeDance 1.5 Pro, and Vidu Q2 for text-to-video, image-to-video, first-last-frame, and reference-image video generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dai-shuo](https://clawhub.ai/user/dai-shuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to generate short videos, promotional clips, social media content, animated images, and multi-shot video concepts through IMA Studio models. Developers and agents can use it to select video modes, run the bundled API helper, and return generated video URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an IMA API key and sends prompts and selected images to IMA services. <br>
Mitigation: Install only if you trust IMA Studio with those inputs, use a revocable or low-quota API key, and avoid sensitive media. <br>
Risk: Video generation can consume paid credits through the configured IMA account. <br>
Mitigation: Monitor credit usage and prefer low-quota or scoped keys for testing. <br>
Risk: The skill keeps small local preference and log files. <br>
Mitigation: Periodically review or delete ~/.openclaw/memory/ima_prefs.json and ~/.openclaw/logs/ima_skills/ if local history matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dai-shuo/ima-ai-video-generator) <br>
- [IMA Studio homepage](https://imastudio.com) <br>
- [IMA API key management](https://www.imaclaw.ai/imaclaw/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated video URL results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMA_API_KEY; image-based tasks may upload provided images to IMA services and return remote video URLs.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
