## Description:

Generates influencer vetting reports from creator profile or video URLs with Memories.ai video analysis, brand safety checks, content quality scoring, and engagement metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnshenopeninterx](https://clawhub.ai/user/shawnshenopeninterx)

### License/Terms of Use:


## Use Case:

Developers, marketing teams, and creator partnership reviewers use this skill to vet influencers by analyzing recent or supplied videos and producing a concise brand safety and content quality report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Profile mode can include unrelated videos from the Memories.ai account library.

Mitigation: Prefer direct video URLs or use a dedicated Memories.ai library/account for one creator at a time, then verify every report video belongs to the intended influencer.

Risk: Creator profile or video URLs and derived transcript or metadata content are sent to Memories.ai services.

Mitigation: Use the skill only when that data sharing is acceptable for the creator, brand, and account policy.

Risk: Automated brand safety and approval scores can affect business decisions.

Mitigation: Treat the report as review support and require human verification before approving, rejecting, or acting on an influencer.

## Reference(s):

- [Influencer Vetting Report Format](references/report-format.md)
- [ClawHub Skill Page](https://clawhub.ai/shawnshenopeninterx/skills/memories-influencer-report)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration]

**Output Format:** [Markdown influencer vetting report with terminal status text and optional report file output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MEMORIES_V1_API_KEY and MEMORIES_API_KEY; profile mode may include videos retrieved from the Memories.ai account library.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
