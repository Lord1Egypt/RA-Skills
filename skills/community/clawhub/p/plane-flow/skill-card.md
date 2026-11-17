## Description:

Plane Flow lets agents operate a local or self-hosted Plane workspace to read and update projects, issues, states, labels, members, assignments, priorities, comments, cycles, and project summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uncooldog](https://clawhub.ai/user/uncooldog)

### License/Terms of Use:

MIT-0

## Use Case:

Product, project, and operations teams use Plane Flow after administrator setup to manage Plane backlogs, convert meeting notes or action items into issues, triage work, assign owners, manage cycles, and summarize project progress. Administrators and technical owners use the bundled helpers to configure and validate the Plane connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local file upload features can expose sensitive files if untrusted notes or inline image directives are converted directly into Plane issues.

Mitigation: Review every attachment path before execution and do not allow inline [image: path] directives unless each path was explicitly approved by a human.

Risk: The skill can access sensitive Plane data through the configured Plane API token.

Mitigation: Use a least-privileged Plane API token, require HTTPS Plane URLs, and connect only to a trusted administrator-configured Plane instance.

Risk: Untrusted notes may introduce misleading or inappropriate issue descriptions, comments, or project updates.

Mitigation: Review generated Plane changes before write operations when the source text is untrusted or the requested action is ambiguous.

## Reference(s):

- [Plane Flow CLI Usage](artifact/references/cli-usage.md)
- [Plane Flow on ClawHub](https://clawhub.ai/uncooldog/skills/plane-flow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and JSON-formatted CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires administrator-provided Plane environment variables; may upload explicitly selected local files as Plane issue attachments.]

## Skill Version(s):

0.1.3 (source: server release evidence and README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
