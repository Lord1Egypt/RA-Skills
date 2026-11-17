## Description:

Integrates with the Google Forms API through managed OAuth so agents can create forms, add questions, export responses to Excel, and summarize response data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dfaaa](https://clawhub.ai/user/dfaaa)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agents use this skill to create and manage Google Forms, retrieve or summarize responses, and export response data. It is useful when a workflow needs Google Forms automation through the Forms for Google Drive API and a valid GFORMS_API_KEY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Form contents and response exports may be routed through api.gformsfree.com, which can include personal, employee, customer, health, or regulated data.

Mitigation: Use the skill only after confirming that this third-party handling is acceptable for the data involved, and avoid sending regulated or sensitive form data unless the deployment has appropriate approvals.

Risk: The skill requires a GFORMS_API_KEY for authenticated access.

Mitigation: Store the API key only in the environment, never disclose it in user-facing messages, and rotate it from the Forms for Google Drive app if exposure is suspected.

Risk: Exported Excel download links provide access to response data until they expire.

Mitigation: Treat export links as sensitive, share them only with authorized users, and remind users that documented download links expire after 10 minutes.

Risk: Creating or modifying forms can affect live surveys and respondent workflows.

Mitigation: Confirm with the user before creating or modifying forms, collect the survey topic, audience, question count, and preferred question types, and return both responder and editor links after creation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dfaaa/skills/google-forms-with-forms-ios-app)
- [Forms for Google Drive App](https://apps.apple.com/us/app/forms-for-google-drive/id6468928038)
- [Google Forms API Reference](https://developers.google.com/workspace/forms/api/reference/rest)
- [Forms for Google Drive skill API base](https://api.gformsfree.com/skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return Google Forms responder and editor links, natural-language response summaries, and time-limited Excel export download links.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
