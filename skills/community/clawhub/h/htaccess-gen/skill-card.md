## Description:

Generates Apache .htaccess configurations for redirects, rewrites, security headers, HTTPS enforcement, IP blocking, caching, custom error pages, hotlink protection, and nginx-to-Apache translation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to generate Apache .htaccess directives for common web server tasks, including redirects, URL rewrites, security headers, HTTPS enforcement, caching, compression, CORS, IP blocking, custom error pages, and hotlink protection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted or malformed domains, origins, IPs, paths, and rewrite expressions can lead to unsafe or incorrect Apache directives.

Mitigation: Use trusted, simple input values and review generated .htaccess content before deployment.

Risk: The --output option writes to the named file and may overwrite existing content.

Mitigation: Choose output paths deliberately and keep a backup or review the destination before writing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnywang2001/skills/htaccess-gen)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [Plain text Apache .htaccess directives, optionally written to a file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated configuration to stdout by default; the --output option writes to the named file.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
