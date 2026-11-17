## Description:

Volcengine Ark (volcengine.com) supports reading, creating, updating, and deleting data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Volcengine Ark connector schemas and run OOMOL-connected actions for Seedance video generation task submission, retrieval, listing, and cancellation or deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad oo CLI authority for Volcengine Ark actions.

Mitigation: Install and use the skill only when OOMOL and the oo CLI are trusted for the target account.

Risk: Documented remote installer commands may execute unverified code.

Mitigation: Prefer verified releases or package-manager installation paths over pipe-to-shell installers.

Risk: Write and destructive actions can change or delete Volcengine Ark task state.

Mitigation: Confirm the exact payload, target, and expected effect with the user before running write or destructive actions.

## Reference(s):

- [Volcengine Ark homepage](https://www.volcengine.com/product/ark)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-volcengine-ark)
- [Skill icon](https://static.oomol.com/logo/third-party/volcengine_ark.svg)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce oo CLI commands that call Volcengine Ark through an OOMOL-connected account.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
