## Description:

Use mustache.js (logic-less Mustache templates) for any templating task in JavaScript/Node.js environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for help rendering Mustache templates, creating .mustache files, generating HTML, configuration, or code from templates, and applying mustache.js API and CLI patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw HTML rendering, global escape overrides, or innerHTML insertion can expose web-facing code to unsafe output when templates or data are untrusted.

Mitigation: Use escaped variables by default and only use unescaped output, escape overrides, or innerHTML with trusted or sanitized templates and data.

Risk: Global npm installation changes the user's broader environment and may be unnecessary for project-specific templating work.

Mitigation: Prefer project-local npm installation unless the Mustache CLI is explicitly needed globally.

## Reference(s):

- [Mustache ClawHub skill page](https://clawhub.ai/openlark/skills/mustache)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JavaScript, HTML, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Mustache templates, rendered-output examples, npm install commands, CLI usage, and implementation guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
