## Description:

GitLab workflow assistant for merge request management, code review, CI/CD status checks, branch management, issue handling, and merge operations through MorphixAI-mediated GitLab access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paul-leo](https://clawhub.ai/user/paul-leo)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to operate GitLab workflows: reviewing merge requests, checking CI/CD status, managing branches and issues, and approving or merging changes according to team conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide actions that approve, merge, retry pipelines, or change merge request and issue state in GitLab.

Mitigation: Require explicit approval before GitLab write actions and use least-privilege GitLab permissions.

Risk: The MorphixAI integration requires a GitLab account connection and an API key.

Mitigation: Use a reviewed or pinned plugin version when available, protect MORPHIXAI_API_KEY, and grant only the access needed for the intended repositories.

Risk: The workflow may run local git commands against selected repositories.

Mitigation: Review shell commands before execution and confirm they run in the intended repository path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paul-leo/skills/gitlab-workflow)
- [MorphixAI API keys](https://morphix.app/api-keys)
- [MorphixAI connections](https://morphix.app/connections)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown with inline shell commands and structured GitLab tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and a linked GitLab account; may use local git commands for repository review.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
