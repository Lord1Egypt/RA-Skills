## Description:

Generate vertical life-hack and gadget demo shorts with WeryAI, using a problem-tool-payoff structure for scenes such as stains, food prep, storage, quick fixes, and product demos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create short vertical life-hack or gadget demonstration videos from a brief, optional public HTTPS image inputs, and confirmed WeryAI generation parameters. The skill expands concise ideas into full English production prompts, submits them through a Node.js helper, and returns playable video URLs or clear API errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires WERYAI_API_KEY and sends prompts plus any public image URLs to WeryAI.

Mitigation: Install only when WeryAI use is intended, keep the API key secret, and run generation in a short-lived or isolated environment when higher assurance is needed.

Risk: Successful wait runs consume paid WeryAI credits, and repeated runs create additional paid tasks.

Mitigation: Review and confirm the full expanded prompt and generation parameters before each API submission.

Risk: An artifact example shows generate_audio true even though the documented default is audio off.

Mitigation: Check generate_audio explicitly in the pre-submit confirmation table and align the submitted JSON with the confirmed value.

Risk: Invalid model, duration, aspect ratio, resolution, or image URL inputs can cause WeryAI API failures.

Mitigation: Use the documented allowed parameter sets, omit unsupported resolution fields, and require public HTTPS image URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/life-hack-video)
- [Publisher profile](https://clawhub.ai/user/zoucdr)
- [WeryAI video generation API host](https://api.weryai.com)
- [WeryAI model registry API host](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with confirmation tables, inline shell commands, and JSON API results containing task status, video URLs, or error details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, WeryAI network access, and public HTTPS image URLs for image-to-video inputs.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
