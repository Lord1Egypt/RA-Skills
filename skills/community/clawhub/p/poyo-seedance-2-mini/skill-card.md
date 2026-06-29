## Description: <br>
Helps agents prepare PoYo Seedance 2.0 Mini video-generation requests, including text-to-video, image-to-video, reference-guided video, async submission, polling, and webhook guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create Seedance 2.0 Mini payloads, choose video-generation parameters, and submit or explain PoYo async video jobs. It is useful for text-to-video, image-to-video, first/last-frame, reference-media, polling, and webhook workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys could be exposed if used in browser code, logs, screenshots, public repositories, or chat output. <br>
Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and avoid printing or storing it in user-visible places. <br>
Risk: Prompts, media URLs, reference files, and callback URLs submitted to PoYo or a webhook receiver may contain sensitive information. <br>
Mitigation: Submit only data the user is comfortable sharing with PoYo and the callback receiver; avoid confidential media and private endpoints unless those parties are trusted. <br>
Risk: The included submission script can make live network calls and create PoYo video-generation tasks when run with a payload and API key. <br>
Mitigation: Run live submissions only after explicit user approval in a trusted shell, and review the payload before executing the script. <br>


## Reference(s): <br>
- [PoYo Seedance 2.0 Mini API Reference](references/api.md) <br>
- [PoYo Seedance 2.0 Mini documentation](https://docs.poyo.ai/api-manual/video-series/seedance-2-mini) <br>
- [PoYo Seedance 2 Mini model page](https://poyo.ai/models/seedance-2-mini) <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-seedance-2-mini) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, Shell commands, API calls] <br>
**Output Format:** [Markdown guidance with JSON payloads and curl or bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live submissions require POYO_API_KEY; otherwise the skill produces payloads, examples, and polling or webhook guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
