## Description:

Guides agents through structure-preserving rerenders or continuations from an authorized public reference video while preserving shot timing, framing, spatial layout, and motion cues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ofoxai](https://clawhub.ai/user/ofoxai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to turn rough previs, blockout, wireframe, clay, or animatic clips into finished visual treatments, or to create standalone continuations from a reference clip's final state. It helps agents collect required inputs, prepare prompts, run dry-run quotes, request spend approval, and review generated video artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an Ofox API key and a separate video execution dependency.

Mitigation: Verify trust in the Ofox skill source and the ofox-video-core dependency before installation, and provide OFOX_API_KEY only through the environment.

Risk: The workflow uses public or externally reachable video URLs and may transform footage.

Mitigation: Use only video URLs the user is authorized to transform and avoid exposing signed URLs or payloads containing them in chat or logs.

Risk: Real generation may incur paid Ofox usage.

Mitigation: Review the dry-run quote and require explicit approval before submitting a paid generation job.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ofoxai/skills/previs-rerender)
- [Skill homepage](https://github.com/ofoxai/skills/tree/main/skills/previs-rerender)
- [Ofox API keys](https://app.ofox.ai)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and structured prompt guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OFOX_API_KEY, a public video URL the user is authorized to transform, dry-run quote review, and explicit approval before paid generation.]

## Skill Version(s):

1.0.0 (source: server evidence, frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
