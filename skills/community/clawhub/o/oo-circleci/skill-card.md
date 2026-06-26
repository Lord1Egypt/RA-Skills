## Description: <br>
CircleCI helps agents operate CircleCI through an OOMOL-connected account for project, pipeline, workflow, job, artifact, Insights, and environment-variable queries, with guarded pipeline triggering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect CircleCI users, projects, pipelines, workflows, jobs, artifacts, Insights summaries, and masked project environment variables through the OOMOL CircleCI connector. It can also trigger a new project pipeline after the agent confirms the exact payload and effect with the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on OOMOL brokering access to the user's CircleCI account, and returned artifacts or masked environment-variable listings may still contain sensitive project information. <br>
Mitigation: Install only when the user trusts OOMOL for CircleCI access, keep connector scopes limited to the needed tasks, and treat returned project data as sensitive. <br>
Risk: The trigger_pipeline action changes CircleCI state and may start jobs that consume resources or affect deployment workflows. <br>
Mitigation: Confirm the exact project, branch, parameters, and intended effect with the user before running trigger_pipeline. <br>
Risk: Connector payloads can be wrong if the agent relies on stale action assumptions. <br>
Mitigation: Inspect the live action schema with oo connector schema before constructing each payload. <br>


## Reference(s): <br>
- [ClawHub CircleCI Skill Page](https://clawhub.ai/oomol/oo-circleci) <br>
- [Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [CircleCI Homepage](https://circleci.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [CircleCI Icon](https://static.oomol.com/logo/third-party/CircleCI.svg) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON connector payloads or results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs agents to inspect the live connector schema before building payloads and to confirm write actions before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
