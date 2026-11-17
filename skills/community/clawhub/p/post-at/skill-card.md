## Description:

Manage Austrian Post (post.at) deliveries - list packages, check delivery status, set delivery place preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krausefx](https://clawhub.ai/user/krausefx)

### License/Terms of Use:


## Use Case:

External users and automation-focused developers use this skill to manage Austrian Post deliveries, inspect package status and delivery details, and prepare post-at CLI commands for delivery-place preferences.

### Deployment Geography for Use:

Global, for Austrian Post (post.at) account workflows.

## Known Risks and Mitigations:

Risk: Post.at account credentials may be exposed if users place passwords directly in command-line flags or logs.

Mitigation: Prefer POST_AT_USERNAME and POST_AT_PASSWORD environment variables or an interactive secret mechanism, and avoid storing credentials in shell history or shared scripts.

Risk: Delivery-place preference commands may change where a package is delivered.

Mitigation: Review the tracking number, selected place option, and description before running routing commands, especially in scripts that process multiple deliveries.

Risk: Session tokens expire and not all deliveries support Wunschplatz redirection or package pictures.

Mitigation: Handle reauthentication and missing fields in automation, and verify CLI output before relying on it for downstream actions.

## Reference(s):

- [Post.at Tracking ClawHub page](https://clawhub.ai/krausefx/skills/post-at)
- [post-at-cli homepage](https://github.com/krausefx/post-at-cli)
- [krausefx ClawHub profile](https://clawhub.ai/user/krausefx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON CLI output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance assumes the post-at CLI and Node.js are available, with post.at credentials supplied by environment variables or an interactive secret mechanism.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
