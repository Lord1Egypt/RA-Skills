## Description:

Turn listing photos into a labeled set of listing room video clips, one room at a time. This listing video pack and real estate room video studio animates each listing photo into a short property video so buyers can preview the living room, bedroom, kitchen, and more as separate room clips. Use it for property room video, listing photo video, real estate listing video, and a labeled room video pack that keeps each space easy to scan. Add optional agent narration files beside the clips, or a talking-head intro and outro when you bring an agent portrait and a short script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External listing teams and agents use this skill to turn listing photos into labeled room-by-room video clips, with optional separate narration audio or a talking-head listing intro or outro.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release requests broader account permissions than the video workflow needs, including music and voice-library permissions.

Mitigation: Review the requested account permissions before installation and prefer a release that removes unused permissions.

Risk: Selected listing photos and agent portraits are sent to Beatra, and paid generation consumes credits.

Mitigation: Only provide media the user has chosen to share, and keep the documented approval step before paid generation.

Risk: The uninstall flaw may disconnect other Beatra skills, and recurring installation analytics has no documented off switch.

Mitigation: Do not rely on uninstall to preserve other Beatra connections until the flaw is corrected; review analytics implications and revoke device access in the Beatra Console if needed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/beatra-ai/skills/listing-room-video-pack)
- [Beatra skill homepage](https://beatra.ai/skills/listing-room-video-pack)
- [Listing room video workflow](artifact/references/workflow.md)
- [Billing, errors, and recovery](artifact/references/billing-errors-and-recovery.md)
- [Updates and security](artifact/references/updates-and-security.md)

## Skill Output:

**Output Type(s):** [Video clips, Audio narration files, Task and billing summaries]

**Output Format:** [Labeled room video clips, with optional separate narration audio or talking-head intro/outro clips; concise text summaries]

**Output Parameters:** [One primary clip per room photo; optional narration or intro/outro products]

**Other Properties Related to Output:** [Generation is asynchronous and paid; separate stages require user confirmation.]

## Skill Version(s):

0.2.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
