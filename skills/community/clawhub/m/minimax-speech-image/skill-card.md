## Description: <br>
Provides MiniMax Token Plan speech and image workflows, including text-to-speech, asynchronous speech generation, voice cloning, voice design, voice management, text-to-image generation, and image-to-image editing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[percivalee](https://clawhub.ai/user/percivalee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to call MiniMax speech and image APIs from an agent workflow, producing audio files, generated images, edited images, voice IDs, task IDs, and voice-management responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected prompts, audio, and images to MiniMax APIs. <br>
Mitigation: Use only prompts, audio, and images that are approved for processing by MiniMax and set MINIMAX_REGION deliberately before execution. <br>
Risk: Voice cloning and voice deletion can affect sensitive or account-bound voice assets. <br>
Mitigation: Clone only voices the user is authorized to process and double-check voice IDs before running delete operations. <br>
Risk: API calls consume MiniMax Token Plan quota. <br>
Mitigation: Confirm quota expectations before running generation, cloning, or editing workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/percivalee/minimax-speech-image) <br>
- [MiniMax China API endpoint](https://api.minimaxi.com/v1) <br>
- [MiniMax International API endpoint](https://api.minimax.io/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Files, API responses] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, JSON responses, MP3 audio files, PNG image files, voice IDs, and task IDs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and consumes MiniMax Token Plan quota.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
