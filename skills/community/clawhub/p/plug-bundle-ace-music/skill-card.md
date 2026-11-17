## Description:

ace-music组合包 bundles ace-music, ai-image-gen, comfyui-painter, and solo-build to support creative music and media workflows with read, command execution, and file-writing capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this ClawHub plug bundle to coordinate four creative skills for music recommendation, generation support, style conversion, lyrics creation, and related file or command-assisted workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundle requests broad command, file, and API capabilities without clearly scoping how each member skill uses them.

Mitigation: Use it in a contained workspace, confirm file writes and command execution before allowing them, and provide API keys only when a specific member skill requirement is understood.

Risk: Security evidence marks the release suspicious because the bundle is documentation-only but asks for broad capabilities.

Mitigation: Review and scan the bundle and member skills before deployment; do not treat the bundle description as sufficient operational assurance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/plug-bundle-ace-music)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose command execution and file writes through member skills; review actions before allowing them.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
