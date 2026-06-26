## Description: <br>
Rewrites English, Chinese, or mixed serious nonfiction in academic or popular-science mode so AI-looking prose reads more human while preserving register and avoiding new facts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentjiang06](https://clawhub.ai/user/vincentjiang06) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, researchers, editors, and agents use this skill to triage and revise AI-looking thesis chapters, abstracts, literature reviews, policy reports, and serious science explainers while keeping the source meaning intact. It can also return a detect-only signal map when the user asks to score prose without rewriting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vincentjiang06/skills/humanizer-academic) <br>
- [SKILL.md](SKILL.md) <br>
- [README.en.md](README.en.md) <br>
- [Academic Register](references/academic-register.md) <br>
- [Popular-Science Register](references/popsci-register.md) <br>
- [Blind-Judge Rubric](references/blind-judge-rubric.md) <br>
- [Rewrite Protocol](rules/rewrite-protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown; detect-only mode may include JSON-like diagnostic results and shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Abstain-first behavior may return the original text unchanged with a short note; rewrites must preserve source facts, citations, numbers, named entities, and register.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release evidence, SKILL.md, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
