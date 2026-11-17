## Description:

Helps agents inspect Jenkins jobs and builds, read console logs, trigger builds, and enable or disable jobs through the Jenkins Remote API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weiguang1017](https://clawhub.ai/user/weiguang1017)

### License/Terms of Use:

MIT

## Use Case:

Developers and CI operators use this skill to inspect Jenkins jobs, check build results and logs, and, with approval, trigger builds or change job availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent with Jenkins credentials can trigger builds or enable or disable jobs without an enforced confirmation step.

Mitigation: Require explicit user confirmation of the job and parameters before any change; limit changes to approved, non-production jobs.

Risk: Jenkins credentials grant the agent access beyond routine job inspection if the token has write permissions.

Mitigation: Use a least-privilege Jenkins token and prefer read-only credentials for inspection.

## Reference(s):

- [Jenkins Skills usage guide](references/USAGE.md)
- [ClawHub skill release](https://clawhub.ai/weiguang1017/skills/jenkins-ci-skill)
- [Server-resolved source repository](https://github.com/weiguang1017/jenkins-ci-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with command examples, JSON job and build results, and plain-text log excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Build triggers may return a queue URL before a build number is available.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
