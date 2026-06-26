## Description: <br>
Self-reflection engine for AI agents. Extracts patterns from session transcripts into a weighted graph with Hebbian learning and time decay. Compiles a token-budgeted lens of active self-knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeycacciatore3](https://clawhub.ai/user/joeycacciatore3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to maintain local reflective memory from session transcripts, reinforce recurring insights, and compile a concise lens that can guide later agent behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent summaries of session history and notes can influence future agent behavior or retain sensitive information. <br>
Mitigation: Inspect memory/metacognition.json and scripts/metacognition-lens.md periodically, and edit or delete entries that are sensitive, stale, or misleading. <br>
Risk: Reflective text can be sent to an environment-controlled embeddings endpoint. <br>
Mitigation: Leave EMBEDDINGS_URL unset unless a trusted local endpoint is intentionally configured and reviewed. <br>
Risk: Scheduled extraction can reinforce incorrect or low-quality insights without human review. <br>
Mitigation: Review the workflow before enabling cron and check generated insights before relying on them for future behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/joeycacciatore3/nate-metacognition) <br>
- [Project Homepage](https://github.com/meimakes/metacognition) <br>
- [OpenClaw](https://openclaw.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown lens file, JSON memory store, and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes persistent memory/metacognition.json and scripts/metacognition-lens.md; optional embeddings should use a trusted local endpoint only.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
