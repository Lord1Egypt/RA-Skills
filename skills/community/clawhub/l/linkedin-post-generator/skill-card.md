## Description:

AI-powered LinkedIn post generator for professionals that creates posts, thought leadership content, and career updates using the Sloan agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icepopma](https://clawhub.ai/user/icepopma)

### License/Terms of Use:

MIT

## Use Case:

Professionals, thought leaders, and job seekers use this skill to draft LinkedIn posts for career updates, announcements, celebrations, and thought leadership.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review verdict is suspicious because the paid skill includes an embedded payment merchant key and has supply-chain and scoping issues.

Mitigation: Install only if paid networked behavior is acceptable; the publisher should remove and rotate the embedded merchant key, pin reviewed dependency versions, regenerate the lockfile from HTTPS sources, and fix the syntax error before users rely on it.

Risk: Normal use charges 0.002 USDT per generation through SkillPay before content generation.

Mitigation: Confirm payment behavior and user consent before use; use the documented test mode only for evaluation.

Risk: The skill contacts SkillPay and a local OpenClaw/Sloan agent during execution.

Mitigation: Run it only in environments where those external and local agent calls are expected and authorized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/icepopma/skills/linkedin-post-generator)
- [Publisher profile](https://clawhub.ai/user/icepopma)
- [GitHub support link from artifact](https://github.com/icepopma/linkedin-post-generator)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Console text containing generated LinkedIn post content and generation metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posts are constrained by the artifact to a maximum of 3000 characters.]

## Skill Version(s):

1.0.7 (source: server release metadata and SKILL.md frontmatter; package.json shows 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
