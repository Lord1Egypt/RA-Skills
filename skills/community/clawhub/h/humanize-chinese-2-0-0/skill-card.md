## Description: <br>
Detect and humanize AI-generated Chinese text with weighted scoring, sentence-level analysis, style transforms, sentence restructuring, and context-aware replacement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xspeter](https://clawhub.ai/user/0xspeter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, and agents use this skill for legitimate Chinese text review, style improvement, and AI-pattern scoring. It can detect AI-like patterns, rewrite text into selected styles, compare before-and-after scores, and batch-process local text files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to reduce AI-detection signals in Chinese text and may be misused to bypass disclosure rules. <br>
Mitigation: Use only for legitimate editing and style-improvement work; do not use it to evade academic, workplace, publisher, or platform AI-disclosure requirements. <br>
Risk: Automated rewrites can alter meaning, tone, or factual nuance. <br>
Mitigation: Review outputs against the original before replacing source text, especially for formal, academic, workplace, or regulated content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0xspeter/humanize-chinese-2-0-0) <br>
- [README](README.md) <br>
- [Skill Instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI outputs may be plain text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write transformed text files when an output path is provided; pattern and scoring behavior is configurable through scripts/patterns_cn.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact package.json and _meta.json report 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
