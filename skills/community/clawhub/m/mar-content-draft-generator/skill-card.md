## Description: <br>
Generates new content drafts by analyzing reference content, extracting reusable patterns, gathering user context, and producing multiple draft variations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and content teams use this skill to analyze supplied reference URLs, derive content structure and audience patterns, interview the user for context, and generate three draft variations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reference URL fetching can disclose URLs, page metadata, or request context to external sites, including the FxTwitter service used for Twitter/X links. <br>
Mitigation: Use only public, non-sensitive reference URLs unless the skill is updated to clearly disclose outbound requests and ask for approval before fetching. <br>
Risk: Generated breakdowns, anatomy guides, context notes, meta-prompts, and drafts are saved locally and may preserve user-provided business context. <br>
Mitigation: Avoid entering private campaign details or confidential source material unless local file retention is acceptable for the workspace. <br>
Risk: Drafts are modeled from supplied references and may reproduce unsuitable structure, claims, tone, or audience assumptions. <br>
Mitigation: Review generated drafts for factual accuracy, originality, brand fit, and compliance before publishing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/marjoriebroad/mar-content-draft-generator) <br>
- [Content Deconstructor](references/content-deconstructor.md) <br>
- [Content Anatomy Generator](references/content-anatomy-generator.md) <br>
- [Content Context Generator](references/content-context-generator.md) <br>
- [Meta Prompt Generator](references/meta-prompt-generator.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown files and conversational text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates timestamped content breakdowns, anatomy guides, context requirements, meta-prompts, and draft files; generates exactly three draft variations per run.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
