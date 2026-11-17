## Description:

Peter CI Gate helps an agent inspect remote PR checks, diagnose CI failures, apply a one-time rerun policy for likely flaky failures, and report whether a PR can merge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasilva](https://clawhub.ai/user/chinasilva)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill when a pull request is near merge and needs a clear remote CI gate decision. It helps inspect checks, diagnose failed jobs from GitHub Actions evidence, distinguish code failures from likely flaky failures, and return a merge or blocked conclusion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to rerun GitHub Actions workflows, which may consume CI resources or obscure flaky failures if done without explicit evidence.

Mitigation: Require the agent to show flaky-failure evidence and ask before any `gh run rerun` command; keep reruns to one attempt and do not treat a passing rerun as root-cause resolution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chinasilva/skills/peter-ci-gate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with GitHub CLI commands, CI evidence summaries, and a merge-gate conclusion]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose a single GitHub Actions rerun for likely flaky failures; conclusions should cite job or log evidence.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
