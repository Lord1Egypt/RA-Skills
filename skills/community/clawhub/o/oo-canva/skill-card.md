## Description:

Canva (canva.com). Use this skill for ANY Canva request — reading, creating, and updating data. Whenever a task involves Canva, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users can use this skill to inspect Canva designs, assets, folders, and account details, and to create, export, upload, or organize Canva content through an OOMOL-connected account. It guides the agent to check the connector schema and confirm state-changing actions before running them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup instructions download and run installer code without a separate approval step.

Mitigation: Install and verify the oo CLI from a trusted source before enabling the skill; review the installer and any bundled-skill installation behavior before using the fallback setup path.

## Reference(s):

- [Canva](https://www.canva.com)
- [Canva REST API documentation](https://www.canva.dev/docs/apps/rest-apis/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Canva skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-canva)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with oo CLI command examples and JSON action payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs follow the live connector schema; write actions change Canva state and destructive actions require explicit approval.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
