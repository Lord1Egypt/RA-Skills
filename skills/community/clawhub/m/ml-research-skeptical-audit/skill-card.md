## Description:

Adversarial, code-cited audit of ML research claims, objectives, leakage, controls, and baseline fairness with ranked risks and explicit falsification tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers, ML researchers, and reviewers use this skill to challenge experimental ML claims by tracing implementation evidence, ranking validity risks, and proposing falsification checks without running experiments unless separately authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install example uses an unpinned npx command.

Mitigation: Prefer a pinned or source-reviewed installation path and avoid elevated privileges when installing.

Risk: The skill is a static research review method, not an experiment runner.

Mitigation: Do not run training, download restricted data, launch paid compute, mutate repositories, or write to experiment trackers unless separately authorized.

Risk: Skill instructions do not provide a sandbox or override host permissions.

Mitigation: Keep the audit within the user's declared scope and rely on host-level permission controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/antreasantoniou/skills/ml-research-skeptical-audit)
- [Skill Instructions](SKILL.md)
- [README](README.md)
- [Security Policy](SECURITY.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown audit with code citations, verdicts, ranked risks, and falsification tests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proposed commands or experiments should be labeled unexecuted unless separately authorized.]

## Skill Version(s):

1.0.0 (source: changelog, released 2026-09-05; server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
