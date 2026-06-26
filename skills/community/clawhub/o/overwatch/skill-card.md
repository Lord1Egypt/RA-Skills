## Description: <br>
Prevent agents from going dark by requiring communication during long-running tasks, background work, and multi-step execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tooled-app](https://clawhub.ai/user/tooled-app) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use Overwatch to keep agents visibly accountable during multi-step work, delays, retries, background tasks, and sub-agent activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Frequent status updates may reveal sensitive task state during confidential work. <br>
Mitigation: Keep Overwatch subordinate to privacy, confidentiality, and safety instructions, and omit sensitive details from progress updates. <br>
Risk: The skill may make agents overly verbose during routine work. <br>
Mitigation: Prefer concise milestone, blocker, retry, and completion updates rather than repeating low-value status messages. <br>


## Reference(s): <br>
- [Overwatch on ClawHub](https://clawhub.ai/tooled-app/overwatch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text and Markdown status updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces progress updates, blocker notices, retry explanations, sub-agent status summaries, and completion reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and changelog; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
