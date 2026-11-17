## Description:

Web-first skill for working with Proof documents via proofeditor.ai. Use when a Proof URL is shared, when creating collaborative docs in Proof, or when the user wants comments, suggestions, and provenance tracked in a shared doc.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dshipper](https://clawhub.ai/user/dshipper)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to join, create, read, edit, comment on, and suggest changes in shared Proof Markdown documents when a user provides or requests a Proof workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proof document URLs and share tokens can grant access to shared document contents.

Mitigation: Use the skill only with Proof links the user intentionally shares, and avoid providing sensitive Proof links unless agent access and editing are intended.

Risk: Document contents and agent presence or activity are sent to proofeditor.ai during use.

Mitigation: Confirm the user is comfortable with the hosted Proof workflow before creating, joining, or editing sensitive documents.

Risk: Edits, comments, suggestions, or rewrites can change collaborative Markdown documents.

Mitigation: Read current document state before editing, include the required AI authorship marker, and use suggestion or comment workflows when human review is expected.

## Reference(s):

- [Proof homepage](https://www.proofeditor.ai)
- [Proof agent discovery JSON](https://www.proofeditor.ai/.well-known/agent.json)
- [Proof agent docs](https://www.proofeditor.ai/agent-docs)
- [Proof agent setup](https://www.proofeditor.ai/agent-setup)
- [ClawHub skill page](https://clawhub.ai/dshipper/skills/proofeditor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown guidance with curl examples and JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, read, edit, comment on, or suggest changes in hosted Proof documents when the user provides or requests a Proof workflow.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
