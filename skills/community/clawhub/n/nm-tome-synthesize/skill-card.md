## Description:

Merges, dedupes, ranks, and formats research findings into a report. Use after research agents return results from multiple channels to produce a ranked report

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill after research agents return findings from multiple channels. It combines and deduplicates those findings, ranks and groups them, then formats a report, brief, or transcript.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The possible overlap between the “merge” and “format” triggers may affect which skills activate in a particular agent setup.

Mitigation: Check trigger behavior in the intended agent setup and adjust activation rules if the overlap causes unwanted activations.

## Reference(s):

- [Tome plugin reference](https://github.com/athola/claude-night-market/tree/master/plugins/tome)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown report, brief, or transcript]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are merged, deduplicated, ranked, and grouped before formatting.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
