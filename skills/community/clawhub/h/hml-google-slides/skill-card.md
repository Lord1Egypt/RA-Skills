## Description:

Create, edit, and export Google Slides presentations for workflows that need new decks, slide updates, content inspection, PDF/PPTX export, or deck creation from scratch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nethunter](https://clawhub.ai/user/nethunter)

### License/Terms of Use:


## Use Case:

Agents supporting HML slide workflows use this skill to create, inspect, update, comment-manage, and export Google Slides presentations. It is intended for users who already have a working gog Google account authentication setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Google OAuth tokens unsafely and stores an exported token at /tmp/gog_slides_token.json.

Mitigation: Use only an explicitly chosen Google account, revoke and reissue credentials if the temporary token path may already exist, and review token handling before installation.

Risk: The documented re-auth command requests broad Google service access beyond normal Slides work.

Mitigation: Avoid the broad re-auth command unless the requested scopes are approved for the deployment account.

Risk: Batch update requests can make broad or destructive presentation changes.

Mitigation: Review generated batch request JSON before execution and operate on a copy when changing important presentations.

Risk: Comment resolution writes to Google Drive comment threads.

Mitigation: Confirm the target presentation and comment ID before resolving comments or posting replies.

## Reference(s):

- [Google Slides Batch Request Patterns](artifact/references/batch_requests.md)
- [Google Slides API batchUpdate reference](https://developers.google.com/slides/api/reference/rest/v1/presentations/batchUpdate)
- [ClawHub skill page](https://clawhub.ai/nethunter/skills/hml-google-slides)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON request examples, and Python helper command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation, editing, comment resolution, and PDF/PPTX export of Google Slides presentations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
