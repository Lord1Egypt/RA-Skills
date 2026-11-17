## Description:

Guides an agent through a release loop from local changes through selective commit, push, target-branch merge, CI deployment, workload restart, end-to-end API and database verification, and patch-and-repeat recovery when validation fails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to move ready code changes through a controlled deployment workflow and verify that the deployed service, database effects, and rollback or patch loop are complete. It is intended for operational release coordination, especially when CI/CD, Kubernetes workloads, and database checks are involved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide high-impact deployment actions such as pushing code, merging branches, triggering CI, restarting pods, or changing shared data.

Mitigation: Require human review before approving high-impact steps, especially production pod deletion, force pushes, broad DELETE operations, and token use.

Risk: Deployment verification can be misleading if CI builds, pod readiness, or database effects are not actually confirmed.

Mitigation: Follow the skill's explicit gates for merge status, CI success, SHA reconciliation, pod readiness, API assertions, and database SELECT evidence before considering the loop complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hgvgfgvh/skills/merge-deploy-verify-loop)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples, checklists, and deployment reconciliation tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes staged release steps, verification evidence prompts, and failure-loop guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
