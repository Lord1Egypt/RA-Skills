## Description: <br>
AI-powered fashion model pose transfer tool. Generate pose variations of a model/product image using reference pose images while keeping clothing and background consistent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[3cpj](https://clawhub.ai/user/3cpj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and fashion-commerce teams use this skill to generate model or product image pose variations from local source and reference pose images through fal.ai, saving image outputs and a JSON result summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads selected original and reference images to fal.ai for processing. <br>
Mitigation: Use a dedicated fal.ai API key with spending limits, and avoid uploading confidential, regulated, or unreleased commercial images unless fal.ai processing is approved. <br>
Risk: The downloader disables normal HTTPS certificate verification when saving generated outputs. <br>
Mitigation: Fix the downloader to use standard HTTPS certificate verification before relying on saved outputs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/3cpj/pose-transfer) <br>
- [fal.ai API keys](https://www.fal.ai/dashboard/keys) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, JSON] <br>
**Output Format:** [Command-line output with generated JPEG files and a generation_results.json manifest] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FAL_KEY, Python 3.8+, fal-client, one original image, and one to four pose reference images.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
