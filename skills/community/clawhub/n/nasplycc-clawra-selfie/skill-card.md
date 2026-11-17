## Description:

Generate Clawra-style selfie images with a Qwen-first image backend (with optional Gemini and HF fallback) and send them to messaging channels via OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nasplycc](https://clawhub.ai/user/nasplycc)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and agent developers use this skill to generate persona-consistent selfie or daily-state images from prompts and optionally send them through configured messaging channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated images can be sent to external messaging channels.

Mitigation: Require explicit confirmation before sending and test with the no-send path when reviewing prompts, channels, or captions.

Risk: The skill relies on API credentials for Qwen, Gemini, and Hugging Face services.

Mitigation: Use dedicated low-scope keys, avoid logging secrets, and rotate credentials if prompts, logs, or generated artifacts may have been exposed.

Risk: The installer supports a mutable remote script path.

Mitigation: Prefer ClawHub installation or a pinned clone, and review install scripts before execution.

Risk: Prompts and reference images may contain sensitive personal information.

Mitigation: Avoid sensitive prompts or personal reference images, and keep private references outside public repositories and shared logs.

Risk: Changing the Hugging Face API base can redirect model requests.

Mitigation: Keep HF_API_BASE fixed to the official Hugging Face endpoint unless a trusted deployment explicitly requires otherwise.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nasplycc/skills/nasplycc-clawra-selfie)
- [Project repository](https://github.com/nasplycc/clawra-selfie)
- [Original Clawra reference project](https://github.com/SumeLabs/clawra)
- [Hugging Face token settings](https://huggingface.co/settings/tokens)

## Skill Output:

**Output Type(s):** [Files, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Generated image file with JSON status output and optional messaging-channel delivery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses direct, mirror, or auto mode; supports Qwen, optional Gemini, and Hugging Face fallback backends.]

## Skill Version(s):

1.1.3 (source: server release and changelog, released 2026-03-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
