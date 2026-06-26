## Description: <br>
Complete Venice AI platform: text generation, web search, embeddings, TTS, speech-to-text, image generation, video creation, upscaling, and AI editing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to access Venice-style AI capabilities through SkillBoss/HeyBoss-hosted Python scripts for chat, search, embeddings, audio, image, video, upscaling, and image editing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an API key and sends prompts, files, audio, images, and videos through SkillBoss/HeyBoss and downstream AI services. <br>
Mitigation: Use a dedicated low-privilege key, rotate it regularly, and avoid regulated, confidential, or sensitive personal data. <br>
Risk: The security summary flags a mismatch between privacy-oriented Venice branding and the actual SkillBoss/HeyBoss routing path. <br>
Mitigation: Review the service path and trust model before use, and disclose the routing behavior to users who provide content. <br>
Risk: URL-based scraping and media inputs can retrieve or process untrusted external content. <br>
Mitigation: Use trusted URLs, inspect inputs before execution, and keep generated outputs isolated until reviewed. <br>
Risk: Generated files or embedded metadata may contain prompt details when metadata options are enabled. <br>
Mitigation: Disable metadata embedding where possible and scrub generated media before sharing outside the workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/godferylindsay/martin-ai) <br>
- [SkillBoss API Reference](references/api.md) <br>
- [Venice AI](https://venice.ai) <br>
- [Venice API Docs](https://docs.venice.ai) <br>
- [Venice Status](https://veniceai-status.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash examples; scripts can return text, JSON, media URLs, and generated audio, image, or video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and SKILLBOSS_API_KEY; some operations write generated media under local tmp output directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
