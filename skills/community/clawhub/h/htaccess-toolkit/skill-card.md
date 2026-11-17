## Description:

Generate, validate, lint, and explain Apache .htaccess files for redirects, security headers, caching, CORS, file protection, and configuration audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and web operators use this skill to generate Apache .htaccess snippets, lint existing .htaccess files, explain directives, and choose presets for redirects, security headers, caching, CORS, compression, file protection, and custom error pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated .htaccess content can change live web-server behavior or overwrite an active configuration file.

Mitigation: Review generated output before deployment, keep a backup of the current .htaccess file, and avoid direct writes to .htaccess unless the target environment and rollback path are understood.

Risk: Untrusted domain, redirect, or path values can be inserted into generated rules without strong validation.

Mitigation: Use trusted values only, validate domains and redirect targets before generation, and test the resulting rules in a staging environment.

## Reference(s):

- [Htaccess Toolkit on ClawHub](https://clawhub.ai/charlie-morrison/skills/htaccess-toolkit)
- [Publisher profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with Apache .htaccess configuration snippets and optional JSON lint output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated .htaccess content to a requested output file when used with the script's output option.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
