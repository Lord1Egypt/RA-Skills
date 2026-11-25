## Description:

Use SocialScrape to retrieve profile details, recent posts, video transcripts, and team credit balances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve SocialScrape profile details, recent posts, video transcripts, and account credit data through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports that setup runs a downloaded installer and starts a separate CLI login flow that are not clearly connected to the skill's stated purpose; its verdict is suspicious.

Mitigation: Consider the suspicious verdict before installing. Review the setup instructions and downloaded installer, and proceed only when the requested account privileges and separate authentication flow are understood.

## Reference(s):

- [SocialScrape homepage](https://socialscrape.dev)
- [SocialScrape API documentation](https://socialscrape.dev/docs)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-socialscrape)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON connector responses presented as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas define request fields; the listed actions retrieve profile, post, transcript, or credit data.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
