## Description:

Build and test HTTP requests with CLI interface: headers, auth, body, cookies, with history and templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derick001](https://clawhub.ai/user/derick001)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to build, send, save, and replay HTTP requests from a terminal while testing or debugging REST API endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Templates and local history can store API tokens, Authorization or Cookie headers, passwords, and sensitive request bodies in plaintext.

Mitigation: Avoid saving secrets in templates or history, prefer short-lived tokens, rotate any secret already used with this tool, and treat ~/.http-request-builder/ as sensitive.

Risk: Untrusted template names are used directly in file paths.

Mitigation: Use trusted template names and review saved templates before executing them.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Terminal text with JSON request templates and history files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores templates and request history under ~/.http-request-builder/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
