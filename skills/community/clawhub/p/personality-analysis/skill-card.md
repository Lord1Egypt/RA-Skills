## Description:

Analyzes chat records to infer personality traits, speaking style, and psychological profile, then produces a structured report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangmanqi2104201431-ship-it](https://clawhub.ai/user/yangmanqi2104201431-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to analyze permitted chat records or extracted screenshot text for personality, communication style, values, emotional patterns, and relationship needs. Outputs should be treated as speculative, non-clinical observations rather than definitive psychological assessments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill analyzes chat records and screenshots that may contain private or third-party data.

Mitigation: Use only with conversations the user is allowed to analyze; remove unnecessary personal data and avoid uploading sensitive screenshots.

Risk: The skill asks for personality and psychological judgments that can be mistaken for clinical or factual conclusions.

Mitigation: Frame outputs as speculative, evidence-limited, non-clinical observations and avoid diagnostic language.

Risk: The artifact includes dark-trait, manipulation, and style-imitation sections that can enable harmful profiling or impersonation.

Mitigation: Keep outputs focused on benign understanding and communication safety, and refuse requests that support harassment, coercion, or impersonation.

## Reference(s):

- [Analysis Framework](artifact/references/analysis-framework.md)
- [Report Template](artifact/references/report-template.md)
- [ClawHub Skill Page](https://clawhub.ai/yangmanqi2104201431-ship-it/skills/personality-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, files]

**Output Format:** [Markdown report with optional PDF file conversion]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured personality analysis report covering HEXACO, MBTI-style inference, values, emotional patterns, interpersonal needs, and communication guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
