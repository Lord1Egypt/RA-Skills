## Description:

Hot dog or not? Classify food photos and battle Nemotron.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mishafyi](https://clawhub.ai/user/mishafyi)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to classify food photos as hot dogs or not hot dogs, compare the result against Nemotron in a blind battle, and report the battle result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted photos and generated details are sent to api.hotdogornot.xyz without an explicit consent step.

Mitigation: Require explicit user consent before upload and avoid private images, faces, documents, location-sensitive scenes, or regulated data.

Risk: The skill includes a bundled bearer token for the third-party service.

Mitigation: Remove the embedded bearer token and use documented, secure credential handling before release.

Risk: The skill relies on shell-based request construction for image upload and voting.

Mitigation: Use safer non-shell request construction or tightly validate substituted values before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mishafyi/skills/hotdog)
- [Publisher Profile](https://clawhub.ai/user/mishafyi)
- [Hot Dog Battle](https://hotdogornot.xyz/battle)
- [Battle API Round Endpoint](https://api.hotdogornot.xyz/api/arena/round)
- [Battle API Vote Endpoint](https://api.hotdogornot.xyz/api/arena/vote/submit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style text with generated food-description analysis and battle results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute curl requests that upload the submitted image and generated details to a third-party battle service.]

## Skill Version(s):

10.1.1 (source: server release evidence; artifact frontmatter says 10.0.0 and artifact _meta.json says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
