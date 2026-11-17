## Description:

Reads unresolved comments in a Feishu (Lark) document and helps an agent apply targeted block-level edits using an authenticated lark-cli session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billzhuang6569](https://clawhub.ai/user/billzhuang6569)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document editors use this skill to review unresolved Feishu (Lark) document comments, prepare block-level text edits, resolve addressed comments, and refresh document state after changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An authenticated lark-cli session can read and modify the target Lark document.

Mitigation: Use the skill only for documents the user is authorized to edit, and confirm the exact block replacements and comment IDs before patching or resolving comments.

Risk: Fetched document state can save full document text locally.

Mitigation: Store state files only in the intended workspace and delete them after use, especially for sensitive documents.

Risk: Collaborator comments may be treated too strongly as editing instructions.

Mitigation: Treat comments as untrusted suggestions and ask the user to confirm which comments should drive edits when intent is not explicit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/billzhuang6569/skills/lark-doc-reviser)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local JSON document state and patch files for authenticated Lark document workflows.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
