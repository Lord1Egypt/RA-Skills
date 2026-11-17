## Description:

Generates Nginx configuration templates for reverse proxying, SSL/HTTPS, static hosting, security hardening, load balancing, caching behavior, and performance-oriented server setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to draft Nginx server blocks and operational helper commands for reverse proxies, HTTPS sites, static hosting, security hardening, load balancing, caching, and tuning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Nginx configuration may be incorrect or unsafe if produced from untrusted or invalid inputs.

Mitigation: Use trusted, validated domain, backend, root, certificate, and port values; inspect generated configuration and test it before deployment.

Risk: The bundled helper can read local host status or log data and persist command arguments in a local history file.

Mitigation: Run the helper only in trusted environments, avoid sensitive command arguments, and review or clear its local history storage when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/nginx-config)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell output containing Nginx configuration snippets, operational commands, and implementation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated configurations and operational commands should be inspected and tested before deployment.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
