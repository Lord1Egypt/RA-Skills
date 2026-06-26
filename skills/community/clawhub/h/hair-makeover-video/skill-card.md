## Description: <br>
Generate vertical short WeryAI videos showing hair makeover or dye transformations with scissor cuts, color gradients, and clear before-and-after contrast. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to help creators generate hair transformation reels, salon-style dye clips, or character grooming glow-up videos through WeryAI. The skill expands brief user ideas into production prompts, confirms paid generation parameters, runs the video API CLI, and returns playable video URLs or actionable failure details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires WERYAI_API_KEY and sends authenticated requests to WeryAI. <br>
Mitigation: Provide the API key only in a trusted runtime, keep it out of source control, and use isolated or short-lived environments for higher assurance. <br>
Risk: Prompts and any public image URLs are sent to WeryAI during generation. <br>
Mitigation: Avoid sensitive prompts or images, and use only public HTTPS image URLs that are appropriate to share with the service. <br>
Risk: Successful wait runs consume WeryAI credits. <br>
Mitigation: Review the full prompt and parameters in the confirmation table before approving generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/hair-makeover-video) <br>
- [Publisher profile](https://clawhub.ai/user/zoucdr) <br>
- [WeryAI video API endpoint](https://api.weryai.com) <br>
- [WeryAI models endpoint](https://api-growth-agent.weryai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with confirmation tables, shell commands, and parsed JSON API results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return WeryAI video URLs after a paid API call; prompts and public image URLs are sent to WeryAI.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
