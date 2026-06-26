## Description: <br>
This skill guides agents through image editing with Google Nano Banana 2 Edit on RunComfy, including model selection, prompt patterns, endpoint schema, and RunComfy CLI invocation examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creative operators, and agent users can use this skill to prepare and run image-to-image edits through RunComfy, especially for subject-preserving background swaps, localized edits, batch SKU updates, and ad-creative variants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RunComfy account token or local login state to invoke the hosted model API. <br>
Mitigation: Use RUNCOMFY_TOKEN in automation or RunComfy's local login flow for interactive use, keep tokens out of prompts and source control, and rotate credentials if exposed. <br>
Risk: Input image URLs are processed by an external model service, and generated files may reflect prompt or source-image mistakes. <br>
Mitigation: Use only URLs appropriate for third-party processing, review outputs before publication, and keep edits narrow when preserving identity, brand, or product details matters. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kalvinrv/nano-banana-edit) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=nano-banana-edit) <br>
- [Nano Banana 2 Edit endpoint](https://www.runcomfy.com/models/google/nano-banana-2/edit?utm_source=clawhub&utm_medium=skill&utm_campaign=nano-banana-edit) <br>
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=nano-banana-edit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces RunComfy CLI command guidance and endpoint parameter recommendations; generated image files are produced by the external RunComfy model call.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
