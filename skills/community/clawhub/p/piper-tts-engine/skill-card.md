## Description: <br>
Piper Tts Engine helps agents guide local text-to-speech workflows for batch synthesis, custom voice training, multilingual speech generation, SSML control, API service deployment, and audio post-processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, automation teams, and content teams use this skill to plan and run local TTS workflows for audiobook production, multilingual customer-service audio, enterprise notifications, API-backed synthesis, and custom voice experimentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API deployment examples may be unsafe if exposed without access controls. <br>
Mitigation: Keep APIs bound to localhost unless authentication, TLS, authorization, request limits, and logging are added. <br>
Risk: Custom voice training can involve sensitive or restricted voice recordings. <br>
Mitigation: Use only recordings the operator has permission to process, store them securely, and define deletion and retention rules. <br>
Risk: Shell and subprocess examples are illustrative and may need hardening before production use. <br>
Mitigation: Review commands before execution, avoid unsanitized user input, and tighten ffmpeg and subprocess usage for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/piper-tts-engine) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local files, command-line invocations, API request examples, and configuration values for TTS workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
