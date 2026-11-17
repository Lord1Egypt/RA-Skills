## Description:

Nex Keyring helps agents guide users through local API key and secret rotation tracking, stale credential checks, audit log review, and metadata-only exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexaiguy](https://clawhub.ai/user/nexaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, system administrators, and security reviewers use this skill to track credential metadata, check rotation posture, scan environment key names, and prepare audit-oriented reports without storing plaintext secret values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports an arbitrary-code-execution path flaw in setup.sh path handling.

Mitigation: Review or fix setup.sh before installation, and run it only from a trusted local skill directory.

Risk: The security evidence says the encryption claims are not backed by the implementation.

Mitigation: Treat the local database, audit log, hashes, paths, and exports as sensitive metadata; protect ~/.nex-keyring and exported files with local access controls.

Risk: Scanning broad environments or production .env files can expose sensitive metadata about credential names and usage.

Mitigation: Use explicit file paths, scan only what is necessary, and avoid broad environment scans on production systems unless reviewed.

## Reference(s):

- [Nex Keyring on ClawHub](https://clawhub.ai/nexaiguy/skills/nex-keyring)
- [Publisher profile: nexaiguy](https://clawhub.ai/user/nexaiguy)
- [Nex AI homepage](https://nex-ai.be)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain-text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce metadata-only JSON, CSV, or Markdown exports when the user runs the documented CLI commands.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
