## Description: <br>
IMA Sevio AI Generation lets agents create videos with Ima Sevio 1.0 and Ima Sevio 1.0-Fast across text-to-video, image-to-video, first-last-frame, and reference-image workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allenfancy-gan](https://clawhub.ai/user/allenfancy-gan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill to generate short videos from prompts and optional images using the two Sevio model choices. It supports quality-oriented generation, faster drafts, first-last-frame transitions, and reference-image motion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected media, and the IMA API key are sent to documented IMA services during generation and local-media upload flows. <br>
Mitigation: Install only if the publisher and IMA services are trusted, use a revocable API key, and avoid sending sensitive local media. <br>
Risk: Local logs can retain sensitive request details and may capture an API key during some upload failures. <br>
Mitigation: Periodically inspect or delete ~/.openclaw/logs/ima_skills/ and ~/.openclaw/memory/ima_prefs.json, especially after failed local-media uploads. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/allenfancy-gan/ima-sevio-ai) <br>
- [Publisher profile](https://clawhub.ai/user/allenfancy-gan) <br>
- [IMA Studio](https://imastudio.com/) <br>
- [IMA API key page](https://www.imaclaw.ai/imaclaw/apikey) <br>
- [IMA subscription and credits](https://www.imaclaw.ai/imaclaw/subscription) <br>
- [Security disclosure](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, video URL, guidance] <br>
**Output Format:** [JSON task/result payloads and concise user-facing text with remote video URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMA_API_KEY; accepts prompts, model choice, task type, and optional image inputs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
