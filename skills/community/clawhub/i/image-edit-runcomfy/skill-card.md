## Description: <br>
Routes existing-image editing requests to the appropriate RunComfy Model API edit endpoint for background swaps, object changes, text rewrites, multi-reference edits, batch edits, and mask-based edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content-production teams use this skill to transform existing images through RunComfy while selecting an edit route that matches the requested operation. It supports workflows such as product-image cleanup, localized text replacement, background changes, and mask-constrained retouching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends source images, masks, and prompts to RunComfy for processing. <br>
Mitigation: Use it only when RunComfy is trusted for the content being edited, and avoid sensitive private images unless third-party processing is acceptable. <br>
Risk: Image edits can affect watermark, branding, identity, or rights-sensitive content. <br>
Mitigation: Confirm the user has rights to modify the provided images and review generated outputs before publication. <br>
Risk: The skill depends on the RunComfy CLI, account authentication, and a valid RUNCOMFY_TOKEN or local login. <br>
Mitigation: Install the CLI from a trusted source, keep tokens protected, and verify authentication before running edit commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kalvinrv/image-edit-runcomfy) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI Documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=image-edit-runcomfy) <br>
- [RunComfy Image Edit Models](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=image-edit-runcomfy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown guidance with inline RunComfy CLI commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for invoking RunComfy image-edit endpoints and saving generated image files to an output directory.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
