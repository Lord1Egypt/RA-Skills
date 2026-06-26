## Description: <br>
Nanobanana Pro generates and edits images through Google's Gemini Image API with automatic model fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yazelin](https://clawhub.ai/user/yazelin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to generate new images, edit existing images, or compose up to 14 input images through Gemini while saving the result locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected input images are sent to Google's Gemini service. <br>
Mitigation: Use the skill only with prompts and images that are appropriate to share with that service. <br>
Risk: Generated files may overwrite existing local outputs when filenames are reused. <br>
Mitigation: Save outputs to a dedicated folder or use unique filenames, such as timestamped names. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yazelin/nanobanana-pro-fallback) <br>
- [uv Documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and GEMINI_API_KEY; supports 1K, 2K, and 4K output requests; prints a MEDIA line for supported OpenClaw chat providers.] <br>

## Skill Version(s): <br>
0.4.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
