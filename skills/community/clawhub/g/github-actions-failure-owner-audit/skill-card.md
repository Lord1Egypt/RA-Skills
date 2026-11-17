## Description:

Audit failing GitHub Actions runs by actor ownership to expose who/workflow combinations generate the most CI noise and wasted minutes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to triage GitHub Actions failures by repository, actor, owner, workflow, branch, conclusion, and failed runtime so CI stabilization work can be routed by impact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text reports generated from untrusted GitHub export files can be visually spoofed by crafted workflow, actor, repository, or owner strings.

Mitigation: Prefer JSON output for automation and review text reports with care when source GitHub export files are untrusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-failure-owner-audit)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text reports or JSON summaries emitted by a shell command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JSON output includes summary, top groups, all groups, and critical groups; reporting mode exits 0 by default, with optional failure on critical groups.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
