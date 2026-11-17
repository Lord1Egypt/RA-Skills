## Description:

Health Reasoner scores daily lifestyle habits such as sleep, diet, exercise, stress, smoking, and alcohol use and returns rule-based wellness suggestions; it is not for medical diagnosis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen-feng123](https://clawhub.ai/user/chen-feng123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can run the skill locally to assess lifestyle habit inputs and generate non-diagnostic wellness scores, risk levels, and improvement suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer offers an unnecessary unpinned Flask install for an API mode the code does not implement.

Mitigation: Use CLI, JSON input, or Python import modes; do not accept the Flask install prompt unless the publisher provides a working reviewed API mode with pinned dependencies.

Risk: History files can contain health-related assessment summaries when a history path is configured.

Mitigation: Leave history disabled by default or store history files only in private, unsynced locations and remove them when no longer needed.

Risk: The skill outputs lifestyle wellness scoring and suggestions, not medical diagnosis or treatment advice.

Mitigation: Treat the output as informational habit guidance and consult a qualified medical professional for health concerns.

## Reference(s):

- [API_SPEC.md](API_SPEC.md)
- [USE_GUIDE.md](USE_GUIDE.md)
- [DESIGN.md](references/DESIGN.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured JSON or plain text wellness assessment with score, risk level, suggestions, risk factors, and scoring details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local rule-based processing; optional history files store recent assessment summaries only when explicitly configured.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
