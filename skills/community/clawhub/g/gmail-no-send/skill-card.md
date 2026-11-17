## Description:

Read-only Gmail CLI that cannot send email by design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[madebydia](https://clawhub.ai/user/madebydia)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent search and read Gmail, create or update drafts for human review, and archive messages without exposing a send command in the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests Gmail read, compose, and modify permissions, which are broader than the no-send framing may imply.

Mitigation: Install only after reviewing the requested OAuth permissions and confirming they match the intended Gmail workflow.

Risk: The reusable local Gmail token is sensitive if exposed.

Mitigation: Restrict token file permissions, protect or encrypt it at rest, and revoke the token from the Google account if exposure is suspected.

Risk: The no-send property is enforced by the current application code path rather than a platform-level Gmail restriction.

Mitigation: Use a reviewed pinned release or local source review, verify the installed code has no send path, and keep human review as the final step for sending drafts.

## Reference(s):

- [Threat Model](references/threat-model.md)
- [ClawHub Skill Page](https://clawhub.ai/madebydia/skills/gmail-no-send)
- [Project Homepage](https://github.com/meimakes/gmail-no-send)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Google Cloud OAuth credentials and stores token and audit log data locally.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
