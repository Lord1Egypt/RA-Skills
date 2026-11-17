## Description:

Run evidence-gated coding sprints with frozen ACs, separated builder/verifier roles, and durable proof artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leostehlik](https://clawhub.ai/user/leostehlik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use Proof Loop to run coding tasks with frozen acceptance criteria, a separate fresh verifier, and durable evidence before declaring work complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses file and shell capabilities, and runtime permissions were not verified.

Mitigation: Review its requested file and shell access, confirm the task ID and repository root, and run helper scripts with the least privilege available.

Risk: The artifact checker cannot authenticate verifier independence or prove that recorded checks ran.

Mitigation: Have a fresh verifier inspect the evidence and independently run the checks before accepting a PASS verdict.

## Reference(s):

- [Workflow](references/workflow.md)
- [Brief Template](references/brief-template.md)
- [Artifacts](references/artifacts.md)
- [Loopsmith Bridge](references/loopsmith-bridge.md)
- [ClawHub Skill Page](https://clawhub.ai/leostehlik/skills/proof-loop)
- [Publisher Profile](https://clawhub.ai/user/leostehlik)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown task briefs and evidence, JSON verdicts, shell commands, and optional Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates repo-local proof artifacts for a specified task; the mechanical gate checks artifact consistency but does not authenticate verifier independence or evidence truth.]

## Skill Version(s):

0.3.3 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
