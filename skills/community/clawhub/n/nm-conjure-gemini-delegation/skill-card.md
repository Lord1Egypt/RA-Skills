## Description:

Delegates to the Gemini CLI

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill after delegation-core selects Gemini, or when a task benefits from Gemini's large context window. It supports batch processing, summarization, and pattern extraction through the Gemini CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that local files may be sent to Gemini without a privacy warning, and that a specific external model is selected.

Mitigation: Before delegation, review the included file scope and chosen model, and confirm that sending those contents to Gemini is appropriate. The scan was partial because a referenced local path could not be resolved.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-conjure-gemini-delegation)
- [Conjure plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)
- [Gemini API deprecations](https://ai.google.dev/gemini-api/docs/deprecations)
- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Delegation prompts and responses; saved Markdown files, with optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegated output is saved under a timestamped delegations/gemini/ path; prompts can include selected local files and specify a model.]

## Skill Version(s):

1.10.3 (source: skill frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
