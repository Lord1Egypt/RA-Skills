## Description:

Helps compare experimental protocol steps across research papers, with the packaged executable currently limited to demo output.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and evidence-review agents use this skill to compare experimental methods and protocol steps across papers for systematic reviews, reproducibility checks, and protocol optimization. Treat packaged execution as demo-limited until real paper input and output path handling is implemented.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged script only runs demo data and does not process the advertised paper input or output file paths.

Mitigation: Use it as a demonstration helper until the --papers and --output behavior is implemented or the documentation is corrected.

Risk: Methodology comparisons can be incomplete or misleading if extracted protocol steps are accepted without checking the source papers.

Mitigation: Review extracted steps against the original methods sections and state assumptions, missing inputs, and unresolved evidence in the final response.

Risk: The workflow may read input files and write workspace outputs when expanded beyond the current demo behavior.

Mitigation: Run in a sandboxed workspace, validate input and output paths, and avoid sensitive or unapproved paper data.

## Reference(s):

- [Audit Reference](references/audit-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/methodology-extractor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries and terminal text; demo comparison output is printed to stdout.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documented comparison table, parameter variation, and recommendation outputs should be validated against actual paper evidence before use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
