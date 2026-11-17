## Description:

Accepts Xiaoyuzhou or Ximalaya episode links and produces timestamped, speaker-labeled transcripts with in-depth summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Podcast listeners use the skill to turn individual Xiaoyuzhou or Ximalaya episodes into timestamped transcripts, speaker-organized notes, and structured summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions ask users to paste a full Cue API key into chat, which can expose the credential.

Mitigation: Configure the key locally through CUE_API_KEY or a user-only configuration file; do not paste it into chat, restrict file access, and rotate any key already shared.

Risk: Short-link redirects and polling behavior need validation before processing.

Mitigation: Validate the final destination of short links and correct the polling limits before use.

Risk: Podcast links and processing are sent to Cue's remote service, whose retention and cleanup behavior is not independently verified in the supplied security evidence.

Mitigation: Check Cue's retention practices before sending sensitive material.

## Reference(s):

- [Cue Omni Reader online experience](https://cuecue.cn/hub/omni-reader)
- [Cue Omni Reader remote endpoint](https://mcp.cuecue.cn/api/omni-reader/mcp/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown transcript and structured summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcripts are segmented with timestamps and speaker labels; summaries organize themes, viewpoints, quotations, and mentioned resources.]

## Skill Version(s):

1.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
