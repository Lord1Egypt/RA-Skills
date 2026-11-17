## Description:

Objectively scores meeting quality from a transcript across decision clarity, time efficiency, and participation balance, producing Markdown and HTML reports with an OpenAI-compatible LLM endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ucsdzehualiu](https://clawhub.ai/user/ucsdzehualiu)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use this skill to evaluate meeting transcripts, identify weak decision follow-through, inefficient time use, and participation imbalance, and generate reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting transcripts are sent to the configured LLM endpoint, which may expose sensitive meeting content if the endpoint is not approved for that data.

Mitigation: Use a local or approved provider for sensitive meetings, keep API keys out of shared config files where possible, and protect config file permissions.

Risk: The current package appears to be missing report templates needed for the advertised Markdown and HTML output.

Mitigation: Verify the report templates are present and run report-generation tests before relying on the generated reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ucsdzehualiu/skills/meeting-quality-scorer)
- [Publisher profile](https://clawhub.ai/user/ucsdzehualiu)
- [README](README.md)
- [License](LICENSE)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, HTML, Files, Configuration instructions]

**Output Format:** [Markdown and HTML report files with numeric scores, decision tables, filler findings, speaker balance charts, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured OpenAI-compatible LLM endpoint; labeled transcripts enable participation scoring, while plain transcripts use a two-dimension degraded mode.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
