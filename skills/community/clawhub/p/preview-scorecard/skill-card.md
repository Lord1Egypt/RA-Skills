## Description:

Creates a short-lived RooQuiz preview link for a scored questionnaire whose answer choices contribute points to a total and result level.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloevib](https://clawhub.ai/user/chloevib)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, test, and share temporary RooQuiz scorecard previews for self-assessments, readiness checks, maturity checks, satisfaction surveys, and other scored questionnaires.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-created scorecard questions, scoring rules, result text, and configuration to an external RooQuiz preview service.

Mitigation: Do not include secrets, confidential business logic, private client data, or sensitive personal information unless the user intends to share that content with RooQuiz.

Risk: The generated preview is a public, short-lived link that can expose the submitted scorecard content to anyone who has the token.

Mitigation: Treat preview links as shareable public artifacts and use them only for content that can be disclosed during the preview window.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chloevib/skills/preview-scorecard)
- [Publisher profile](https://clawhub.ai/user/chloevib)
- [RooQuiz preview API](https://preview.rooquiz.com/api/preview-forms)
- [RooQuiz preview link base](https://quizster.app)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples, shell commands, and a preview URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a short-lived public preview link after submitting scorecard content to RooQuiz.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
