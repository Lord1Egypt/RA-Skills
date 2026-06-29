## Description: <br>
Helps agents prepare and submit PoYo Kling Avatar 2.0 audio-driven avatar video jobs, then explain polling or webhook follow-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure PoYo Kling Avatar 2.0 standard or pro jobs with one avatar image, one driving audio URL, optional prompt guidance, and optional webhook handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: POYO_API_KEY could be exposed if included in browser code, repositories, logs, screenshots, or chat output. <br>
Mitigation: Keep POYO_API_KEY in a server-side environment variable or secret manager and avoid echoing it in generated examples or live output. <br>
Risk: Avatar images, audio URLs, prompts, or callback URLs may contain private or confidential information sent to PoYo or a callback receiver during live submissions. <br>
Mitigation: Submit private media, prompts, and callback URLs only when the user trusts PoYo and the callback receiver, and avoid logging sensitive URLs. <br>
Risk: Live generation requests may incur provider costs or be subject to provider terms. <br>
Mitigation: Confirm user intent, provider terms, and expected costs before making live API calls. <br>


## Reference(s): <br>
- [PoYo Kling Avatar 2.0 API Manual](https://docs.poyo.ai/api-manual/video-series/kling-avatar-2-0) <br>
- [PoYo Kling Avatar 2.0 Model Page](https://poyo.ai/models/kling-avatar-2-0) <br>
- [API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON payloads and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include the selected model id, payload summary, task_id after live submission, and the next polling or webhook step.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
