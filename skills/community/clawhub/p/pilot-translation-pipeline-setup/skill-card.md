## Description:

Deploy an automated three-agent translation pipeline for extracting source content, translating it, reviewing quality, and publishing approved translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure a coordinated extractor, translator, and reviewer workflow for multilingual content pipelines. It provides role-specific setup guidance, required skills, hostnames, manifests, handshakes, and example data-flow commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup commands use user-provided prefixes and role names when setting hostnames and writing manifests.

Mitigation: Use a hostname-safe prefix containing only lowercase letters, numbers, and hyphens before running setup commands.

Risk: The pipeline installs and links multiple dependent skills across agents.

Mitigation: Review and pin dependent skills before installation, and verify each peer before completing handshakes.

Risk: Approved translations may be published to an external webhook destination.

Mitigation: Confirm that the destination is approved for the translated content before publishing.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-translation-pipeline-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON manifest examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Role-specific setup output for extractor, translator, or reviewer agents.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
