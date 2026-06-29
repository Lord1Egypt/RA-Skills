## Description: <br>
HiAPI GPT Image 2 helps an agent generate or edit images through HiAPI's GPT Image 2 family, using text prompts, optional public reference image URLs, model selection, aspect ratios, and resolution settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hiapiai](https://clawhub.ai/user/hiapiai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Use this skill when an agent needs to create text-to-image outputs or image-to-image edits with HiAPI GPT Image 2 models, save generated image files, return image URLs, or guide users through HiAPI API key, billing, rate-limit, and safety-policy errors. <br>

### Deployment Geography for Use: <br>
Global, subject to the user's HiAPI account terms, local laws, and organizational policy for sending prompts and reference image URLs to a third-party image generation service. <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends image prompts and any reference image URLs to HiAPI under the user's account. <br>
Mitigation: Install and run it only when users are comfortable sharing that content with HiAPI, keep the API key in the environment, and avoid printing credentials in logs or final answers. <br>
Risk: Changing the HiAPI base URL can redirect prompts and credentials to a different endpoint. <br>
Mitigation: Keep HIAPI_BASE_URL at the default unless the user intentionally trusts another endpoint. <br>
Risk: Generated image tasks may fail because of missing or invalid credentials, insufficient balance, rate limits, content policy blocks, or missing image output. <br>
Mitigation: Use the skill's built-in error guidance to report the status and next action, and do not invent an image result when the API call fails. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hiapiai/hiapi-gpt-image-2) <br>
- [HiAPI Publisher Profile](https://clawhub.ai/user/hiapiai) <br>
- [HiAPI Documentation](https://docs.hiapi.ai) <br>
- [HiAPI API Key Registration](https://www.hiapi.ai/en/register) <br>
- [HiAPI Pricing](https://www.hiapi.ai/en/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Agent instructions and CLI-generated JSON describing saved image file paths or returned image URLs.] <br>
**Output Parameters:** [Prompt, model, optional input image URLs for image-to-image models, aspect ratio, resolution, output directory, and HiAPI configuration through environment variables.] <br>
**Other Properties Related to Output:** [Requires Node.js 18 or newer, a HiAPI API key, and usually a paid HiAPI account; successful data URI images are saved under outputs/ while remote image URLs are returned directly.] <br>

## Skill Version(s): <br>
1.0.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
