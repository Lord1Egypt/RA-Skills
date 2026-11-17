## Description:

Generates concise, accessibility-friendly alt text for a publicly reachable image using Alt Text Generator AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators can generate concise, accessibility-friendly alt text for images through their connected Alt Text Generator AI account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI may install or refresh other agent skills during startup without explaining those changes.

Mitigation: Review the CLI installation separately and decide whether it may manage skills across your agents; set OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization.

Risk: The workflow sends a public image URL to the hosted service.

Mitigation: Use only image URLs you intend to share publicly, and account for usage credits.

Risk: The exact remote installer and hosted connector implementation were not verified.

Mitigation: Review the CLI installation and service connection separately before relying on them.

## Reference(s):

- [Alt Text Generator AI](https://alttextgeneratorai.com)
- [Alt Text Generator AI API documentation](https://alttextgeneratorai.com/api-docs)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Generated alt text returned in a JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a publicly reachable image URL, a connected account, and available usage credits.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
