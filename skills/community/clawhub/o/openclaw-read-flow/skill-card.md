## Description: <br>
OpenClaw Read Flow guides an agent through a FreshRSS-based reading pipeline, from unread-item collection and yesterday-window slicing to Digest construction, six-section Daily Review generation, and human-confirmed knowledge capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gcdd1993](https://clawhub.ai/user/gcdd1993) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers who use FreshRSS with OpenClaw or ClawHub use this skill to turn unread feeds into deduplicated Digests, fixed-column Daily Reviews, and material ready for reviewed knowledge-base or note workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can expose private FreshRSS unread-feed contents to the agent. <br>
Mitigation: Use a FreshRSS-specific API password and set feed or item limits for sensitive accounts. <br>
Risk: Referenced external scripts or connected workflows may fetch content, mark items read, or write to downstream knowledge stores. <br>
Mitigation: Review referenced scripts before running them and keep read-state changes or knowledge-base writes approval-gated. <br>
Risk: Generated Digests or Daily Reviews may omit context when article bodies are inaccessible or quality checks fail. <br>
Mitigation: Require inaccessible content to be explicitly marked and review outputs before treating them as long-term knowledge. <br>


## Reference(s): <br>
- [OpenClaw Read Flow Workflow](references/workflow.md) <br>
- [ClawHub skill page](https://clawhub.ai/gcdd1993/openclaw-read-flow) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Configuration, Shell commands] <br>
**Output Format:** [Markdown with structured sections and referenced script commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Chinese summaries for English source articles, deduplicated Digests, and six-column Daily Reviews.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
