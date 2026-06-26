## Description: <br>
Tencent Cloud Hunyuan Image Generation 3.0 creates images from text prompts, with optional reference-image guidance, resolution controls, seeds, and prompt rewriting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neck-cn](https://clawhub.ai/user/Neck-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit and monitor Tencent Cloud Hunyuan text-to-image or guided image-generation jobs from command-line scripts. It is suited for workflows that need generated image URLs, job IDs, revised prompts, and setup guidance for Tencent Cloud credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tencent Cloud API use requires credentials and may affect account quota or billing. <br>
Mitigation: Use a least-privilege Tencent API key, monitor quota and billing, and install only when Tencent Cloud Hunyuan image generation is intended. <br>
Risk: Prompts and reference image URLs are sent to the Tencent Cloud image-generation service. <br>
Mitigation: Avoid confidential prompts and private image URLs unless the deployment has approved that data flow. <br>
Risk: The scripts can automatically install the Tencent Cloud SDK when it is missing. <br>
Mitigation: Preinstall and pin an approved Tencent SDK version in managed environments. <br>


## Reference(s): <br>
- [Submit Text-to-Image API reference](references/submit_text_to_image_api.md) <br>
- [Query Text-to-Image API reference](references/query_text_to_image_api.md) <br>
- [Tencent Cloud SubmitTextToImageJob documentation](https://cloud.tencent.com/document/product/1668/124632) <br>
- [Tencent Cloud QueryTextToImageJob documentation](https://cloud.tencent.com/document/product/1668/124633) <br>
- [ClawHub release page](https://clawhub.ai/Neck-cn/hy-image-generation) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses with job status, generated image URLs, revised prompts, request IDs, and plain-text setup or error guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated image URLs are temporary; the skill documentation states they are valid for 1 hour.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
