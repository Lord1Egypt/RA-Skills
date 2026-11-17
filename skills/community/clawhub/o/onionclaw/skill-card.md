## Description:

Search the Tor dark web, fetch .onion hidden-service pages, rotate Tor identities, and run structured multi-step OSINT investigations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacobjandon](https://clawhub.ai/user/jacobjandon)

### License/Terms of Use:

MIT-0

## Use Case:

Security researchers, threat-intelligence analysts, and developers use this skill to run Tor-based dark-web searches, fetch .onion pages, rotate Tor identities, and produce structured OSINT reports for leak, ransomware, credential, and corporate exposure investigations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended for Tor-based dark-web OSINT and may surface sensitive leak, credential, or corporate exposure data.

Mitigation: Use it only for lawful security research or threat-intelligence work, and handle search terms, fetched pages, and generated reports as sensitive data.

Risk: Setup can involve Tor configuration changes and unpinned Python dependency installation.

Mitigation: Use a virtual environment, review the referenced source repository before running setup scripts, pin dependencies where possible, and avoid system-wide Tor changes unless they are intentionally accepted.

Risk: Recurring watch jobs and output locations can retain sensitive investigation results.

Mitigation: Choose output and watch directories carefully, restrict access to generated files, and remove investigation outputs when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jacobjandon/skills/onionclaw)
- [OnionClaw repository](https://github.com/JacobJandon/OnionClaw)
- [SICRY upstream repository](https://github.com/JacobJandon/Sicry)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, STIX, MISP, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and optional Markdown, JSON, CSV, STIX 2.1, or MISP investigation outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate reports, result lists, watch outputs, and Tor status or rotation results depending on the selected command.]

## Skill Version(s):

2.1.13 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
