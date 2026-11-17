## Description:

多源深度研究工具，支持系统性信息探索、来源评估与方法论追踪，生成结构化研究报告，适合个人研究与学习。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, students, individual researchers, and developers use this skill to plan multi-source research, assess source credibility, reconcile conflicting information, and produce structured research reports. It is suited to personal research, learning, technical comparison, academic topic exploration, market information gathering, and SEO-oriented research that avoids black-hat tactics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad command and file authority for research tasks.

Mitigation: Restrict use to specific search, parsing, and report-generation commands and review file writes before execution.

Risk: Research workflows may propose package installation, script execution, file writes, or external API calls.

Mitigation: Review each pip install, script execution, file write, and external API call before allowing the agent to run it.

Risk: Generated research can include incorrect, stale, or poorly supported claims.

Mitigation: Require source lists, credibility notes, confidence ratings, and identified information gaps in final reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/in-depth-research-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured research sections and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source lists, credibility notes, confidence ratings, research methods, and identified information gaps.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
