## Description:

Project Analyzer helps agents inspect software projects and generate SDD documentation, including requirements, architecture, detailed design, database, API, and test design Markdown documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whiskeyforsun](https://clawhub.ai/user/whiskeyforsun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze a project path, identify structure, APIs, database assets, and technology signals, and generate structured software design documentation for onboarding, maintenance, and project review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads project source, SQL, tests, and configuration files, which may include sensitive implementation details or secrets.

Mitigation: Run it on a narrow project path, remove or redact secrets before use, and review generated Markdown before sharing.

Risk: Untrusted project text can be carried into generated Markdown.

Mitigation: Review generated Markdown before opening it in permissive renderers or publishing it.

Risk: Apifox-related instructions may involve external synchronization, and safe external sync behavior is not documented in the release evidence.

Mitigation: Use Apifox-related workflows only with separate explicit consent and appropriately scoped credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whiskeyforsun/skills/project-analyzer)
- [constraints.yaml](references/configs/constraints.yaml)
- [SRS template](references/templates/01-srs.md)
- [SAD template](references/templates/02-sad.md)
- [DBD template](references/templates/04-dbd.md)
- [APID template](references/templates/05-apid.md)
- [TSD template](references/templates/06-tsd.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documents plus terminal progress text and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated documentation under the selected output directory, commonly docs/sdd; requires python3.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
