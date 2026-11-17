## Description:

Quick health check on a public GitHub repo before depending on it — stars, days since last push, license, archived flag, and a health heuristic. Single unauthenticated API call. Use when the user asks whether a GitHub repo is maintained, trustworthy, or safe to adopt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nenadzivotic](https://clawhub.ai/user/nenadzivotic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to quickly assess public GitHub repository activity and adoption signals before depending on a project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A maintenance report could be mistaken for proof that repository code is safe.

Mitigation: Treat it only as a maintenance indicator; review and pin the installer and source before installation.

Risk: Repeated checks can exhaust GitHub's shared unauthenticated API rate limit.

Mitigation: Use it for individual repository checks and avoid looping over many repositories.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nenadzivotic/skills/github-repo-due-diligence-lite)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [JSON repository report with a concise health heuristic]

**Output Parameters:** [One public GitHub repository per invocation]

**Other Properties Related to Output:** [Uses one unauthenticated public GitHub API request; the health label is a maintenance heuristic, not a code-safety assessment.]

## Skill Version(s):

1.1.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
