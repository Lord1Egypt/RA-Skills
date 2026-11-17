## Description:

Kalodata (kalodata.com). Use this skill for ANY Kalodata request — searching and reading data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users with an OOMOL-connected Kalodata account can ask an agent to search TikTok Shop categories and retrieve analytics for creators, products, shops, videos, and livestreams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute downloaded code that has not been verified and may introduce broader changes across agents.

Mitigation: Review setup before enabling the skill, install a verified oo CLI release yourself, and decide whether to allow automatic synchronization across agents.

Risk: Requests run through the connected Kalodata account, and some requests consume credits.

Mitigation: Review the action before running it and check the account's credit balance when cost matters.

## Reference(s):

- [Kalodata Open Center API Documentation](https://www.kalodata.com/open-center/docs)
- [Kalodata](https://www.kalodata.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Kalodata skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-kalodata)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON]

**Output Format:** [Natural-language summaries and structured JSON from Kalodata actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some review-insight requests may consume Kalodata credits; signed image and video URLs are temporary.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
