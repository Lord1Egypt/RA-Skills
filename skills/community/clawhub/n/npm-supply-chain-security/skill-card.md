## Description:

Helps secure JavaScript projects by identifying npm supply chain risks, configuring trusted publishing, verifying releases, and auditing dependencies for suspicious patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robinyves](https://clawhub.ai/user/robinyves)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to harden JavaScript package publishing workflows and review npm dependencies for supply chain attack indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The trusted-publishing workflow example includes an npm token secret, which could lead to long-lived or overly broad token use if copied directly.

Mitigation: Adapt the workflow to the registry's current trusted publishing guidance and prefer short-lived, scoped credentials or tokenless OIDC where supported.

Risk: The package-release and dependency heuristics are simplified and can miss malicious behavior or flag benign packages.

Mitigation: Use the examples as review prompts alongside registry metadata, release provenance, dependency diffs, scanning tools, and human review before taking action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robinyves/skills/npm-supply-chain-security)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, YAML, Python, JavaScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes practical security heuristics and publishing examples that should be reviewed before production use.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
