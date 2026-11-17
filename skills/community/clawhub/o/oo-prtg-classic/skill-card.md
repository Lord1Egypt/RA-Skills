## Description:

Use this skill to search and read data in PRTG Classic through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and monitoring operators use this skill to list PRTG Classic devices and sensors and inspect their status, messages, and latest values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup may execute unverified remote installer code without a clear approval step.

Mitigation: Review setup first; install a reviewed, verified CLI release yourself and require approval before further installation or agent-skill changes.

Risk: The connected service can access PRTG monitoring data.

Mitigation: Use a read-only PRTG connection and consider OOMOL's access to monitoring data.

## Reference(s):

- [PRTG Classic skill page](https://clawhub.ai/oomol/skills/oo-prtg-classic)
- [PRTG Classic homepage](https://www.paessler.com/prtg)
- [PRTG HTTP API documentation](https://www.paessler.com/manuals/prtg/http_api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [PRTG device and sensor data returned as text or Markdown; action requests use JSON payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only device and sensor listings.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
