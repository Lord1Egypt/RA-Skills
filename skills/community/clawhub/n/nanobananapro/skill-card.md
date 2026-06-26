## Description: <br>
Generates and edits images with Nano Banana Pro (Gemini 3 Pro Image), supporting text-to-image and image-to-image workflows at 1K, 2K, and 4K resolutions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youthzenith](https://clawhub.ai/user/youthzenith) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate new PNG images or edit existing images through Google's Gemini image API from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected input images are sent to Google's Gemini image API. <br>
Mitigation: Use the skill only when that data sharing is acceptable for the content being generated or edited. <br>
Risk: The skill requires a Gemini API key and supports passing it on the command line. <br>
Mitigation: Prefer GEMINI_API_KEY from a protected environment or secret store, especially on shared systems or logged terminal sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/youthzenith/nanobananapro) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated PNG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are saved as PNG files in the user's current working directory or the requested output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
