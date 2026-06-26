## Description: <br>
All-in-one AI content generator for creative, marketing, and social media workflows across image, video, music, and text-to-speech generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dai-shuo](https://clawhub.ai/user/dai-shuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, marketers, creators, and developers use this skill to generate AI images, videos, music, speech, ads, social content, and multi-step creative workflows through IMA Studio services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid IMA credits, private prompts, or local media may be used or uploaded during generation. <br>
Mitigation: Use a scoped or test IMA key first, confirm the intended media task and model before execution, and avoid sensitive local files unless upload is intended. <br>
Risk: Local preferences and operational logs can retain usage metadata. <br>
Mitigation: Periodically inspect or delete ~/.openclaw/memory/ima_prefs.json and ~/.openclaw/logs/ima_skills/ when local retention is not desired. <br>
Risk: Broad auto-activation and multimodal routing can lead to unintended API calls or costs. <br>
Mitigation: Review the planned media type, model, estimated cost, and requested output before running generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dai-shuo/ima-ai-creative-content-generator) <br>
- [Publisher profile](https://clawhub.ai/user/dai-shuo) <br>
- [IMA Studio homepage](https://imastudio.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration guidance, Media URLs] <br>
**Output Format:** [Markdown guidance with shell commands, JSON command output, progress messages, and generated media URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMA_API_KEY and python3; image/video/music/TTS results are returned as service-generated URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
