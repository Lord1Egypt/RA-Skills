## Description:

Generates medical-aesthetic short-video content by extracting key points from doctor interview material, filtering prohibited advertising language, and drafting 30-second scripts for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuan3249](https://clawhub.ai/user/yuan3249)

### License/Terms of Use:

MIT-0

## Use Case:

Medical-aesthetic doctors and content operators use this skill to analyze raw interview transcripts, identify technical talking points, filter medical-advertising prohibited terms, and draft short-video scripts for human compliance review.

### Deployment Geography for Use:

China-oriented; review before adapting to other jurisdictions.

## Known Risks and Mitigations:

Risk: Generated content may include mandatory promotional contact text.

Mitigation: Remove or override promotional footers and contact prompts unless they are explicitly intended and approved for the deployment.

Risk: The workflow may encourage collection of sensitive facial or medical-aesthetic photos through unspecified channels.

Mitigation: Use only a compliant privacy workflow with clear consent, data minimization, access controls, and deletion practices before requesting or processing such materials.

Risk: Medical advertising and platform compliance claims may not be sufficient for every publication context.

Mitigation: Require qualified human review before publishing generated medical or medical-aesthetic content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuan3249/skills/medical-ip-director-free)
- [Publisher profile](https://clawhub.ai/user/yuan3249)
- [README.md](artifact/README.md)
- [30-second short-video example](artifact/examples/short-video-example.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style Chinese analysis notes and short-video scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append promotional contact text in generated content; final medical and advertising compliance review is required.]

## Skill Version(s):

2.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
