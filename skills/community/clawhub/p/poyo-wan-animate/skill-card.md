## Description: <br>
Poyo Wan Animate helps agents prepare, submit, and follow up on PoYo Wan Animate video generation jobs for character animation and character replacement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to build PoYo Wan Animate requests, choose the character replacement or character animation model, prepare payloads, and explain polling or webhook follow-up. It is intended for workflows using one source video URL, one target image, and supported 480p, 580p, or 720p output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys could be exposed if copied into browser code, public repositories, logs, screenshots, or chat output. <br>
Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager and avoid echoing it in generated examples. <br>
Risk: Submitting private likeness images, private videos, or private callback URLs sends sensitive material to PoYo or a webhook receiver. <br>
Mitigation: Use the skill only when the user trusts PoYo and the callback receiver, and review payloads before submission. <br>
Risk: A live API submission may create an external asynchronous video generation job. <br>
Mitigation: Make live calls only after an explicit user request from a trusted shell environment, then preserve the returned task id for polling or webhook follow-up. <br>


## Reference(s): <br>
- [PoYo Wan Animate API Documentation](https://docs.poyo.ai/api-manual/video-series/wan-animate) <br>
- [PoYo Wan Animate Model Page](https://poyo.ai/models/wan-animate) <br>
- [PoYo Wan Animate API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-wan-animate) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON payloads and inline bash or curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include chosen model id, concise parameter summaries, prepared request payloads, task ids from user-directed submissions, and next-step polling or webhook guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
