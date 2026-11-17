## Description:

OpenClaw Self-Improve provides an evidence-based, approval-gated workflow and helper scripts for improving OpenClaw or other projects with measurable before-and-after validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gopendrasharma89-tech](https://clawhub.ai/user/gopendrasharma89-tech)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to run audit, proposal, and approved implementation loops that baseline a repository, prepare an approval package, validate changes, summarize outcomes, and export run data for CI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository-mutating rollback workflows can revert more files than intended if broad rollback targets are used.

Mitigation: Review proposal.md before rollback, avoid broad rollback targets such as . or whole directories, and keep a separate commit, stash, or backup for uncommitted work.

Risk: UX feedback examples can involve real user data when adapted for live studies.

Mitigation: Add privacy and consent handling before using the UX feedback examples with real users.

## Reference(s):

- [Output Contract](references/output-contract.md)
- [Improvement Playbooks](references/playbooks.md)
- [ClawHub Listing](https://clawhub.ai/gopendrasharma89-tech/openclaw-self-improve)
- [ClawHub Skill Page](https://clawhub.ai/gopendrasharma89-tech/skills/openclaw-self-improve)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown artifacts, JSON summaries, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Run artifacts follow references/output-contract.md; helper scripts require bash, git, python3, and zip.]

## Skill Version(s):

1.3.0 (source: release evidence and skill body)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
