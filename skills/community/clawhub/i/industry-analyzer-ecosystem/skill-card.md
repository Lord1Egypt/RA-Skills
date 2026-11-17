## Description:

Map the supply chain ecosystem of a given industry by identifying upstream, midstream, downstream, and horizontal-support positions with representative companies at each position.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zrxparley](https://clawhub.ai/user/zrxparley)

### License/Terms of Use:

MIT-0

## Use Case:

Industry analysts, strategy teams, and agent workflows use this skill to generate a structured industry ecosystem report from a session file. The skill produces a four-position supply-chain breakdown, representative companies, barriers, key metrics, and a Mermaid ecosystem diagram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on third-party web research, so generated company lists, metrics, or industry structure may be incomplete, stale, or misleading.

Mitigation: Review the generated report, cited sources, and any important claims before using the output for business decisions.

Risk: The skill may create or overwrite output/{industry-slug}/02-ecosystem.md and update output/{industry-slug}/session.json.

Mitigation: Run it in a controlled workspace and review file changes before committing or publishing results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zrxparley/skills/industry-analyzer-ecosystem)
- [Ecosystem positions template](references/ecosystem-positions.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with a Mermaid diagram and session state updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes output/{industry-slug}/02-ecosystem.md and updates output/{industry-slug}/session.json.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
