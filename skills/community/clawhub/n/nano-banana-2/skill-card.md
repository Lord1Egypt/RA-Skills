## Description: <br>
Generate images with Google Gemini 3.1 Flash Image Preview (Nano Banana 2) via inference.sh CLI for text-to-image, image editing, multi-image input, and Google Search grounding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to invoke inference.sh workflows for image generation, image editing, multi-image prompts, and optional Google Search grounded image prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and input images are sent to external inference.sh and model services. <br>
Mitigation: Install only if you trust inference.sh, and avoid sending secrets, private images, personal data, or regulated content. <br>
Risk: Google Search grounding can send prompt context to external real-time information services. <br>
Mitigation: Enable Google Search grounding only when current information is needed and keep sensitive or regulated content out of grounded prompts. <br>


## Reference(s): <br>
- [Nano Banana 2 on ClawHub](https://clawhub.ai/okaris/nano-banana-2) <br>
- [inference.sh](https://inference.sh) <br>
- [inference.sh CLI install](https://cli.inference.sh) <br>
- [inference.sh CLI checksums](https://dist.inference.sh/cli/checksums.txt) <br>
- [Running Apps](https://inference.sh/docs/apps/running) <br>
- [Streaming Results](https://inference.sh/docs/api/sdk/streaming) <br>
- [File Handling](https://inference.sh/docs/api/sdk/files) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands and SDK examples invoke inference.sh and may return generated or edited images, model descriptions, and output metadata.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
