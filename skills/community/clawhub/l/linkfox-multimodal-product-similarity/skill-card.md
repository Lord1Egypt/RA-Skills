## Description:

Analyzes an existing product list with multimodal image comparison to group visually similar products and identify same-style or cross-brand lookalike items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and commerce analysts use this skill to post-process product search or recommendation results, cluster visually similar product images, and review cross-brand lookalike groups. It requires a preceding product list and does not fetch product data on its own.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product lists, image URLs, user prompts, and related metadata may be sent to LinkFox services for similarity analysis.

Mitigation: Use the skill only with data approved for LinkFox processing, and avoid submitting sensitive or restricted product data.

Risk: The onboarding flow can involve phone/SMS login, API key retrieval, plan selection, and payment actions.

Mitigation: Run onboarding or billing commands only when the user explicitly intends account or payment activity, and review the command output before continuing.

Risk: API keys can be exposed if copied into shell startup files, transcripts, or logs.

Mitigation: Store credentials through the user's approved secret-management process and avoid printing or persisting keys in shared logs.

Risk: Similarity calls consume LinkFox compute credits and may create unexpected cost if repeated.

Mitigation: Confirm cost-sensitive runs with the user, reuse the documented cache when appropriate, and avoid automatic retries with changed parameters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-multimodal-product-similarity)
- [Publisher profile](https://clawhub.ai/user/linkfox-ai)
- [API reference](references/api.md)
- [Onboarding and billing reference](references/onboarding.md)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON analysis results with Markdown-facing summaries, product tables, saved result files, and shell commands for API calls or onboarding when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Groups include product identifiers, brands, image URLs, grouping reasons, analysis totals, similarity threshold, timestamps, and cost token counts; large responses are saved locally with summarized stdout by default.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
