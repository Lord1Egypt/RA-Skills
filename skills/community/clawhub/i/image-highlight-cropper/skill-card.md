## Description: <br>
Extracts five visually interesting square crops from an uploaded image, saves them as downloadable files, and presents labeled close-ups with brief explanations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rosemaxio](https://clawhub.ai/user/rosemaxio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creative or technical reviewers use this skill to inspect large artwork, photographs, or technical drawings by extracting notable square close-ups. It also requires a visible painter's signature to be included as one of the crop highlights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes user-supplied images and creates cropped image files in local output storage. <br>
Mitigation: Use it for images the user is comfortable having locally processed into crop files. <br>
Risk: If Pillow is missing, the skill suggests installing it with pip using --break-system-packages. <br>
Mitigation: Approve dependency installation only in an environment where modifying the Python package setup is acceptable; a virtual environment or preinstalled dependency is safer. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/rosemaxio/image-highlight-cropper) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown summary with generated JPEG crop files and inline Python/Pillow commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates five square highlight_N.jpg crop files and asks whether to choose different areas or adjust crop sizes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
