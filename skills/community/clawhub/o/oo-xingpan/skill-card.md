## Description:

Xingpan API (xingpan.vip). Use this skill for ANY Xingpan API request — searching and reading data. Whenever a task involves Xingpan API, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Xingpan API can ask an agent to retrieve chart calculations, chart configuration, or daily horoscope data through their connected Xingpan account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions execute downloaded installer code, and its installation effects have not been inspected.

Mitigation: Review the installer and its effects, or use an installation method you trust, before running it.

Risk: The CLI can install or synchronize persistent skills across agent applications.

Mitigation: Review the CLI's automatic installation and synchronization controls and limit destinations to those you intend to modify.

Risk: Chart requests can send personal birth details, including another person's details, through OOMOL to Xingpan.

Mitigation: Share birth details only when comfortable sending them through those services, and include only the details needed for the requested chart.

## Reference(s):

- [Xingpan API documentation](https://www.xingpan.vip/astrology/Apiinterface)
- [Xingpan API homepage](https://xingpan.vip/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON API responses with chart, configuration, or horoscope data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action and its input data.]

## Skill Version(s):

1.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
