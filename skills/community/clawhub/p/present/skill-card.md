## Description:

Authors a narrated presentation and publishes it to a shareable watch URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bisque.cloud](https://clawhub.ai/user/bisque.cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create HTML-based narrated presentations, check narration plans, synthesize local voice audio, and publish the result to a Bisque watch URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to run remote installer scripts for Bisque Voice.

Mitigation: Review the installer path first; prefer downloading a versioned installer, verifying its checksum or signature, and running it only after inspection.

Risk: Login stores an API key locally and publishing sends selected presentation files and assets to Bisque.

Mitigation: Use the intended account and visibility, avoid private material in presentation context, and review the local Bisque configuration before publishing.

Risk: The login and publish flow may send basic device-identifying information to the configured Bisque API endpoint.

Mitigation: Confirm the configured endpoint and disclose this behavior to users before they authenticate or publish.

## Reference(s):

- [Present skill page](https://clawhub.ai/bisque.cloud/skills/present)
- [Bisque Cloud](https://bisque.cloud)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, shell commands, configuration files, and a published watch URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce index.html, context.md, design.md, local asset files, narration plans, and publish status messages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
