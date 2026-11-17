## Description:

Creates vertical reveal shorts that contrast a polished product with a harsh origin, add a one-line verdict, and include timed English captions through WeryAI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and agents use this skill to turn everyday-product origin topics into short vertical WeryAI video prompts with a fixed four-beat reveal structure, timed English captions, and a final video link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted prompt text in the documented shell workflow could execute unintended local commands.

Mitigation: Pass generation JSON without shell interpolation, such as through an argument array, stdin, or a secure temporary file, and review commands before execution.

Risk: Prompts, images, or supply-chain details may be shared with the WeryAI service during generation.

Mitigation: Avoid sending confidential prompts, private images, secrets, or proprietary details unless the user accepts WeryAI processing.

Risk: The skill requires a WERYAI_API_KEY and may consume paid generation credits.

Mitigation: Run only with the required key in an isolated environment and confirm credit-consuming wait or generation requests before submission.

## Reference(s):

- [WeryAI Video API Reference](resources/WERYAI_VIDEO_API.md)
- [ClawHub Skill Page](https://clawhub.ai/zoucdr/skills/hidden-truth-reveal-video-gen)
- [WeryAI Video Tasks API](https://api.weryai.com)
- [WeryAI Models Registry API](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with confirmation tables, inline shell commands, JSON command parameters, and a final video link or error.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY and Node.js 18+; normal operation sends prompts or public image URLs to WeryAI and may consume credits.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
