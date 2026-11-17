## Description:

Records browser sessions with Playwright and converts them to GIFs for web UI demos and tutorials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use it to automate browser-based UI demonstrations and tutorials, capturing Playwright sessions as video and converting them to GIFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recordings may capture personal, credential, or confidential information.

Mitigation: Use synthetic data where possible and review recordings before sharing.

Risk: The Playwright dependency reference is unpinned, creating a supply-chain consideration.

Mitigation: Review the dependency source and pin a version in project dependencies before installation.

Risk: The security scan had partial coverage and did not include behavioral execution checks.

Mitigation: Review the skill and its dependencies before use; treat the benign scan result as limited evidence.

## Reference(s):

- [ClawHub release](https://clawhub.ai/athola/skills/nm-scry-browser-recording)
- [Project homepage (Clawdis metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/scry)
- [Spec execution guidance](artifact/modules/spec-execution.md)
- [Video capture guidance](artifact/modules/video-capture.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Video files, GIF images]

**Output Format:** [Markdown guidance with shell commands, TypeScript examples, and WebM/GIF outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser recordings are WebM; GIF conversion uses the separate gif-generation skill.]

## Skill Version(s):

1.10.3 (source: frontmatter; ClawHub release 1.10.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
