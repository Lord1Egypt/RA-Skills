## Description:

An information-literacy exam assistant that checks a 1,017-question local bank first, then researches unmatched questions using rule cards and documented site entries, with sources and human-review steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glgeneral15](https://clawhub.ai/user/glgeneral15)

### License/Terms of Use:

MIT

## Use Case:

External learners preparing for information-literacy competitions use the skill to answer practice questions, find supporting evidence for unfamiliar questions, and review the evidence trail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser recovery instructions may terminate unrelated browser sessions.

Mitigation: Restrict recovery to the ilradar session and remove global browser-cleanup actions before use.

Risk: Saved browser login-state files may expose authenticated session data.

Mitigation: Keep browser profiles separate and protect saved login-state files.

Risk: Question-bank answers are provided without independent verification.

Mitigation: Independently verify bank answers against authoritative sources when correctness is important.

## Reference(s):

- [il-reader on ClawHub](https://clawhub.ai/glgeneral15/skills/il-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Answer text with sources, confidence, and a human-review sheet; language follows the user's prompt.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source URLs and review steps for research-based answers; local question-bank answers are not independently verified.]

## Skill Version(s):

1.2.1 (source: SKILL.md frontmatter, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
