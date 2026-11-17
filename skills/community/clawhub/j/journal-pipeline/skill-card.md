## Description:

Autonomous journal content pipeline for UniqueStaysUSA that researches keywords, writes editorial content, publishes to Payload CMS, and tracks results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhigh1594](https://clawhub.ai/user/jhigh1594)

### License/Terms of Use:

MIT-0

## Use Case:

External site operators and content teams use this skill to run a seven-phase travel editorial workflow for selecting topics, researching stays, drafting, optimizing, publishing to Payload CMS, and syncing progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish live CMS content.

Mitigation: Use a staging CMS by default, verify the CMS URL before each run, and require manual confirmation before publishing.

Risk: The skill can use API credentials against a Payload CMS.

Mitigation: Use a narrowly scoped API key with only the permissions needed for the intended environment.

Risk: The skill can commit repository changes and continue a publishing loop across sessions.

Mitigation: Require manual confirmation before committing changes or allowing loop continuation.

## Reference(s):

- [Article Templates](references/article-templates.md)
- [Quality Checklist](references/quality-checklist.md)
- [SEO Requirements](references/seo-requirements.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls, files]

**Output Format:** [Markdown drafts, JSON-compatible CMS payloads, API call plans, shell commands, and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May publish live CMS content and update repository tracking files when configured with production access.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
