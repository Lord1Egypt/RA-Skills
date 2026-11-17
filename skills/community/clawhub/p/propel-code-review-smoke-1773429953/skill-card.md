## Description:

Run async diff-based code reviews using the Propel Review API, poll for completion, retrieve structured findings, and send comment feedback for current branch diffs or other Git diffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonyuezhang](https://clawhub.ai/user/jasonyuezhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to submit Git diffs to Propel for asynchronous code review, retrieve structured findings, apply valid fixes, and send feedback about each review comment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads reviewed diffs to Propel and requires a token with reviews:read and reviews:write scopes.

Mitigation: Install only when sharing diffs with Propel is acceptable, scope the token to review access, and store PROPEL_API_KEY outside chat or in a proper secret store.

Risk: Untrusted PROPEL_API_BASE_URL or PROPEL_API_URL values could redirect review data or credentials away from the intended service.

Mitigation: Use the production Propel API endpoint unless there is a trusted reason to override it, and inspect override environment variables before running helper scripts.

Risk: The documented workflow writes a review diff to a fixed /tmp path, which can expose source changes on shared systems.

Mitigation: Use a private mktemp file for diffs and remove it after the review flow completes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jasonyuezhang/skills/propel-code-review-smoke-1773429953)
- [Propel Code homepage](https://www.propelcode.ai/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PROPEL_API_KEY plus curl, git, and jq; submits review diffs to Propel and can return structured comments with file, line, message, and severity.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
