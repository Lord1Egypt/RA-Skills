## Description: <br>
Interact with GitHub using the gh CLI for issues, PRs, CI runs, and advanced queries, and access 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TobeyRebecca](https://clawhub.ai/user/TobeyRebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to draft or execute SkillBoss API calls for chat, media generation, document processing, search, email, SMS, and related model-routing tasks. Reviewers should confirm they intentionally want this broad multi-provider API behavior rather than only GitHub automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is labeled as a GitHub helper but primarily documents broad SkillBoss API behavior. <br>
Mitigation: Confirm the intended use is SkillBoss multi-provider API access before installation or deployment. <br>
Risk: External AI processing, email, and SMS actions may expose sensitive prompts, files, audio, images, or contact data. <br>
Mitigation: Use a limited API key where available, avoid confidential inputs unless approved, and require explicit approval before email or SMS sends. <br>
Risk: Referenced helper commands such as `run.mjs` were not part of the reviewed artifact evidence. <br>
Mitigation: Review any helper scripts or local wrappers separately before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TobeyRebecca/github-ai) <br>
- [SkillBoss website](https://www.skillboss.co) <br>
- [SkillBoss API base URL](https://api.heybossai.com/v1) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Video Models](artifact/video-models.md) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Search & Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference generated media URLs or files when an agent executes the documented API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
