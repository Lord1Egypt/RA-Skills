## Description: <br>
Humanizes AI-generated text by detecting common LLM writing patterns, scoring text, and suggesting or applying more natural rewrites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[penglovemeng](https://clawhub.ai/user/penglovemeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to review drafts for AI-writing signals, generate concise rewrite guidance, and produce humanized text while preserving the original meaning and intended tone. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be used to remove cues that disclose AI authorship or to add first-person experience that is not true. <br>
Mitigation: Use it as an editing aid only where policy allows, keep required AI-use disclosures, and review rewritten claims before sharing. <br>
Risk: Always-on prompt templates can persistently change an agent's writing behavior across unrelated tasks. <br>
Mitigation: Enable always-on guidance only for agents where that writing style is intended, and keep the configuration scoped and reviewable. <br>
Risk: Mechanical rewrites and auto-fixes can change nuance, accuracy, or tone. <br>
Mitigation: Compare the rewritten text against the source, preserve factual claims, and reject edits that introduce unsupported specifics. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/penglovemeng/peng-ai-humanizer) <br>
- [README](README.md) <br>
- [Pattern documentation](docs/PATTERNS.md) <br>
- [Real-world before/after examples](docs/EXAMPLES.md) <br>
- [AI vocabulary reference](references/ai-vocabulary.md) <br>
- [Writing style guide](references/style-guide.md) <br>
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) <br>
- [Copyleaks stylometric research](https://arxiv.org/abs/2503.01659) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, rewritten text, JSON analysis, or CLI-style reports depending on the requested workflow.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include AI-writing scores, pattern findings, suggested edits, safe auto-fixes, and brief change summaries.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
