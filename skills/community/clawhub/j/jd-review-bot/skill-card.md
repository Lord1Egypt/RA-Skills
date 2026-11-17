## Description:

Automates bulk posting of preset five-star JD.com product reviews from a logged-in real browser session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fzuim](https://clawhub.ai/user/fzuim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers or power users can use this skill to drive browser-use automation that collects pending JD.com review orders and submits preset positive reviews from their own logged-in JD account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post many public five-star reviews from a real JD account using preset text.

Mitigation: Use only with explicit account-owner approval, review each batch before submission, and start with a small supervised run.

Risk: The skill lacks clear confirmation controls before public review submission.

Mitigation: Run in headed mode under human supervision and add a manual confirmation step before clicking publish.

Risk: The artifact can install unpinned third-party browser automation tooling.

Mitigation: Install dependencies in an isolated environment and pin or review browser-use and browser dependencies before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fzuim/skills/jd-review-bot)
- [JD review center](https://club.jd.com/myJdcomments/myJdcomment.action)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown instructions with bash, JavaScript, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a Python automation script and browser-use CLI commands for a headed real-browser session.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
