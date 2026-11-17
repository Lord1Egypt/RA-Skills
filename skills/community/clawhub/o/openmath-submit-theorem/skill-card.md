## Description:

Submits proofs to the OpenMath platform through a two-stage commit-reveal flow for committing proof hashes and revealing Lean/Rocq proofs on the Shentu network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bennyzhe](https://clawhub.ai/user/bennyzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, theorem provers, and external agents use this skill to prepare and submit OpenMath proofs, verify authz and feegrant readiness, broadcast commit-reveal transactions, and check theorem status on Shentu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured shentud binary may be installed without integrity verification.

Mitigation: Use an official Shentu release and verify the binary with a checksum or signature before trusting it.

Risk: Wallet feegrant or authz checks may accept overly broad spending authority.

Mitigation: Use narrow allowed messages, finite spend limits, and expiration dates; review and revoke existing broad grants before treating readiness as sufficient.

Risk: Local key setup or recovery can expose seed phrases or recovery material.

Mitigation: Keep seed phrases out of chat and perform key creation or recovery manually in a local trusted environment.

Risk: Manual authz examples include an expiration date that was already past on 2026-09-12.

Mitigation: Replace example expiration values with a reviewed future expiration before creating grants.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bennyzhe/skills/openmath-submit-theorem)
- [Init setup](references/init-setup.md)
- [Shentu proof submission guidelines](references/submission_guidelines.md)
- [OpenMath authz setup](references/authz_setup.md)
- [OpenMath environment example](references/openmath-env.example.json)
- [Authz submit configuration example](references/authz-submit-config.example.json)
- [Shentu releases](https://github.com/shentufoundation/shentu/releases)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local transaction JSON filenames, readiness checks, broadcast commands, and status-query guidance.]

## Skill Version(s):

1.0.7 (source: server release metadata; artifact frontmatter v1.0.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
