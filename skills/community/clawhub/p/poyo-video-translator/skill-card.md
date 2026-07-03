## Description: <br>
Helps agents prepare and submit PoYo Video Translator jobs, including payloads, curl commands, status polling, callbacks, subtitle outputs, and response parsing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and integration teams use this skill to prepare server-side PoYo video translation requests, submit confirmed jobs, and handle async status or webhook workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys, private media URLs, callback URLs, task IDs, generated outputs, or authorization headers may be exposed if copied into logs, screenshots, public repositories, or chat. <br>
Mitigation: Keep POYO_API_KEY server-side, review payloads before submission, and avoid logging private request or output details unless product policy allows it. <br>
Risk: Live submissions send user-provided media URLs and translation jobs to PoYo. <br>
Mitigation: Make live API calls only after explicit user confirmation and from a trusted server-side environment. <br>


## Reference(s): <br>
- [PoYo Video Translator API Reference](references/api.md) <br>
- [PoYo Video Translator Model Page](https://poyo.ai/models/video-translator) <br>
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-video-translator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payload examples and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include returned task IDs and next-step status or webhook guidance when a request is submitted.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
