## Description:

Delegates to the Gemini CLI

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to route suitable tasks to the Gemini CLI for large-context analysis, batch processing, summarization, or pattern extraction when Gemini is installed and authenticated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected source files are sent to Google when included in a Gemini request.

Mitigation: Review the included files and confirm that external processing is allowed by your data-sharing rules before delegation.

Risk: A selected Gemini model or account may not be the one intended for the task.

Mitigation: Check the selected model and authenticated account before sending a request.

Risk: The security scan was partial because a referenced path could not be resolved.

Mitigation: Review the skill and its referenced files before installation or use.

## Reference(s):

- [Night Market Conjure project](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)
- [Gemini API model deprecations](https://ai.google.dev/gemini-api/docs/deprecations)
- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with shell command examples; delegated responses can be saved as Markdown or requested in JSON format.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegated output depends on the selected task and Gemini CLI output format.]

## Skill Version(s):

1.10.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
