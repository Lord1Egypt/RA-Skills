## Description:

Generates, edits, and animates images and videos, creates transparent subject cutouts, and turns images into 3D meshes through a configured ComfyUI server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshinejnjn](https://clawhub.ai/user/sunshinejnjn)

### License/Terms of Use:

BSD 3-Clause

## Use Case:

External users and developers use this skill to generate or edit images and videos, extract transparent cutouts, or create 3D meshes with a ComfyUI server they configure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and source images are sent to the configured ComfyUI server, and generated media is saved locally.

Mitigation: Use a server you trust, use HTTPS for remote connections, and check the output location before submitting sensitive content.

Risk: After successful retrieval, the skill may delete this run's generated files and uploaded inputs from the server.

Mitigation: Tell the user before running when this cleanup will occur; use `--keep` or `COMFYUI_PURGE=0` when server copies need to remain.

Risk: Server authentication, cleanup behavior, separately installed plugins, and model files depend on external components that were not tested in the security assessment.

Mitigation: Review the ComfyUI server's authentication and deletion setup, and separately review installed plugins and model files.

## Reference(s):

- [ComfyUI setup and CLI guidance](README.md)
- [Workflow attribution](references/attribution.md)
- [Media delivery guidance](references/delivery.md)
- [ComfyUI purge-after-retrieval plugin](https://github.com/sunshinejnjn/comfyui-purge-after-retrieval)

## Skill Output:

**Output Type(s):** [Image files, Video files, 3D mesh archives]

**Output Format:** [PNG or JPG images, generated video files, and ZIP archives containing GLB meshes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media is saved locally under the configured output directory; image format and generation options can be selected per request.]

## Skill Version(s):

4.7.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
