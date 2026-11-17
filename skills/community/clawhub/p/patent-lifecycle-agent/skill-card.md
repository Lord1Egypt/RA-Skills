## Description:

Patent Lifecycle Agent supports patent professionals across disclosure intake, portfolio planning, prior-art and FTO search, patent drafting support, office-action response planning, maintenance review, enforcement analysis, and patent drawing generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent agents, IP teams, and invention managers use this skill to structure patent lifecycle work, including technical disclosures, novelty and FTO reports, claim-drafting inputs, office-action response suggestions, maintenance assessments, infringement-risk analysis, and patent drawing packages. Outputs are decision support and should be reviewed by qualified patent counsel before filing or legal action.

### Deployment Geography for Use:

China by default; other jurisdictions when the user specifies a target country or region.

## Known Risks and Mitigations:

Risk: The skill may process confidential patent disclosures and invention materials.

Mitigation: Run it only in an isolated agent or runtime environment without unrelated confidential files or unnecessary credentials.

Risk: The skill asks the agent to install unpinned Python dependencies and execute generated drawing scripts.

Mitigation: Use pre-provisioned or pinned dependencies for drawing generation, and review generated scripts before execution.

Risk: Patent deadlines, filing strategy, jurisdictional law, and infringement analysis are high-impact legal areas.

Mitigation: Confirm the target jurisdiction and have qualified patent counsel review outputs before filing, responding to official actions, or making legal decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuanzhian-patsnap/skills/patent-lifecycle-agent)
- [Zhihuiya Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Configuration, Guidance]

**Output Format:** [Markdown and HTML reports, generated Python drawing code, PNG and DXF drawing files, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May embed generated PNG drawings as Base64 inside standalone HTML reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
