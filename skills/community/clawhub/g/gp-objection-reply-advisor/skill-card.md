## Description:

Assists purchasers and procurement agencies in Chinese government-procurement objection workflows by checking intake timing, analyzing each objection, drafting corrective or denial replies, and producing an internal complaint-risk forecast.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement purchasers and procurement agencies use this skill to prepare government-procurement objection responses, including deadline checks, per-issue legal and factual analysis, reply drafting, and internal complaint-risk planning.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Generated objection replies may include forced author branding.

Mitigation: Review drafts before external use and remove the author signature unless it is explicitly wanted.

Risk: The skill is domain-specific and may be misapplied outside Chinese government-procurement purchaser or agency objection replies.

Mitigation: Use it only for that domain and route other procurement, bidder-side, scoring, contract, or drafting tasks to appropriate review.

Risk: Procurement records can contain sensitive or confidential information.

Mitigation: Provide only the objection materials, procurement-file excerpts, and review records needed for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/gp-objection-reply-advisor)
- [Artifact README](artifact/README.md)
- [Skill source](artifact/SKILL.md)
- [Regression test report](artifact/回归测试总报告_5例.md)
- [Regression test cases](artifact/回归测试用例_v1.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown sections containing intake registration, per-objection analysis, a draft reply letter, an internal complaint-risk forecast, and a follow-up checklist.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided objection letters, procurement-file excerpts, and review records; separates external reply text from internal risk notes.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, manifest.yaml, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
