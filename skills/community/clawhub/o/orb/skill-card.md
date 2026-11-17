## Description:

Create and share rich interactive artifacts, including webpages, Markdown documents, and flowcharts, as hosted links from AI conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saibhaskardevatha](https://clawhub.ai/user/saibhaskardevatha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use Orb to create, update, list, and share hosted webpages, Markdown documents, and Mermaid flowcharts from AI conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Artifact content is sent to the hosted Orb service.

Mitigation: Use the skill only for content the user is authorized to send to Orb, and review sensitive material before any API call.

Risk: The skill asks agents to persist ORB_API_KEY in local agent or shell configuration files.

Mitigation: Prefer a session-scoped environment variable or secure secret manager unless the user explicitly approves persistent plaintext storage.

Risk: Hosted artifact links may expose generated content to unintended viewers if shared broadly.

Mitigation: Return only the intended hosted link and verify the generated artifact content before sharing it further.

## Reference(s):

- [ClawHub Orb skill page](https://clawhub.ai/saibhaskardevatha/skills/orb)
- [Orb homepage](https://byorb.app)
- [Orb API endpoint](https://api.byorb.app/v1)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with hosted links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces hosted artifact links and may send artifact content to the Orb API using ORB_API_KEY.]

## Skill Version(s):

1.0.0 (source: release evidence; artifact metadata version 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
