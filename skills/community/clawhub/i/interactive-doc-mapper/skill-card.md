## Description:

Create JSON-driven single-page interactive HTML documentation for app workflows between packages, services, and components.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and engineers use this skill to map app package, service, and component workflows into reviewable flow JSON and a self-contained interactive HTML document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flow JSON and generated HTML can expose secrets or private data if sensitive values are included.

Mitigation: Keep secrets, customer data, cookies, tokens, and private URLs out of flow JSON and generated HTML.

Risk: Generated workflow maps can mislead reviewers if the source flow JSON uses incorrect node references, vague labels, or stale assumptions.

Mitigation: Run the bundled validator, fix reported issues, and review the generated HTML interactively before sharing.

Risk: The skill may inspect the target repository and write JSON, validation, and HTML output files.

Mitigation: Run it in the intended workspace and review generated files before deployment or publication.

## Reference(s):

- [Flow JSON Schema](references/flow-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, HTML files]

**Output Format:** [Markdown guidance with shell commands, JSON flow documents, JSON validation reports, and self-contained HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML works locally from file:// and embeds the flow JSON for interactive review.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
