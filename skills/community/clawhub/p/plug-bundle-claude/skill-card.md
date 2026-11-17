## Description:

A ClawHub Plug bundle that combines four agent skills, centered on claude, to support an end-to-end workflow for data input, processing, decision support, and output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this Plug bundle to combine claude, neosoul-decision-agent, simple-memory-skill, and token-saver-skill into a coordinated Agents workflow. The bundle is positioned for file handling, information retrieval, command execution, configuration, and consolidated task output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundle requests broad powers including file edits, shell execution, and potential API credential use.

Mitigation: Install only in workspaces where those powers are acceptable, limit secrets and API keys, and confirm each bundled skill's behavior before using it on sensitive projects.

Risk: The security verdict is suspicious because the requested capabilities are broad for a bundle listing.

Mitigation: Review and scan the bundled skills before deployment, then grant the minimum tool access needed for the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/plug-bundle-claude)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-oriented guidance with inline code or shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on file, shell, search, edit, and credential access granted to the bundled skills.]

## Skill Version(s):

1.0.1 (source: server release evidence and target metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
