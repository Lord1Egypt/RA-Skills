## Description:

Run throwaway prototypes to validate feasibility, compare approaches, and report a verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to test a concrete feasibility question before committing to a production build. It creates a small prototype, exercises an edge case, and reports a verdict with evidence and a recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One local reference could not be resolved during the security review, leaving its target unassessed.

Mitigation: Resolve and inspect the reference before relying on it, and review a prototype before running it.

## Reference(s):

- [Spike on ClawHub](https://clawhub.ai/hillstreet-ph/skills/oc-spike)
- [Publisher profile: hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

## Skill Output:

**Output Type(s):** [Code, Files, Markdown]

**Output Format:** [A concise Markdown verdict with feasibility evidence and, when useful, a small runnable prototype artifact.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report identifies what worked, what failed or surprised the user, and a next-step recommendation; prototype code should be rewritten before production use.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
