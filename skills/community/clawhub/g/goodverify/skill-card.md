## Description:

Verify emails, phone numbers, and mailing addresses through the GoodVerify CLI and goodverify.dev API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[themusicman](https://clawhub.ai/user/themusicman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use GoodVerify to generate CLI commands and interpretation guidance for email, phone, address, batch, usage, and health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented installation path runs an unpinned remote shell script.

Mitigation: Inspect the installer before use or install only from a pinned, verified release that the deploying organization trusts.

Risk: The skill handles API keys, emails, phone numbers, addresses, and owner lookup results.

Mitigation: Treat this data as sensitive, confirm user consent before sending it to GoodVerify, and avoid exposing API keys or verification results in logs.

## Reference(s):

- [GoodVerify service](https://goodverify.dev)
- [GoodVerify Skill on ClawHub](https://clawhub.ai/themusicman/skills/goodverify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON response-field guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that call the GoodVerify service and guidance for interpreting JSON output.]

## Skill Version(s):

0.1.0 (source: release evidence and skill metadata frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
