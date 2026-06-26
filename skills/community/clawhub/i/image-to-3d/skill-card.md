## Description: <br>
Image-to-3D asset creation for agents through Image Skill's zero-setup hosted runtime, turning an owned input image into a durable hosted 3D mesh asset such as GLB without provider credentials, OAuth, local runtime, or per-provider billing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielgwilson](https://clawhub.ai/user/danielgwilson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn an owned input image into a durable hosted 3D mesh asset such as GLB. It is intended for image-to-3D generation workflows that need inspection, bounded spend, job recovery, asset URLs, receipts, and feedback in one loop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runtime can spend media-generation credits or funds when a creation command is executed. <br>
Mitigation: Start with the no-spend inspection command and run paid creation only when media spend is explicitly allowed. <br>
Risk: Generated output depends on an external hosted service and may require an optional restricted Image Skill token for continuity. <br>
Mitigation: Use the documented hosted contract, keep outputs recoverable through job metadata, and avoid adding unrelated provider credentials or local model servers. <br>


## Reference(s): <br>
- [Image Skill](https://image-skill.com/skill.md) <br>
- [Image Skill LLM Contract](https://image-skill.com/llms.txt) <br>
- [Image Skill CLI Contract](https://image-skill.com/cli.md) <br>
- [Image Skill Hosted API](https://api.image-skill.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON-oriented runtime outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce hosted 3D asset URLs, job metadata, receipts, and feedback records through the Image Skill runtime.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
