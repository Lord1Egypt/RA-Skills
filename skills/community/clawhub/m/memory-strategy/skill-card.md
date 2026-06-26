## Description: <br>
Helps agents manage conversation memory with long-term and short-term stores, importance scoring, time decay, retrieval rules, and session-end organization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hugoiku](https://clawhub.ai/user/Hugoiku) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to decide what conversation details should be remembered, where to store them, and how to retrieve them later with recency-aware weighting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory files can retain sensitive conversation content, contacts, credentials, or project details. <br>
Mitigation: Do not store API keys, tokens, passwords, or other secrets in .memory files; keep .memory out of source control; and review or redact saved content before reuse. <br>
Risk: Automatic Kimi API scoring can transmit confidential text to a third-party service. <br>
Mitigation: Use manual scoring for confidential material, or enable Kimi API scoring only after explicit approval for the data being sent. <br>
Risk: Silent Agent auto-writes can save conversation details without enough consent, retention, or redaction controls. <br>
Mitigation: Require manual approval before automatic writes until consent, retention, and redaction practices are documented and enforced. <br>
Risk: The skill documents helper scripts for scoring, retrieval, cleanup, and indexing, but the artifact only includes the skill instructions. <br>
Mitigation: Verify or provide the referenced helper scripts before relying on scripted workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Hugoiku/memory-strategy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local .memory files and optional scoring, retrieval, and indexing workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
