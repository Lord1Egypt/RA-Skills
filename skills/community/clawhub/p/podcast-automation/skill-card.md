## Description:

Automates a podcast workflow for downloading audio, transcribing it locally, playing episodes on Sonos, and archiving notes to Feishu Wiki.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and podcast operators use this skill to fetch podcast audio, create local Whisper transcripts, control Sonos playback, and archive podcast notes into a Feishu Wiki workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses unpinned third-party tools for transcription and Sonos control.

Mitigation: Install and run it only in environments where unpinned dependencies are acceptable, and review installed tool versions before operational use.

Risk: Podcast transcripts are uploaded to a third-party Feishu workspace during archiving.

Mitigation: Verify the target Wiki space before upload and keep FEISHU_APP_SECRET scoped, protected, and rotated.

Risk: Sonos playback can affect the wrong speaker or play at an unintended volume.

Mitigation: Confirm the target speaker name and volume before issuing playback commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/podcast-automation)
- [archive-to-wiki.sh](references/scripts/archive-to-wiki.sh)
- [sonoscli module](https://github.com/steipete/sonoscli)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu Wiki nodes API](https://open.feishu.cn/open-apis/wiki/v2/spaces/$SPACE_ID/nodes)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command-oriented workflow guidance for podcast download, transcription, Sonos playback, and Feishu Wiki archiving.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
