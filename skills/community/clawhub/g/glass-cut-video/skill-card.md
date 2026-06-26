## Description: <br>
Generate satisfying vertical short videos of glass cutting and shattering with WeryAI, either from text prompts or by animating a glass photo into cuts, crack spread, and break motion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agent users use this skill to prepare and run WeryAI text-to-video or image-to-video jobs for vertical glass cutting, cracking, and shattering ASMR clips. The skill helps collect parameters, expand prompts, validate supported video settings, and return generated video URLs or actionable failure details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a WERYAI_API_KEY and sends generation requests to an external WeryAI API. <br>
Mitigation: Use a dedicated or limited API key, keep it out of committed files, and install only when the publisher is trusted with that credential. <br>
Risk: Confirmed generation runs may consume paid WeryAI credits. <br>
Mitigation: Review the generated prompt and parameter table before confirming a run, and use dry-run behavior when validating request shape. <br>
Risk: Prompts and public image URLs may expose sensitive creative briefs or private imagery to the external provider. <br>
Mitigation: Avoid confidential prompts and private images; use only public HTTPS image URLs that are intended for external processing. <br>
Risk: Unsupported model parameters or local image paths can cause API failures. <br>
Mitigation: Validate model, duration, aspect ratio, resolution, audio settings, and image URL constraints before submitting a job. <br>


## Reference(s): <br>
- [Glass Cut Video on ClawHub](https://clawhub.ai/zoucdr/glass-cut-video) <br>
- [WeryAI video generation API host](https://api.weryai.com) <br>
- [WeryAI video model registry host](https://api-growth-agent.weryai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON command payloads; runtime CLI output is JSON containing task status, errors, and video URLs when generation succeeds.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and WERYAI_API_KEY. Image inputs must be public HTTPS URLs. Confirmed generation runs use paid WeryAI credits and call fixed external API hosts.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
