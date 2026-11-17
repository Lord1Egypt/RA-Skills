## Description:

Converts local video files or public video links into cleaned transcripts and prompt-guided outputs such as summaries, meeting notes, highlights, translations, and platform-specific copy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, and developers use this skill to turn a single video or prior task into readable text and derivative content for summaries, meeting notes, course breakdowns, highlights, translation, and social copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected video content may be sent to GuaiKei or cloud storage for processing.

Mitigation: Do not process sensitive meetings, regulated data, confidential interviews, or private media unless the user has approval and accepts the provider's handling terms.

Risk: Network destinations, retention behavior, and token-error messaging are not consistently disclosed.

Mitigation: Review the provider's current retention and service disclosures before deployment, and avoid using production or privileged tokens in shared environments.

Risk: The skill may store a last-task ID and temporary downloads locally for reuse or cleanup.

Mitigation: Use it in a workspace where temporary files and task identifiers can be cleared after processing, especially on shared machines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-video-copy)
- [engheng-art publisher profile](https://clawhub.ai/user/engheng-art)
- [GuaiKei homepage](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown with shell command examples and environment configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; processes one video file, public video link, or prior task at a time.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact frontmatter and package.json report 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
