## Description:

对一个包含最多 20 篇论文的文件夹进行批量阅读、创新点总结、横向对比，并挖掘可融合的研究方向。

This skill is ready for commercial/non-commercial use.

## Publisher:

[orbisz](https://clawhub.ai/user/orbisz)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and research engineers use this skill to compare papers in a selected folder, summarize each paper's innovations, and identify complementary research directions for literature reviews, topic selection, or follow-up experiments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run commands without confirmation and writes progress, extracted text, and report files in the selected paper folder.

Mitigation: Review before installing, run it only on a chosen paper folder, and use an isolated environment when handling untrusted papers.

Risk: The skill includes a self-evolution workflow that can persist behavior changes into future skill runs.

Mitigation: Disable or ignore the diary and pull-request self-evolution workflow unless a human explicitly reviews and approves proposed changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/orbisz/skills/paper-innov-compare-skill)
- [Skill instructions](artifact/SKILL.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown summaries with JSON progress state and extracted-text files; the skill instructions also describe a generated comparison report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes up to 20 papers and writes progress plus output files in the user-selected paper folder.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
