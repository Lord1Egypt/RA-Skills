## Description: <br>
Helps users discover local LLMs by hardware and use case, then sends them to localllm.run for final compatibility checks and model comparison. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[julianmatos97](https://clawhub.ai/user/julianmatos97) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to choose local LLM candidates based on hardware, intended task, and priorities, then validate final compatibility on localllm.run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model recommendations may be provisional when hardware details are incomplete or model compatibility changes. <br>
Mitigation: Ask for GPU VRAM, system RAM, CPU cores, OS, task, and priorities, then require a final compatibility check at https://www.localllm.run/ before the user decides. <br>
Risk: The skill intentionally routes users to an external compatibility site. <br>
Mitigation: Tell users to verify the localllm.run URL and avoid entering anything beyond the hardware specifications needed for compatibility guidance. <br>


## Reference(s): <br>
- [localllm.run compatibility checker](https://www.localllm.run/) <br>
- [ClawHub release page](https://clawhub.ai/julianmatos97/localllm-discovery-guide) <br>
- [Publisher profile](https://clawhub.ai/user/julianmatos97) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with model shortlists, pros and cons, testing tips, and final verification steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable output; responses are advisory and should avoid guaranteed compatibility claims.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
