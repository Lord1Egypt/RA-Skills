## Description: <br>
Generate vertical life-hack and gadget demo shorts with WeryAI, using a problem-tool-payoff story for stains, prep, storage, quick fixes, and similar short-form demonstrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to plan and submit WeryAI video-generation tasks for short vertical life-hack or gadget demo clips. It expands brief prompts into production-ready English prompts, confirms parameters, runs the WeryAI helper script, and returns playable video URLs or clear API errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and public image URLs are sent to WeryAI for video generation. <br>
Mitigation: Use only prompts and image URLs that are appropriate to share with WeryAI, and avoid secrets or sensitive personal data. <br>
Risk: Successful generation consumes WeryAI credits through WERYAI_API_KEY. <br>
Mitigation: Review the confirmation table before approving generation and use a revocable or scoped API key where possible. <br>
Risk: The skill executes a Node.js helper that submits and polls remote API tasks. <br>
Mitigation: Run it in a short-lived or isolated environment when higher assurance is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/life-hack-video) <br>
- [Publisher profile](https://clawhub.ai/user/zoucdr) <br>
- [WeryAI video API host](https://api.weryai.com) <br>
- [WeryAI models API host](https://api-growth-agent.weryai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with parameter tables, shell commands, JSON request payloads, and returned video URLs or API error details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, network access, and public HTTPS image URLs for image-to-video inputs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
