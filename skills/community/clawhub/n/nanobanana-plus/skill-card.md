## Description: <br>
Nanobanana Plus uses the nanobanana-plus CLI to generate image files with per-call model switching, aspect ratio control, health checks, and model listing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[webkubor](https://clawhub.ai/user/webkubor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to invoke a local Node.js wrapper for image generation from text prompts, selecting model, aspect ratio, output filename, and output count per call. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill passes environment credentials to an unpinned external nanobanana-plus CLI. <br>
Mitigation: Confirm the executable path and source before use, and run the skill in an environment that contains only the API key required for image generation. <br>
Risk: The skill requires NANOBANANA_GEMINI_API_KEY or GEMINI_API_KEY credentials. <br>
Mitigation: Use a scoped or limited API key, rotate it according to local policy, and avoid sharing unrelated secrets with the runtime environment. <br>
Risk: Generated images are written to local file paths chosen at invocation time. <br>
Mitigation: Direct outputs to an expected workspace path and review generated files before publishing or sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/webkubor/nanobanana-plus) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Text and shell-command guidance with generated local image file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated image files are saved locally; the wrapper prints media paths for compatible chat providers.] <br>

## Skill Version(s): <br>
1.5.5 (source: server release metadata; artifact frontmatter reports 1.5.4 and package.json reports 1.5.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
