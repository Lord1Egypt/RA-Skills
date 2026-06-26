## Description: <br>
Use the OpenClaw `infer` CLI for provider-backed model, image, audio transcription, TTS, video, web-search, and embedding tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[takhoffman](https://clawhub.ai/user/takhoffman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to choose and run OpenClaw `infer` commands for text, image, audio, TTS, video, web search, and embeddings. It is most useful when the task needs provider-backed inference through a consistent CLI with JSON output available for automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider-backed inference may send prompts, search queries, audio, images, or videos to configured services. <br>
Mitigation: Avoid secrets or regulated personal data unless authorized, and confirm the configured provider policies before use. <br>
Risk: The skill depends on the `openclaw` CLI package and local provider configuration. <br>
Mitigation: Install the CLI only from a trusted package source and verify available providers before running inference commands. <br>


## Reference(s): <br>
- [OpenClaw Infer skill page](https://clawhub.ai/takhoffman/openclaw-infer) <br>
- [OpenClaw infer CLI documentation](https://docs.openclaw.ai/cli/infer) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON-oriented command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the `openclaw` binary on PATH; command examples commonly use `--json` for machine-readable output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
