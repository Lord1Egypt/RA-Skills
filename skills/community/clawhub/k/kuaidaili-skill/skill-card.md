## Description:

Integrates Kuaidaili proxy service workflows so an agent can fetch proxy IPs, check account balance, manage proxy-related API parameters, and test proxy connectivity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclaw-baixing](https://clawhub.ai/user/openclaw-baixing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to configure Kuaidaili credentials, retrieve private, dedicated, or tunnel proxy IPs, check account balance, and test whether a proxy endpoint works before using it in scraping or network automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API signatures and proxy credentials can be exposed through command history, URLs, logs, or captured output.

Mitigation: Prefer environment variables or a secret manager, avoid passing real secrets on the command line, redact logs, and rotate credentials that have already been exposed.

Risk: The skill invokes Kuaidaili API and proxy endpoints that may handle account, order, balance, or network-routing data.

Mitigation: Run it only in controlled environments, review target URLs and proxy use policies, and avoid unredacted execution in CI or shared terminals.

## Reference(s):

- [Kuaidaili API Reference](references/api_reference.md)
- [Kuaidaili Official Site](https://www.kuaidaili.com/)
- [Kuaidaili API Docs](https://www.kuaidaili.com/doc/)
- [ClawHub Skill Page](https://clawhub.ai/openclaw-baixing/skills/kuaidaili-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python examples; scripts may output JSON, plain text proxy lists, balance text, or proxy test status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KUAIDAILI_SECRET_ID and KUAIDAILI_SIGNATURE or equivalent command-line arguments for live API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
