## Description:

Fetches public LIGO/Virgo/KAGRA gravitational wave events from GWOSC, downloads detector strain data, runs signal processing and merger classification, and produces analysis plots and summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yash-kavaiya](https://clawhub.ai/user/yash-kavaiya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and science communicators use this skill to retrieve public GWOSC event data, run local strain-analysis workflows, and generate event summaries and plots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Output filenames may not always be safely contained within the selected output directory.

Mitigation: Install and run the skill in a sandboxed or low-privilege environment, use a dedicated output directory, and validate event names and detector identifiers before execution.

Risk: Unpinned dependency versions may change analysis behavior or introduce dependency risk over time.

Mitigation: Pin or lock dependency versions before production use and review package updates before deployment.

## Reference(s):

- [GWOSC](https://gwosc.org/)
- [ClawHub Skill Page](https://clawhub.ai/yash-kavaiya/skills/gravitational-wave-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, analysis files]

**Output Format:** [Markdown guidance with Python and shell command examples; generated PNG plots, JSON summaries, and text reports when the analyzer runs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public GWOSC data and writes outputs to a user-selected directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
