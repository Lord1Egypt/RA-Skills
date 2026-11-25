## Description:

Builds a structured US interview question set and scoring rubric for one role, with unlawful questions flagged for removal. Use when the user asks for interview question kit, behavioral interview questions, illegal interview questions. For US hiring managers, recruiters and interview panels hiring hourly and salaried staff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US hiring managers, recruiters and interview panels can use the skill to prepare structured, role-specific interview questions, follow-up probes, scoring anchors and a do-not-ask list. The included script checks a supplied kit for required sections and flagged phrases, then writes a Markdown lint report.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The scanner reports a mismatch between the interview-kit purpose and script behavior, along with file writing that is not declared in the skill metadata; the scanner analysis was partial.

Mitigation: Review the included script and its input and output paths before use, and treat the benign verdict as limited because some referenced paths were unresolved.

Risk: The optional Windows toolkit download is a separate, unsigned executable and is not included in the bundle.

Mitigation: If choosing to download it, verify the documented SHA-256, keep it in its own folder, and avoid running it as administrator unless needed.

## Reference(s):

- [US pre-employment question rules](references/interview-question-rules.md)
- [ClawHub release page](https://clawhub.ai/rapidworker1/skills/interview-question-kit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration]

**Output Format:** [Interview-kit YAML template and Markdown lint report, with structured question, probe, rubric and panel-note content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The standalone Python script checks a supplied file and writes a lint report; it does not score or rank candidates.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
