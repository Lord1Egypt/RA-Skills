## Description: <br>
Manage OpenAI files, assistants, vector stores, batches, fine-tuning jobs, and model resources via the OpenAI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage OpenAI platform resources through ClawLink, including assistants, files, vector stores, batches, fine-tuning jobs, model listings, and generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires trust in ClawLink with access to the user's OpenAI account and API key. <br>
Mitigation: Install only when ClawLink is trusted for the connected OpenAI account. <br>
Risk: Uploads, generation calls, fine-tuning jobs, batches, assistant changes, deletions, and cancellations may send data to OpenAI, change account resources, or incur API costs. <br>
Mitigation: Review previews carefully and confirm write or destructive actions only when the target resource and expected effect are clear. <br>


## Reference(s): <br>
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference) <br>
- [Assistants API Overview](https://platform.openai.com/docs/assistants/overview) <br>
- [Fine-tuning Documentation](https://platform.openai.com/docs/guides/fine-tuning) <br>
- [Batch API](https://platform.openai.com/docs/guides/batch) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=openai-ai) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/openai-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce OpenAI API requests through ClawLink; write and destructive operations require user confirmation.] <br>

## Skill Version(s): <br>
1.0.6 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
