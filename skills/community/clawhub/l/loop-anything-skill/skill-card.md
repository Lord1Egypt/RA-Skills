## Description:

Improve important deliverables by looping them through multiple isolated AI reviewers, each evaluating from a different angle, until all reviewers give full approval (Score 120).

This skill is ready for commercial/non-commercial use.

## Publisher:

[ariesshin](https://clawhub.ai/user/ariesshin)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to improve high-value deliverables such as prompts, plans, code, designs, documents, workflows, and decisions through multi-perspective review and revision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can increase token use and cost because it runs multiple reviewer passes.

Mitigation: Use it deliberately for high-value artifacts where additional review effort is justified.

Risk: Artifacts sent to subagents may contain sensitive content.

Mitigation: Run the skill only on material the user is comfortable sending to subagents, and keep reviewer packets bounded to the minimum required context.

Risk: A PASS with Score 120 is a structured review result, not a guarantee that the artifact is correct or risk-free.

Mitigation: Treat final approval as a review aid and keep human judgment or domain validation for high-impact uses.

Risk: The workflow depends on the current runtime's ability to create isolated subagents; some runtimes only support degraded self-review.

Mitigation: Run the documented isolation probe, disclose degraded fallback when isolation is unavailable, and avoid claiming full approval without isolated reviewers.

Risk: Installing from mutable or untrusted sources can expose users to changed skill behavior.

Mitigation: Install through ClawHub or another trusted skill installer and review the release evidence before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ariesshin/skills/loop-anything-skill)
- [Runtime Compatibility](references/runtime-compatibility.md)
- [Facet Patterns](references/facet-patterns.md)
- [Evidence Guide](references/evidence-guide.md)
- [Reviewer Packet Template](templates/reviewer-packet.md)
- [Reviewer Output Template](templates/reviewer-output.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, plain text reviewer outputs, JSON manifest data, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a final summary, reviewer outputs, an issue ledger, and a loop-run manifest; the workflow intentionally uses multiple review passes.]

## Skill Version(s):

1.0.0 (source: SKILL.md metadata.version and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
