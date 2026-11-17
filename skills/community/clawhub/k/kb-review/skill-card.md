## Description:

Generate and save knowledge-base reviews such as literature reviews, research gaps, onboarding notes, stage summaries, and experiment suggestions based on existing KB sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and knowledge-base maintainers use this skill to synthesize existing KB material into reviews, research-gap analyses, method comparisons, onboarding notes, stage summaries, and experiment-improvement suggestions. The skill is intended to ground answers in selected KB sources and save generated review or onboarding documents back to the configured knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Gitea access to read and persist knowledge-base content, and the security evidence flags broad persistent write capability.

Mitigation: Install with a repository-scoped token over HTTPS, avoid site-admin tokens, constrain allowed repositories and writable draft paths, and require explicit user confirmation before saving generated material.

Risk: The security evidence reports unsafe default transport settings and administrator-level Gitea access expectations.

Mitigation: Configure an HTTPS Gitea URL, keep credentials out of prompts and logs, and separate system-configuration/control-plane functions from review-generation use.

Risk: Generated reviews or onboarding notes can become misleading if the available KB sources are incomplete or stale.

Mitigation: Require source citations in generated content, disclose insufficient KB coverage, and have a human review material before publishing it to the knowledge base.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/myd2002/skills/kb-review)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown review or onboarding content with shell command invocations and JSON status responses from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated content must include a sources section, state when KB evidence is insufficient, and avoid adding unsupported general knowledge.]

## Skill Version(s):

3.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
