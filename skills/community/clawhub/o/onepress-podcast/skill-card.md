## Description:

Drafts an editable podcast script from a topic or source material, then can use OnePress to voice and mix an MP3 episode with the user's approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[getonepress](https://clawhub.ai/user/getonepress)

### License/Terms of Use:

MIT

## Use Case:

People creating narrated briefings or podcast episodes from topics, documents, or slide decks can review and edit a local script before choosing whether to produce audio through OnePress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source documents, scripts, and voice samples selected for audio generation are uploaded for OnePress cloud processing.

Mitigation: Review the script and source material before approving an upload; avoid sending content that should not leave the local environment.

Risk: A stored OnePress API key grants ongoing account access.

Mitigation: Keep the key in a secret store rather than chat or logs, and revoke it in account settings when access is no longer needed.

Risk: Voice cloning can reproduce a person's voice from an uploaded sample.

Mitigation: Use only voice samples you are authorized to use and manage cloned voices in the OnePress account.

## Reference(s):

- [OnePress Podcast on ClawHub](https://clawhub.ai/getonepress/skills/onepress-podcast)
- [OnePress](https://www.getonepress.com)

## Skill Output:

**Output Type(s):** [Markdown script, MP3 audio file, Text guidance]

**Output Format:** [Editable Markdown script and, if requested, a downloaded MP3 with a text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audio generation requires user approval and a OnePress account connection; the script can be drafted locally without one.]

## Skill Version(s):

1.2.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
