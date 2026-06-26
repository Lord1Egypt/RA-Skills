## Description: <br>
Kie Ai Skill gives agents unified API access to kie.ai image-generation models with local storage, optional Google Drive upload, usage tracking, and task resume support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jon-xo](https://clawhub.ai/user/jon-xo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to generate images through kie.ai, inspect model pricing and balance information, resume tasks, and optionally upload completed files to Google Drive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to kie.ai for generation, and generated files are sent to Maton only when Drive upload is enabled. <br>
Mitigation: Use a limited KIE API key, keep Drive upload disabled unless needed, and review the third-party services before using sensitive prompts or outputs. <br>
Risk: Generated images and task history may remain in local storage after use. <br>
Mitigation: Delete the images directory and .task-state.json when prompts or outputs are sensitive. <br>
Risk: The security review flags unsafe input handling and API-key forwarding as review-worthy risks before installation. <br>
Mitigation: Avoid untrusted text for the models category option and prefer a release that validates download hosts before forwarding Authorization headers. <br>


## Reference(s): <br>
- [Publisher profile](https://clawhub.ai/user/jon-xo) <br>
- [ClawHub skill page](https://clawhub.ai/jon-xo/kie-ai-skill) <br>
- [Skill homepage](https://github.com/jon-xo/kie-ai-skill) <br>
- [kie.ai documentation](https://docs.kie.ai) <br>
- [kie.ai pricing](https://docs.kie.ai/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Terminal text with generated image files and optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KIE_API_KEY; optional Drive upload requires MATON_API_KEY and configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
