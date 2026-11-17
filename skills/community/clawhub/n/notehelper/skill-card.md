## Description:

Saves user-approved articles or links to the NoteHelper cloud notebook, searches saved items, and guides API-key setup when explicitly requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[notesynchelper](https://clawhub.ai/user/notesynchelper)

### License/Terms of Use:

MIT-0

## Use Case:

People who use NoteHelper can ask an agent to save an article or link to their cloud notebook, search saved notes, or get help setting up the NoteHelper key. The skill is intended only for explicit NoteHelper requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-selected article content and search terms are sent to NoteHelper's cloud service.

Mitigation: Send only content and terms the user has chosen to share, and follow the skill's confirmation step for uploads.

Risk: The API key grants access to the user's NoteHelper account.

Mitigation: Keep the key private and prefer OpenClaw SecretRef configuration.

Risk: Link processing can incur points charges.

Mitigation: Explain applicable charges and obtain confirmation before submitting links.

## Reference(s):

- [NoteHelper developer integration](https://www.bijitongbu.site/tutorials/developer-integration/)
- [NoteHelper points and pricing](https://www.bijitongbu.site/tutorials/points-explained/)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown notes and plain-text status or search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include saved-note summaries, source links, task status, or search results.]

## Skill Version(s):

1.2.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
