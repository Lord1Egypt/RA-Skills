## Description: <br>
Convenes a multi-LLM expert panel to pressure-test hard-to-reverse decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to convene a structured expert panel for high-stakes architecture, strategy, or implementation decisions. It helps assess reversibility, compare courses of action, pressure-test assumptions, and produce a synthesized decision record. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deliberation records may contain sensitive strategy, architecture, or incident-response details and can be persisted locally. <br>
Mitigation: Use the skill only where local retention is acceptable, avoid confidential or credential-bearing inputs, and apply repository privacy and retention controls before use. <br>
Risk: The workflow defaults to publishing decision summaries and phase comments to GitHub Discussions. <br>
Mitigation: Review the generated decision content before publication, disable or decline publishing for sensitive work, and confirm the target repository visibility and Discussions settings. <br>
Risk: The artifact documents external model-tool invocation patterns, including a GLM fallback that skips permissions. <br>
Mitigation: Prefer configured safe aliases and authenticated tools, avoid the permission-skipping fallback, and require operator review before running generated commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-attune-war-room) <br>
- [Configured homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>
- [Reversible and Irreversible Decisions](https://fs.blog/reversible-irreversible-decisions/) <br>
- [One-Way and Two-Way Door Decision-Making](https://tapandesai.com/one-way-two-way-doors-decision-making/) <br>
- [Amazon's Type 1 vs Type 2 Decisions](https://ashikuzzaman.com/2025/03/03/amazons-type-1-vs-type-2-decisions-a-framework-for-effective-decision-making/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown decision documents with shell command snippets and local session artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist deliberation records locally and publish summaries to GitHub Discussions unless disabled.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
