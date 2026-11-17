## Description:

nl2ms-ui helps agents generate Midscene automation scripts from natural-language requests for Web, Android, iOS, and PC test workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-xiyou](https://clawhub.ai/user/wu-xiyou)

### License/Terms of Use:


## Use Case:

Developers and QA engineers use this skill to turn natural-language testing goals into Midscene automation scripts for mobile, web, and desktop UI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated automation can accept permission prompts or user agreements without explicit review.

Mitigation: Remove blanket auto-consent instructions and require human review for permission, agreement, or login flows before running generated scripts.

Risk: Generated examples can send messages or otherwise act in live applications.

Mitigation: Run scripts only in controlled test environments with test accounts, test recipients, and non-production session state.

Risk: Browser automation examples may disable the browser sandbox.

Mitigation: Keep the browser sandbox enabled unless an isolated runtime explicitly requires disabling it.

## Reference(s):

- [Midscene API documentation](https://midscenejs.com/api.html)
- [Android YAML examples](references/examples-android-yaml.md)
- [Android TypeScript examples](references/examples-android-ts.md)
- [iOS YAML examples](references/examples-ios-yaml.md)
- [iOS TypeScript examples](references/examples-ios-ts.md)
- [Web YAML examples](references/examples-web-yaml.md)
- [Web TypeScript examples](references/examples-web-ts.md)
- [PC YAML examples](references/examples-pc-yaml.md)
- [PC TypeScript examples](references/examples-pc-ts.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with TypeScript and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated scripts may target Android, iOS, Web, or PC Midscene automation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
