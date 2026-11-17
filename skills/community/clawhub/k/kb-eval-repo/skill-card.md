## Description:

Evaluates whether a GitHub or open-source repository is useful for the selected Research KB context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Research KB users use this skill to judge repository relevance, reproducibility, activity, adaptation cost, and unique value against selected knowledge-base materials. It can return cited evaluations and optionally write a Markdown review page into the selected knowledge repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Gitea administrator token for knowledge-repository access.

Mitigation: Install only in a trusted Research KB backend, restrict task JSON creation, and replace the administrator token with least-privilege credentials before broad use.

Risk: The skill writes review files by default when writeReview is not false.

Mitigation: Make review writes explicitly opt-in or set writeReview to false unless repository changes are intended and reviewed.

Risk: The security verdict is suspicious because credentials and repository writes require careful operational controls.

Mitigation: Review the skill before installation, restrict Gitea access to approved KB repositories, and pin or remove dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/myd2002/skills/kb-eval-repo)

## Skill Output:

**Output Type(s):** [text, JSON, markdown]

**Output Format:** [JSON object containing an answer, citations, used scopes, read pages, and an optional generated review page path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a Markdown repository evaluation page when writeReview is enabled.]

## Skill Version(s):

1.0.0 (source: server release evidence, artifact _meta.json, main.js)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
