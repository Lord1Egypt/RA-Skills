## Description:

LMeterX Web Load Test analyzes a webpage URL, pre-checks discovered APIs, and creates LMeterX load-testing tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckyyc](https://clawhub.ai/user/luckyyc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run authorized web load tests by analyzing a target page, checking API connectivity, and creating LMeterX task reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create live load-test tasks for website targets.

Mitigation: Run it only against systems the user owns or is explicitly authorized to test, and require manual confirmation before task creation.

Risk: The release evidence notes use of a shared default LMeterX token.

Mitigation: Replace the shared token with a user-specific secret before real use.

Risk: The release evidence flags unsafe TLS certificate verification.

Mitigation: Fix TLS certificate verification before using the skill in a real environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luckyyc/skills/lmeterx-web-loadtest)
- [LMeterX service endpoint](https://lmeterx.openxlab.org.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown response with an execution summary, failure classification, task IDs, and report links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a webpage URL and optionally accepts concurrency, duration, and spawn-rate parameters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
