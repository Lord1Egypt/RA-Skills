## Description:

Create a shareable RooQuiz preview personality or outcome test where answer options vote for result types, then return a temporary browser-openable preview link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloevib](https://clawhub.ai/user/chloevib)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, educators, marketers, and developers use this skill to build and share temporary RooQuiz personality or outcome quiz previews without needing an account, login, API key, or credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quiz title, questions, answers, scoring mappings, and result text are uploaded to RooQuiz to generate a shareable preview.

Mitigation: Do not use the skill with secrets, private business material, regulated personal data, or content that should not be hosted behind a preview link.

Risk: Preview links are temporary and expire automatically after about 1 hour.

Mitigation: Use previews for review and testing only, and publish through RooQuiz if the quiz needs to persist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chloevib/skills/preview-outcome)
- [RooQuiz preview service](https://preview.rooquiz.com)
- [RooQuiz quiz preview viewer](https://quizster.app)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, HTTP requests, shell command snippets, and a preview link.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces short-lived RooQuiz preview links that expire after about 1 hour.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
