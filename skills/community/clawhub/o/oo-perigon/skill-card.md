## Description:

Use Perigon to search and read news, journalist, company, people, media-source, story, topic, and Wikipedia data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to query Perigon for news articles and related journalists, companies, people, media sources, stories, topics, and Wikipedia content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute downloaded installer code without a clear approval step.

Mitigation: Install a verified oo CLI version separately and require approval before running downloaded installers.

Risk: The CLI may automatically synchronize skills and make unwanted changes.

Mitigation: Review its synchronization behavior and disable unwanted changes before enabling it.

Risk: Perigon queries and authorization through OOMOL may incur charges.

Mitigation: Check OOMOL credit and the Perigon account plan before use.

## Reference(s):

- [Perigon](https://perigon.io)
- [Perigon API documentation](https://docs.goperigon.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Text]

**Output Format:** [JSON responses and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Perigon action and search filters.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
