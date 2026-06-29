## Description: <br>
Guides agents to apply adversarial review to non-trivial decisions so overconfident assumptions are challenged before they become costly mistakes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqyougitcom](https://clawhub.ai/user/qqyougitcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent operators, and review-focused agents use this skill when correctness matters more than speed to structure a bounded adversarial review of architecture choices, code changes, deployments, migrations, and other non-trivial decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Artifacts or contracts sent to reviewer subagents or cross-model reviewers may include unnecessary sensitive information. <br>
Mitigation: Share only the minimal artifact and contract needed for review, remove secrets or private data first, and require explicit approval for each reviewer or cross-model call. <br>
Risk: Adversarial reviewers can produce false positives or findings caused by an unclear contract. <br>
Mitigation: Reconcile every finding against the artifact text and classify it as a contract misread, actionable issue, accepted tradeoff, or noise before changing the work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/mimo-doubt-driven-development) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with checklists and adversarial prompt templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code; may ask the agent to request explicit approval before spawning reviewer subagents or using cross-model review.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
