## Description:

Initializes, updates, queries, and searches cross-project API specification documentation for backend projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexxxiong](https://clawhub.ai/user/alexxxiong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to maintain a local API specification registry, generate YAML API documentation from backend route and handler files, and quickly look up or search existing API definitions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The update workflow can publish generated API details to a remote repository.

Mitigation: Require explicit review and approval of generated API docs before any commit or push.

Risk: Route and handler analysis may expose internal endpoints, schemas, tokens, or business-sensitive API details.

Mitigation: Limit use to repositories whose API details are approved for registry storage, and review generated YAML before sharing.

Risk: The skill maintains a persistent API-spec registry under ~/.apispec.

Mitigation: Confirm the registry location and access controls before initialization or update.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexxxiong/skills/inspirai-apispec)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise text and Markdown with shell command, YAML configuration, and API-spec examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update .api-spec.yaml and YAML API specification files in a local registry.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
