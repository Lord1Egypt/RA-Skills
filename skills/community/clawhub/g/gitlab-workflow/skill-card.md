## Description: <br>
GitLab workflow helper for merge request management, code review, CI/CD status checks, branch management, and merge operations through MorphixAI-mediated GitLab access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paul-leo](https://clawhub.ai/user/paul-leo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect GitLab projects, review merge requests, check pipelines, create issues, update reviewers, approve merge requests, and merge changes while following team workflow conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can approve, merge, retry, create, and update GitLab resources through a linked account. <br>
Mitigation: Use a least-privilege GitLab connection, limit access to intended projects, and require explicit confirmation before state-changing GitLab actions. <br>
Risk: The skill depends on MorphixAI access and a MORPHIXAI_API_KEY for GitLab operations. <br>
Mitigation: Install only if MorphixAI is trusted, store the API key securely, and rotate or revoke it if the linked account or workspace is no longer needed. <br>
Risk: The workflow may run local git commands while inspecting merge requests. <br>
Mitigation: Confirm the repository path and command intent before running local git commands, especially before fetching or diffing private project branches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paul-leo/gitlab-workflow) <br>
- [MorphixAI API keys](https://morphix.app/api-keys) <br>
- [MorphixAI connections](https://morphix.app/connections) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline YAML and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and a linked GitLab account.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
