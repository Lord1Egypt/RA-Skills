## Description:

Jev (typesafe.ai). Use this skill for ANY Jev request — searching and reading data. Whenever a task involves Jev, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use Jev to evaluate text or structured state against typed Noul, Choice, and Score questions, then read the evaluation results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs downloaded code immediately, and automatic skill synchronization may install additional skills.

Mitigation: Install a reviewed, pinned CLI release and disable automatic skill synchronization before use.

Risk: Content sent for evaluation is processed by OOMOL and Jev.

Mitigation: Send only content you intend OOMOL and Jev to process.

## Reference(s):

- [Jev homepage](https://typesafe.ai)
- [Jev API documentation](https://developers.cloudflare.com/ai/models/typesafe/jev/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-jev)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Jev evaluation results as JSON with explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The action payload follows the live Jev connector schema.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
