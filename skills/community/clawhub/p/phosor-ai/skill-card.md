## Description: <br>
Generate AI videos (text-to-video, image-to-video) with optional custom LoRA styles via the Phosor AI platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JasonStarlight](https://clawhub.ai/user/JasonStarlight) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit text-to-video and image-to-video jobs, manage generated video requests, and upload or import custom LoRA styles through the Phosor AI platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, uploaded images, LoRA files, and imported URLs are sent to Phosor AI for processing and may be billed to the configured API key. <br>
Mitigation: Use a trusted Phosor account, avoid sensitive prompts or media, keep the API key private, and review pricing and quota output before submitting jobs. <br>
Risk: A custom PHOSOR_BASE_URL changes where authenticated requests and uploaded content are sent. <br>
Mitigation: Use the default Phosor endpoint unless a trusted alternate endpoint is required, and verify any override before running commands. <br>
Risk: The CLI stores pending job metadata locally in phosor-pending.json. <br>
Mitigation: Remove the local pending job file when retained job metadata is no longer needed. <br>
Risk: The delete-lora command can remove a LoRA model from the user's Phosor account. <br>
Mitigation: Confirm the target LoRA ID before deletion. <br>


## Reference(s): <br>
- [Phosor AI API Reference](references/api.md) <br>
- [Phosor AI](https://phosor.ai) <br>
- [Phosor AI API Documentation](https://phosor.ai/docs) <br>
- [ClawHub skill page](https://clawhub.ai/JasonStarlight/phosor-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill's CLI sends authenticated requests to Phosor AI and can write local pending job metadata.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
