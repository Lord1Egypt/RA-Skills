## Description: <br>
Generate Clawra-style selfie images with a Qwen-first image backend (with optional Gemini and HF fallback) and send them to messaging channels via OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nasplycc](https://clawhub.ai/user/nasplycc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw operators use this skill to generate role-consistent Clawra/Raya selfie or daily-status images from a prompt and send the generated image to a configured messaging channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send generated images through configured OpenClaw channels from broad chat prompts without a clear confirmation step. <br>
Mitigation: Require explicit user intent and destination confirmation before sending, or run with NO_SEND=1 when reviewing output. <br>
Risk: Prompt text and generated-image requests are sent to third-party image-generation providers. <br>
Mitigation: Avoid sensitive prompt content and use separate scoped API keys for Qwen, Gemini, and Hugging Face providers. <br>
Risk: Reference images may involve private or real-person likenesses. <br>
Mitigation: Use reference images only with consent and avoid real-person impersonation use cases. <br>
Risk: The README documents a remote installer pattern. <br>
Mitigation: Prefer ClawHub installation or inspect and pin the remote installer before executing it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nasplycc/nasplycc-clawra-selfie) <br>
- [Source repository](https://github.com/nasplycc/clawra-selfie) <br>
- [Original Clawra reference project](https://github.com/SumeLabs/clawra) <br>
- [Hugging Face token settings](https://huggingface.co/settings/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Generated image file plus JSON or command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send the generated image and caption to an OpenClaw messaging channel unless NO_SEND is set.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence and changelog, released 2026-03-25) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
