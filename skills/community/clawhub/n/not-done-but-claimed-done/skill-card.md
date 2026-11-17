## Description:

未做却说做了 discovery skill for VeriClaw 爪印. Use when the intent is 未做却说做了, AI未做却说做了, 明明没做却说做了, 装作做完了, AI以为自己工作了, or fake completion diagnosis after a model claims the task is done.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheygoodbai](https://clawhub.ai/user/sheygoodbai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this routing skill to recognize Chinese fake-completion queries and direct them to VeriClaw resources for evidence inspection, diagnosis, intervention, and verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill links to external VeriClaw pages and recommends the `clawhub install vericlaw` command.

Mitigation: Verify the package, publisher, and requested permissions before installing or following linked resources.

Risk: The skill is a routing aid and may not itself prove whether an agent completed a task.

Mitigation: Use the routed VeriClaw review materials to inspect evidence and verify corrections before trusting completion claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sheygoodbai/skills/not-done-but-claimed-done)
- [VeriClaw ClawHub page](https://clawhub.ai/sheygoodbai/vericlaw)
- [未做却说做了 page](https://sheygoodbai.github.io/vericlaw/not-done-but-claimed-done/)
- [Fake completion diagnosis page](https://sheygoodbai.github.io/vericlaw/fake-completion-diagnosis/)
- [Review kit](https://sheygoodbai.github.io/vericlaw/review-kit/)
- [Search intents](references/search-intents.txt)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance with links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes fake-completion discovery requests to VeriClaw resources; does not execute code.]

## Skill Version(s):

0.1.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
