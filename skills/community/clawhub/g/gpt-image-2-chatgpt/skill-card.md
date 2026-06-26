## Description: <br>
Generate and edit images with GPT Image 2 inside Claude Code through the local Codex CLI, using the user's existing ChatGPT Plus or Pro subscription. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when they explicitly want an agent to generate, edit, restyle, or compose images through GPT Image 2 using their local Codex CLI login and ChatGPT subscription. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow stores prompts and image-generation artifacts in local Codex session logs under ~/.codex/sessions, then reads newly created rollout files to recover generated images. <br>
Mitigation: Use the skill only when local session-log retention is acceptable, and avoid highly sensitive prompts or reference images unless that retention has been reviewed. <br>
Risk: The skill depends on a local Codex CLI login, a ChatGPT subscription with image-generation entitlement, and local access to ~/.codex/sessions. <br>
Mitigation: Confirm codex, python3, Codex login state, and subscription entitlement before relying on the workflow for image generation. <br>
Risk: Image generation is performed by the Codex CLI using the user's existing ChatGPT login rather than by this skill as a standalone service. <br>
Mitigation: Treat failures as authentication, entitlement, quota, network, or model availability issues in the local Codex setup before changing prompts or switching routes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/gpt-image-2-chatgpt) <br>
- [Publisher profile](https://clawhub.ai/user/kalvinrv) <br>
- [agentspace.so](https://agentspace.so/?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-image-2-chatgpt) <br>
- [Source skill repository path](https://github.com/agentspace-so/skills/tree/main/gpt-image-2) <br>
- [OpenAI Codex CLI](https://github.com/openai/codex) <br>
- [RunComfy GPT Image 2 text-to-image](https://www.runcomfy.com/models/openai/gpt-image-2/text-to-image) <br>
- [RunComfy GPT Image 2 image edit](https://www.runcomfy.com/models/openai/gpt-image-2/edit) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands that produce image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The shell workflow writes a PNG, JPEG, or WebP image file to the caller-selected output path.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
