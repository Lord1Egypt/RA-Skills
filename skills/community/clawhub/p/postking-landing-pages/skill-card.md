## Description:

Generate, edit, vibe-edit, and publish landing pages on PostKing, including comparison/side pages and custom domains, for launches and campaigns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitsandtea](https://clawhub.ai/user/bitsandtea)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing teams and PostKing users use this skill to create, edit, manage versions for, translate, and publish landing pages and side pages for launches and campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing, unpublishing, deleting, restoring, renaming, or domain-removal actions can change public landing pages, URLs, versions, or custom-domain state.

Mitigation: Confirm the exact page, side page, version, or domain and review the preview or current state before allowing the action.

Risk: AI regeneration and vibe-edit workflows can introduce inaccurate, off-brand, or unintended marketing copy before publication.

Mitigation: Use the propose-review-apply flow, inspect the listed changes or draft preview, and publish only after the accepted edits are confirmed.

Risk: Custom-domain support can register and verify domains but does not attach a verified domain to a landing page through MCP or CLI.

Mitigation: Finish landing-page domain attachment in the PostKing dashboard and avoid using blog-only domain connection tools for landing pages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bitsandtea/skills/postking-landing-pages)
- [PostKing MCP endpoint](https://mcp.postking.app/mcp)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown with MCP tool-call guidance and optional CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes preview or live URLs when PostKing tool responses provide them.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
