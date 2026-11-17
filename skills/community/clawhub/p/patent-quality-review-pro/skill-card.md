## Description:

Patent Quality Review Pro reviews uploaded PDF or Word patent application documents across all evaluation indicators, incorporates reexamination and invalidation decision points for drafting-quality and claim-stability assessment, switches among chemistry, mechanical, electrical, and general AHP weighting schemes after user confirmation, and generates a standard two-page Word evaluation report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent professionals, agents, and IP review teams use this skill to perform structured quality review of patent application drafts and produce a Word evaluation table with scores, issue descriptions, and modification suggestions. Live patent-data-backed conclusions require authorized PatSnap Open Platform MCP access and explicit novelty-check and non-obviousness-check evidence when assessing claim stability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install the python-docx dependency at runtime without a pinned version.

Mitigation: Run it in a contained workspace and pin and vet python-docx before enabling runtime installation.

Risk: The Word generator can open the output directory through platform-specific local commands after writing files.

Mitigation: Pass an explicit safe output path under the intended session output directory and use --no-open-output where automatic directory opening is not needed.

Risk: Patent-data-backed novelty and inventive-step conclusions depend on authorized PatSnap Open Platform MCP access and complete evidence artifacts.

Mitigation: Confirm MCP authorization and require the validation scripts to pass before relying on scores, claim-stability conclusions, or generated reports.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/yuanzhian-patsnap/skills/patent-quality-review-pro)
- [PatSnap Open Platform](https://open.zhihuiya.com/)
- [Issue 9 data-format patch](references/issue9_patch.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Chinese-language review guidance and generated Word .docx evaluation reports, with JSON review data and command invocations used during execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The Word output is a two-page patent application quality evaluation table with a main scoring table and an appendix for key issues and recommendations.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
