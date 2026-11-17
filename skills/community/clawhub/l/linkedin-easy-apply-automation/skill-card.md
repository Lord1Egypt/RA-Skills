## Description:

Automate LinkedIn Easy Apply searches and applications with Puppeteer/Chromium, a verified resume PDF, remote/job-title filtering, stateful daily reruns, and conservative answer guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ralyodio](https://clawhub.ai/user/ralyodio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations agents use this skill to build and run a repeatable LinkedIn Easy Apply workflow from a verified resume PDF while skipping unknown or subjective application questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent live authority to submit job applications on behalf of the operator.

Mitigation: Keep DRY_RUN enabled until search targets and answers are inspected, and require manual approval before each live submission.

Risk: The skill uses an authenticated browser profile, which can expose account state during automation.

Mitigation: Use a dedicated browser profile and preferably a separate OS account or container for the workflow.

Risk: The suggested Chromium launch pattern disables sandbox protections.

Mitigation: Remove the sandbox-disabling flags unless the execution environment has a reviewed and well-understood reason to keep them.

Risk: Automated application flows may encounter CAPTCHA, MFA, identity verification, or suspicious-login checks.

Mitigation: Stop automation and return control to the operator whenever account-security prompts appear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ralyodio/skills/linkedin-easy-apply-automation)
- [Publisher profile](https://clawhub.ai/user/ralyodio)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, JavaScript, JSON, and text snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operator-guided browser automation steps, environment-variable configuration, dry-run defaults, and state/log file conventions.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
