## Description:

hivulse蜂巢 AI generates standardized technical documents from a specified project directory, including requirements, design, testing, and security self-assessment reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mojo-bo-coder](https://clawhub.ai/user/mojo-bo-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to upload a selected code project to the hivulseAI cloud service and generate standardized project documentation such as requirements, design, test, and security self-assessment reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload many readable files from the selected project directory to the hivulseAI cloud service.

Mitigation: Run it only on a reviewed, sanitized copy of the project and remove secrets, private keys, customer data, regulated data, and unrelated files before execution.

Risk: The API key may be stored in local plaintext configuration.

Mitigation: Prefer environment or platform-managed secret storage when available, restrict local file permissions, and rotate the key if exposure is suspected.

Risk: The generated documentation may be incomplete or inaccurate for the project under review.

Mitigation: Have project maintainers review generated documents before sharing, relying on them for compliance, or using them as authoritative design or test records.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/mojo-bo-coder/skills/hivulse-openclaw-skill)
- [hivulseAI cloud service](https://cloud.hivulse.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-oriented technical documentation with command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an HIVULSE_API_KEY and a readable project directory; generated content depends on the selected document type.]

## Skill Version(s):

0.1.4 (source: server release metadata; artifact package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
