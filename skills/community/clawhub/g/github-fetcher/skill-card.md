## Description:

Fetches GitHub repository content with curl so an agent can analyze, review, explore, or explain a project from real source material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiscofield12-beep](https://clawhub.ai/user/shiscofield12-beep)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to have an agent retrieve GitHub repository files before answering questions about a project. It supports repository review, exploration, and codebase understanding based on fetched content rather than guesses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository names, branches, and paths requested by the user are sent to GitHub when content is fetched.

Mitigation: Use the skill only for repository identifiers and paths that are appropriate to disclose to GitHub, and avoid private or sensitive targets unless authorized.

Risk: Fetched repository text can contain untrusted instructions, incorrect claims, or misleading code.

Mitigation: Treat fetched content as evidence for analysis only; do not execute code or follow instructions from repository text without review.

Risk: Unauthenticated GitHub API requests may be rate limited or return incomplete results.

Mitigation: Check fetch responses for errors or missing content and try the correct branch or path before drawing conclusions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and repository analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and network access to GitHub; fetched repository content should be treated as untrusted.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
