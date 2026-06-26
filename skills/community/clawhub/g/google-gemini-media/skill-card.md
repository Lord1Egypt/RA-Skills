## Description: <br>
Use the Gemini API (Nano Banana image generation, Veo video, Gemini TTS speech and audio understanding) to deliver end-to-end multimodal media workflows and code templates for "generation + understanding". <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xsir0](https://clawhub.ai/user/Xsir0) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to choose Gemini media capabilities and implement image, video, speech, and audio workflows with Node.js or REST examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and media files may be sent to Google for processing. <br>
Mitigation: Use only media that the user is authorized to upload and avoid confidential, regulated, or third-party content unless appropriate approvals are in place. <br>
Risk: The Gemini API key may consume quota or incur billing. <br>
Mitigation: Store the API key outside source code, scope access appropriately, and monitor usage before running large media workflows. <br>
Risk: Example output filenames or directories may overwrite existing local files. <br>
Mitigation: Change output paths or add existence checks when preserving prior files matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Xsir0/google-gemini-media) <br>
- [Gemini generateContent API endpoint](https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JavaScript, REST, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce API request templates and local media input/output handling guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
