## Description:

Turn any subject into an adorable handmade plush toy or stuffed animal image with fluffy fabric textures, visible stitching, and button eyes via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to generate plush toy and stuffed animal image concepts from text prompts, including commission references, merch mockups, gift ideas, and character or pet plush designs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the user's prompt and API token to an external image service.

Mitigation: Confirm that api.talesofai.com is the intended provider before use, avoid sending sensitive prompts, and use a token appropriate for the task.

Risk: Passing an API token on the command line can expose it through shell history or process listings.

Mitigation: Avoid using real tokens on shared machines or in logged command histories, and rotate the token if exposure is suspected.

Risk: Unpinned npx installation can install a changed package after review.

Mitigation: Prefer a pinned version or ClawHub-managed installation path for reviewed deployments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/omactiengartelle/skills/plush-toy-generator)
- [Neta API Token Setup](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a direct image URL after polling the external image generation service; requires a user-provided Neta API token.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
