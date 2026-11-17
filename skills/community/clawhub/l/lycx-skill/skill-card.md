## Description:

Summarizes long texts, articles, conversations, meeting notes, and reports by extracting concise summaries and key points without altering the original meaning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yrqian](https://clawhub.ai/user/yrqian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to summarize provided Chinese text, documents, meetings, and reports into concise summaries and key-point lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Chinese trigger phrases may route ordinary summarization requests to this skill unexpectedly.

Mitigation: Review trigger scope before deployment and limit activation to intended summarization workflows.

Risk: The included implementation is placeholder-style summarization rather than a complete model integration.

Mitigation: Connect it to an approved summarization model or service and test output quality before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yrqian/skills/lycx-skill)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Structured text with summary, key_points, original_length, and output_length fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-only summarization output; length mode can be short, normal, or detail]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
