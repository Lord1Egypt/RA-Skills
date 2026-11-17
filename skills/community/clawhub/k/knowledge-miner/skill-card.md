## Description:

Knowledge Miner is a Chinese-language teaching skill that analyzes Git commits or visible session evidence, turns scattered concepts into a functional cause-and-effect learning chain, and helps novice learners understand through Feynman-style explanation and a minimal creation task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlykan](https://clawhub.ai/user/wlykan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and learners use this skill to turn a specified commit, recent commits, or visible session context into a novice-friendly Chinese lesson about what changed, why the steps connect, and how to recreate the core mechanism in a minimal version.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous prompts such as '刚才' or '上文' can cause the skill to summarize the visible conversation instead of a narrower commit or source.

Mitigation: Ask for a specific commit hash or explicitly name the evidence source when a narrow review is intended.

Risk: Lessons are generated from Git history or visible session evidence and can be misleading if the selected evidence is incomplete or not the intended source.

Mitigation: Review the cited evidence boundaries and confirm the selected mode before relying on the lesson.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wlykan/skills/knowledge-miner)
- [Teaching Guide](references/teaching-guide.md)
- [Session Evidence Guide](references/session-evidence-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Chinese-language Markdown lesson with evidence notes, cause-and-effect chains, learner checks, and optional command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Mermaid diagrams or pseudocode when they help explain the evidence-backed learning chain.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
