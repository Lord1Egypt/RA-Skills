## Description:

Generate a comprehensive influencer vetting report from a creator profile URL or video URLs using Memories.ai video intelligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnshenopeninterx](https://clawhub.ai/user/shawnshenopeninterx)

### License/Terms of Use:


## Use Case:

Marketing, brand safety, and creator partnership teams use this skill to vet influencers by analyzing recent creator videos, scoring content quality and brand safety, and generating a concise report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process unrelated videos from a user's Memories.ai library.

Mitigation: Use isolated Memories.ai API keys or libraries for the specific creator or job, and verify the video set before analysis.

Risk: Creator URLs, video URLs, transcripts, visual descriptions, and metadata may be sent to Memories.ai services and demo.memories-ai.org.

Mitigation: Avoid confidential campaign research unless that data sharing is approved and result retrieval is documented or secured.

Risk: Results are retrieved through an under-disclosed endpoint.

Mitigation: Review and document result retrieval behavior before relying on outputs for creator or campaign decisions.

## Reference(s):

- [Influencer Vetting Report Format](artifact/references/report-format.md)
- [Influencer Report on ClawHub](https://clawhub.ai/shawnshenopeninterx/skills/influencer-report)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown report with tables, scores, recommendations, and optional saved file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Memories.ai API keys; may process creator profile URLs, video URLs, transcripts, visual descriptions, and metadata.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
