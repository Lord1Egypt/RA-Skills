## Description:

Daily-scheduled AI news tracker that collects updates from 80+ AI entities across six sources and generates scored, deduplicated Markdown reports for unattended daily runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[octo-patch](https://clawhub.ai/user/octo-patch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use MorningAI to automate daily monitoring of AI product, model, benchmark, and funding updates, producing date-stamped reports with optional digests and infographics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installed startup hook automatically executes workspace or user MorningAI configuration files as shell code.

Mitigation: Review before installing, remove or change the SessionStart hook in untrusted repositories, and treat configuration files as trusted local inputs only.

Risk: Optional API keys are read from local configuration for GitHub and image-generation providers.

Mitigation: Store only the needed keys, restrict token scopes, and verify that keys are sent only to their respective services.

Risk: Generated news reports can include incorrect or misleading claims if source material is weak or unverified.

Mitigation: Require traceable source URLs, cross-check high-score items, and review reports before publication or redistribution.

## Reference(s):

- [MorningAI ClawHub Listing](https://clawhub.ai/octo-patch/skills/morning-ai)
- [MorningAI Homepage](https://github.com/octo-patch/MorningAI)
- [Infographic Style Reference](docs/styles.md)
- [Tracking List Specification](skills/tracking-list/SKILL.md)
- [Message Digest Specification](skills/gen-message/SKILL.md)
- [Social Content Specification](skills/gen-social/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown reports, JSON collection data, optional Markdown digests, and optional image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Date-stamped, idempotent outputs; optional API keys can improve GitHub rate limits and enable image generation.]

## Skill Version(s):

1.2.5 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
