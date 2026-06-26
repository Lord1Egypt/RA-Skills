## Description: <br>
Generate vertical organizing shorts from chaos to order with WeryAI for closets, fridges, vanities, desks, luggage, and similar satisfying before-and-after scenes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to turn organizing-video briefs, optional image inputs, and confirmed WeryAI parameters into paid vertical video generation runs. It guides prompt expansion, parameter confirmation, CLI execution, and result handling for text-to-video or image-to-video organizing clips. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid WeryAI calls can consume quota and expose prompts to an external service. <br>
Mitigation: Use dry-run first, confirm parameters before paid submits, and run only with an API key whose permissions and quota are acceptable. <br>
Risk: Image-to-video inputs may upload selected local images to WeryAI when local file paths are used. <br>
Mitigation: Prefer public HTTPS image URLs and use local paths only after reviewing the script behavior and obtaining explicit consent for that exact upload. <br>
Risk: The WERYAI_API_KEY is a sensitive credential required at runtime. <br>
Mitigation: Keep the key out of source, chat, and logs; use a limited-scope or test key until the workflow is trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zoucdr/organize-room-video) <br>
- [WeryAI Video API Reference](resources/WERYAI_VIDEO_API.md) <br>
- [WeryAI Video API Host](https://api.weryai.com) <br>
- [WeryAI Models and Upload API Host](https://api-growth-agent.weryai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls] <br>
**Output Format:** [Markdown with parameter tables, inline shell commands, and JSON command payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces WeryAI task status summaries, error messages, and playable video URLs when generation succeeds.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
