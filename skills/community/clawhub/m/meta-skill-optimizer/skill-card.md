## Description: <br>
Self-improving AI skill optimizer that learns from feedback, auto-tunes prompts, optimizes tool usage patterns, and evolves based on success/failure analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to record execution outcomes, learn from failures and successes, tune prompts, select tools, assess capability gaps, and export learned optimization knowledge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optimizer can keep a persistent local history of prompts, task context, errors, outcomes, and tool parameters. <br>
Mitigation: Avoid recording sensitive work unless redaction, retention limits, inspection and deletion workflows, and an explicit storage path are in place. <br>
Risk: Optimization recommendations may become misleading if low-quality or stale execution records dominate the knowledge base. <br>
Mitigation: Review learned records periodically, remove bad examples, and validate optimized prompts, tool choices, and parameters before applying them to important workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jason-aka-chen/meta-skill-optimizer) <br>
- [Publisher profile](https://clawhub.ai/user/jason-aka-chen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, shell commands, and JSON-like optimization records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist learned execution records to a local JSON knowledge base when used through the included Python optimizer.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
