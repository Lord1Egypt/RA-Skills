## Description: <br>
My Work Profile Cross Agent maintains a local cross-agent work profile and domain knowledge so agents can personalize responses and update useful work knowledge from conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jshxemail](https://clawhub.ai/user/jshxemail) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals using ClawHub agents use this skill to keep a reusable local profile of their role, responsibilities, preferences, and business-domain knowledge across agent sessions. The skill loads relevant profile context for answers and can update stored knowledge after conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can silently read and automatically write a persistent local work profile and business-domain knowledge during normal conversations. <br>
Mitigation: Review the home-directory profile folder regularly and set autoUpdate to off if updates should require confirmation. <br>
Risk: Cross-agent shared memory may carry outdated or incorrect work assumptions into later answers. <br>
Mitigation: Use the provided view, correction, and delete commands to audit stored entries and remove stale or incorrect domain knowledge. <br>
Risk: Sensitive business or personal details discussed while the skill is active could become relevant to memory handling. <br>
Mitigation: Avoid sharing sensitive details while the skill is active and inspect stored files for anything that should be removed. <br>


## Reference(s): <br>
- [Skill Page](https://clawhub.ai/jshxemail/my-work-profile-cross-agent) <br>
- [Knowledge Record Format Specification](artifact/references/format-spec.md) <br>
- [Extraction Examples and Scenarios](artifact/references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries and local Markdown/configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can remain silent when no new high-value work knowledge is found; otherwise may produce a short execution summary and log path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
