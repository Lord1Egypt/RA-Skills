## Description:

Create a shareable RooQuiz preview quiz: a right/wrong assessment where correct answers earn points and the taker gets a score, then get a browser-openable preview link without an account, login, or API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloevib](https://clawhub.ai/user/chloevib)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to build, preview, and share temporary graded RooQuiz quizzes, tests, trivia, or exams with correct answers and final scoring. It is intended for creating a short-lived hosted preview link that can be opened in a browser or moved into RooQuiz for publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quiz questions, answers, labels, and report text are sent to RooQuiz's hosted preview service when using the default endpoint.

Mitigation: Avoid confidential or regulated material in hosted previews, or use the documented endpoint overrides for a trusted self-hosted RooQuiz deployment.

Risk: Preview links are temporary and expire after about one hour.

Mitigation: Use preview links for short review cycles only; publish from the RooQuiz preview page when a durable quiz is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chloevib/skills/preview-quiz)
- [RooQuiz preview API](https://preview.rooquiz.com/api/preview-forms)
- [RooQuiz preview service](https://preview.rooquiz.com)
- [RooQuiz browser preview base](https://quizster.app)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON examples and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces RooQuiz quiz JSON guidance and a temporary browser preview link when the preview API call succeeds.]

## Skill Version(s):

0.1.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
