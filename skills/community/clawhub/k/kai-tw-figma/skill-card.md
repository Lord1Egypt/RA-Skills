## Description: <br>
Interact with Figma files to read structure, export layers as images, and retrieve comments using the Figma REST API with authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kai-tw](https://clawhub.ai/user/kai-tw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and design-focused agents use this skill to inspect Figma files, retrieve comments, navigate team and project structures, and export selected design layers for implementation work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Figma personal access token, which is a sensitive credential. <br>
Mitigation: Use the least-privileged Figma token available, keep FIGMA_TOKEN out of shared logs or prompts, and rotate the token if exposure is suspected. <br>
Risk: Export operations write image files to the current working directory. <br>
Mitigation: Run exports from a directory intended for generated assets and review or clean up exported files before sharing the workspace. <br>


## Reference(s): <br>
- [Figma API Documentation](https://www.figma.com/developers/api) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/kai-tw/kai-tw-figma) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON API responses, and exported image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FIGMA_TOKEN and may write exported assets to the current working directory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
