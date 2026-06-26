## Description: <br>
Clawra's core ontology engine uses a three-layer memory architecture to model objects, relationships, logic, and rules for reasoning rather than general note-taking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-xiaochen](https://clawhub.ai/user/wu-xiaochen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add ontology-guided reasoning, persistent memory rules, confidence labels, and decision support to a Clawra or Hermes-style agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad persistent memory and global prompt-layer influence. <br>
Mitigation: Install only after reviewing the memory rules, limiting where memory files can be read or written, and confirming that global prompt behavior is intended. <br>
Risk: The auto-enhancer behavior can perform git commits, git pushes, and ClawHub publishing. <br>
Mitigation: Disable or remove scripts/auto_enhancer.py unless automatic publishing is explicitly required, and require manual review before any release action. <br>
Risk: Memory files or backups can expose personal, secret, or identifying details. <br>
Mitigation: Keep secrets and identifying details out of memory files and review any memory, SOUL.md, or repository content before backup or publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-xiaochen/ontology-clawra) <br>
- [SKILL.md](SKILL.md) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>
- [Evaluation scenarios](evals/evals.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text guidance with optional Python-generated JSONL/YAML memory files and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update persistent memory files; auto-enhancement behavior can commit, push, and publish if enabled.] <br>

## Skill Version(s): <br>
4.7.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
