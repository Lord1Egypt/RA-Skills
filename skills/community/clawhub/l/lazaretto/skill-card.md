## Description:

Verify a third-party skill, tool, or npm/GitHub package for malicious behavior before installing or running it, using known-bad hash lookup, behavioral scanning, and on-disk byte verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamesdfinance-dev](https://clawhub.ai/user/jamesdfinance-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Lazaretto before installing untrusted skills, MCP servers, npm packages, GitHub repositories, raw URLs, or ClawHub skills to check for malicious behavior and confirm the installed bytes match the scanned artifact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scans contact a remote service and inline scans upload the selected file.

Mitigation: Use the skill only for artifacts that may be sent to Lazaretto, and avoid inline scans for sensitive local files.

Risk: Custom API endpoints can receive API keys or scan payloads when LAZARETTO_API or --api is used.

Mitigation: Use the default Lazaretto endpoint unless a custom endpoint is fully trusted, and do not pass an API key to custom endpoints.

Risk: Local verify results are helpful signals but may not be byte-perfect for binary files or directories with symlinks.

Mitigation: Treat mismatches as unscanned and manually review cases involving binary content, symlinks, or packaging differences.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jamesdfinance-dev/skills/lazaretto)
- [Lazaretto Homepage](https://lazaretto.dev)
- [Lazaretto Pricing](https://lazaretto.dev/#pricing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Node.js and the LAZARETTO_KEY environment variable for keyed scans.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
