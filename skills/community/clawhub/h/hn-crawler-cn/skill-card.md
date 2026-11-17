## Description:

Crawls hn.aimaker.dev or another configured URL, extracts article data, organizes it, and produces summary reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drowning-in-codes](https://clawhub.ai/user/drowning-in-codes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run a Python pipeline that crawls web news, extracts structured article records, cleans and categorizes them, and generates JSON and Markdown summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler can fetch any URL supplied through CLI arguments or environment variables, including URLs outside the default public source.

Mitigation: Run it in an isolated environment with restricted outbound network access and avoid using it against internal or sensitive URLs.

Risk: The skill writes local output files and can process local input files.

Mitigation: Use a dedicated workspace, review input and output paths before running the pipeline, and inspect generated files before reusing them.

Risk: Dependencies are specified with lower bounds rather than pinned versions.

Mitigation: Pin and review dependency versions before installation or deployment.

Risk: The security evidence reports a syntax error in organize.py that may prevent the full pipeline from running.

Mitigation: Fix and validate the organize stage before relying on end-to-end pipeline output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drowning-in-codes/skills/hn-crawler-cn)
- [Target source site](https://hn.aimaker.dev/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; generated pipeline artifacts include HTML, JSON, and Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The pipeline supports TARGET_URL, OUTPUT_DIR, TIMEOUT, URL, input file, min-score, and stage-skip options.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
