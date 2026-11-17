## Description:

Checks an npm package's latest version, publish recency, deprecation status, and license to help assess whether to add it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nenadzivotic](https://clawhub.ai/user/nenadzivotic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill before adding an npm dependency to check its latest release, publication age, deprecation notice, and reported license.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented installer command runs code from an external source.

Mitigation: Trust the installer and its source before running it; pin or verify the installer when stronger supply-chain control is needed.

Risk: Publish recency and deprecation alone cannot establish that a package is safe or actively maintained.

Mitigation: Treat the health label as a screening heuristic and review the package separately before adding it.

## Reference(s):

- [npm package health lite on ClawHub](https://clawhub.ai/nenadzivotic/skills/npm-package-health-lite)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown summary based on a JSON npm registry report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the latest version, days since publication, deprecation status, license, and a recency-based health label.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
