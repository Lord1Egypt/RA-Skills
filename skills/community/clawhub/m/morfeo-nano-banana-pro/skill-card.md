## Description: <br>
Generates and edits images using Google's Nano Banana Pro (Gemini 3 Pro Image) API, including text-to-image, image editing, reference images, and configurable 1K, 2K, or 4K resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PauldeLavallaz](https://clawhub.ai/user/PauldeLavallaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to have an agent prepare prompts and run image generation or image editing workflows through Google's Gemini image API. Common uses include product photography, style transfer, character or subject consistency, and editing existing images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and any specified input or reference images are sent to Google for processing. <br>
Mitigation: Use only content that is acceptable to send to Google, and avoid sensitive personal, confidential, or regulated images unless that upload is approved. <br>
Risk: Passing an API key directly on the command line can expose the key through shell history or process listings. <br>
Mitigation: Prefer the GEMINI_API_KEY environment variable over the --api-key argument. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/PauldeLavallaz/morfeo-nano-banana-pro) <br>
- [Google AI Studio Gemini image API endpoint](https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key=${API_KEY}) <br>
- [Vertex AI Gemini image API endpoint](https://${REGION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${REGION}/publishers/google/models/gemini-3-pro-image-preview:predict) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance, files] <br>
**Output Format:** [Plain text guidance with shell commands; generated or edited images are saved as PNG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Gemini API key via GEMINI_API_KEY or --api-key and can use input or reference image paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
