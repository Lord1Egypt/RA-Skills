## Description: <br>
Generate professional advertising images from product URLs using the Ad-Ready pipeline on ComfyDeploy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PauldeLavallaz](https://clawhub.ai/user/PauldeLavallaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and marketing teams use this skill to generate ad-ready product imagery from a product URL, brand profile, campaign objective, and optional logo, talent, or reference assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product URLs and image assets are sent to ComfyDeploy for ad generation. <br>
Mitigation: Use public product pages and only upload assets that the user is comfortable processing through ComfyDeploy. <br>
Risk: Likeness-preserving model images and reference ads can create consent, rights, or brand-safety concerns. <br>
Mitigation: Use model, reference, logo, and product assets only when the user has clear consent and commercial usage rights. <br>
Risk: Reference-image workflows may copy the style, pose, or location cues of an existing ad. <br>
Mitigation: Keep reference images off by default and use them only when explicitly requested and rights-cleared. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/PauldeLavallaz/product-to-ads) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash commands; generated ad image files when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires product URL, brand profile, prompt profile, output path, and a ComfyDeploy API key; may use optional product image, logo, model, reference, aspect ratio, language, and creative brief inputs.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
