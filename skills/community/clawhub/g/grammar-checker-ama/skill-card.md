## Description: <br>
Grammar checking tool for AMA style medical writing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, and medical writers use this skill to check supplied text for AMA-style grammar issues and receive concise correction guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local execution processes user-supplied medical writing, which may contain sensitive content. <br>
Mitigation: Run the skill in a trusted local workspace and avoid checking confidential or regulated text unless permitted by policy. <br>
Risk: Server security guidance notes meaningful local file access and possible local logs, state, baselines, or snapshots. <br>
Mitigation: Review any monitoring, notification, and cron setup before enabling it, especially where diffs or logs could contain sensitive content. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text CLI output with issue lists and brief explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a --text string; no additional Python packages are declared.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
