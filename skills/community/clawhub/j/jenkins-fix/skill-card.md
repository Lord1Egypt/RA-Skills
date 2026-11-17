## Description:

Jenkins build assistant for listing Jenkins jobs, triggering default or branch-specific builds, and checking build status and artifact links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitboy123](https://clawhub.ai/user/gitboy123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CI/CD operators use this skill to inspect Jenkins jobs, trigger builds with optional branch or tag parameters, and receive build status, failure details, and artifact links in agent responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Jenkins credentials and build permissions can have high impact if the skill is installed too broadly.

Mitigation: Use a least-privilege Jenkins service token, restrict the runtime environment, and limit which users or chats can invoke build actions.

Risk: Build commands may trigger unintended Jenkins jobs when project names are ambiguous.

Mitigation: Require exact job matching or an explicit confirmation step before triggering a matched job.

Risk: Raw build logs can expose secrets, internal paths, or operational details in chat responses.

Mitigation: Redact sensitive log content or disable console-log output before returning failures to chat.

Risk: The documented default Jenkins endpoint uses HTTP.

Mitigation: Configure an HTTPS Jenkins URL before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Jenkins status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Jenkins job names, build numbers, build duration, artifact links, and excerpts from failing build logs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
