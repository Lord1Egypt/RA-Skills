## Description:

Helps agents turn image briefs into production-ready GPT Image 2.5 Studio jobs with exact-text manifests, reference-image role contracts, controlled edit rounds, and visual QA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[julianreed888](https://clawhub.ai/user/julianreed888)

### License/Terms of Use:

MIT-0

## Use Case:

Creative operators, designers, marketers, and agent users use this skill to prepare reviewable GPTImage-2-5.com Studio jobs for posters, packaging, ecommerce images, UI mockups, storyboards, localized creatives, and precise image edits. It helps capture prompt, ratio, resolution, reference-role, upload, cost-confirmation, and visual QA decisions before and after generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to a third-party web Studio where uploads, account access, and credit use occur outside OpenAI.

Mitigation: Confirm the signed-in account, selected files, prompt, settings, and displayed cost before any upload or generation.

Risk: Reference images or source assets could be used without the user's authorization.

Mitigation: Use only files and URLs the user is authorized to provide, and assign explicit roles to each reference before upload.

Risk: Generated exact text can be incorrect or misleading, especially for legal, medical, financial, or safety-critical copy.

Mitigation: Verify required text character-for-character at delivery size and move critical copy to a deterministic layout tool when generation cannot meet the manifest.

Risk: Undocumented service behavior could lead an agent to invent unsupported API, authentication, ratio, resolution, or pricing details.

Mitigation: Use only the visible Studio controls and current on-screen cost, and do not claim API support unless current public documentation exists.

## Reference(s):

- [GPTImage-2-5.com homepage](https://gptimage-2-5.com/)
- [GPT Image 2.5 Studio](https://gptimage-2-5.com/studio)
- [Production contracts](references/production-contracts.md)
- [ClawHub skill page](https://clawhub.ai/julianreed888/skills/gpt-image-2-5-production-studio)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files]

**Output Format:** [Markdown production job cards, prompts, QA checklists, edit ledgers, and optional generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before file uploads or credit-consuming generation.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
