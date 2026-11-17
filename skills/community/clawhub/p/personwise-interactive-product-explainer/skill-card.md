## Description:

Creates a source-grounded, askable digital-human explainer for a SaaS or software product page using verified product materials and PersonWise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, product, and growth teams use this skill to turn verified product materials into an interactive PersonWise website explainer that visitors can question, embed, or share. It is intended for product launches, product pages, help centers, and sales follow-up when current source material is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or update a user-level PersonWise CLI and uses browser OAuth.

Mitigation: Install only when the user explicitly approves and trusts PersonWise; do not request or handle passwords, tokens, callback URLs, cookies, or other secrets.

Risk: The update workflow may rely on command text returned by the service or CLI.

Mitigation: Review any requested update command carefully before approval; prefer fixed, validated update metadata when available.

Risk: Selected product materials may be uploaded to the PersonWise service and a course credit may be consumed.

Mitigation: Use only materials the user selected or authorized, keep the run ledger secret-free, and rely on the existing credit authorization for normal course creation.

Risk: A product explainer could include unsupported product claims or invented UI details.

Mitigation: Build a claim ledger from current authoritative sources, audit outline and script content against it, and remove or qualify unsupported claims.

## Reference(s):

- [Product grounding guidance](references/product-grounding.md)
- [PersonWise CLI workflow](references/workflow.md)
- [ClawHub skill page](https://clawhub.ai/personwiseai/skills/personwise-interactive-product-explainer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create bounded JSON input files for the PersonWise CLI and returns course/run IDs, review status, and the final access URL only when playability is proven.]

## Skill Version(s):

2.1.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
