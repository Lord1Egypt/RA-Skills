## Description:

The habits every Phantra skill assumes, loaded before any writing tool: reuse what the person has, hold every scene to a photo, quote before anything costs, wait for the person's yes before anything spends, and never overwrite. Use when work on the connector starts, before the first `write_scene`, `create_project` or `add_element`, or when unsure what a tool spends or changes. NOT for one job's steps: a scene (write-scene), a render (price-and-render) or credits (credits-and-limits).

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeropage-onryo](https://clawhub.ai/user/zeropage-onryo)

### License/Terms of Use:

MIT-0

## Use Case:

People using the Phantra studio connector can use this guidance to reuse existing projects and media, prepare scenes with photo references, and manage credit spending and edits with explicit consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media generation and effect actions can spend credits.

Mitigation: Show the tool's quote and wait for the person's explicit yes before spending; do not approve twice for one yes.

Risk: Writing to an existing scene replaces its text.

Mitigation: Show the complete replacement text and get the person's yes before calling write_scene with a scene_id.

Risk: The skill can access connected studio projects, chat, and media, while the connector implementation and its claimed pricing, token, and copy protections were not available for verification.

Mitigation: Review the relevant workspace content before acting, use tool responses to confirm costs and effects, and treat the connector protections as unverified.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zeropage-onryo/skills/phantra-ai-phantra-ai-use)
- [Publisher profile](https://clawhub.ai/user/zeropage-onryo)

## Skill Output:

**Output Type(s):** [Guidance, Tool calls]

**Output Format:** [Natural-language guidance and structured tool call arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions depend on the user's workspace and explicit approval; paid media actions require a quote and consent.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
