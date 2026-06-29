## Description: <br>
Helps agents prepare, submit, and follow up on PoYo Happy Horse 1.1 text-to-video, image-to-video, and reference-to-video jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to prepare Happy Horse 1.1 video-generation payloads, submit trusted PoYo jobs, and explain polling or webhook follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: POYO_API_KEY can be exposed if copied into browser code, public repositories, logs, screenshots, or chat output. <br>
Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager and avoid echoing it in generated commands or responses. <br>
Risk: Prompts, source images, reference images, and callback URLs may contain confidential information sent to PoYo or a webhook receiver. <br>
Mitigation: Submit private media, prompts, or callback URLs only when the user trusts PoYo and the receiving webhook. <br>
Risk: The submit script sends a user-prepared JSON payload to the PoYo generation endpoint. <br>
Mitigation: Review the payload JSON before running the script and make live API calls only from a trusted shell when the user explicitly asks. <br>


## Reference(s): <br>
- [PoYo Happy Horse 1.1 API Reference](references/api.md) <br>
- [PoYo Happy Horse 1.1 Documentation](https://docs.poyo.ai/api-manual/video-series/happy-horse-1-1) <br>
- [PoYo Happy Horse 1.1 Model Page](https://poyo.ai/models/happy-horse-1-1) <br>
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-happy-horse-1-1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes selected model, workflow type, payload or parameter summary, source or reference image use, task_id if submitted, and the next polling or webhook step.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
