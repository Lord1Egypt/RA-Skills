## Description: <br>
Transforms text or public image prompts into holy ceremony and celebration-style video generation requests for WeryAI Seedance 2.0, with prompt expansion, parameter confirmation, and playable video links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn a short event brief or public image URL into a polished ceremonial video-generation prompt, confirm Seedance 2.0 parameters, submit the WeryAI job, and return video links or actionable errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a paid WeryAI API key and may consume credits when generation jobs are submitted or re-run. <br>
Mitigation: Use a revocable or quota-limited WERYAI_API_KEY and confirm the request table before submission. <br>
Risk: Prompts or public image URLs are sent to WeryAI for video generation. <br>
Mitigation: Avoid sensitive personal data and private media URLs; use only public HTTPS image URLs that are appropriate to share with the service. <br>
Risk: The bundled CLI does not enforce the package's required SEEDANCE_2_0 model in code. <br>
Mitigation: Review the confirmation table before submission and verify that the model is SEEDANCE_2_0. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/holy-ceremony-transform-video-gen-seedance2-0) <br>
- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown confirmation tables, inline shell commands, JSON CLI responses, and Markdown video links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, network access to WeryAI, and public HTTPS image URLs for image-to-video inputs.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
