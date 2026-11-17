## Description:

Collects news images for AI technology daily articles from official or trusted sources, with watermark checks, quality checks, and relevance validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lunadelo](https://clawhub.ai/user/lunadelo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to find, download, optimize, and review article images for AI technology news posts. It is intended to reduce random image use by preferring official sources and applying basic watermark, quality, and relevance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads images over the network and the security review warns that downloaded images should be treated as unverified.

Mitigation: Review downloaded files and their sources before publication, and constrain network access when running the skill.

Risk: The security review says the skill overstates its whitelist, watermark, and relevance checks.

Mitigation: Do not rely on the automated checks alone; manually confirm image rights, relevance, watermark status, and quality.

Risk: Dependency installation and dependency versions are not pinned in the release metadata.

Mitigation: Pin Pillow and requests versions in the deployment environment and review dependency provenance before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lunadelo/skills/image-collector)
- [Publisher profile](https://clawhub.ai/user/lunadelo)

## Skill Output:

**Output Type(s):** [text, shell commands, code, files, guidance]

**Output Format:** [Markdown guidance, shell command examples, terminal status text, and downloaded or optimized image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python >=3.8 with Pillow and requests; downloaded images should be reviewed before publication.]

## Skill Version(s):

1.0.0 (source: server release evidence and package metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
